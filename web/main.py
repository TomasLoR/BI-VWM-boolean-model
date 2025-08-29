from flask import Flask, render_template, request
import json
import re
import math
import os
import time


app = Flask(__name__)

filenames = os.listdir("original_data")
with open('inverted_index.json', 'r') as f:
    inverted_index = json.load(f)


# Funkce nahradí operátory AND, OR a NOT ze zadaného výrazu za jejich ekvivalenty
def replace_operators(input_str):
    return input_str.replace(' AND ', '&').replace(' OR ', '|').replace('NOT ', '!').lower()


# Funkce tokenizuje zadaný výraz
def tokenize(bool_query):
    regex = re.compile(r'\b\w+\b|\S|[&|()!]')
    return regex.findall(bool_query)


# Funkce zpracuje tokeny z tokenizace a vytvoří z nich postfixový zápis
def process_token(token, parsed_str, stack):
    if re.match(r'\b\w+\b', token):
        parsed_str.append(token)
        if stack and stack[-1] == '!':
            parsed_str.append(stack.pop())
    elif token in ['&', '|']:
        while stack and stack[-1] in ['&', '|']:
            parsed_str.append(stack.pop())
        stack.append(token)
    elif token == '!':
        stack.append(token)
    elif token == '(':
        stack.append(token)
    elif token == ')':
        while stack[-1] != '(':
            parsed_str.append(stack.pop())
        if stack and stack[-1] == '!':
            parsed_str.append(stack.pop())
        stack.pop()


# Funkce vyprázdní zásobník
def empty_stack(stack, parsed_str):
    while stack:
        parsed_str.append(stack.pop())


# Funkce vrátí stem slova
def parse_input(input_str):
    bool_query = replace_operators(input_str)
    tokens = tokenize(bool_query)

    parsed_str = []
    stack = []

    for token in tokens:
        process_token(token, parsed_str, stack)

    empty_stack(stack, parsed_str)
    return list(reversed(parsed_str))


# Funkce vrátí váhu termu v dokumentu, vyhledává inverted-indexem pomocí mapování
def get_weight_map(term, file_name):
    global inverted_index

    if term in inverted_index:
        if file_name in inverted_index[term]:
            return inverted_index[term][file_name]

    return 0


# Funkce vrátí váhu termu v dokumentu, vyhledává inverted-indexem sekvenčně
def get_weight_seq(term, file_name):
    global inverted_index

    for word in inverted_index:
        if word == term:
            for file in inverted_index[word]:
                if file == file_name:
                    return inverted_index[word][file]
    return 0


# Funkce rekurzivně vypočítá váhu zadaného výrazu pro daný soubor
def rec(parsed_query, filename, stype):
    if parsed_query[0] == '!':
        parsed_query.pop(0)
        return 1 - rec(parsed_query, filename, stype)

    elif parsed_query[0] == '&':
        parsed_query.pop(0)
        return 1 - math.sqrt(((1 - rec(parsed_query, filename, stype)) ** 2 + (
                1 - rec(parsed_query, filename, stype)) ** 2) / 2)

    elif parsed_query[0] == '|':
        parsed_query.pop(0)
        return math.sqrt(
            (rec(parsed_query, filename, stype) ** 2 + rec(parsed_query, filename, stype) ** 2) / 2)

    else:
        term = parsed_query[0]
        parsed_query.pop(0)

        if stype == 'map':
            return get_weight_map(term, filename)

        return get_weight_seq(term, filename)


# Funkce vrátí váhy pro všechny soubory
def get_file_weights(parsed_list, search_type):
    global inverted_index, filenames

    weights = {}

    for name in filenames:
        term_list = list(parsed_list)
        weight = rec(term_list, name, search_type)

        if weight > 0:
            weights[name] = weight

    return weights


# Funkce načte z formuláře zadaný výraz a typ vyhledávání
def read():
    expr = request.form.get("expression")
    search_type = request.form.get("drone")
    return expr, search_type


# Funkce zkontroluje zda byl zadaný výraz a typ vyhledávání
def check_input(expr, search_type):
    if expr == '' or search_type is None:
        return False
    return True


# Funkce zkontroluje zda byly správně zadané závorky
def check_brackets(expr):
    stack = []
    for char in expr:
        if char == '(':
            stack.append(char)
        elif char == ')':
            if not stack:
                return False
            stack.pop()
    if stack:
        return False
    return True

# Funkce zkontroluje zda je boolovský výraz validní
def valid_boolean_expression(expr):
    tokens = expr.split()
    if tokens[0] in ['AND', 'OR'] or tokens[-1] in ['AND', 'OR', 'NOT']:
        return False
    
    for i in range(len(tokens) - 1):
        if (tokens[i] in ['AND', 'OR', 'NOT'] and tokens[i+1] in ['AND', 'OR', ')']) or \
            (tokens[i] in ['('] and tokens[i+1] in ['AND', 'OR', ')']) or \
            (tokens[i] in [')'] and tokens[i+1] in ['NOT', '(']) or \
           (tokens[i] not in ['AND', 'OR', 'NOT', '(', ')', '(NOT'] and tokens[i+1] not in ['AND', 'OR', 'NOT', '(', ')']):
            return False
    return True  

# Funkce vypíše chybovou hlášku
def write_blank_input():
    result = '<div style="text-align: center; color: red;">Vyplň vše potřebné!</div>'
    return render_template("mainPage.html", result=result)


# Funkce vypíše chybovou hlášku
def write_invalid_input():
    result = '<div style="text-align: center; color: red;">Neplatný vstup!</div>'
    return render_template("mainPage.html", result=result)


# Funkce vypíše výsledky vyhledávání
def write(sorted_items, expr, search_type, start_time, end_time):
    result = ''
    if len(sorted_items) != 0:
        for filename, weight in sorted_items:
            url = f"http://localhost:8000/original_data/{filename}"
            result += f'<div style="text-align: center;"><a href="{url}">{filename}</a>, {round(weight, 9)}</div>\n'

    else:
        result = '<div style="text-align: center; color: red;"> Výraz se v žádném souboru nenachází!</div>'

    if search_type == "map":
        search_type = "Inverted-Index"
    else:
        search_type = "Sekvenční"

    stat_res = f'<div style="text-align: center;"> Zadaný výraz: <b>{expr}</b>, Typ vyhledávání: <b>{search_type}</b>, Počet nalezených souborů: <b>{len(sorted_items)}</b>, Čas vyhledávání: <b>{round((end_time - start_time) * 1000, 4)} ms</b></div>'
    return render_template("mainPage.html", result=result, stat_res=stat_res)


@app.route('/', methods=["GET", "POST"])

def search():
    global filenames, inverted_index

    if request.method == "POST":

        # Načtení vstupu
        expr, search_type = read()

        # Kontrola vstupu
        if not check_input(expr, search_type):
            return write_blank_input()

        # Kontrola výrazu
        if "()" in expr or not all(c.isalnum() or c.isspace() or c in '()' for c in expr):
            return write_invalid_input()

        # Kontrola závorek a validity boolovského výrazu
        if not check_brackets(expr) or not valid_boolean_expression(expr):
            return write_invalid_input()

        # Zpracování vstupu
        parsed_list = parse_input(expr)

        start_time = time.time()

        # Ziskaní vah pro každý soubor
        file_weights = get_file_weights(parsed_list, search_type)

        # Seřazení souborů podle váhy sestupně
        sorted_items = sorted(file_weights.items(), key=lambda x: x[1], reverse=True)

        end_time = time.time()

        # Výpis výsledků
        return write(sorted_items, expr, search_type, start_time, end_time)

    else:
        return render_template("mainPage.html")


if __name__ == '__main__':
    app.run(debug=True, port=5001)

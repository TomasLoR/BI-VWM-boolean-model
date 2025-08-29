import json
import os
import math
from collections import Counter
import numpy as np
from sklearn.preprocessing import MinMaxScaler


def get_files(path):
    return os.listdir(path)


def calculate_frequencies(files, path):

    # Vytvořím slovník pro uchování počtu dokumentů, ve kterých se vyskytuje daný term
    df = Counter()

    # Vytvořím slovník pro uchování počtu výskytů termu v jednotlivých dokumentech
    tf = {}
    for file in files:
        with open(os.path.join(path, file), 'r') as f:
            terms = f.read().splitlines()

            # Přidám unikátní termy do slovníku df
            df.update(set(terms))

            # Spočítám počet výskytů termů v daném dokumentu
            tf[file] = Counter(terms)
    return df, tf


def calculate_weights(df, tf, files):
    N = len(files)
    inverted_index = {}

    # Procházím všechny termy ve všech dokumentech
    for file, term_freq in tf.items():
        for term, freq in term_freq.items():

            # Spočítám maximální počet výskytů termu ve všech dokumentech
            max_freq = max(tf[doc][term] for doc in files)

            # Spočítám váhu termu v daném dokumentu
            weight = (freq / max_freq) * math.log(N / df[term])
            if term not in inverted_index:
                inverted_index[term] = {}
            inverted_index[term][file] = weight
    return inverted_index


def normalize_weights(inverted_index):

    # Initializace MinMaxScaleru
    scaler = MinMaxScaler()
    weights = []

    # Přidám váhy termů do pole
    for term in inverted_index:
        for file, weight in inverted_index[term].items():
            weights.append(weight)

    # Normalizuji váhy termů (váhy termů budou v rozmezí <0, 1>)
    weights = np.array(weights).reshape(-1, 1)
    weights_normalized = scaler.fit_transform(weights)

    # Přidám normalizované váhy zpět do inverted indexu
    index = 0
    for term in inverted_index:
        for file in inverted_index[term]:
            inverted_index[term][file] = round(weights_normalized[index][0], 9)
            index += 1
    return inverted_index


def save_weights(inverted_index, filename):

    # Uložím invertovaný seznam do souboru jako JSON
    with open(filename, 'w') as f:
        json.dump(inverted_index, f)


path = 'preprocessed_data'
files = get_files(path)
df, tf = calculate_frequencies(files, path)
print("term frequencies and document frequencies calculated")
inverted_index = calculate_weights(df, tf, files)
print("weights calculated")
inverted_index = normalize_weights(inverted_index)
print("weights normalized")
save_weights(inverted_index, 'inverted_index.json')
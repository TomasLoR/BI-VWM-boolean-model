from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import nltk
import os


def stemming_docs(src_dir, dst_dir):

    # Stáhnu potřebné zdroje pro NLTK
    nltk.download('wordnet')

    # Inicialiuji lemmatizer
    lemmatizer = WordNetLemmatizer()

    # Vytvořím cílový adresář, pokud neexistuje
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)

    # Procházím všechny soubory ve zdrojovém adresáři
    for filename in os.listdir(src_dir):
        if filename.endswith('.txt'):
            with open(os.path.join(src_dir, filename), 'r') as f:

                # Přečtu obsah souboru, tokenizuji text
                words = word_tokenize(f.read())
            
            # Lemmatizuji slova (neboli převedu na základní tvar)
            lemmatized_words = [lemmatizer.lemmatize(word) for word in words]
            
            # Uložím lemmatizovaná slova do cílového souboru
            with open(os.path.join(dst_dir, filename), 'w') as f:
                f.write('\n'.join(lemmatized_words))


src_dir = 'data_src'
dst_dir = 'data_dst'

stemming_docs(src_dir, dst_dir)

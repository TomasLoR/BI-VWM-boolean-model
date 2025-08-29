import os
import nltk
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


def remove_stopwords_and_punctuation(src_dir, dst_dir):

    # Stáhnu potřebné zdroje pro NLTK
    nltk.download('punkt')
    nltk.download('stopwords')

    # Načtu seznam stop slov
    stop_words = set(stopwords.words('english'))

    # Vytvořím cílový adresář, pokud neexistuje
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)

    # Procházím všechny soubory ve zdrojovém adresáři
    for filename in os.listdir(src_dir):
        if filename.endswith('.txt'):
            with open(os.path.join(src_dir, filename), 'r') as file:

                # Přečtu obsah souboru, tokenizuji text a odstraním stop slova a interpunkci
                text = file.read()
                word_tokens = word_tokenize(text)
                filtered_text = [w for w in word_tokens if not w in stop_words and not w in string.punctuation]
                filtered_text = "\n".join(filtered_text)

            # Uložím filtrovaný text do cílového souboru
            with open(os.path.join(dst_dir, filename), 'w') as file:
                file.write(filtered_text)


src_dir = 'data_src'
dst_dir = 'data_dst'

remove_stopwords_and_punctuation(src_dir, dst_dir)
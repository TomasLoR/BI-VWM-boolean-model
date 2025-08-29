import os


def convert_to_lowercase(src_dir, dst_dir):
    # Vytvořím cílový adresář, pokud neexistuje
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)

    # Procházím všechny soubory ve zdrojovém adresáři
    for filename in os.listdir(src_dir):
        if filename.endswith('.txt'):
            src_file = os.path.join(src_dir, filename)
            dst_file = os.path.join(dst_dir, filename)

            # Otevřu zdrojový soubor, převedu jeho obsah na malá písmena a uložím do cílového souboru
            with open(src_file, 'r') as src, open(dst_file, 'w') as dst:
                dst.write(src.read().lower())

src_dir = 'data_src'
dst_dir = 'data_dst'

convert_to_lowercase(src_dir, dst_dir)

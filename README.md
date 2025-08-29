## Přehled projektu

Tento projekt implementuje rozšířený booleovský model vyhledávání, který umožňuje fuzzy booleovské operace pomocí matematických vzorců namísto striktní binární logiky. Systém zpracovává velkou kolekci textových dokumentů, vytváří inverzní index s normalizovanými TF-IDF váhami a poskytuje webové rozhraní pro vyhledávání pomocí booleovských výrazů.

## Funkce

- **Ppředzpracování textu**: Automatická konverze na malá písmena, odstranění stop slov a lematizace
- **TF-IDF vážený inverzní index**: Normalizované váhy pro přesné hodnocení dokumentů
- **Rozšířená booleovská logika**: Podpora operátorů AND, OR, NOT s fuzzy vyhodnocováním
- **Duální metody vyhledávání**: Sekvenční vyhledávání vs. inverzní index pro porovnání výkonu
- **Webové rozhraní**: Flask aplikace s možnostmi vyhledávání v reálném čase
- **Metriky výkonu**: Měření času vyhledávání a statistiky výsledků

## Struktura projektu

```
BI-VWM-boolean-model/
├── inverted index/
│   └── inverted_index.py          # Hlavní generování inverzního indexu
├── preprocessing/
│   ├── makeLowerCase.py           # Normalizace textu
│   ├── removeStopWords.py         # Odstranění stop slov a interpunkce
│   └── stemming.py                # Zpracování lematizace
├── web/
│   ├── main.py                    # Flask webová aplikace
│   ├── inverted_index.json        # Vygenerovaný inverzní index
│   ├── original_data/             # Původní textové dokumenty (~1,400 souborů)
│   ├── preprocessed_data/         # Zpracované textové dokumenty
│   └── templates/
│       └── mainPage.html          # Šablona webového rozhraní
├── bi-vwm_zadani_rozsireny_booleovsky_model_vyhledavani.pdf
└── Dokumentace.pdf
```

## Technická implementace

### Pipeline zpracování textu

1. **Normalizace** (`makeLowerCase.py`): Převádí veškerý text na malá písmena
2. **Čištění** (`removeStopWords.py`): Odstraňuje anglická stop slova a interpunkci pomocí NLTK
3. **Lematizace** (`stemming.py`): Redukuje slova na jejich základní tvary pomocí WordNet lemmatizeru

### Generování inverzního indexu

Systém vytváří vážený inverzní index pomocí:
- **Frekvence termů (TF)**: Počet výskytů termů v každém dokumentu
- **Frekvence dokumentů (DF)**: Počet dokumentů obsahujících každý term
- **TF-IDF váhování**: Vzorec `(tf/max_tf) * log(N/df)`
- **Normalizace**: Min-max škálování do rozsahu [0,1] pomocí scikit-learn

### Zpracování dotazů

1. **Tokenizace**: Parsování booleovských výrazů s korektní prioritou operátorů
2. **Převod na postfix**: Transformace infixové notace na postfixovou pro vyhodnocení
3. **Rekurzivní vyhodnocení**: Rekurzivní zpracování postfixového výrazu
4. **Hodnocení výsledků**: Řazení dokumentů podle vypočítaných vah sestupně

## Instalace a nastavení

### Předpoklady

- Python 3.7+
- Požadované Python balíčky:
  ```bash
  pip install flask nltk scikit-learn numpy
  ```

### Nastavení NLTK dat

Stažení požadovaných NLTK zdrojů:
```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
```

### Příprava dat

1. **Předzpracování** (pokud začínáte ze surových dat):
   ```bash
   cd preprocessing/
   python makeLowerCase.py
   python removeStopWords.py
   python stemming.py
   ```

2. **Generování inverzního indexu**:
   ```bash
   cd "inverted index/"
   python inverted_index.py
   ```

3. **Spuštění webové aplikace**:
   ```bash
   cd web/
   python main.py
   ```

## Použití

### Webové rozhraní

1. Přejděte na `http://localhost:5001` po spuštění aplikace
2. Zadejte booleovské vyhledávací výrazy pomocí klíčových slov z kolekce dokumentů
3. Vyberte mezi sekvenčním nebo inverzní-indexovým způsobem vyhledávání
4. Prohlédněte si výsledky seřazené podle relevance s vypočítanými váhami

### Příklady booleovských dotazů

- **Jednoduchý term**: `education`
- **Operace AND**: `education AND legal`
- **Operace OR**: `lawyer OR attorney`
- **Operace NOT**: `NOT criminal`
- **Složitý výraz**: `(legal OR law) AND NOT criminal`
- **Vnořené operace**: `legal AND (education OR training)`

### Metody vyhledávání

- **Sekvenční vyhledávání**: Iteruje přes všechny dokumenty pro každý dotaz (pomalejší, vzdělávací)
- **Inverzní index**: Používá předpočítaný index pro rychlé vyhledávání (rychlejší, praktické)

## Výkon

Systém zpracovává přibližně 1,400 dokumentů s následujícími charakteristikami:
- **Generování indexu**: Vytváří normalizované TF-IDF váhy pro všechny termy
- **Využití paměti**: Ukládá kompletní inverzní index ve formátu JSON
- **Rychlost vyhledávání**: Metoda inverzního indexu významně překonává sekvenční vyhledávání
- **Přesnost**: Fuzzy booleovské operace poskytují nuancované hodnocení relevance

## Technické detaily

### Závislosti

- **Flask**: Webový framework pro vyhledávací rozhraní
- **NLTK**: Zpracování přirozeného jazyka pro předzpracování textu
- **scikit-learn**: Knihovna strojového učení pro normalizaci vah
- **NumPy**: Numerické výpočty pro TF-IDF kalkulace

### Formáty souborů

- **Vstup**: Obyčejné textové dokumenty (`.txt` soubory)
- **Index**: JSON formát s vnořenou strukturou `{term: {document: weight}}`
- **Výstup**: HTML výsledky s názvy dokumentů, váhami a statistikami


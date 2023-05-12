# BI-VWM Semestral

Cílem bylo implementovat Faginův Top-K algoritmus na vyhledání nejlepších K výsledků v databázi produktů. Uživatel si pomocí webového rozhrazní zvolí, podle jakých parametrů chce produkty řadit. Výstupem je tabulka seřazených výsledků, změřený čas běhu algoritmu a počet, kolik bylo provedeno požadavků na databázi.

Projekt obsahuje jak Faginův Top-K, tak i naivní algoritmus sekvenčním průchodem. Je tak možné vyzkoušet rozdílné přístupy a porovnat jejich efektivitu.

## Závislosti

Pro spuštění je potřeba mít nainstalovaný Python.

1. Aplikace využívá další podpůrné balíčky, proto je vhodné si nejdříve vytvořit virtuální prostředí, například do složky `~/.venv` příkazem:

```bash
python -m venv .venv
```

2. A aktivovat jej

```shell
.venv\Scripts\Activate.ps1 (PowerShell)
.venv\Scripts\activate.bat (CMD)
source .venv/Scripts/activate (Bash)
```

3. Nainstalovat balíčky (závislosti)

```bash
pip install -r requirements.txt
```

## Spuštění aplikace

Samotnou aplikaci lze spustit příkazem

```bash
python main.py
```

Webové rozhraní poté běží na adrese http://127.0.0.1:7860/

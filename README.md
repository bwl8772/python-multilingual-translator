# Python Multilingual Translator

A command-line translator that looks up a word on Linguee, prints translations and usage examples, and saves the results to a UTF-8 text file.

## Requirements

- Python 3.10 or later
- `requests`
- `beautifulsoup4`

Install the dependencies with:

```bash
python -m pip install -r requirements.txt
```

## Usage

Run the translator from the project root:

```bash
python "Multilingual Online Translator/task/translator/translator.py" <source-language> <target-language|all> <word>
```

For example:

```bash
python "Multilingual Online Translator/task/translator/translator.py" english french hello
```

Supported languages are German, English, Spanish, French, Japanese, Dutch, Polish, Portuguese, Romanian, and Russian. Language names are case-insensitive. Use `all` as the target to search every supported language except the source language.

When results are found, they are printed to the terminal and saved as `<word>.txt` in the current directory. Lookups require an internet connection and depend on Linguee being available.

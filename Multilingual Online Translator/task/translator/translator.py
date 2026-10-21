import argparse
from pathlib import Path

import requests
from bs4 import BeautifulSoup


def translate(source, target, word):
    response = requests.get(
        f"https://www.linguee.com/{source}-{target}/search",
        params={"source": source, "query": word},
        headers={"User-Agent": "Mozilla/5.0 AppleWebKit/537.36 Chrome/93.0.4577.82 Safari/537.36"},
        timeout=10,
    )
    if response.status_code == 404:
        return [], []
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    translations = []
    for heading in soup.select("h3.translation_desc"):
        entry = heading.select_one("span.tag_trans a.dictLink")
        if entry:
            translations.append(entry.get_text().strip())
    examples = []
    for example in soup.select("div.example.line"):
        original = example.select_one("span.tag_s")
        translated = example.select_one("span.tag_t")
        if original and translated:
            examples.extend([original.get_text().strip(), translated.get_text().strip()])
    inexact = soup.select_one("div.example_lines.inexact")
    if inexact:
        for lemma in inexact.select("div.lemma"):
            original = lemma.select_one("span.tag_lemma a.dictLink")
            translated = lemma.select_one("span.tag_trans a.dictLink")
            if original and translated:
                examples.extend([original.get_text().strip(), translated.get_text().strip()])
    return translations, examples


LANGUAGES = ["German", "English", "Spanish", "French", "Japanese", "Dutch",
             "Polish", "Portuguese", "Romanian", "Russian"]


def format_results(target, translations, examples):
    lines = [f"{target.title()} Translations:"]
    lines.extend(translations[:1] or ["No translation found."])
    lines.extend(["", f"{target.title()} Examples:"])
    lines.extend(examples[:2] or ["No example found."])
    return "\n".join(lines) + "\n\n"


def save_results(source, target, word):
    targets = [language.lower() for language in LANGUAGES
               if language.lower() != source] if target == "all" else [target]
    results = []
    found = False
    for language in targets:
        translations, examples = translate(source, language, word)
        found = found or bool(translations or examples)
        results.append(format_results(language, translations, examples))
    if not found:
        print(f"Sorry, unable to find {word}")
        return
    text = "\n".join(results)
    print(text, end="")
    Path(Path(word).name + ".txt").write_text(text, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Translate a word using Linguee.")
    parser.add_argument("source")
    parser.add_argument("target")
    parser.add_argument("word")
    args = parser.parse_args()
    source, target = args.source.lower(), args.target.lower()
    supported = {language.lower() for language in LANGUAGES}
    for language, allowed in ((source, supported), (target, supported | {"all"})):
        if language not in allowed:
            print(f"Sorry, the program doesn't support {language}")
            return
    try:
        save_results(source, target, args.word)
    except requests.RequestException:
        print("Something wrong with your internet connection")


if __name__ == "__main__":
    main()

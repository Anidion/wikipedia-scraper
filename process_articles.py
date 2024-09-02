"""os"""

import os
import shutil
import re

ENABLE_DBG = True

KNOWN_GOOD_ARTICLES = [
    "Empire (1973 video game)",
    "Maze (1973 video game)",
    "Empire (1977)",
    "Alto Trek (1978)",
    "MUD (1978)",
    "Avatar (1979)",
    "Sopwith (video game)",
    "SGI Dogfight",
]

QUERY_KW = ["network", "networked", "online"]

OUTPUT_DIR = "matches"


def dbg(msg):
    """Print iff flag is set"""
    if ENABLE_DBG:
        print(msg)


def does_article_match(article_text):
    """Checks if article matches query kws"""
    # One of these headers is usually present at the end of the article
    article_end = re.search(
        r"==\s*References\s*==|==\s*Reception\s*==|==\s*Reviews\s*==|==\s*Sources\s*==|==\s*See also\s*==|==\s*External links\s*==",
        article_text,
    )
    if article_end is None:
        article_end = len(article_text)
    else:
        article_end = article_end.start()

    # Find one matching keyword in the article
    for kw in QUERY_KW:
        found = re.search(r"\b" + kw + r"\b", article_text, re.IGNORECASE)
        if found is not None:
            return True
    return False


def main():
    """
    Loops through raw files and sends them to be processed and writes them to matches if needed
    """
    for root, _, files in os.walk("./out"):
        for file_name in files:
            with open(os.path.join(root, file_name), "r", encoding="utf-8") as article:
                # First 7 lines are metadata we added in dump-wikipedia.py, skip them
                article_text = article.readlines()[7:]
                article_text = "".join(article_text)

                # Skip short articles and redirects
                if len(article_text) < 3:
                    continue
                if article_text.find("#REDIRECT") != -1:
                    continue

                if does_article_match(article_text):
                    dbg(f"Match found in {file_name}")
                    with open(
                        f"./{OUTPUT_DIR}/{file_name}", "w", encoding="utf-8"
                    ) as out_file:
                        out_file.write(article_text)


def prep_output_dir():
    """Clears output dir and recreates it"""
    if os.path.isdir(f"./{OUTPUT_DIR}"):
        shutil.rmtree(OUTPUT_DIR)
    os.mkdir(OUTPUT_DIR)


def post_process():
    """Post-process to check if all known good articles were found"""
    found_kg = []

    for root, _, files in os.walk("./matches"):
        for file_name in files:
            with open(os.path.join(root, file_name), "r", encoding="utf-8") as article:
                if file_name in KNOWN_GOOD_ARTICLES:
                    dbg(f"Found known good article {file_name}")
                    found_kg.append(file_name)

    not_found = set(KNOWN_GOOD_ARTICLES) - set(found_kg)
    if not_found:
        print("The following known good articles were not found:")
        for article in not_found:
            print(article)
    else:
        print("All known good articles were found.")


if __name__ == "__main__":
    print("Processing...")
    prep_output_dir()
    main()
    post_process()
    print("Done.")

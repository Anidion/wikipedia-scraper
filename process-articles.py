import os
import re

known_good_articles = [
    "Empire (1973 video game)",
    "Maze (1973 video game)",
    "Empire (1977)",
    "Alto Trek (1978)",
    "MUD (1978)",
    "Avatar (1979)",
    "Sopwith (video game)",
    "SGI Dogfight",
]

query_keywords = ["network", "networked", "online"]

debug_mode = True

def dbg(msg):
    if debug_mode:
        print(msg)


def does_article_match(article_text):
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
    for kw in query_keywords:
        found = re.search(r"\b" + kw + r"\b", article_text, re.IGNORECASE)
        if found is not None:
          return True
    return False


def main():
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
                    with open(f"./matches/{file_name}", "w", encoding="utf-8") as out_file:
                        out_file.write(article_text)


if __name__ == "__main__":
    print("Processing...")
    main()
    print("Done.")

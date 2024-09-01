import os
import re

known_good_articles = [
    "Empire (1973 video game)",
    "Maze (1973 video game)",
    "Airfight",
    "Spasim",
    "Star Trader",
    "Moria (1975)",
    "Panther (1975)",
    "Empire (1977)",
    "Alto Trek (1978)",
    "MUD (1978)",
    "Avatar (1979)",
    "Sopwith (video game)",
    "SGI Dogfight",
]

target_modes = ["network", "networked", "online"]

debug_mode = True

def dbg(msg):
    if debug_mode:
        print(msg)


def process_article(text, filename="none"):
    article_end = re.search(
        r"==\s*References\s*==|==\s*Reception\s*==|==\s*Reviews\s*==|==\s*Sources\s*==|==\s*See also\s*==|==\s*External links\s*==",
        text,
    )
    if article_end is None:
        article_end = len(text)
    else:
        article_end = article_end.start()

    for target in target_modes:
        mode_start = text.rfind(f" {target} ", 0, article_end)
        if mode_start != -1:
            return True
    return False


def main():
    for root, _, files in os.walk("./out"):
        for file in files:
            with open(os.path.join(root, file), "r", encoding="utf-8") as article:
                # First 7 lines are metadata, skip them
                article_text = article.readlines()[7:]
                article_text = "".join(article_text)
                if len(article_text) < 3:
                    continue
                if article_text.find("#REDIRECT") != -1:
                    continue

                mode_matches = process_article(article_text, file)
                if mode_matches:
                    dbg(f"Match found in {file}")
                    with open(f"./matches/{file}", "w", encoding="utf-8") as out_file:
                        out_file.write(article_text)


if __name__ == "__main__":
    print("Processing...")
    main()
    print("Done.")

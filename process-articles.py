import os
import re


def process_infobox(text):
    infobox_start = text.find("{{Infobox")
    if infobox_start == -1:
        return None

    infobox_end = text.find("\n}}", infobox_start)
    infobox = text[infobox_start : infobox_end + 3]
    infobox_lines = infobox.split("\n")

    # Extract infobox type
    infobox_type_match = re.match(r"\{\{Infobox ([^\|]+)", infobox_lines[0])
    infobox_type = (
        infobox_type_match.group(1).strip() if infobox_type_match else "Unknown"
    )

    # Extract key-value pairs
    infobox_dict = {"type": infobox_type}
    for line in infobox_lines[1:]:
        if line.startswith("|"):
            key_value = line[1:].split("=", 1)
            if len(key_value) == 2:
                key = key_value[0].strip()
                value = key_value[1].strip()
                infobox_dict[key] = value

    return infobox_dict


def process_article(filename, text):
    dict_box = process_infobox(text)
    if dict_box is None:
        return

    modes = dict_box.get("modes", None)

    if modes is None:
        return

    lower_modes = modes.lower()

    if "multiplayer" not in lower_modes and "multi-player" not in lower_modes:
        return

    mode_list = modes.split(",")

    only_mp = list(
        filter(
            lambda x: "multiplayer" in x.lower() or "multi-player" in x.lower(),
            mode_list,
        )
    )

    print(only_mp)


for root, dirs, files in os.walk("./out"):
    for file in files:
        with open(os.path.join(root, file), "r", encoding="utf-8") as article:
            process_article(file, article.read())

from os import mkdir
from pywikibot import Site, Category
from datetime import datetime

site = Site()

# year >= 1971 and year < 1990
year_range = range(1971, 1990)

# Dump all pages in these categories into text files for further processing
for year in year_range:
    category_name = f"Category:{year}_video_games"
    print("Reading category:", category_name)
    category = Category(site, category_name)
    articles = list(category.articles())
    for page in articles:
        page_title = page.title()
        windows_safe_filename = (
            page_title.replace("\\", "")
            .replace("/", "")
            .replace(":", "")
            .replace("*", "")
            .replace("?", "")
            .replace('"', "")
            .replace("<", "")
            .replace(">", "")
            .replace("|", "")
        )

        file_path = f"./out/{year}_video_games/"

        print("\tReading article:", page_title)
        # Create directory if it doesn't exist
        try:
            mkdir(file_path)
        except FileExistsError:
            pass
        with open(
            f"{file_path}{windows_safe_filename}.wikitext", "w", encoding="utf-8"
        ) as file:
            file.write(f"{page_title}\n")
            file.write(f"Permalink: {page.permalink()}\n")
            file.write(f"Accessed on: {datetime.now().isoformat()}\n")
            file.write("\n\n\n------\n")
            file.write(f"{page_title}\n")
            file.write(page.text)

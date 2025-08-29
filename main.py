# This is a sample Python script.
import asyncio

from dotenv import load_dotenv

from csv_output import format_would_you_rather_strings
from scraper import scraper

load_dotenv()


# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


async def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    all_titles = scraper.reddit_title_scraper()
    format_would_you_rather_strings(all_titles, "wyr_test.csv")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

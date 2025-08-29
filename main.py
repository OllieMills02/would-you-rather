# This is a sample Python script.
import asyncio

from dotenv import load_dotenv

from scraper import scraper

load_dotenv()


# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


async def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    scraper.reddit_title_scraper()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

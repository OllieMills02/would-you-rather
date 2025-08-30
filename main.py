# This is a sample Python script.
import asyncio

from dotenv import load_dotenv

from json_output import format_would_you_rather_strings
from scraper.scraper import RedditScraper, txt_scraper
from split import split_data_source
from train import WyrModelTrainer

load_dotenv()


# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


async def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    reddit_scraper = RedditScraper()
    all_titles = reddit_scraper.reddit_title_scraper()
    all_comments = reddit_scraper.reddit_comment_scraper()
    all_txt_questions = txt_scraper()
    print(f"Found {len(all_titles)} titles")
    print(f"Found {len(all_comments)} comments")
    print(f"Found {len(all_txt_questions)} text questions")
    all_questions = all_titles + all_comments + all_txt_questions
    filename = "wyr_data.json"
    format_would_you_rather_strings(all_questions, filename)
    split_data_source(filename)

    trainer_instance = WyrModelTrainer()
    trainer_instance.train()
    # Once trained, you can generate text
    prompt = ""
    while True:
        prompt = input("Enter prompt: ")
        if prompt == "quit" or prompt == "exit":
            exit(0)
        generated_question = trainer_instance.generate_text(prompt)
        print("\n--- Generated Question ---")
        print(generated_question)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/

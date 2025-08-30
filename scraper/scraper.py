import os
import re

import praw
import requests
from bs4 import BeautifulSoup


def txt_scraper() -> list[str] :
    wyr_pattern = r'^(\d+\.\s+)?(wyr|would you rather|would you rather:|wyr:)\s+(.*)\s+or\s+(.*)'

    found_questions = []
    with open("sample_questions.txt", "r") as file:

        for line in file:
            text = line.strip()
            if re.search(wyr_pattern, text, re.IGNORECASE):
                found_questions.append(text)

    return found_questions


def general_web_scraper(url: str) -> list[str] :
    session = requests.Session()

    # Add multiple headers to mimic a real browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': 'https://www.google.com/',  # Mimics a search engine referral
        'Accept-Language': 'en-US,en;q=0.9'
    }

    try:
        response = session.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        all_text_elements = soup.find_all(['h1', 'h2', 'h3', 'h4', 'p', 'a', 'div'])

        wyr_pattern = r'^(\d+\.\s+)?(wyr|would you rather|would you rather:|wyr:)\s+(.*)\s+or\s+(.*)'

        found_questions = []

        for element in all_text_elements:
            text = element.get_text().strip()

            if re.search(wyr_pattern, text, re.IGNORECASE):
                found_questions.append(text)
        return found_questions

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching the page: {e}")
        return []


class RedditScraper:
    def __init__(self):
        self.reddit: praw.Reddit = praw.Reddit(
            client_id=os.environ["PRAW_CLIENT_ID"],
            client_secret=os.environ["PRAW_CLIENT_SECRET"],
            user_agent=os.environ["PRAW_USER_AGENT"],
        )

    def reddit_title_scraper(self) -> list[str] :

        subreddit_name = "WouldYouRather"

        all_titles = []
        subreddit = self.reddit.subreddit(subreddit_name)

        posts = subreddit.hot(limit=1000)

        for post in posts:
            all_titles.append(post.title)

        return all_titles

    def reddit_comment_scraper(self) -> list[str]:
        submission = self.reddit.submission(id='8vieca')

        submission.comments.replace_more(limit=0)

        top_level_comments = []
        for top_level_comment in submission.comments.list():
            top_level_comments.append(top_level_comment.body)


        return top_level_comments

#
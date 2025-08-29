import os

import praw


def reddit_title_scraper():

    reddit = praw.Reddit(
        client_id=os.getenv("PRAW_CLIENT_ID"),
        client_secret=os.getenv("PRAW_CLIENT_SECRET"),
        user_agent=os.getenv("PRAW_USER_AGENT"),
    )
    subreddit_name = "WouldYouRather"
    pages_to_scrape = 100
    posts_per_page = 100

    all_titles = []
    subreddit = reddit.subreddit(subreddit_name)

    for _ in range(pages_to_scrape):
        posts = subreddit.hot(limit=posts_per_page)

        for post in posts:
            all_titles.append(post.title)

    for title in all_titles:
        print(title)


#
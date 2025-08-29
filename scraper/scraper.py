import os
import praw


def reddit_title_scraper() -> list[str] :
    reddit = praw.Reddit(
        client_id=os.environ["PRAW_CLIENT_ID"],
        client_secret=os.environ["PRAW_CLIENT_SECRET"],
        user_agent=os.environ["PRAW_USER_AGENT"],
    )
    subreddit_name = "WouldYouRather"

    all_titles = []
    subreddit = reddit.subreddit(subreddit_name)

    posts = subreddit.hot(limit=1000)

    for post in posts:
        all_titles.append(post.title)

    print(f"Found {len(all_titles)} posts")

    return all_titles


#
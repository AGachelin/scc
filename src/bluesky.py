from atproto import Client
from yaml import load, FullLoader
import pandas as pd
import argparse
import os

os.makedirs("data", exist_ok=True)

parser = argparse.ArgumentParser()
parser.add_argument("--search", type=str, help="Search query")
parser.add_argument("--n", type=int, default=1000, help="Number of posts to fetch")
parser.add_argument("-a", action="store_true", help="Fetch all")
parser.add_argument("-s", action="store_true", help="Search only latest posts")
parser.add_argument("-t", action="store_true", help="Search only top posts")
parser.add_argument("-f", action="store_true", help="Feed posts")

args = parser.parse_args()

creds = load(open("./env.yaml"), Loader=FullLoader)
client = Client()
client.login(creds["BLUESKY_EMAIL"], creds["BLUESKY_PASSWORD"])

n_elements = args.n

if args.a:
    args.s = True
    args.t = True
    args.f = True

if args.search is not None:
    args.s = True
    args.t = True
else:
    args.search = "trump"
    args.s = True

if args.s:
    latest_posts = []
    cursor = None
    while True: 
        response = client.app.bsky.feed.search_posts({"q":args.search, "limit":100, "sort": 'latest',"cursor":cursor, "lang":"en"})
        latest_posts.extend(response["posts"])
        cursor = response.cursor
        if not cursor:
            break
        if len(latest_posts) >= n_elements:
            break
        print(len(latest_posts))

    df = pd.DataFrame([[post.record.created_at, post.record.text, post.author.did, 
                        post.author.handle, post.author.display_name, post.author.created_at, 
                        post.reply_count, post.like_count, post.repost_count]
    for post in latest_posts], columns=["created_at", "text", "author_did", "author_handle", 
                                    "author_display_name", "author_created_at", "reply_count", "like_count", "repost_count"])
    df["created_at"] = pd.to_datetime(df["created_at"], format="mixed", utc=True)
    df.set_index("created_at", inplace=True)
    df.to_csv("./data/bsky_latest_posts.csv")


if args.t:
    cursor = None
    top_posts = []
    while True: 
        response = client.app.bsky.feed.search_posts({"q":args.search, "limit":100, "sort": 'top',"cursor":cursor, "lang":"en"})
        top_posts.extend(response["posts"])
        cursor = response.cursor
        if not cursor:
            break
        if len(top_posts) >= n_elements:
            break
        print(len(top_posts))

    df = pd.DataFrame([[post.record.created_at, post.record.text, post.author.did, 
                        post.author.handle, post.author.display_name, post.author.created_at, 
                        post.reply_count, post.like_count, post.repost_count]
    for post in top_posts], columns=["created_at", "text", "author_did", "author_handle", 
                                    "author_display_name", "author_created_at", "reply_count", "like_count", "repost_count"])
    df["created_at"] = pd.to_datetime(df["created_at"], format="mixed", utc=True)
    df.set_index("created_at", inplace=True)
    df.to_csv("./data/bsky_top_posts.csv")

if args.f:
    feed_uri = 'at://did:plc:z72i7hdynmk6r22z27h6tvur/app.bsky.feed.generator/whats-hot'
    feed_posts = []
    cursor = None
    while True:
        response = client.app.bsky.feed.get_feed({"feed": feed_uri, "limit": 100, "cursor": cursor})
        feed_posts.extend(response["feed"])
        cursor = response.cursor
        if not cursor:
            break
        if len(feed_posts) >= n_elements:
            break
        print(len(feed_posts))
    df = pd.DataFrame([[post.post.record.created_at, post.post.record.text, post.post.author.did, 
                        post.post.author.handle, post.post.author.display_name, post.post.author.created_at, 
                        post.post.reply_count, post.post.like_count, post.post.repost_count]
    for post in feed_posts], columns=["created_at", "text", "author_did", "author_handle", 
                                    "author_display_name", "author_created_at", "reply_count", "like_count", "repost_count"])
    df["created_at"] = pd.to_datetime(df["created_at"], format="mixed", utc=True)
    df.set_index("created_at", inplace=True)
    df.to_csv("./data/bsky_feed_posts.csv")

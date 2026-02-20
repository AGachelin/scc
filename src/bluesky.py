from atproto import Client
from yaml import load, FullLoader
import pandas as pd

creds = load(open("./env.yaml"), Loader=FullLoader)
client = Client()
client.login(creds["BLUESKY_EMAIL"], creds["BLUESKY_PASSWORD"])


all_posts = []
cursor = None
n_elements = 10000
while True: 
    response = client.app.bsky.feed.search_posts({"q":"computational social science", "limit":100, "sort": 'latest',"cursor":cursor})
    all_posts.extend(response["posts"])
    cursor = response.cursor
    if not cursor:
        break  # No more posts to fetch
    if len(all_posts) >= n_elements:
        break
    print(len(all_posts))

df = pd.DataFrame([[post.record.created_at, post.record.text, post.author.did, 
                    post.author.handle, post.author.display_name, post.author.created_at, 
                    post.reply_count, post.like_count, post.repost_count]
 for post in all_posts], columns=["created_at", "text", "author_did", "author_handle", 
                                  "author_display_name", "author_created_at", "reply_count", "like_count", "repost_count"])
df["created_at"] = pd.to_datetime(df["created_at"], format="mixed", utc=True)
df.set_index("created_at", inplace=True)
df.to_csv("./data/bsky_posts.csv")


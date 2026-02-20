import json

from atproto import Client
from yaml import load, FullLoader
import pandas as pd

creds = load(open("env.yaml"), Loader=FullLoader)
client = Client()
client.login(creds["BLUESKY_EMAIL"], creds["BLUESKY_PASSWORD"])

url = "https://bsky.app/profile/bdecourson.bsky.social/post/3meiwcx6jts26"
handle = "bdecourson.bsky.social"
post_id = "3meiwcx6jts26"



user_info = client.resolve_handle(handle)
did = user_info.did

post_uri = f"at://{did}/app.bsky.feed.post/{post_id}"
post = client.app.bsky.feed.get_post_thread({"uri":post_uri})
json_post = post.model_dump()

with open("data/post.json", "w") as f:
    f.write(json.dumps(json_post, indent=4))



reposted = client.app.bsky.feed.get_reposted_by({"uri":post_uri})
len(reposted.model_dump()["reposted_by"])


all_posts = []
cursor = None

while True:
    response = client.app.bsky.feed.get_author_feed({"actor":did, "limit":100, "cursor":cursor})
    all_posts.extend(response["feed"])
    cursor = response.cursor
    if not cursor:
        break  # Fin de la pagination

print(f"Nombre total de posts récupérés : {len(all_posts)}")

# Optionnel : Afficher les 5 premiers posts
for post in all_posts[:5]:
    print(post["post"]["record"]["text"])

user_info = client.resolve_handle("clairem.secondlife.bio")
did = user_info.did
feed_id = "aaajf4zkrdcte"
feed_uri = f"at://{did}/app.bsky.feed.generator/{feed_id}"
print(feed_uri)

# Retrieve all posts from the feed
all_posts = []
cursor = None

while True:
    # Request feed posts with pagination
    response = client.app.bsky.feed.get_feed({"feed":feed_uri, "limit":100, "cursor":cursor})

    # Add posts to the list
    all_posts.extend(response["feed"])

    # Handle pagination
    cursor = response.cursor
    if not cursor:
        break  # No more posts to fetch

# Print total posts retrieved
print(f"Total posts retrieved from feed '{feed_uri}': {len(all_posts)}")

print(all_posts[10].dict()["post"]["record"]["text"])




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


post = all_posts[1100]

dump = post.model_dump()


df = pd.DataFrame([[post.record.created_at, post.record.text, post.author.did, 
                    post.author.handle, post.author.display_name, post.author.created_at, 
                    post.reply_count, post.like_count, post.repost_count]
 for post in all_posts], columns=["created_at", "text", "author_did", "author_handle", 
                                  "author_display_name", "author_created_at", "reply_count", "like_count", "repost_count"])
df["created_at"] = pd.to_datetime(df["created_at"], format="mixed", utc=True)
df.set_index("created_at", inplace=True)
df.to_csv("../data/bsky_posts.csv")


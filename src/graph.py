from bertopic import representation
import pandas as pd
import openai
from yaml import load, FullLoader
from bertopic import BERTopic
from bertopic.representation import OpenAI
import matplotlib.pyplot as plt
import os

os.makedirs("./plots", exist_ok=True)

URL_API = "https://openrouter.ai/api/v1"
creds = load(open("./env.yaml"), Loader=FullLoader)

df = pd.read_csv("./data/bsky_posts.csv", index_col=0, parse_dates=True)
df["text"] = df["text"].astype(str).fillna("")
docs = df["text"].values.tolist()

openai_client = openai.OpenAI(api_key=creds["OPEN_ROUTER"], base_url=URL_API)
representation_model = OpenAI(openai_client, model="gpt-4o-mini", chat=True)

topic_model = BERTopic(representation_model=representation_model)
topics, probs = topic_model.fit_transform(documents=docs)

# Results
info = topic_model.get_topic_info()
print(info)

plt_fig = plt.figure()
fig = topic_model.visualize_hierarchy()

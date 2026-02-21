import pandas as pd
import openai
from yaml import load, FullLoader
from bertopic import BERTopic
from bertopic.representation import OpenAI
import os
# ADD [CSS2026] TO EMAIL

os.makedirs("./plots", exist_ok=True)

URL_API = "https://openrouter.ai/api/v1"
creds = load(open("./env.yaml"), Loader=FullLoader)

df = pd.read_csv("./data/bsky_top_posts.csv", index_col=0, parse_dates=True)
df["text"] = df["text"].astype(str).fillna("")
docs = df["text"].values.tolist()

openai_client = openai.OpenAI(api_key=creds["OPEN_ROUTER"], base_url=URL_API)
representation_model = OpenAI(openai_client, model="gpt-4o-mini", chat=True)

topic_model = BERTopic(representation_model=representation_model)
topics, probs = topic_model.fit_transform(documents=docs)

# Results
info = topic_model.get_topic_info()
print(info)

fig = topic_model.visualize_documents(
    docs=docs,
    hide_annotations=True,
)
fig.update_layout(
    title="BERTopic Document Clustering",
    title_font_size=20,
    width=1000,
    height=800,
    hovermode="closest",
)
fig.show()

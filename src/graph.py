import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from bertopic import BERTopic

df = pd.read_csv("./data/bsky_posts.csv", index_col=0, parse_dates=True)

topic_model = BERTopic()
topics, probs = topic_model.fit_transform(df["text"].tolist())
print(topics)

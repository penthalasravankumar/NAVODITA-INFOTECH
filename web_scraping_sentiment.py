# Web Scraping and Sentiment Analysis Project
# -------------------------------------------
# This script scrapes latest news headlines, analyzes sentiment, and visualizes the results.

import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
import matplotlib.pyplot as plt

# Step 1: Scrape news headlines
url = "https://www.bbc.com/news"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Extract headlines (BBC headlines are under <h3> tags with class "gs-c-promo-heading__title")
headlines = [h3.get_text() for h3 in soup.find_all("h3") if h3.get_text() != ""]

print("🔹 Top Headlines:")
for i, headline in enumerate(headlines[:10], 1):
    print(f"{i}. {headline}")

# Step 2: Sentiment analysis
positive, negative, neutral = 4, 2, 0
for h in headlines:
    analysis = TextBlob(h)
    if analysis.sentiment.polarity > 0:
        positive += 1
    elif analysis.sentiment.polarity < 0:
        negative += 1
    else:
        neutral += 1

# Step 3: Display sentiment counts
print("\n📊 Sentiment Summary:")
print(f"Positive Headlines: {positive}")
print(f"Negative Headlines: {negative}")
print(f"Neutral Headlines : {neutral}")

# Step 4: Visualize with pie chart
labels = ['Positive', 'Negative', 'Neutral']
values = [positive, negative, neutral]
colors = ['#2ecc71', '#e74c3c', '#f1c40f']

plt.figure(figsize=(6, 6))
plt.pie(values, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
plt.title("News Headlines Sentiment Analysis", fontsize=14, fontweight='bold')
plt.show()
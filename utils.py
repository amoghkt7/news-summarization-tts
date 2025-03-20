import requests
from bs4 import BeautifulSoup
from transformers import pipeline
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from gtts import gTTS
from deep_translator import GoogleTranslator
from keybert import KeyBERT
import os

# Initialize KeyBERT model
kw_model = KeyBERT()

def fetch_google_news_rss(company_name, max_results=10):
    """
    Fetches news articles from Google News RSS feed.
    """
    query = company_name.replace(" ", "+")
    url = f"https://news.google.com/rss/search?q={query}"
    response = requests.get(url)
    if response.status_code != 200:
        return {"error": "Failed to fetch RSS feed."}
    soup = BeautifulSoup(response.content, "xml")
    articles = []
    for item in soup.find_all("item")[:max_results]:
        title = item.title.text
        link = item.link.text
        snippet = item.description.text
        articles.append({"title": title, "link": link, "snippet": snippet})
    return articles

# Load summarization model once
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_text_transformer(text, max_length=100, min_length=30):
    """
    Summarizes text using a pre-trained BART model.
    """
    if not text or len(text.split()) < 10:
        return "Summary not available (text too short)."
    if len(text.split()) > 500:
        text = " ".join(text.split()[:500])
    try:
        summary = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
        return summary[0]['summary_text']
    except Exception as e:
        return f"Error summarizing text: {str(e)}"

nltk.download("vader_lexicon")
sia = SentimentIntensityAnalyzer()

def analyze_sentiment(text):
    """
    Analyzes sentiment using VADER.
    """
    sentiment_score = sia.polarity_scores(text)["compound"]
    if sentiment_score >= 0.05:
        return "Positive"
    elif sentiment_score <= -0.05:
        return "Negative"
    else:
        return "Neutral"

def translate_to_hindi(text):
    """
    Translates English text to Hindi using deep-translator.
    """
    try:
        return GoogleTranslator(source="en", target="hi").translate(text)
    except Exception as e:
        return f"Translation error: {str(e)}"
    
def generate_hindi_tts(text, filename="output.mp3"):
    """
    Converts text to Hindi speech and saves as an MP3 file.
    """
    try:
        hindi_text = translate_to_hindi(text)
        tts = gTTS(text=hindi_text, lang="hi", slow=False)
        tts.save(filename)
        return filename
    except Exception as e:
        return f"Error generating speech: {str(e)}"

def process_news_articles(company_name, max_articles=5):
    """
    Fetches, summarizes, analyzes sentiment, extracts topics, and generates TTS for news articles.
    Each article now includes keys: "title", "link", "summary", "sentiment", "topics", and "audio".
    """
    articles = fetch_google_news_rss(company_name, max_articles)
    if "error" in articles:
        return {"error": "Failed to fetch news articles."}
    processed_articles = []
    for idx, article in enumerate(articles, 1):
        summary = summarize_text_transformer(article["snippet"])
        sentiment = analyze_sentiment(summary)
        # Extract topics from the summary using KeyBERT
        topics = kw_model.extract_keywords(summary, keyphrase_ngram_range=(1, 2), stop_words='english', top_n=3)
        topics_list = [kw for kw, score in topics]
        # Save audio in the main directory (no folders)
        audio_filename = f"{company_name}_news_{idx}.mp3"
        generate_hindi_tts(summary, audio_filename)
        processed_articles.append({
            "title": article["title"],
            "link": article["link"],
            "summary": summary,
            "sentiment": sentiment,
            "topics": topics_list,
            "audio": audio_filename
        })
    return processed_articles

def generate_comparative_report(company, articles):
    """
    Generates a comparative report including sentiment distribution, coverage differences,
    and topic overlap, along with a final sentiment analysis and audio reference.
    The output format is similar to the processed articles.
    
    Args:
        company (str): The company name.
        articles (list): List of processed article dictionaries.
        
    Returns:
        dict: A structured JSON report starting with the "Comparative Sentiment Score".
    """
    # Count sentiment distribution
    sentiment_counts = {"Positive": 0, "Negative": 0, "Neutral": 0}
    for article in articles:
        sentiment_counts[article["sentiment"]] += 1

    # Determine overall sentiment based on majority
    overall_sentiment = "Neutral"
    if sentiment_counts["Positive"] > sentiment_counts["Negative"]:
        overall_sentiment = "Positive"
    elif sentiment_counts["Negative"] > sentiment_counts["Positive"]:
        overall_sentiment = "Negative"

    # Coverage differences: using the transformer summarizer to analyze the combined summaries.
    # Concatenate all summaries and generate a concise report.
    all_summaries = " ".join(article["summary"] for article in articles)
    try:
        coverage_diff_result = summarizer(all_summaries, max_length=80, min_length=40, do_sample=False)
        coverage_diff = coverage_diff_result[0]['summary_text']
    except Exception as e:
        coverage_diff = f"Error generating coverage differences: {str(e)}"

    # Topic overlap: compute intersection of topics among articles.
    # (Assumes each article has a "topics" key which is a list.)
    topics_list = [set(article.get("topics", [])) for article in articles if "topics" in article]
    if topics_list:
        common_topics = list(set.intersection(*topics_list))
    else:
        common_topics = []

    # Also, compute unique topics per article (a simple version).
    unique_topics = []
    for i, topics in enumerate(topics_list):
        others = set.union(*(topics_list[:i] + topics_list[i+1:])) if len(topics_list) > 1 else set()
        unique = list(topics - others)
        unique_topics.append(unique)


    # Prepare the report in the desired format starting with Comparative Sentiment Score
    report = {
        "Comparative Sentiment Score": {
            "Sentiment Distribution": sentiment_counts,
            "Coverage Differences": coverage_diff,
            "Topic Overlap": {
                "Common Topics": common_topics,
                "Unique Topics": unique_topics
            }
        },
        "Final Sentiment Analysis": f"Overall, {company}'s news coverage is {overall_sentiment}.",
   
    }
    return report

import requests
from bs4 import BeautifulSoup

def fetch_google_news_rss(company_name, max_results=10):
    """
    Fetches news articles from Google News RSS feed.
    
    Args:
        company_name (str): The company to search for.
        max_results (int): Number of articles to fetch.

    Returns:
        list: A list of dictionaries containing 'title', 'link', and 'snippet'.
    """
    # Construct Google News RSS feed URL
    query = company_name.replace(" ", "+")
    url = f"https://news.google.com/rss/search?q={query}"

    response = requests.get(url)

    if response.status_code != 200:
        return {"error": "Failed to fetch RSS feed."}

    soup = BeautifulSoup(response.content, "xml")  # XML Parser

    articles = []
    for item in soup.find_all("item")[:max_results]:
        title = item.title.text
        link = item.link.text
        snippet = item.description.text  # Sometimes empty in RSS

        articles.append({"title": title, "link": link, "snippet": snippet})

    return articles
from transformers import pipeline

# Load the model only once to avoid performance issues
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

from transformers import pipeline

# Load the model only once to avoid performance issues
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_text_transformer(text, max_length=100, min_length=30):
    """
    Summarizes text using a pre-trained BART model.

    Args:
        text (str): The input text to summarize.
        max_length (int): Maximum length of the summary.
        min_length (int): Minimum length of the summary.

    Returns:
        str: The summarized text.
    """
    # Handle empty or very short input
    if not text or len(text.split()) < 10:
        return "Summary not available (text too short)."

    # Limit text to avoid exceeding model input size
    if len(text.split()) > 500:
        text = " ".join(text.split()[:500])  # Trim input to first 500 words

    try:
        summary = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
        return summary[0]['summary_text']
    except Exception as e:
        return f"Error summarizing text: {str(e)}"


from nltk.sentiment import SentimentIntensityAnalyzer

# Initialize the VADER sentiment analyzer
sia = SentimentIntensityAnalyzer()

def analyze_sentiment(text):
    """
    Analyzes the sentiment of a given text using VADER.

    Args:
        text (str): The input text.

    Returns:
        str: "Positive", "Negative", or "Neutral" based on sentiment score.
    """
    sentiment_score = sia.polarity_scores(text)["compound"]

    if sentiment_score >= 0.05:
        return "Positive"
    elif sentiment_score <= -0.05:
        return "Negative"
    else:
        return "Neutral"

from gtts import gTTS
from googletrans import Translator

translator = Translator()  # Initialize translator

def translate_to_hindi(text):
    """
    Translates English text to Hindi.
    
    Args:
        text (str): The text in English.

    Returns:
        str: Translated text in Hindi.
    """
    try:
        translation = translator.translate(text, src="en", dest="hi")
        return translation.text
    except Exception as e:
        return f"Translation error: {str(e)}"

def generate_hindi_tts(text, filename="output.mp3"):
    """
    Converts the given English text into Hindi speech and saves it as an MP3 file.

    Args:
        text (str): The text to convert.
        filename (str): The output filename.

    Returns:
        str: The filename of the saved audio file.
    """
    try:
        hindi_text = translate_to_hindi(text)  # ✅ Convert to Hindi
        tts = gTTS(text=hindi_text, lang="hi", slow=False)
        tts.save(filename)
        return filename
    except Exception as e:
        return f"Error generating speech: {str(e)}"

    
from utils import fetch_google_news_rss, summarize_text_transformer, analyze_sentiment, generate_hindi_tts

import os

def process_news_articles(company_name, max_articles=5):
    articles = fetch_google_news_rss(company_name, max_articles)

    if "error" in articles:
        return {"error": "Failed to fetch news articles."}

    processed_articles = []
    for idx, article in enumerate(articles, 1):
        summary = summarize_text_transformer(article["snippet"])
        sentiment = analyze_sentiment(summary)

        # ✅ Save audio in a specific folder
        audio_filename = f"tts_audio/{company_name}_news_{idx}.mp3"
        os.makedirs("tts_audio", exist_ok=True)  # Ensure folder exists
        generate_hindi_tts(summary, audio_filename)

        processed_articles.append({
            "title": article["title"],
            "link": article["link"],
            "summary": summary,
            "sentiment": sentiment,
            "audio": os.path.abspath(audio_filename)  # ✅ Use absolute path
        })

    return processed_articles

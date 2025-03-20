from fastapi import FastAPI
from utils import process_news_articles
import uvicorn

app = FastAPI()

@app.get("/fetch-news/")
def fetch_news(company: str, max_articles: int = 5):
    """Fetch summarized news, sentiment analysis, and TTS."""
    return process_news_articles(company, max_articles)

@app.get("/compare-sentiment/")
def compare_sentiment(company: str, max_articles: int = 5):
    """Compare sentiment across multiple news articles."""
    articles = process_news_articles(company, max_articles)
    sentiment_counts = {"Positive": 0, "Negative": 0, "Neutral": 0}

    for article in articles:
        sentiment_counts[article["sentiment"]] += 1

    return {
        "company": company,
        "total_articles": len(articles),
        "sentiment_distribution": sentiment_counts,
        "analysis_summary": f"{company} has {sentiment_counts['Positive']} positive, "
                            f"{sentiment_counts['Negative']} negative, and "
                            f"{sentiment_counts['Neutral']} neutral articles."
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
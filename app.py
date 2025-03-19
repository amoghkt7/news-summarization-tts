import streamlit as st
from utils import process_news_articles
import os

st.set_page_config(page_title="News Summarization & TTS", layout="wide")

st.title("📰 News Summarization & TTS Application")
st.write("Enter a company name to fetch the latest news, summarize it, analyze sentiment, and generate a Hindi speech output.")

company_name = st.text_input("Enter Company Name", "")

if st.button("Get News Summary"):
    if company_name:
        st.write(f"Fetching news for: **{company_name}**...")
        
        news_data = process_news_articles(company_name)

        if "error" in news_data:
            st.error(news_data["error"])
        else:
            st.write("### News Articles")
            
            for idx, article in enumerate(news_data, 1):
                st.subheader(f"{idx}. {article['title']}")
                st.markdown(f"[Read Full Article]({article['link']})", unsafe_allow_html=True)
                st.write(f"**Summary:** {article['summary']}")
                st.write(f"**Sentiment:** {article['sentiment']}")
                
                # ✅ Check if the audio file exists before playing
                if article["audio"] and os.path.exists(article["audio"]):
                    st.audio(article["audio"], format="audio/mp3")
                else:
                    st.warning("Audio not available.")

    else:
        st.warning("Please enter a company name.")

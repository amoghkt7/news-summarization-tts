# 📰 News Summarization & Sentiment Analysis with Hindi TTS

## 🚀 Overview
This project **fetches news articles**, summarizes them using NLP, analyzes sentiment, extracts key topics, and generates **Hindi Text-to-Speech (TTS)** for the final sentiment analysis.

It is built with:
- **Streamlit** for an interactive UI
- **Hugging Face Transformers** for NLP-based summarization
- **VADER** for sentiment analysis
- **KeyBERT** for topic extraction
- **gTTS** for Hindi text-to-speech

---

## **🎯 Features**
✔ **Fetch Latest News**: Retrieves articles from **Google News RSS**  
✔ **Summarization**: Uses **BART Transformer Model** to generate concise summaries  
✔ **Sentiment Analysis**: Classifies news as **Positive, Negative, or Neutral**  
✔ **Topic Extraction**: Uses **KeyBERT** to extract key discussion points  
✔ **Comparative Analysis**: Provides an overall sentiment trend of a company  
✔ **Hindi TTS**: Converts the **Final Sentiment Analysis** to **Hindi speech**  

---

## **🛠 Installation & Setup**
### **1️⃣ Install Dependencies**
Ensure you have Python installed, then install the required libraries:
```bash
pip install -r requirements.txt

2️⃣ Run the Streamlit App
bash

streamlit run app.py
🌐 Usage
📌 Fetch News, Summarize, & Analyze
1️⃣ Enter Company Name
2️⃣ Click Get News Summary
3️⃣ View Summarized Articles with:

Title
Summary
Sentiment (Positive/Negative/Neutral)
Topics
🎧 Audio (MP3)
4️⃣ View Overall Comparative Analysis
📊 Sentiment Distribution
🔎 Topic Overlap
🎧 Hindi TTS of Final Sentiment
📡 Deployment (Hugging Face)
To deploy on Hugging Face Spaces, follow these steps:

1️⃣ Create a new Hugging Face Space
2️⃣ Upload all project files (app.py, utils.py, requirements.txt, etc.)
3️⃣ Set "App File" to app.py in the Space settings
4️⃣ Restart the Space


👨‍💻 Technologies Used
✔ Python
✔ Streamlit
✔ BeautifulSoup (Web Scraping)
✔ Hugging Face Transformers (Summarization)
✔ VADER Sentiment Analysis
✔ KeyBERT (Topic Extraction)
✔ gTTS (Text-to-Speech)


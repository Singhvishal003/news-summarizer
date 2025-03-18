from fastapi import FastAPI # type: ignore
from utils import fetch_articles, analyze_sentiment, summarize_text, extract_topics, comparative_analysis, generate_tts

app = FastAPI()

@app.post("/analyze")
async def analyze_company(company: dict):
    """Analyze news articles for a given company."""
    print(f"Received request payload: {company}")  # Debug log
    company_name = company.get("company")
    language = company.get("language", "en")  # Default to English
    if not company_name:
        print("Error: Company name is missing.")
        return {"error": "Company name is required."}
    
    articles = fetch_articles(company_name)
    print(f"Fetched articles: {articles[:2]}...")  # Debug log (first two articles for brevity)
    if not articles or all("Error" in article["Title"] for article in articles):
        print("Error: No articles found or API key issue.")
        return {"error": "No articles found or API key issue."}
    
    for article in articles:
        article["Sentiment"] = analyze_sentiment(article["Summary"])
        article["Summary"] = summarize_text(article["Summary"])
        article["Topics"] = extract_topics(article["Summary"])
    
    comparative = comparative_analysis(articles)
    
    positive_count = comparative["Sentiment Distribution"]["Positive"]
    final_sentiment = "mostly positive" if positive_count > 5 else "mixed"
    hindi_summary = f"{company_name} के समाचार {final_sentiment} हैं।" if language.lower() == "hi" else f"{company_name}’s news coverage is {final_sentiment}."
    audio_file = generate_tts(hindi_summary if language.lower() == "hi" else final_sentiment, language)
    
    return {
        "Company": company_name,
        "Articles": articles,
        "Comparative Sentiment Score": comparative,
        "Final Sentiment Analysis": hindi_summary if language.lower() == "hi" else final_sentiment,
        "Audio": audio_file
    }
import requests # type: ignore
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer # type: ignore
from yake import KeywordExtractor # type: ignore
from gtts import gTTS # type: ignore

# Initialize sentiment analyzer and keyword extractor
analyzer = SentimentIntensityAnalyzer()
kw_extractor = KeywordExtractor(lan="en", n=1, top=3)

def fetch_articles(company_name):
    """Fetch news articles for a given company using GNews API."""
    api_key = "https://gnews.io/api/v4/search?q=example&apikey=c88b628045ad7155d094fdc4d87e75b8"  # Replace with your GNews API key
    if not api_key or api_key == "your-gnews-api-key":
        return [{"Title": "Error", "Summary": "GNews API key is missing or invalid.", "Link": "#"}]
    
    url = f"https://gnews.io/api/v4/search?q={company_name}&lang=en&max=10&token={api_key}"
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        data = response.json()
        if 'errors' in data:
            error_message = data['errors'][0] if data['errors'] else "Unknown GNews API error."
            print(f"GNews API error: {error_message}")
            return [{"Title": "Error", "Summary": f"GNews API error: {error_message}", "Link": "#"}]
    except requests.RequestException as e:
        print(f"Error fetching articles from GNews: {e}")
        return [{"Title": "Error", "Summary": f"Failed to fetch articles: {e}", "Link": "#"}]
    
    articles = []
    for item in data.get('articles', [])[:10]:
        try:
            title = item['title'] if item['title'] else "No title available"
            link = item['url'] if item['url'] else "#"
            summary = item['description'][:200] if item['description'] else "No summary available"
            articles.append({"Title": title, "Summary": summary, "Link": link})
        except Exception as e:
            print(f"Error processing article: {e}")
            continue
    
    return articles if len(articles) >= 10 else articles + [{"Title": f"Dummy {i}", "Summary": "N/A", "Link": "#"} for i in range(10 - len(articles))]

def analyze_sentiment(text):
    """Analyze sentiment of text with VADER for better accuracy."""
    try:
        score = analyzer.polarity_scores(text)
        if score['compound'] >= 0.05:
            return "Positive"
        elif score['compound'] <= -0.05:
            return "Negative"
        return "Neutral"
    except Exception as e:
        print(f"Error in sentiment analysis: {e}")
        return "Neutral"

def summarize_text(text):
    """Summarize text to a short paragraph."""
    try:
        sentences = text.split('.')
        return sentences[0] + '.' if sentences and len(sentences[0]) > 10 else text[:100] + "..."
    except Exception as e:
        print(f"Error in summarization: {e}")
        return text[:100] + "..."

def extract_topics(text):
    """Extract key topics from text using YAKE."""
    try:
        keywords = kw_extractor.extract_keywords(text)
        return [kw[0] for kw in keywords] if keywords else ["Topic 1", "Topic 2", "Topic 3"]
    except Exception as e:
        print(f"Error extracting topics: {e}. Returning default topics.")
        return ["Topic 1", "Topic 2", "Topic 3"]

def comparative_analysis(articles):
    """Perform comparative sentiment and topic analysis."""
    sentiment_dist = {"Positive": 0, "Negative": 0, "Neutral": 0}
    for article in articles:
        sentiment = analyze_sentiment(article["Summary"])
        sentiment_dist[sentiment] += 1
    
    coverage_diff = []
    if len(articles) > 1:
        coverage_diff = [{
            "Comparison": f"{articles[0]['Title']} highlights positives, while {articles[1]['Title']} focuses on negatives.",
            "Impact": "Positive news boosts confidence; negative news raises concerns."
        }]
    
    topic_overlap = {"Common Topics": [], "Unique Topics in Article 1": [], "Unique Topics in Article 2": []}
    if len(articles) > 1:
        try:
            if "Topics" in articles[0] and "Topics" in articles[1]:
                common_topics = set(articles[0]["Topics"]) & set(articles[1]["Topics"])
                unique_1 = set(articles[0]["Topics"]) - set(articles[1]["Topics"])
                unique_2 = set(articles[1]["Topics"]) - set(articles[0]["Topics"])
                topic_overlap = {
                    "Common Topics": list(common_topics),
                    "Unique Topics in Article 1": list(unique_1),
                    "Unique Topics in Article 2": list(unique_2)
                }
        except Exception as e:
            print(f"Error in topic overlap: {e}")
    
    return {
        "Sentiment Distribution": sentiment_dist,
        "Coverage Differences": coverage_diff,
        "Topic Overlap": topic_overlap
    }

def generate_tts(text, language="en", filename="output.mp3"):
    """Generate TTS for text in specified language (en or hi)."""
    try:
        lang_code = "hi" if language.lower() == "hi" else "en"
        tts = gTTS(text=text, lang=lang_code)
        tts.save(filename)
        return filename
    except Exception as e:
        print(f"Error generating TTS: {e}")
        return None
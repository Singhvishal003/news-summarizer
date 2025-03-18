# News Summarizer & Text-to-Speech Application

A web-based application that extracts news articles for a company using the GNews API, performs sentiment analysis with VADER and TextBlob, conducts comparative analysis, and generates text-to-speech (TTS) summaries in English and Hindi. Features include a "Read Screen" functionality to speak all visible text, a dark-themed interface, and configurable API ports.

## Project Setup
1. **Clone the Repository**:
2. **Navigate to the Project Folder**:
3. **Create and Activate a Virtual Environment**:
- Windows: `venv\Scripts\activate`
- Mac/Linux: `source venv/bin/activate`
4. **Install Dependencies**:
5. **Download NLTK Data**:
6. **Obtain a GNews API Key**:
- Sign up at https://gnews.io, copy your API key, and replace `your-gnews-api-key` in `utils.py` with your key.
7. **Run the API**:
- If port 8000 is in use, try `--port 8001` or select the port in the Streamlit app sidebar.
8. **Run the Streamlit App**:
- Open `http://localhost:8501` in your browser.

## Features
- Fetches news articles for a given company using the GNews API.
- Summarizes articles (first sentence or truncated to 100 characters).
- Performs sentiment analysis using `vaderSentiment` (with intensity labels like "Very Positive") and `TextBlob` as a fallback.
- Extracts topics using `yake`.
- Generates TTS summaries in English and Hindi using `gTTS`.
- "Read Aloud" feature to play article summaries and final sentiment.
- "Read Screen" feature to play all visible text on the screen in the selected language.
- Dark-themed interface with eye-comfortable colors.
- Language switch between English and Hindi.
- Configurable API port to avoid conflicts.

## Models Used
- **Summarization**: Manual method (first sentence or truncate to 100 characters).
- **Sentiment Analysis**: `vaderSentiment` for accurate polarity scoring, with `TextBlob` as a fallback.
- **Topic Extraction**: `yake` for keyword extraction.
- **Text-to-Speech**: `gTTS` for generating English/Hindi audio.
- **News Source**: GNews API (https://gnews.io).

## API Development
- **Endpoint**: `/analyze`
- **Method**: POST
- **Input**: `{"company": "Tesla", "language": "en"}` or `{"company": "Tesla", "language": "hi"}`
- **Output**: JSON with article data, sentiment analysis, comparative analysis, and audio file path.
- **Test with Postman or `curl`**:

## Assumptions & Limitations
- **Assumptions**:
- Users provide valid company names recognizable by GNews.
- A valid GNews API key is provided.
- **Limitations**:
- GNews free tier limits to 100 requests/day.
- Sentiment analysis may miss sarcasm or nuanced language.
- Hindi TTS quality depends on `gTTS` and may lack natural intonation.
- Summarization is basic (first sentence or truncation).

## Deployment
- Deploy on Hugging Face Spaces: [Insert Link]
- Ensure `requirements.txt` is included, and `app.py` is the entry point.

## Dependencies
- `requests`, `beautifulsoup4`, `nltk`, `textblob`, `gtts`, `streamlit`, `fastapi`, `uvicorn`, `rake-nltk`, `vaderSentiment`, `yake`

## Usage
- Enter a company name (e.g., "Tesla") in the input field.
- Select a language (English or Hindi) from the sidebar.
- Click "Analyze" to fetch and display articles.
- Use "Read Aloud" to hear article summaries and final sentiment.
- Use "Read Screen" to hear all visible text on the screen in the selected languages.
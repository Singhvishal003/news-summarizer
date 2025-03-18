import streamlit as st # type: ignore
import requests # type: ignore
import os
from gtts import gTTS # type: ignore

# Define generate_tts at the top to avoid NameError
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

# Set page configuration with dark theme
st.set_page_config(page_title="News Summarizer", layout="wide", initial_sidebar_state="expanded")
st.markdown(
    """
    <style>
    .reportview-container {
        background: #000000;
        color: #E0E0E0;
    }
    .sidebar .sidebar-content {
        background: #1A1A1A;
        color: #E0E0E0;
    }
    .widget-label {
        color: #B0B0B0;
    }
    .stButton>button {
        background-color: #4A90E2;
        color: white;
        border-radius: 5px;
    }
    .stButton>button:hover {
        background-color: #357ABD;
    }
    .stAudio {
        background-color: #2A2A2A;
        border-radius: 5px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("News Summarizer & Text-to-Speech App")
st.markdown("---")

# Sidebar for language selection and port configuration
with st.sidebar:
    st.header("Settings")
    language = st.radio("Select Language", ["English", "Hindi"], index=0)
    api_port = st.selectbox("API Port", [8000, 8001], index=0)  # Fallback port option

# User input
company_name = st.text_input("Enter Company Name (e.g., Tesla):", key="company_input")

# Placeholder to store the screen text for the "Read Screen" feature
if 'screen_text' not in st.session_state:
    st.session_state.screen_text = []

# Placeholder to store the result for reuse
if 'result' not in st.session_state:
    st.session_state.result = None

if st.button("Analyze"):
    if company_name:
        with st.spinner("Fetching and analyzing news..."):
            try:
                # Ensure the payload is correctly structured
                payload = {"company": company_name.strip(), "language": language.lower()}
                st.write(f"Sending payload: {payload}")  # Debug log
                api_url = f"http://localhost:{api_port}/analyze"
                st.write(f"Connecting to API at: {api_url}")  # Debug log
                response = requests.post(
                    api_url,
                    json=payload,
                    timeout=30
                )
                response.raise_for_status()
                st.session_state.result = response.json()
                
                # Clear previous screen text
                st.session_state.screen_text = []

                if "error" in st.session_state.result:
                    st.error(st.session_state.result["error"])
                    st.session_state.screen_text.append(st.session_state.result["error"])
                else:
                    # Display analysis and collect screen text
                    st.subheader(f"Analysis for {st.session_state.result['Company']}", help="Click 'Read Aloud' to hear the summaries or 'Read Screen' to hear all text")
                    st.session_state.screen_text.append(f"Analysis for {st.session_state.result['Company']}")

                    for i, article in enumerate(st.session_state.result['Articles']):
                        with st.expander(f"Article {i+1}: {article['Title']}"):
                            st.write(f"**Summary**: {article['Summary']}")
                            # Handle Sentiment as dictionary or fallback to string
                            sentiment_label = article['Sentiment'].get('label') if isinstance(article['Sentiment'], dict) else article['Sentiment']
                            st.write(f"**Sentiment**: {sentiment_label}")
                            if isinstance(article['Sentiment'], dict):
                                st.write(f"**Sentiment Scores (VADER)**: Positive: {article['Sentiment']['vader_scores']['positive']:.2f}, Negative: {article['Sentiment']['vader_scores']['negative']:.2f}, Neutral: {article['Sentiment']['vader_scores']['neutral']:.2f}, Compound: {article['Sentiment']['vader_scores']['compound']:.2f}")
                                st.write(f"**Sentiment Polarity (TextBlob)**: {article['Sentiment']['textblob_polarity']:.2f}")
                            st.write(f"**Topics**: {', '.join(article['Topics'])}")
                            st.write(f"**Link**: [Read More]({article['Link']})")
                            # Collect text for "Read Screen"
                            st.session_state.screen_text.append(f"Article {i+1}: {article['Title']}")
                            st.session_state.screen_text.append(f"Summary: {article['Summary']}")
                            st.session_state.screen_text.append(f"Sentiment: {sentiment_label}")
                            if isinstance(article['Sentiment'], dict):
                                st.session_state.screen_text.append(f"Sentiment Scores from VADER: Positive: {article['Sentiment']['vader_scores']['positive']:.2f}, Negative: {article['Sentiment']['vader_scores']['negative']:.2f}, Neutral: {article['Sentiment']['vader_scores']['neutral']:.2f}, Compound: {article['Sentiment']['vader_scores']['compound']:.2f}")
                                st.session_state.screen_text.append(f"Sentiment Polarity from TextBlob: {article['Sentiment']['textblob_polarity']:.2f}")
                            st.session_state.screen_text.append(f"Topics: {', '.join(article['Topics'])}")
                            st.session_state.screen_text.append(f"Link: {article['Link']}")
                    
                    st.subheader("Comparative Analysis")
                    st.json(st.session_state.result["Comparative Sentiment Score"])
                    st.session_state.screen_text.append("Comparative Analysis")
                    st.session_state.screen_text.append(str(st.session_state.result["Comparative Sentiment Score"]))

                    st.write(f"**Final Sentiment**: {st.session_state.result['Final Sentiment Analysis']}")
                    st.session_state.screen_text.append(f"Final Sentiment: {st.session_state.result['Final Sentiment Analysis']}")

                    # Display audio from API (summary of final sentiment)
                    if st.session_state.result["Audio"]:
                        st.audio(st.session_state.result["Audio"], format="audio/mp3")
                    else:
                        st.warning("Audio generation failed for final sentiment.")
            except requests.RequestException as e:
                st.error(f"Error connecting to the API: {e}")
                st.session_state.screen_text.append(f"Error connecting to the API: {e}")
    else:
        st.warning("Please enter a company name.")
        st.session_state.screen_text.append("Please enter a company name.")

# Display "Read Aloud" and "Read Screen" buttons if analysis has been performed
if st.session_state.result or st.session_state.screen_text:
    if st.session_state.result and "error" not in st.session_state.result:
        # "Read Aloud" for summaries and final sentiment
        if st.button("Read Aloud", key=f"read_aloud_{company_name}"):
            with st.spinner("Generating audio for summaries..."):
                full_text = "\n".join([f"Article {i+1}: {a['Summary']}" for i, a in enumerate(st.session_state.result["Articles"])]) + f"\nFinal Sentiment: {st.session_state.result['Final Sentiment Analysis']}"
                audio_file = generate_tts(full_text, language.lower(), "summary_output.mp3")
                if audio_file:
                    st.audio(audio_file, format="audio/mp3")
                    os.remove(audio_file)  # Clean up temporary file
                else:
                    st.warning("Audio generation failed for summaries.")

    # "Read Screen" for all visible text
    if st.button("Read Screen", key=f"read_screen_{company_name}"):
        if st.session_state.screen_text:
            with st.spinner("Generating audio for screen text..."):
                screen_text = "\n".join(st.session_state.screen_text)
                audio_file = generate_tts(screen_text, language.lower(), "screen_output.mp3")
                if audio_file:
                    st.audio(audio_file, format="audio/mp3")
                    os.remove(audio_file)  # Clean up temporary file
                else:
                    st.warning("Audio generation failed for screen text.")
        else:
            st.warning("No screen text available to read.")
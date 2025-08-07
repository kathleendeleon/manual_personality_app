import streamlit as st
import requests
from bs4 import BeautifulSoup
import re

# Placeholder MBTI classifier based on word matching
def classify_mbti(text):
    traits = {
        "I": 0, "E": 0,
        "S": 0, "N": 0,
        "T": 0, "F": 0,
        "J": 0, "P": 0
    }

    keywords = {
        "I": ["introspective", "reserved", "reflective", "independent", "internal"],
        "E": ["outgoing", "energetic", "team", "sociable", "talkative"],
        "S": ["practical", "realistic", "detail", "concrete", "facts"],
        "N": ["visionary", "imaginative", "theoretical", "conceptual", "future"],
        "T": ["logical", "analytical", "strategy", "data", "objective"],
        "F": ["empathetic", "caring", "values", "feelings", "emotion"],
        "J": ["organized", "structured", "plan", "schedule", "decisive"],
        "P": ["flexible", "spontaneous", "adaptive", "explore", "open-ended"]
    }

    text = text.lower()
    for letter, words in keywords.items():
        for word in words:
            if word in text:
                traits[letter] += 1

    mbti = ""
    mbti += "I" if traits["I"] >= traits["E"] else "E"
    mbti += "S" if traits["S"] >= traits["N"] else "N"
    mbti += "T" if traits["T"] >= traits["F"] else "F"
    mbti += "J" if traits["J"] >= traits["P"] else "P"
    return mbti

# Streamlit UI
st.set_page_config(page_title="MBTI Analyzer from LinkedIn", page_icon="🧠")
st.title("🔗 MBTI Personality Analyzer from LinkedIn")

st.markdown("""
Paste a public LinkedIn profile URL below, and we'll try to infer the person's MBTI type based on visible text
(like their summary, headline, or experience).
""")

linkedin_url = st.text_input("🔗 LinkedIn Profile URL")

if st.button("Analyze"):
    if not linkedin_url.startswith("https://www.linkedin.com/in/"):
        st.error("Please enter a valid public LinkedIn profile URL (must start with https://www.linkedin.com/in/).")
    else:
        try:
            headers = {
                "User-Agent": "Mozilla/5.0"
            }
            response = requests.get(linkedin_url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")
            text = soup.get_text(separator=" ")
            clean_text = re.sub(r'\s+', ' ', text)
            st.subheader("🧠 Inferred MBTI Type:")
            st.success(classify_mbti(clean_text))
        except Exception as e:
            st.error(f"Failed to fetch or analyze the profile. Error: {e}")
else:
    st.info("Enter a valid LinkedIn profile URL to begin.")




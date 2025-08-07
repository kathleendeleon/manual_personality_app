import streamlit as st
import spacy
from collections import Counter

# Load spaCy English model
try:
    nlp = spacy.load('en_core_web_sm')
except OSError:
    st.error("Please run: python -m spacy download en_core_web_sm")
    st.stop()

# Rule-based personality scoring
def analyze_traits(doc):
    trait_keywords = {
        "openness": ["imagine", "creative", "explore", "theory", "fantasy", "curious"],
        "conscientiousness": ["organized", "schedule", "goal", "punctual", "focused"],
        "extraversion": ["social", "party", "talk", "friends", "energy", "outgoing"],
        "agreeableness": ["kind", "help", "empathy", "forgive", "caring", "cooperate"],
        "neuroticism": ["worried", "anxious", "stressed", "upset", "moody", "sensitive"]
    }

    counts = Counter({trait: 0 for trait in trait_keywords})
    for token in doc:
        for trait, keywords in trait_keywords.items():
            if token.lemma_.lower() in keywords:
                counts[trait] += 1
    return counts

# UI
st.set_page_config(page_title="NLP Personality Analyzer", page_icon="🧠")
st.title("🧠 NLP-Based Personality Analyzer")
st.markdown("Enter a writing sample below. This app uses spaCy's NLP model and a keyword scoring system to estimate your personality profile.")

user_text = st.text_area("✍️ Paste your writing sample here:", height=250)

if st.button("🔍 Analyze"):
    if not user_text.strip():
        st.warning("Please enter some text to analyze.")
    else:
        doc = nlp(user_text)
        results = analyze_traits(doc)
        st.subheader("📋 Personality Analysis")
        for trait, score in results.items():
            st.write(f"**{trait.title()}**: {'High' if score > 0 else 'Low'} ({score} match{'es' if score != 1 else ''})")
else:
    st.info("Paste a text sample and click 'Analyze' to begin.")

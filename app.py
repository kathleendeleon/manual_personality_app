import streamlit as st

# Rule-based tone and personality classifier
def analyze_text(text):
    traits = {
        "openness": 0,
        "conscientiousness": 0,
        "extraversion": 0,
        "agreeableness": 0,
        "neuroticism": 0,
    }

    # Naive keyword rules
    if any(word in text.lower() for word in ["imagine", "creative", "fantasy", "explore"]):
        traits["openness"] += 1
    if any(word in text.lower() for word in ["organized", "plan", "schedule", "detail"]):
        traits["conscientiousness"] += 1
    if any(word in text.lower() for word in ["party", "talk", "friends", "social"]):
        traits["extraversion"] += 1
    if any(word in text.lower() for word in ["help", "kind", "care", "empathy"]):
        traits["agreeableness"] += 1
    if any(word in text.lower() for word in ["anxious", "worried", "tense", "stressed"]):
        traits["neuroticism"] += 1

    return traits

# Streamlit UI
st.set_page_config(page_title="Offline Personality Analyzer", page_icon="🧠")
st.title("🧠 Offline Personality Analyzer")
st.markdown("""
Enter a short writing sample below (e.g., journal entry, email, or personal reflection), and we'll give you a basic personality breakdown based on keyword cues.
""")

user_input = st.text_area("✍️ Paste your writing sample here:", height=250)

if st.button("🔍 Analyze"):
    if not user_input.strip():
        st.warning("Please enter some text to analyze.")
    else:
        traits = analyze_text(user_input)
        st.subheader("📋 Personality Analysis")
        for trait, score in traits.items():
            st.write(f"**{trait.title()}**: {'High' if score > 0 else 'Low'}")
else:
    st.info("Paste a text sample and click 'Analyze' to begin.")

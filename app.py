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
        "I": [
            "introspective", "reserved", "reflective", "independent", "internal",
            "focused", "thoughtful", "private", "self-aware", "inward-looking",
            "autonomous", "quiet", "observer", "self-contained", "works independently",
            "concentrated", "needs space", "low profile", "solo", "minimalist"
        ],
        "E": [
            "outgoing", "energetic", "team player", "sociable", "talkative",
            "networker", "presenter", "collaborative", "leadership", "extroverted",
            "enthusiastic", "dynamic", "connector", "client-facing", "group-oriented",
            "influencer", "likes people", "public speaker", "driven by connection", "enthusiasm"
        ],
        "S": [
            "practical", "realistic", "detail-oriented", "concrete", "facts",
            "hands-on", "executor", "accurate", "methodical", "step-by-step",
            "process-driven", "routine", "planner", "results-oriented", "implementation",
            "traditional", "measurable", "observable", "reporting", "logistics"
        ],
        "N": [
            "visionary", "imaginative", "theoretical", "conceptual", "future-focused",
            "abstract thinker", "strategic", "pattern recognition", "innovative", "idea generator",
            "ideation", "growth mindset", "change-driven", "possibility", "intuitive",
            "dreamer", "nonlinear", "long-term vision", "blue sky thinker", "outside the box"
        ],
        "T": [
            "logical", "analytical", "strategy", "data-driven", "objective",
            "critical thinker", "problem-solving", "metrics", "rational", "evidence-based",
            "direct", "frameworks", "detached", "diagnostic", "evaluation",
            "process optimization", "reasoning", "efficiency", "competitive", "outcome-focused"
        ],
        "F": [
            "empathetic", "caring", "values-driven", "feelings", "emotionally aware",
            "nurturing", "supportive", "people-centered", "intuitive", "compassionate",
            "ethical", "relationship-focused", "harmonious", "sensitive", "inclusive",
            "culture-building", "trusted", "helps others", "loyal", "heart-led"
        ],
        "J": [
            "organized", "structured", "plans", "schedules", "decisive",
            "time management", "goal-setting", "predictable", "prioritized", "methodical",
            "disciplined", "closure-seeking", "follow-through", "roadmap", "task management",
            "systematic", "execution-focused", "checklists", "calendar-driven", "decision-making"
        ],
        "P": [
            "flexible", "spontaneous", "adaptive", "exploratory", "open-ended",
            "curious", "multitasking", "agile", "thrives in ambiguity", "experimental",
            "fluid", "unstructured", "discovery-driven", "nonlinear", "reactive",
            "improvisational", "freestyle", "serendipitous", "emergent", "comfortable with change"
        ]
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


# MBTI type summaries
mbti_summaries = {
    "INTJ": "The Mastermind: Strategic, independent, and visionary. INTJs are driven by logic and a desire to improve systems and ideas. They are future-oriented, analytical, and excellent at long-term planning.",
    "INTP": "The Thinker: Curious, inventive, and intellectually driven. INTPs love exploring ideas, solving abstract problems, and theorizing about how things work. They value autonomy and innovation.",
    "ENTJ": "The Commander: Bold, decisive, and natural leaders. ENTJs are focused on efficiency, organization, and achieving big goals. They excel at setting direction and motivating teams.",
    "ENTP": "The Visionary: Energetic, adaptable, and full of ideas. ENTPs thrive in fast-paced environments where they can debate, innovate, and explore new possibilities with enthusiasm.",
    "INFJ": "The Advocate: Insightful, empathetic, and quietly intense. INFJs are driven by a deep sense of purpose and value helping others through meaningful connections and long-term vision.",
    "INFP": "The Idealist: Gentle, imaginative, and values-driven. INFPs seek authenticity, creativity, and harmony. They care deeply about their principles and are passionate about causes they believe in.",
    "ENFJ": "The Protagonist: Charismatic, warm, and altruistic. ENFJs are natural leaders who inspire others with their emotional intelligence and desire to create a better world.",
    "ENFP": "The Campaigner: Enthusiastic, creative, and spontaneous. ENFPs love exploring new ideas and forming deep relationships. They bring warmth and inspiration to the people around them.",
    "ISTJ": "The Inspector: Responsible, reliable, and detail-oriented. ISTJs are grounded and methodical, with a strong sense of duty. They value structure and thrive on consistency.",
    "ISFJ": "The Defender: Loyal, thoughtful, and practical. ISFJs are deeply caring and committed to helping others. They prefer behind-the-scenes work and excel at nurturing relationships.",
    "ESTJ": "The Executive: Organized, assertive, and results-focused. ESTJs are born leaders who value tradition, logic, and order. They’re excellent at managing people and systems.",
    "ESFJ": "The Consul: Social, supportive, and dependable. ESFJs are highly tuned into the needs of others and enjoy creating harmony. They excel in collaborative, people-oriented environments.",
    "ISTP": "The Virtuoso: Practical, analytical, and action-oriented. ISTPs love to explore how things work and enjoy solving hands-on problems. They are independent and adaptable.",
    "ISFP": "The Adventurer: Artistic, free-spirited, and sensitive. ISFPs value personal freedom and self-expression. They are quiet creators who seek beauty and authenticity in everything they do.",
    "ESTP": "The Dynamo: Energetic, bold, and hands-on. ESTPs are quick-thinking problem solvers who thrive in the moment. They love excitement, challenge, and high-stakes environments.",
    "ESFP": "The Entertainer: Playful, outgoing, and fun-loving. ESFPs are natural performers who live in the present and enjoy bringing joy to others. They excel at engaging and energizing social situations."
}

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
            
            mbti_type = classify_mbti(clean_text)
            st.success(mbti_type)
            st.subheader("🔍 Personality Summary:")
            st.markdown(mbti_summaries.get(mbti_type, "No summary available."))

        except Exception as e:
            st.error(f"Failed to fetch or analyze the profile. Error: {e}")
else:
    st.info("Enter a valid LinkedIn profile URL to begin.")

import streamlit as st
import pandas as pd
import streamlit_antd_components as sac
from openai import OpenAI
from fpdf import FPDF
from pypdf import PdfReader

# ---------------------------------
# CONFIG
# ---------------------------------
st.set_page_config(page_title="AI Study Abroad Counselor", layout="wide")

# ---------------------------------
# PREMIUM CSS
# ---------------------------------
st.markdown("""
<style>
.center-box {text-align:center; padding:20px;}
.card-box {
    background:white; padding:20px;
    border-radius:18px;
    box-shadow:0px 6px 25px rgba(0,0,0,0.08);
    margin-bottom:15px;
}
.user-msg {
    background:#d1e7ff;
    padding:12px;
    border-radius:14px;
    margin:6px;
    text-align:right;
}
.ai-msg {
    background:#f2f3f5;
    padding:12px;
    border-radius:14px;
    margin:6px;
    text-align:left;
}
.chat-input-box {
    position: fixed;
    bottom: 20px;
    width: 75%;
    background: white;
    padding: 10px;
    border-radius: 14px;
    box-shadow: 0px 4px 18px rgba(0,0,0,0.15);
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------
# OPENROUTER API
# ---------------------------------
OPENROUTER_API_KEY = "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"

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY
)

def get_ai_response(prompt):
    completion = client.chat.completions.create(
        model="mistralai/mistral-7b-instruct",
        messages=[
            {"role": "system",
             "content": "You are a friendly AI chatbot. Reply like ChatGPT, not emails."},
            {"role": "user", "content": prompt}
        ]
    )
    return completion.choices[0].message.content

# ---------------------------------
# PDF CLEANING
# ---------------------------------
def clean_text(txt):
    return txt.replace("**", "").replace("##", "").encode("latin-1", "ignore").decode("latin-1")

# ---------------------------------
# LOAD UNIVERSITIES
# ---------------------------------
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@st.cache_data
def load_universities():
    file_path = os.path.join(BASE_DIR, "universities2.csv")
    return pd.read_csv(file_path)

uni_df = load_universities()

# ---------------------------------
# SESSION INIT
# ---------------------------------
if "profile" not in st.session_state:
    st.session_state.profile = {}

if "shortlisted" not in st.session_state:
    st.session_state.shortlisted = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "sop_feedback" not in st.session_state:
    st.session_state.sop_feedback = ""

# ---------------------------------
# MATCH SCORE FUNCTION
# ---------------------------------
def calculate_match_score(cgpa, budget_value, uni):
    score = 0
    score += 40 if cgpa >= 9 else 30 if cgpa >= 8 else 20 if cgpa >= 7 else 10
    score += 30 if uni["tuition"] <= budget_value else 15
    scholarship_map = {"Very High": 30, "High": 25, "Medium": 15, "Low": 5}
    score += scholarship_map.get(uni["scholarship"], 10)
    return min(score, 100)

# ---------------------------------
# HEADER
# ---------------------------------
st.markdown("""
<div class="card-box center-box">
<h1>🎓 AI Study Abroad Counselor</h1>
<p>Your premium AI platform for matching, SOP review, and chatbot support.</p>
</div>
""", unsafe_allow_html=True)

# ---------------------------------
# SIDEBAR MENU
# ---------------------------------
with st.sidebar:
    menu = sac.menu([
        sac.MenuItem("Home", icon="house-fill"),
        sac.MenuItem("Onboarding", icon="person-fill"),
        sac.MenuItem("University Explorer", icon="bank"),
        sac.MenuItem("SOP Review", icon="file-earmark-text"),
        sac.MenuItem("AI Chatbot", icon="robot"),
        sac.MenuItem("Export Report", icon="download")
    ], open_all=True)

# ---------------------------------
# HOME PAGE FIXED ✅
# ---------------------------------
if menu == "Home":
    st.markdown("""
    <div class="card-box">
    <h2>🚀 Welcome</h2>
    ✅ AI-based University Recommendation<br>
    ✅ Shortlist + Compare Universities<br>
    ✅ Voice + Text Chat Counseling<br>
    ✅ SOP + Resume AI Review<br>
    ✅ Download Final Report
    </div>
    """, unsafe_allow_html=True)

# ---------------------------------
# ONBOARDING UPDATED ✅
# ---------------------------------
elif menu == "Onboarding":

    st.markdown("## 📝 Student Profile Setup")

    with st.form("profile_form"):
        name = st.text_input("Full Name")
        cgpa = st.number_input("CGPA", 0.0, 10.0, step=0.1)

        country = st.selectbox("Target Country", sorted(uni_df["country"].unique()))

        budget = st.selectbox(
            "Annual Budget",
            ["< $15k", "$15k-25k", "$25k-40k", "$40k-60k", "$60k-80k", "$80k+"]
        )

        course = st.text_input("Intended Course (Eg: MBA, MS CS, AI, Data Science)")

        if st.form_submit_button("Save Profile"):
            st.session_state.profile = {
                "name": name,
                "cgpa": cgpa,
                "country": country,
                "budget": budget,
                "course": course
            }
            st.success("✅ Saved!")

# ---------------------------------
# UNIVERSITY EXPLORER (FINAL VERSION ✅)
# ---------------------------------
elif menu == "University Explorer":

    st.markdown("## 🏫 Top University Matches")

    if not st.session_state.profile:
        st.warning("Complete onboarding first.")

    else:
        profile = st.session_state.profile

        # ✅ Budget Map
        budget_map = {
            "< $15k": 15000,
            "$15k-25k": 25000,
            "$25k-40k": 40000,
            "$40k-60k": 60000,
            "$60k-80k": 80000,
            "$80k+": 120000
        }

        # ✅ Step 1: Filter by Country
        filtered = uni_df[uni_df["country"] == profile["country"]]

        # ✅ Step 2: Intended Course Filter (AI Mandatory)
        intended_course = profile["course"].lower().strip()

        # ✅ Smart Keyword Expansion
        course_map = {
            "ai": ["ai", "artificial intelligence", "machine learning"],
            "ml": ["machine learning", "ai"],
            "cs": ["computer science", "software engineering"],
            "data science": ["data science", "business analytics"],
            "mba": ["mba", "business analytics", "finance"]
        }

        # ✅ Determine keywords
        if intended_course in course_map:
            keywords = course_map[intended_course]
        else:
            keywords = [intended_course]

        # ✅ Apply filtering if course entered
        if intended_course != "":
            filtered = filtered[
                filtered["programs"].str.lower().apply(
                    lambda x: any(k in x for k in keywords)
                )
            ]

        # ✅ If nothing matched → fallback
        if filtered.empty:
            st.warning(
                "⚠️ No universities found for this course in selected country.\n"
                "Showing top-ranked universities instead."
            )
            filtered = uni_df[uni_df["country"] == profile["country"]]

        # ✅ Step 3: Sort by Ranking
        filtered = filtered.sort_values(by="ranking", ascending=True)

        # ✅ Step 4: Take Top 10
        filtered = filtered.head(10)

        st.markdown(
            f"### 🎯 Showing Top 10 Universities for **{profile['course']}**"
        )

        # ✅ Step 5: Display Universities
        for _, uni in filtered.iterrows():

            # ✅ Match Score Calculation
            score = calculate_match_score(
                profile["cgpa"],
                budget_map[profile["budget"]],
                {"tuition": uni["tuition"], "scholarship": uni["scholarship"]}
            )

            st.markdown("<div class='card-box'>", unsafe_allow_html=True)

            # ✅ University Name
            st.subheader(uni["name"])

            # ✅ Match Score
            st.progress(score / 100)
            st.write(f"🎯 Match Score: **{score}%**")

            # ✅ New Fields
            st.write(f"🏙️ City: **{uni['city']}**")
            st.write(f"🌍 Global Ranking: **#{uni['ranking']}**")
            st.write(f"📚 Programs Offered: {uni['programs']}")

            # ✅ Tuition + Scholarship
            st.write(f"💰 Tuition Fee: **${uni['tuition']} / year**")
            st.write(f"🎓 Scholarship Chance: **{uni['scholarship']}**")

            # ✅ Website Link
            st.markdown(
                f"🌐 Official Website: [{uni['website']}]({uni['website']})"
            )

            # ✅ Shortlist Button
            if st.button("⭐ Shortlist", key=uni["name"]):
                if uni["name"] not in st.session_state.shortlisted:
                    st.session_state.shortlisted.append(uni["name"])
                    st.success(f"✅ {uni['name']} Shortlisted!")

            st.markdown("</div>", unsafe_allow_html=True)

        # ✅ Shortlisted Universities Display
        st.markdown("### ✅ Shortlisted Universities")
        if st.session_state.shortlisted:
            st.json(st.session_state.shortlisted)
        else:
            st.info("No universities shortlisted yet.")


# ---------------------------------
# SOP REVIEW FIXED ✅
# ---------------------------------
elif menu == "SOP Review":

    st.markdown("## 📄 SOP / Resume Feedback")

    uploaded = st.file_uploader("Upload PDF/TXT", type=["pdf", "txt"])

    if uploaded:
        text = ""

        if uploaded.type == "application/pdf":
            reader = PdfReader(uploaded)
            for page in reader.pages:
                text += page.extract_text()
        else:
            text = uploaded.read().decode()

        if st.button("Get AI Feedback"):

            prompt = f"""
You are an expert SOP/Resume reviewer.

Give feedback ONLY in this format:

1. Key Strengths
2. Weaknesses / Missing Areas
3. Improvements
4. Rewrite Suggestions

Do NOT repeat the resume text.

DOCUMENT:
{text}
"""

            feedback = get_ai_response(prompt)
            st.session_state.sop_feedback = feedback

            st.success("✅ Feedback Generated!")
            st.write(feedback)


# ---------------------------------
# AI CHATBOT (TEXT ONLY ✅ Stable Deployment Version)
# ---------------------------------
elif menu == "AI Chatbot":

    st.markdown("## 🤖 AI Chatbot")

    # ✅ Greeting Message
    st.markdown(
        "<p style='font-size:18px; color:gray;'>Hi 👋 How can I help you today?</p>",
        unsafe_allow_html=True
    )

    st.divider()

    # ✅ Display Chat History
    for role, msg in st.session_state.chat_history:

        if role == "User":
            st.markdown(
                f"<div class='user-msg'>{msg}</div>",
                unsafe_allow_html=True
            )

        else:
            st.markdown(
                f"<div class='ai-msg'>{msg}</div>",
                unsafe_allow_html=True
            )

    st.divider()

    # ✅ Text Input Only (Works Like ChatGPT)
    user_text = st.chat_input("Message...")

    if user_text:

        prompt = f"""
Student Profile:
{st.session_state.profile}

Shortlisted Universities:
{st.session_state.shortlisted}

User Question:
{user_text}

Reply conversationally like ChatGPT in bullet points.
"""

        response = get_ai_response(prompt)

        # ✅ Save Chat History
        st.session_state.chat_history.append(("User", user_text))
        st.session_state.chat_history.append(("AI", response))

        # ✅ Refresh Chat
        st.rerun()


# ---------------------------------
# EXPORT REPORT (FINAL CLEAN ✅)
# ---------------------------------
elif menu == "Export Report":

    if st.button("Generate Final Report PDF"):

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.cell(200, 10, clean_text("AI Study Abroad Counseling Report"), ln=True, align="C")
        pdf.ln(10)

        # Profile
        pdf.set_font("Arial", style="B", size=12)
        pdf.cell(200, 10, "1. Student Profile", ln=True)
        pdf.set_font("Arial", size=11)

        for k, v in st.session_state.profile.items():
            pdf.cell(200, 8, clean_text(f"{k}: {v}"), ln=True)

        pdf.ln(8)

        # SOP Feedback
        pdf.set_font("Arial", style="B", size=12)
        pdf.cell(200, 10, "2. SOP / Resume Feedback", ln=True)
        pdf.set_font("Arial", size=11)

        pdf.multi_cell(0, 8, clean_text(st.session_state.sop_feedback))

        pdf.ln(8)

        # Chat Section
        pdf.set_font("Arial", style="B", size=12)
        pdf.cell(200, 10, "3. Chatbot Conversation", ln=True)
        pdf.set_font("Arial", size=11)

        for role, msg in st.session_state.chat_history:
            pdf.multi_cell(0, 8, clean_text(f"{role}: {msg}"))
            pdf.cell(200, 5, "--------------------------", ln=True)

        pdf.output("final_report.pdf")

        with open("final_report.pdf", "rb") as f:
            st.download_button("📄 Download Report", f, file_name="final_report.pdf")

        st.success("✅ Final Report Generated Successfully!")







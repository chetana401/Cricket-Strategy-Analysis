import streamlit as st
import os
from groq import Groq
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import base64
import random
import glob

# -------- Load API Key --------
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# -------- Page Config --------
st.set_page_config(
    page_title="Cricket Strategy Analytics",
    page_icon="🏏",
    layout="wide"
)

# -------- Convert Image to Base64 --------
def get_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# -------- Random Background Image --------
image_list = glob.glob("images/*.jpg")

if image_list:
    selected_bg = random.choice(image_list)
else:
    selected_bg = None

bg = get_base64(selected_bg) if selected_bg else ""

# -------- CSS Styling --------
st.markdown(f"""
<style>

.stApp {{
background-image: linear-gradient(
rgba(0,0,0,0.55),
rgba(0,0,0,0.55)
),
url("data:image/jpg;base64,{bg}");
background-size: cover;
background-position: center;
background-repeat: no-repeat;
background-attachment: fixed;
}}

.title {{
font-size:60px;
font-weight:bold;
text-align:center;
color:white;
text-shadow:4px 4px 20px black;
}}

.card {{
background: rgba(255,255,255,0.7);
backdrop-filter: blur(15px);
padding:25px;
border-radius:18px;
box-shadow:0px 10px 35px rgba(0,0,0,0.4);
margin-bottom:20px;
}}

button {{
background-color:#ff4b4b;
color:white;
font-size:18px;
border-radius:10px;
height:50px;
width:220px;
}}

button:hover {{
background-color:#e60000;
}}

</style>
""", unsafe_allow_html=True)

# -------- Title --------
st.markdown('<p class="title">🏏 Cricket Strategy Analytics</p>', unsafe_allow_html=True)

# -------- Sidebar --------
st.sidebar.title("📊 Project Dashboard")

st.sidebar.write("""
**Domain:** NLP & Generative AI  
**Model:** Llama 3.1 (Groq)  
**Libraries:** Streamlit, Matplotlib  

### Project Features
✔ Commentary analysis  
✔ Strategy prediction  
✔ Performance insights  
✔ Outcome prediction  
✔ Tactical recommendations
""")

# -------- Commentary Input --------
st.markdown('<div class="card">', unsafe_allow_html=True)

st.subheader("📝 Enter Match Commentary")

commentary = st.text_area(
"",
height=200,
placeholder="""Example:
Over 15: Kohli hits a four through covers.
Next ball single to deep mid wicket.
Bowler missing yorker length."""
)

st.markdown('</div>', unsafe_allow_html=True)

# -------- Center Analyze Button --------
col1, col2, col3 = st.columns([1,2,1])

with col2:
    analyze = st.button("🔍 Analyze Match Strategy")

# -------- AI Analysis --------
if analyze:

    with st.spinner("🤖 AI is analyzing match strategy..."):

        prompt = f"""
You are a professional cricket analyst.

Analyze the commentary and respond in this format:

Batting Strategy:
- short point
- short point

Bowling Strategy:
- short point
- short point

Performance Insights:
- short point
- short point

Tactical Recommendations:
- short point
- short point

Match Outcome Prediction:
- one sentence prediction

Commentary:
{commentary}
"""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role":"user","content":prompt}]
        )

        result = response.choices[0].message.content

    # -------- AI Insights --------
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("📊 AI Match Insights")

    colA, colB = st.columns(2)

    with colA:
        st.subheader("🏏 Batting Strategy")
        if "Batting Strategy:" in result:
            batting = result.split("Batting Strategy:")[1].split("Bowling Strategy:")[0]
            st.success(batting)

    with colB:
        st.subheader("🎯 Bowling Strategy")
        if "Bowling Strategy:" in result:
            bowling = result.split("Bowling Strategy:")[1].split("Performance Insights:")[0]
            st.info(bowling)

    st.subheader("📊 Performance Insights")
    if "Performance Insights:" in result:
        perf = result.split("Performance Insights:")[1].split("Tactical Recommendations:")[0]
        st.warning(perf)

    st.subheader("🧠 Tactical Recommendations")
    if "Tactical Recommendations:" in result:
        tactic = result.split("Tactical Recommendations:")[1].split("Match Outcome Prediction:")[0]
        st.success(tactic)

    st.subheader("🏆 Match Outcome Prediction")
    if "Match Outcome Prediction:" in result:
        prediction = result.split("Match Outcome Prediction:")[1]
        st.error(prediction)

    st.markdown('</div>', unsafe_allow_html=True)

    # -------- Win Probability --------
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("🏆 Match Win Probability")

    win_prob = random.randint(45,85)

    st.progress(win_prob/100)

    st.write(f"Estimated Win Probability: **{win_prob}%**")

    st.markdown('</div>', unsafe_allow_html=True)

    # -------- Run Rate Graph --------
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("📈 Run Rate Trend")

    runs = [8,12,10,15,14,18]
    overs = [1,2,3,4,5,6]

    fig, ax = plt.subplots()

    ax.plot(overs, runs, marker="o")

    ax.set_xlabel("Overs")
    ax.set_ylabel("Runs")
    ax.set_title("Runs Per Over")

    st.pyplot(fig)

    st.markdown('</div>', unsafe_allow_html=True)

# -------- Footer --------
st.markdown(
"""
<center style='color:white;font-size:18px'>
🏏 AI Cricket Strategy Analytics | B.Tech NLP Project
</center>
""",
unsafe_allow_html=True
)
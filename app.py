import streamlit as st
from openai import OpenAI
import random
import time

st.set_page_config(page_title="Get Your Best Deal", layout="wide")

# ---------- THEME STATE ----------
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

def toggle_theme():
    st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"

# ---------- SIDEBAR ----------
st.sidebar.image("https://img.icons8.com/fluency/96/shopping-cart.png", width=70)
st.sidebar.markdown("## 🔥 Get Your Best Deal")

if st.sidebar.button("🌗 Toggle Theme"):
    toggle_theme()

st.sidebar.divider()

# API Key
st.sidebar.markdown("### 🔐 API Setup")
api_key = st.sidebar.text_input("OpenAI API Key", type="password")
client = OpenAI(api_key=api_key) if api_key else None

if api_key:
    st.sidebar.success("🟢 AI Connected")
else:
    st.sidebar.warning("🟡 AI Not Connected")

st.sidebar.divider()

# Filters
st.sidebar.markdown("### 🎛 Controls")
price_range = st.sidebar.slider("💰 Price Range", 50000, 100000, (60000, 80000))
sort_option = st.sidebar.selectbox("🔄 Sort By", ["Best Deal", "Lowest Price"])

st.sidebar.divider()

# Insights
st.sidebar.markdown("### 📊 Insights")
st.sidebar.metric("💸 Avg Savings", "₹2,150")
st.sidebar.metric("🔥 Best Platform", "Flipkart")

st.sidebar.divider()
st.sidebar.caption("🤖 AI Powered Price Intelligence")

# ---------- THEME ----------
if st.session_state.theme == "dark":
    bg = "linear-gradient(135deg, #0f2027, #2c5364)"
    card = "rgba(255,255,255,0.08)"
    text = "white"
else:
    bg = "linear-gradient(135deg, #f5f7fa, #c3cfe2)"
    card = "rgba(0,0,0,0.05)"
    text = "black"

# ---------- STYLE ----------
st.markdown(f"""
<style>
body {{
    background: {bg};
}}

.header {{
    text-align:center;
    font-size:48px;
    font-weight:bold;
    color:{text};
}}

.sub {{
    text-align:center;
    color:gray;
    margin-bottom:25px;
}}

.card {{
    background: {card};
    border-radius:18px;
    padding:20px;
    text-align:center;
    backdrop-filter: blur(10px);
    transition: 0.3s;
}}

.card:hover {{
    transform: translateY(-6px);
}}

.price {{
    font-size:30px;
    color:#00c853;
    font-weight:bold;
}}

.badge {{
    background:#00c853;
    padding:5px 12px;
    border-radius:10px;
    font-size:12px;
}}

.save {{
    color:#ffeb3b;
}}

.button {{
    background:#00c853;
    color:white;
    padding:8px 18px;
    border:none;
    border-radius:8px;
}}

.ai-box {{
    background: {card};
    padding:20px;
    border-radius:15px;
    margin-top:25px;
}}
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown('<div class="header">🔥 Get Your Best Deal</div>', unsafe_allow_html=True)
st.markdown('<div class="sub">Compare • Save • Decide Smarter with AI</div>', unsafe_allow_html=True)

product = st.text_input("🔍 Search product", placeholder="e.g. iPhone 15")

# Banner
if product:
    st.image(f"https://source.unsplash.com/1200x300/?{product}", use_container_width=True)

# ---------- DATA ----------
def get_data():
    base = 70000
    return [
        {"site": "Amazon", "price": base + random.randint(-2000, 2000)},
        {"site": "Flipkart", "price": base + random.randint(-2500, 1500)},
        {"site": "Croma", "price": base + random.randint(-1500, 2500)}
    ]

# ---------- MAIN ----------
if st.button("🚀 Find Best Deal"):

    with st.spinner("🔍 Scanning platforms and analyzing deals..."):
        time.sleep(1.5)

    data = [x for x in get_data() if price_range[0] <= x["price"] <= price_range[1]]

    if sort_option == "Lowest Price":
        data = sorted(data, key=lambda x: x["price"])

    best_price = min(x["price"] for x in data)

    st.markdown("## 💰 Price Comparison")

    cols = st.columns(len(data))

    for i, item in enumerate(data):
        savings = item["price"] - best_price

        badge = ""
        if item["price"] == best_price:
            badge = '<div class="badge">BEST DEAL</div>'

        with cols[i]:
            st.markdown(f"""
            <div class="card">
                <h3>{item['site']}</h3>
                {badge}
                <div class="price">₹{item['price']}</div>
                <div class="save">Save ₹{savings if savings > 0 else 0}</div>
                <br>
                <button class="button">🛒 Buy Now</button>
            </div>
            """, unsafe_allow_html=True)

    # ---------- AI ----------
    st.markdown("## 🧠 AI Recommendation")

    if client:
        with st.spinner("🤖 Generating smart insights..."):
            time.sleep(1)

        prompt = f"""
        Compare these deals:
        {data}

        Recommend the best option in a short and smart way.
        """

        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        st.markdown(f'<div class="ai-box">{res.choices[0].message.content}</div>', unsafe_allow_html=True)
    else:
        st.warning("Enter API key to enable AI insights")
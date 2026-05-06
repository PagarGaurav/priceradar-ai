import streamlit as st
from openai import OpenAI
import random
import pandas as pd
import matplotlib.pyplot as plt
import time

st.set_page_config(page_title="Get Your Best Deal", layout="wide")

# ---------- SIDEBAR ----------
st.sidebar.title("🔐 API Setup")
api_key = st.sidebar.text_input("Enter OpenAI API Key", type="password")

client = None
if api_key:
    client = OpenAI(api_key=api_key)
    st.sidebar.success("✅ Connected")
else:
    st.sidebar.warning("⚠️ Enter key for AI insights")

# ---------- UI STYLE ----------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #0f2027, #2c5364);
}

.header {
    text-align:center;
    font-size:48px;
    font-weight:bold;
    color:white;
}

.sub {
    text-align:center;
    color:#ccc;
    margin-bottom:25px;
}

.card {
    background: rgba(255,255,255,0.08);
    border-radius:18px;
    padding:20px;
    text-align:center;
    backdrop-filter: blur(10px);
    transition: 0.3s;
}

.card:hover {
    transform: translateY(-5px);
}

.price {
    font-size:30px;
    color:#00ffcc;
    font-weight:bold;
}

.badge {
    background:#00c853;
    padding:5px 12px;
    border-radius:10px;
    font-size:12px;
    display:inline-block;
    margin:5px;
}

.ai-box {
    background: rgba(255,255,255,0.12);
    padding:20px;
    border-radius:15px;
    margin-top:25px;
}
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown('<div class="header">🔥 Get Your Best Deal</div>', unsafe_allow_html=True)
st.markdown('<div class="sub">Smart comparison • Visual insights • AI recommendation</div>', unsafe_allow_html=True)

product = st.text_input("🔍 Search product", placeholder="e.g. iPhone 15")

# Stable product image
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

    # Loading animation (important for demo feel)
    with st.spinner("Analyzing prices across platforms..."):
        time.sleep(1.5)

    data = get_data()
    best_price = min(x["price"] for x in data)

    st.markdown("## 💰 Price Comparison")

    cols = st.columns(3)

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
                <p>Save ₹{savings if savings > 0 else 0}</p>
                <button>🛒 Buy Now</button>
            </div>
            """, unsafe_allow_html=True)

    # ---------- CHART ----------
    st.markdown("## 📊 Price Insights")

    df = pd.DataFrame(data)

    fig, ax = plt.subplots()
    ax.bar(df["site"], df["price"])
    ax.set_ylabel("Price (₹)")
    ax.set_title("Platform Comparison")

    st.pyplot(fig)

    # ---------- AI ----------
    st.markdown("## 🧠 AI Recommendation")

    if client:
        with st.spinner("Generating smart recommendation..."):
            time.sleep(1)

        prompt = f"""
        Compare these deals:
        {data}

        Recommend the best option in 2-3 lines.
        """

        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        st.markdown(f'<div class="ai-box">{res.choices[0].message.content}</div>', unsafe_allow_html=True)
    else:
        st.warning("Enter API key to enable AI insights")
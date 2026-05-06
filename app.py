import streamlit as st
from openai import OpenAI
import random

client = OpenAI()

st.set_page_config(page_title="AI Shopping Agent", layout="wide")

st.markdown("""
<style>
body {background: linear-gradient(135deg, #141E30, #243B55);}
.title {font-size:42px;font-weight:bold;text-align:center;color:white;}
.subtitle {text-align:center;color:#ccc;margin-bottom:30px;}
.card {background:rgba(255,255,255,0.08);padding:20px;border-radius:15px;
backdrop-filter:blur(14px);margin:10px;text-align:center;color:white;}
.price {font-size:28px;font-weight:bold;color:#00e5ff;}
.old-price {text-decoration:line-through;color:#aaa;font-size:14px;}
.badge {background:#00c853;padding:5px 10px;border-radius:10px;font-size:12px;}
.popular {background:#ff9800;}
.ai-box {background:rgba(255,255,255,0.12);padding:20px;border-radius:15px;margin-top:30px;}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">🛍 AI Shopping Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Compare prices, reviews & get smart recommendations</div>', unsafe_allow_html=True)

product = st.text_input("🔍 Search Product", placeholder="e.g. iPhone 15")

def get_data(product):
    base = 70000
    return [
        {"site":"Amazon","price":base+random.randint(-2000,2000),
         "rating":round(random.uniform(4.2,4.8),1),
         "reviews":random.randint(500,5000),
         "image":f"https://source.unsplash.com/300x200/?{product}"},
        {"site":"Flipkart","price":base+random.randint(-2500,1500),
         "rating":round(random.uniform(4.1,4.7),1),
         "reviews":random.randint(300,4000),
         "image":f"https://source.unsplash.com/300x200/?{product},tech"},
        {"site":"Croma","price":base+random.randint(-1500,2500),
         "rating":round(random.uniform(4.0,4.6),1),
         "reviews":random.randint(100,2000),
         "image":f"https://source.unsplash.com/300x200/?electronics,{product}"}
    ]

if st.button("🚀 Compare Now"):
    data = get_data(product)
    best_price = min(item["price"] for item in data)
    best_rating = max(item["rating"] for item in data)

    st.markdown("### 💰 Compare Deals")
    cols = st.columns(3)

    for i,item in enumerate(data):
        discount = random.randint(5,20)
        old_price = item["price"] + (item["price"]*discount//100)

        badges=""
        if item["price"]==best_price:
            badges += '<span class="badge">BEST DEAL</span> '
        if item["rating"]==best_rating:
            badges += '<span class="badge popular">MOST POPULAR</span>'

        with cols[i]:
            st.markdown(f'''
            <div class="card">
                <img src="{item['image']}" width="100%" style="border-radius:10px"/>
                <h3>{item['site']}</h3>
                {badges}
                <div class="price">₹{item['price']}</div>
                <div class="old-price">₹{old_price}</div>
                <p>⭐ {item['rating']} ({item['reviews']} reviews)</p>
                <button>🛒 Buy Now</button>
            </div>
            ''', unsafe_allow_html=True)

    prompt = f"Compare these deals and suggest best option: {data}"

    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}]
    )

    st.markdown("### 🧠 AI Recommendation")
    st.markdown(f'<div class="ai-box">{res.choices[0].message.content}</div>', unsafe_allow_html=True)

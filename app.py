import streamlit as st
import requests
from openai import OpenAI
import time

st.set_page_config(page_title="Get Your Best Deal", layout="wide")

# ---------- THEME ----------
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

dark_mode = st.sidebar.toggle("🌗 Dark Mode", value=True)
st.session_state.theme = "dark" if dark_mode else "light"

# ---------- COLORS ----------
if st.session_state.theme == "dark":
    bg = "#0f172a"
    text = "white"
    card = "#1e293b"
else:
    bg = "#ffffff"
    text = "black"
    card = "#f1f5f9"

# ---------- CSS ----------
st.markdown(f"""
<style>
html, body, [class*="css"] {{
    background-color: {bg} !important;
    color: {text} !important;
}}

.card {{
    background: {card};
    border-radius: 12px;
    padding: 15px;
    transition: 0.3s;
    height: 100%;
}}

.card:hover {{
    transform: scale(1.03);
}}

.price {{
    font-size: 22px;
    font-weight: bold;
    color: #22c55e;
}}

.old-price {{
    text-decoration: line-through;
    color: gray;
    font-size: 14px;
}}

.badge {{
    background: #22c55e;
    color: white;
    padding: 3px 8px;
    border-radius: 5px;
    font-size: 12px;
}}

.rating {{
    color: orange;
    font-size: 14px;
}}

.button {{
    background:#22c55e;
    color:white;
    padding:6px 12px;
    border-radius:6px;
    text-align:center;
    display:inline-block;
    margin-top:8px;
}}
</style>
""", unsafe_allow_html=True)

# ---------- SIDEBAR ----------
st.sidebar.image("https://img.icons8.com/fluency/96/shopping-cart.png", width=70)
st.sidebar.title("Get Your Best Deal")

SERP_API_KEY = st.sidebar.text_input("🔑 SerpAPI Key", type="password")

st.sidebar.markdown("### Filters")
sort_option = st.sidebar.selectbox("Sort By", ["Best Match", "Lowest Price"])

# ---------- HEADER ----------
st.title("🔥 Get Your Best Deal")
product = st.text_input("Search product (e.g. iPhone 15)")

# ---------- FETCH REAL DATA ----------
def get_data(product):
    if not SERP_API_KEY:
        return []

    url = "https://serpapi.com/search.json"
    params = {
        "engine": "google_shopping",
        "q": product,
        "api_key": SERP_API_KEY,
        "hl": "en",
        "gl": "in"
    }

    res = requests.get(url, params=params)
    data = res.json()

    results = data.get("shopping_results", [])

    output = []
    for item in results[:6]:
        output.append({
            "title": item.get("title"),
            "price": item.get("price"),
            "old_price": item.get("extracted_old_price"),
            "rating": item.get("rating"),
            "image": item.get("thumbnail"),
            "link": item.get("link"),
            "source": item.get("source")
        })

    return output

# ---------- MAIN ----------
if st.button("🔍 Find Products"):

    with st.spinner("Fetching real-time products..."):
        time.sleep(1)

    products = get_data(product)

    if not products:
        st.warning("Add SerpAPI key to fetch real data")
        st.stop()

    # Sort
    if sort_option == "Lowest Price":
        products = sorted(products, key=lambda x: float(x["price"].replace("₹","").replace(",","")) if x["price"] else 999999)

    cols = st.columns(3)

    for i, item in enumerate(products):
        with cols[i % 3]:

            badge = ""
            if i == 0:
                badge = '<span class="badge">🏆 Top Pick</span>'

            st.markdown(f"""
            <div class="card">
                <img src="{item['image']}" width="100%" style="border-radius:10px"/>
                <h4>{item['title'][:60]}...</h4>
                {badge}
                <div class="price">{item['price']}</div>
                <div class="old-price">{item.get('old_price','')}</div>
                <div class="rating">⭐ {item.get('rating','N/A')}</div>
                <p>{item['source']}</p>
                <a href="{item['link']}" target="_blank">
                    <div class="button">🛒 View Deal</div>
                </a>
            </div>
            """, unsafe_allow_html=True)

# ---------- AI ----------
st.markdown("## 🤖 AI Recommendation")

api_key = st.sidebar.text_input("OpenAI Key (optional)", type="password")
client = OpenAI(api_key=api_key) if api_key else None

if client and product:
    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{
            "role": "user",
            "content": f"Recommend best product from this category: {product}"
        }]
    )
    st.write(res.choices[0].message.content)
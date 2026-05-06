import asyncio
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from playwright.async_api import async_playwright
import uvicorn
from openai import OpenAI

app = FastAPI()
client = OpenAI()

async def search_amazon(product):
    results = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(f"https://www.amazon.in/s?k={product}")
        await page.wait_for_timeout(3000)
        items = await page.query_selector_all(".s-result-item")
        for item in items[:5]:
            try:
                title = await item.query_selector("h2 span")
                price = await item.query_selector(".a-price-whole")
                link = await item.query_selector("a")
                if title and price and link:
                    results.append({
                        "site": "Amazon",
                        "title": await title.inner_text(),
                        "price": await price.inner_text(),
                        "link": "https://amazon.in" + await link.get_attribute("href")
                    })
            except:
                continue
        await browser.close()
    return results

async def search_flipkart(product):
    results = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(f"https://www.flipkart.com/search?q={product}")
        await page.wait_for_timeout(3000)
        items = await page.query_selector_all("._1AtVbE")
        for item in items[:5]:
            try:
                title = await item.query_selector("div._4rR01T, a.s1Q9rs")
                price = await item.query_selector("div._30jeq3")
                link = await item.query_selector("a")
                if title and price and link:
                    results.append({
                        "site": "Flipkart",
                        "title": await title.inner_text(),
                        "price": await price.inner_text(),
                        "link": "https://www.flipkart.com" + await link.get_attribute("href")
                    })
            except:
                continue
        await browser.close()
    return results

async def search_croma(product):
    results = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(f"https://www.croma.com/search/?text={product}")
        await page.wait_for_timeout(3000)
        items = await page.query_selector_all(".product-item")
        for item in items[:5]:
            try:
                title = await item.query_selector(".product-title")
                price = await item.query_selector(".amount")
                link = await item.query_selector("a")
                if title and price and link:
                    results.append({
                        "site": "Croma",
                        "title": await title.inner_text(),
                        "price": await price.inner_text(),
                        "link": "https://www.croma.com" + await link.get_attribute("href")
                    })
            except:
                continue
        await browser.close()
    return results

def get_ai_recommendation(data):
    prompt = f"Compare these products and recommend best deal: {data}"
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

@app.get("/compare")
async def compare(product: str):
    amazon, flipkart, croma = await asyncio.gather(
        search_amazon(product),
        search_flipkart(product),
        search_croma(product)
    )
    all_results = amazon + flipkart + croma
    recommendation = get_ai_recommendation(all_results)
    return {"results": all_results, "recommendation": recommendation}

@app.get("/", response_class=HTMLResponse)
def home():
    return """
<!DOCTYPE html>
<html>
<head>
<title>AI Price Agent</title>
<style>
body {font-family: Arial; background:#1f1c2c; color:white; text-align:center;}
input,button {padding:10px; margin:10px;}
.card {background:white; color:black; padding:10px; margin:10px; border-radius:10px;}
</style>
</head>
<body>
<h2>AI Price Comparison</h2>
<input id="product" placeholder="Enter product">
<button onclick="search()">Compare</button>
<div id="results"></div>
<div id="ai"></div>
<script>
async function search(){
 let p = document.getElementById("product").value;
 let res = await fetch(`/compare?product=${p}`);
 let data = await res.json();
 let html="";
 data.results.forEach(i=>{
  html+=`<div class="card">
  <h4>${i.title}</h4>
  ₹${i.price}<br>
  ${i.site}<br>
  <a href="${i.link}" target="_blank">View</a>
  </div>`;
 });
 document.getElementById("results").innerHTML=html;
 document.getElementById("ai").innerHTML="<h3>"+data.recommendation+"</h3>";
}
</script>
</body>
</html>
"""

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

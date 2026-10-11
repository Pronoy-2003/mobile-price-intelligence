"""
Purpose: Scrape mobile product information from Amazon.

Main Tasks:
- Visit predefined Amazon product URLs using Playwright.
- Extract product title, brand, current price, MRP, discount, rating, review count, and availability.
- Record product URLs and scraping timestamps.
- Save the scraped data as JSON and CSV files.
"""


import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import re
import json
import pandas as pd
from datetime import datetime

# List of Amazon Product URLs to scrape
PRODUCT_URLS = [
    #Mobiles
    #iphone
    "https://www.amazon.in/iPhone-Pro-Max-256-Promotion/dp/B0FQFNQ5LX",
    "https://www.amazon.in/iPhone-Pro-512-Promotion-Breakthrough/dp/B0FQF2ZJWT",
    "https://www.amazon.in/iPhone-17-512-Promotion-Resistance/dp/B0FQFYXCC4",
    "https://www.amazon.in/Apple-iPhone-17e-256-GB/dp/B0GQW31KLK",
    "https://www.amazon.in/iPhone-16-128-GB-Control/dp/B0DGHZWBYB",
    #Samsung
    "https://www.amazon.in/Samsung-Smartphone-Silverblue-Snapdragon-ProVisual/dp/B0DSKNKCYX",
    "https://www.amazon.in/Samsung-Snapdragon-Processor-6-2-inch-Smartphone/dp/B0H3FLD9NM",
    "https://www.amazon.in/Samsung-Galaxy-Smartphone-Silver-Storage/dp/B0D73TQLFZ",
    "https://www.amazon.in/Samsung-Galaxy-Smartphone-Storage-Offers/dp/B0DH6YSLFX",
    "https://www.amazon.in/Samsung-Midnight-Complete-Processor-Security/dp/B0DYDQ849T",
    "https://www.amazon.in/Samsung-Awesome-Storage-Premium-Nightography/dp/B0CWPB4X2Q",
    "https://www.amazon.in/Samsung-Storage-Enhanced-Unmatched-Nightography/dp/B0FDBB2VRC",
    #OnePlus & Realme
    "https://www.amazon.in/OnePlus-Snapdragon%C2%AE-7300mAh-Personalised-Game-Changing/dp/B0FTR2PJTV",
    "https://www.amazon.in/OnePlus-Charcoal-Snapdragon%C2%AE-Personalised-Game-Changing/dp/B0FZSWZZW2",
    "https://www.amazon.in/OnePlus-Snapdragon-Segments-Complete-Personalized/dp/B0GRBBPBGQ",
    "https://www.amazon.in/OnePlus-Snapdragon-Segments-Fastest-Response/dp/B0GWLHVJRH",
    "https://www.amazon.in/realme-IceSense-MediaTek-Strongest-Graphene/dp/B0F6YWDMXF",
    "https://www.amazon.in/realme-16-Pro-Smartphone/dp/B0GC75PGRK",
    "https://www.amazon.in/realme-Dimensity-Octa-Core-Processor-6-77-inch/dp/B0HBC2K5XH",
    #Xiaomi & Poco
    "https://www.amazon.in/Xiaomi-Note-14-Pro-5G/dp/B0DQLTWBH7",
    "https://www.amazon.in/Xiaomi-CIVI-Cruise-256GB-Storage/dp/B0D83M6WVX",
    "https://www.amazon.in/POCO-Titanium-8GB-RAM-256GB/dp/B0D5HHW6RQ"   
]

def parse_amazon_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    # Remove script and style elements
    for elem in soup(['script', 'style', 'noscript']):
        elem.decompose()

    # Title
    title_elem = soup.find('span', id='productTitle')
    title = title_elem.get_text(strip=True) if title_elem else None

    # Brand
    brand_elem = soup.find('a', id='bylineInfo') or soup.select_one('tr.po-brand span.a-size-base')
    brand = brand_elem.get_text(strip=True).replace('Brand: ', '').replace('Visit the ', '') if brand_elem else None
    if not brand and title:
        brand = title.split()[0]

    # Current Price
    raw_current_price = None
    price_container = soup.select_one('span.a-price.aok-align-center, span.a-price')
    if price_container:
        offscreen_elem = price_container.select_one('span.a-offscreen')
        if offscreen_elem and offscreen_elem.get_text(strip=True):
            raw_current_price = offscreen_elem.get_text(strip=True)
        else:
            symbol_elem = price_container.select_one('span.a-price-symbol')
            whole_elem = price_container.select_one('span.a-price-whole')
            symbol = symbol_elem.get_text(strip=True) if symbol_elem else '₹'
            whole = whole_elem.get_text(strip=True).rstrip('.,') if whole_elem else ''
            if whole:
                raw_current_price = f"{symbol}{whole}"

    # List Price (MRP)
    list_price_elem = (
        soup.select_one('span.a-price[data-a-strike="true"] span.a-offscreen') or
        soup.select_one('span.a-text-price span.a-offscreen')
    )
    raw_list_price = list_price_elem.get_text(strip=True) if list_price_elem else None

    # Discount Percentage
    discount_elem = (
        soup.select_one('span.savingsPercentage') or 
        soup.find('span', string=re.compile(r'-\d+%', re.IGNORECASE))
    )
    raw_discount_pct = discount_elem.get_text(strip=True) if discount_elem else None

    # Rating Score
    rating_container = soup.find('div', id='averageCustomerReviews') or soup.find('span', id='acrPopover')
    raw_rating = None
    if rating_container:
        if rating_container.get('title'):
            raw_rating = rating_container.get('title')
        else:
            alt_elem = rating_container.select_one('span.a-icon-alt') or rating_container.select_one('span.a-size-small')
            if alt_elem:
                raw_rating = alt_elem.get_text(strip=True)

    if not raw_rating:
        star_elem = soup.select_one('i.a-icon-star span.a-icon-alt') or soup.find('span', class_='a-icon-alt')
        raw_rating = star_elem.get_text(strip=True) if star_elem else None

    # Reviews Count
    reviews_elem = soup.find('span', id='acrCustomerReviewText')
    raw_reviews_count = reviews_elem.get_text(strip=True) if reviews_elem else None

    # Availability
    avail_elem = soup.find('div', id='availability')
    raw_availability = avail_elem.get_text(strip=True) if avail_elem else "In stock"

    return {
        "platform": "Amazon",
        "title": title,
        "brand": brand,
        "raw_current_price": raw_current_price,
        "raw_list_price": raw_list_price,
        "raw_discount_pct": raw_discount_pct,
        "raw_rating": raw_rating,
        "raw_reviews_count": raw_reviews_count,
        "raw_availability": raw_availability
    }

async def run_scraper():
    dataset = []
    
    async with async_playwright() as p:
        # Launch browser in non-headless mode to avoid bot detection block
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        for idx, url in enumerate(PRODUCT_URLS, 1):
            print(f"[{idx}/{len(PRODUCT_URLS)}] Scraping: {url}")
            try:
                await page.goto(url, wait_until="domcontentloaded", timeout=30000)
                await page.wait_for_timeout(3000)  # Wait for dynamic elements to render
                
                content = await page.content()
                data = parse_amazon_html(content)
                data["product_url"] = url
                data["scrape_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                dataset.append(data)
                
            except Exception as e:
                print(f"Error scraping {url}: {e}")

        await browser.close()

    # Save outputs
    with open("amazon_scraped_data.json", "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=4)

    df = pd.DataFrame(dataset)
    df.to_csv("amazon_scraped_data.csv", index=False, encoding="utf-8-sig")
    print("\nScraping Complete! Data saved to 'amazon_scraped_data.json' and 'amazon_scraped_data.csv'.")

if __name__ == "__main__":
    asyncio.run(run_scraper())
"""
Purpose: Scrape mobile product information from Flipkart.

Main Tasks:
- Visit predefined Flipkart product URLs using requests and BeautifulSoup.
- Extract product title, brand, current price, MRP, discount, rating, review count, and availability.
- Separate rating and review count into individual columns.
- Record product URLs and scraping timestamps.
- Save the scraped data as a CSV file.
"""


import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import re


# ==========================================
# PRODUCT URLS
# ==========================================

PRODUCT_URLS = [
    #iphone
    "https://www.flipkart.com/apple-iphone-17-pro-max-cosmic-orange-256-gb/p/itm81f3a173391c4",
    "https://www.flipkart.com/apple-iphone-17-pro-silver-512-gb/p/itmfe915ac778113",
    "https://www.flipkart.com/apple-iphone-17-black-256-gb/p/itmc61b40459dd98",
    "https://www.flipkart.com/apple-iphone-17e-white-256-gb/p/itmb0086ea331d77",
    "https://www.flipkart.com/apple-iphone-16-white-128-gb/p/itm7c0281cd247be",
    #Samsung
    "https://www.flipkart.com/samsung-galaxy-s25-ultra-5g-titanium-silverblue-256-gb/p/itm413a5c3f30151",
    "https://www.flipkart.com/samsung-galaxy-s25-5g-snapdragon-navy-128-gb/p/itm957543a944c80",
    "https://www.flipkart.com/samsung-galaxy-z-fold6-5g-silver-shadow-256-gb/p/itmb72b4d42fcba6",
    "https://www.flipkart.com/samsung-galaxy-z-flip6-5g-blue-256-gb/p/itm8f1b3aefb27f2",
    "https://www.flipkart.com/samsung-galaxy-a56-5g-awesome-olive-256-gb/p/itm7e0f6a3b05352",
    "https://www.flipkart.com/samsung-galaxy-a35-5g-awesome-navy-256-gb/p/itm2d2e398127998",
    "https://www.flipkart.com/samsung-m36-5g-velvet-black-black-128-gb/p/itm1e7be51802033",
    #OnePlus & Realme
    "https://www.flipkart.com/oneplus-15-5g-sand-storm-512-gb/p/itm0106a23b51268",
    "https://www.flipkart.com/oneplus-15r-5g-charcoal-black-256-gb/p/itmc1c624041ba6c",
    "https://www.flipkart.com/oneplus-nord-6-fresh-mint-256-gb/p/itmc49f71cdc4080",
    "https://www.flipkart.com/oneplus-nord-ce6-pitch-black-128-gb/p/itmd7b224b18cb05",
    "https://www.flipkart.com/realme-gt-7t-icesense-blue-256-gb/p/itmda26d662ee28e",
    "https://www.flipkart.com/realme-16-pro-5g-master-gold-256-gb/p/itm0f32797c10002",
    "https://www.flipkart.com/realme-p4-5g-forge-red-128-gb/p/itmf836e6de035a5",
    #Xiaomi & Poco
    "https://www.flipkart.com/redmi-note-14-pro-5g-spectre-blue-128-gb/p/itmf69d377f9a8fb",
    "https://www.flipkart.com/xiaomi-14-civi-cruise-blue-256-gb/p/itm08bfd5b12dee3",
    "https://www.flipkart.com/poco-f6-5g-titanium-256-gb/p/itme731d9a334947"
]


# ==========================================
# SESSION
# ==========================================

session = requests.Session()

session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://google.com"
})


# Homepage first
session.get(
    "https://www.flipkart.com/",
    timeout=30
)


# ==========================================
# SCRAPING
# ==========================================

dataset = []

for idx, product_url in enumerate(PRODUCT_URLS, 1):

    print(f"\n[{idx}/{len(PRODUCT_URLS)}] Scraping")
    print(product_url)

    try:

        # Product page
        response = session.get(
            product_url,
            timeout=30
        )

        print("Status Code:", response.status_code)

        if response.status_code != 200:
            print("Failed")
            continue

        # Parse HTML
        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )


        # ==========================================
        # TITLE
        # ==========================================

        h1_tags = soup.find_all("h1")

        title = None

        if h1_tags:
            title = h1_tags[0].get_text(strip=True)


        # ==========================================
        # BRAND
        # ==========================================

        brand = None

        if title:
            brand = title.split()[0]


        # ==========================================
        # CURRENT PRICE
        # ==========================================

        current_price = None

        price_elem = soup.select_one(
            "div.v1zwn21n.v1zwn20"
        )

        if price_elem:

            price_match = re.search(
                r"₹\s*([\d,]+)",
                price_elem.get_text(
                    " ",
                    strip=True
                )
            )

            if price_match:

                current_price = int(
                    price_match.group(1)
                    .replace(",", "")
                )


        # ==========================================
        # MRP
        # ==========================================

        mrp = None

        # Find all divs containing v1zwn21
        mrp_elements = soup.find_all(
            lambda tag:
            tag.name == "div"
            and "v1zwn21" in tag.get("class", [])
        )

        for element in mrp_elements:

            style = element.get(
                "style",
                ""
            ).lower()

            # MRP is the price with line-through
            if "line-through" in style:

                mrp_text = element.get_text(
                    " ",
                    strip=True
                )

                mrp_match = re.search(
                    r"₹?\s*([\d,]+)",
                    mrp_text
                )

                if mrp_match:

                    mrp = int(
                        mrp_match.group(1)
                        .replace(",", "")
                    )

                    break


        # ==========================================
        # DISCOUNT
        # ==========================================

        discount_pct = None

        if (
            current_price is not None
            and mrp is not None
            and mrp > 0
        ):

            discount_pct = round(
                ((mrp - current_price) / mrp) * 100,
                2
            )


        # ==========================================
        # RATING + REVIEW COUNT TOGETHER
        # ==========================================

        rating_reviews = None

        rating_link = soup.select_one(
            'a[href*="ratings-reviews-details-page"]'
        )

        if rating_link:

            rating_reviews = rating_link.get_text(
                " ",
                strip=True
            )


        # ==========================================
        # AVAILABILITY
        # ==========================================

        buy_now = soup.find(
            lambda tag:
            tag.name in ["button", "div", "a"]
            and "Buy now" in tag.get_text(
                " ",
                strip=True
            )
        )

        notify_me = soup.find(
            lambda tag:
            tag.name in ["button", "div", "a"]
            and "Notify Me" in tag.get_text(
                " ",
                strip=True
            )
        )

        if buy_now:
            availability = "In Stock"

        elif notify_me:
            availability = "Unavailable"

        else:
            availability = "Unavailable"


        # ==========================================
        # STORE DATA
        # ==========================================

        data = {

            "platform": "Flipkart",

            "title": title,

            "brand": brand,

            "current_price": current_price,

            "mrp": mrp,

            "discount_pct": discount_pct,

            "rating_reviews": rating_reviews,

            "availability": availability,

            "product_url": product_url,

            "scrape_at": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        }

        dataset.append(data)


        # ==========================================
        # PRINT RESULT
        # ==========================================

        print("Title:", title)
        print("Brand:", brand)
        print("Current Price:", current_price)
        print("MRP:", mrp)
        print("Discount:", discount_pct, "%")
        print("Rating + Reviews:", rating_reviews)
        print("Availability:", availability)


    except Exception as e:

        print("Error:", e)


# ==========================================
# CREATE DATAFRAME
# ==========================================

df = pd.DataFrame(dataset)


# ==========================================
# SEPARATE RATING AND REVIEW COUNT
# ==========================================

def separate_rating_reviews(value):
    if pd.isna(value):
        return pd.Series([None, None])

    text = str(value).strip()

    rating = None
    review_count = None

    # Flipkart format: "4.6 | 4,272"
    if "|" in text:
        parts = text.split("|")

        # Rating
        rating_text = parts[0].strip()
        rating_match = re.search(r"\d+(?:\.\d+)?", rating_text)

        if rating_match:
            rating = float(rating_match.group())

        # Review count
        if len(parts) > 1:
            review_text = parts[1].strip()
            review_match = re.search(r"[\d,]+", review_text)

            if review_match:
                review_count = int(
                    review_match.group().replace(",", "")
                )

    return pd.Series([rating, review_count])


df[
    ["rating", "review_count"]
] = df["rating_reviews"].apply(
    separate_rating_reviews
)


# Remove combined column
df.drop(
    columns=["rating_reviews"],
    inplace=True
)


# ==========================================
# SAVE CSV
# ==========================================

df.to_csv(
    "flipkart_scraped_data.csv",
    index=False,
    encoding="utf-8-sig"
)


print("\n===================================")
print("Scraping Complete!")
print("Products collected:", len(df))
print("Saved to: flipkart_scraped_data.csv")
print("===================================")
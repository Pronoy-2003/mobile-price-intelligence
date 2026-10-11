"""
Purpose: Clean and standardize the raw Amazon and Flipkart datasets.

Main Tasks:
- Convert prices, MRP, discounts, ratings, and review counts into numeric values.
- Standardize brand names and availability categories.
- Handle missing or invalid values appropriately.
- Calculate discount percentages using MRP and current price.
- Standardize column names, data types, and column order.
- Save the cleaned datasets for further processing.
"""


import pandas as pd
import numpy as np
import re
from pathlib import Path


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

AMAZON_FILE = BASE_DIR / "data" / "raw" / "amazon_scraped_data.csv"
FLIPKART_FILE = BASE_DIR / "data" / "raw" / "flipkart_scraped_data.csv"

OUTPUT_DIR = BASE_DIR / "data" / "processed"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

AMAZON_OUTPUT = OUTPUT_DIR / "amazon_cleaned.csv"
FLIPKART_OUTPUT = OUTPUT_DIR / "flipkart_cleaned.csv"


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def clean_numeric(value):
    """
    Extract numeric value from strings such as:
    ₹79,999
    79,999
    -663
    -2,757
    """

    if pd.isna(value):
        return np.nan

    text = str(value).strip()

    numbers = re.findall(r"\d+(?:,\d+)*", text)

    if not numbers:
        return np.nan

    return float(numbers[0].replace(",", ""))


def clean_review_count(value):
    """
    Convert Amazon review values such as:
    -663
    -2,757

    into:
    663
    2757
    """

    if pd.isna(value):
        return np.nan

    text = str(value).strip()

    match = re.search(r"[\d,]+", text)

    if not match:
        return np.nan

    return int(match.group().replace(",", ""))


def clean_rating(value):
    """
    Extract numeric rating from values such as:
    4.5
    4.5 out of 5 stars
    4.5 out of 5

    Returns a valid rating between 0 and 5.
    """

    if pd.isna(value):
        return np.nan

    text = str(value).strip()

    match = re.search(r"\d+(?:\.\d+)?", text)

    if not match:
        return np.nan

    rating = float(match.group())

    # Keep only valid ratings
    if 0 <= rating <= 5:
        return rating

    return np.nan


def clean_discount(value):
    """
    Convert values such as:
    -20%
    20%

    into positive numeric percentages.
    """

    if pd.isna(value):
        return np.nan

    text = str(value).strip()

    match = re.search(r"\d+(?:\.\d+)?", text)

    if not match:
        return np.nan

    return float(match.group())


def standardize_brand(brand):
    """
    Standardize brand names across Amazon and Flipkart.
    """

    if pd.isna(brand):
        return np.nan

    brand = str(brand).strip()

    brand_lower = brand.lower()

    brand_mapping = {
        "samsung store": "Samsung",
        "samsung": "Samsung",

        "apple store": "Apple",
        "apple": "Apple",

        "oneplus store": "OnePlus",
        "oneplus": "OnePlus",

        "realme store": "realme",
        "realme": "realme",

        "redmi store": "Redmi",
        "redmi": "Redmi",

        "xiaomi": "Xiaomi",
        "mi": "Xiaomi",

        "poco": "POCO"
    }

    return brand_mapping.get(brand_lower, brand)


def standardize_amazon_availability(value):
    """
    Convert Amazon availability into common categories.
    """

    if pd.isna(value):
        return "Unknown"

    text = str(value).strip().lower()

    if "currently unavailable" in text:
        return "Unavailable"

    if "only 1 left" in text or "only 2 left" in text:
        return "Low Stock"

    if "in stock" in text:
        return "In Stock"

    return "Unknown"


def standardize_flipkart_availability(value):
    """
    Standardize Flipkart availability.
    """

    if pd.isna(value):
        return "Unknown"

    text = str(value).strip().lower()

    if "in stock" in text:
        return "In Stock"

    if "unavailable" in text:
        return "Unavailable"

    return "Unknown"


def calculate_discount(mrp, current_price):
    """
    Calculate discount percentage from MRP and current price.
    """

    if pd.isna(mrp) or pd.isna(current_price):
        return np.nan

    if mrp <= 0:
        return np.nan

    discount = ((mrp - current_price) / mrp) * 100

    return round(discount, 2)


# ============================================================
# LOAD RAW DATA
# ============================================================

print("=" * 70)
print("MOBILE PRICE INTELLIGENCE - DATA CLEANING")
print("=" * 70)

amazon = pd.read_csv(AMAZON_FILE)
flipkart = pd.read_csv(FLIPKART_FILE)

print("\nRaw datasets loaded successfully.")

print(f"Amazon rows   : {len(amazon)}")
print(f"Flipkart rows : {len(flipkart)}")


# ============================================================
# AMAZON CLEANING
# ============================================================

print("\n" + "=" * 70)
print("CLEANING AMAZON DATA")
print("=" * 70)

amazon_clean = pd.DataFrame()

amazon_clean["platform"] = "Amazon"

amazon_clean["title"] = (
    amazon["title"]
    .astype(str)
    .str.strip()
    .str.replace(r"\s+", " ", regex=True)
)

amazon_clean["brand"] = amazon["brand"].apply(
    standardize_brand
)

amazon_clean["current_price"] = (
    amazon["raw_current_price"]
    .apply(clean_numeric)
)

amazon_clean["mrp"] = (
    amazon["raw_list_price"]
    .apply(clean_numeric)
)


# ============================================================
# FIXED AMAZON RATING CLEANING
# ============================================================

amazon_clean["rating"] = (
    amazon["raw_rating"]
    .apply(clean_rating)
)


amazon_clean["review_count"] = (
    amazon["raw_reviews_count"]
    .apply(clean_review_count)
)

amazon_clean["availability"] = (
    amazon["raw_availability"]
    .apply(standardize_amazon_availability)
)

amazon_clean["product_url"] = (
    amazon["product_url"]
    .astype(str)
    .str.strip()
)

amazon_clean["scrape_at"] = pd.to_datetime(
    amazon["scrape_at"],
    format="%d-%m-%Y %H:%M",
    errors="coerce"
)


# Calculate discount from MRP and current price

amazon_clean["discount_pct"] = amazon_clean.apply(
    lambda row: calculate_discount(
        row["mrp"],
        row["current_price"]
    ),
    axis=1
)


# Arrange columns

amazon_clean = amazon_clean[
    [
        "platform",
        "title",
        "brand",
        "current_price",
        "mrp",
        "discount_pct",
        "rating",
        "review_count",
        "availability",
        "product_url",
        "scrape_at"
    ]
]


# ============================================================
# FLIPKART CLEANING
# ============================================================

print("\n" + "=" * 70)
print("CLEANING FLIPKART DATA")
print("=" * 70)

flipkart_clean = pd.DataFrame()

flipkart_clean["platform"] = "Flipkart"

flipkart_clean["title"] = (
    flipkart["title"]
    .astype(str)
    .str.strip()
    .str.replace(r"\s+", " ", regex=True)
)

flipkart_clean["brand"] = flipkart["brand"].apply(
    standardize_brand
)

flipkart_clean["current_price"] = (
    flipkart["current_price"]
    .apply(clean_numeric)
)

flipkart_clean["mrp"] = (
    flipkart["mrp"]
    .apply(clean_numeric)
)

flipkart_clean["rating"] = (
    flipkart["rating"]
    .apply(clean_rating)
)

flipkart_clean["review_count"] = pd.to_numeric(
    flipkart["review_count"],
    errors="coerce"
)

flipkart_clean["availability"] = (
    flipkart["availability"]
    .apply(standardize_flipkart_availability)
)

flipkart_clean["product_url"] = (
    flipkart["product_url"]
    .astype(str)
    .str.strip()
)

flipkart_clean["scrape_at"] = pd.to_datetime(
    flipkart["scrape_at"],
    format="%d-%m-%Y %H:%M",
    errors="coerce"
)


# Calculate discount from MRP and current price

flipkart_clean["discount_pct"] = flipkart_clean.apply(
    lambda row: calculate_discount(
        row["mrp"],
        row["current_price"]
    ),
    axis=1
)


# Arrange columns

flipkart_clean = flipkart_clean[
    [
        "platform",
        "title",
        "brand",
        "current_price",
        "mrp",
        "discount_pct",
        "rating",
        "review_count",
        "availability",
        "product_url",
        "scrape_at"
    ]
]


# ============================================================
# DATA TYPES
# ============================================================

print("\n" + "=" * 70)
print("STANDARDIZING DATA TYPES")
print("=" * 70)

for df in [amazon_clean, flipkart_clean]:

    df["current_price"] = pd.to_numeric(
        df["current_price"],
        errors="coerce"
    )

    df["mrp"] = pd.to_numeric(
        df["mrp"],
        errors="coerce"
    )

    df["discount_pct"] = pd.to_numeric(
        df["discount_pct"],
        errors="coerce"
    )

    df["rating"] = pd.to_numeric(
        df["rating"],
        errors="coerce"
    )

    df["review_count"] = pd.to_numeric(
        df["review_count"],
        errors="coerce"
    )

    df["review_count"] = df["review_count"].astype("Int64")


# ============================================================
# SAVE CLEANED DATA
# ============================================================

amazon_clean.to_csv(
    AMAZON_OUTPUT,
    index=False
)

flipkart_clean.to_csv(
    FLIPKART_OUTPUT,
    index=False
)


# ============================================================
# CLEANING SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("CLEANING SUMMARY")
print("=" * 70)

print("\nAmazon cleaned data:")
print(f"Rows              : {len(amazon_clean)}")
print(f"Columns           : {len(amazon_clean.columns)}")

print(
    f"Missing MRP       : "
    f"{amazon_clean['mrp'].isna().sum()}"
)

print(
    f"Missing Discount  : "
    f"{amazon_clean['discount_pct'].isna().sum()}"
)

print(
    f"Missing Rating    : "
    f"{amazon_clean['rating'].isna().sum()}"
)

print(
    f"Missing Reviews   : "
    f"{amazon_clean['review_count'].isna().sum()}"
)

print(
    f"Unknown Availability: "
    f"{(amazon_clean['availability'] == 'Unknown').sum()}"
)


print("\nFlipkart cleaned data:")
print(f"Rows              : {len(flipkart_clean)}")
print(f"Columns           : {len(flipkart_clean.columns)}")

print(
    f"Missing MRP       : "
    f"{flipkart_clean['mrp'].isna().sum()}"
)

print(
    f"Missing Discount  : "
    f"{flipkart_clean['discount_pct'].isna().sum()}"
)

print(
    f"Missing Rating    : "
    f"{flipkart_clean['rating'].isna().sum()}"
)

print(
    f"Missing Reviews   : "
    f"{flipkart_clean['review_count'].isna().sum()}"
)

print(
    f"Unknown Availability: "
    f"{(flipkart_clean['availability'] == 'Unknown').sum()}"
)


# ============================================================
# DISPLAY RATING CHECK
# ============================================================

print("\n" + "=" * 70)
print("AMAZON RATING CHECK")
print("=" * 70)

print(
    amazon_clean[
        ["title", "rating"]
    ].to_string(index=False)
)


# ============================================================
# FILES CREATED
# ============================================================

print("\n" + "=" * 70)
print("CLEANED FILES CREATED")
print("=" * 70)

print(f"Amazon   : {AMAZON_OUTPUT}")
print(f"Flipkart : {FLIPKART_OUTPUT}")

print("\nRaw datasets were NOT modified.")

print("\nNext step:")
print("PRODUCT MATCHING")
print("=" * 70)
"""
Purpose: Validate the raw Amazon and Flipkart datasets before cleaning.

Main Tasks:
- Check dataset dimensions and expected column names.
- Identify missing values, duplicate records, and duplicate product URLs.
- Validate platform names, product URLs, timestamps, prices, and MRP.
- Check rating, review count, and availability fields.
- Print a data validation summary without modifying the raw datasets.
"""


import pandas as pd
import re
from pathlib import Path


# ============================================================
# FILE PATHS
# ============================================================

AMAZON_FILE = Path("data/raw/amazon_scraped_data.csv")
FLIPKART_FILE = Path("data/raw/flipkart_scraped_data.csv")


# ============================================================
# EXPECTED COLUMNS
# ============================================================

EXPECTED_AMAZON_COLUMNS = [
    "platform",
    "title",
    "brand",
    "raw_current_price",
    "raw_list_price",
    "raw_discount_pct",
    "raw_rating",
    "raw_reviews_count",
    "raw_availability",
    "product_url",
    "scrape_at"
]

EXPECTED_FLIPKART_COLUMNS = [
    "platform",
    "title",
    "brand",
    "current_price",
    "mrp",
    "discount_pct",
    "availability",
    "product_url",
    "scrape_at",
    "rating",
    "review_count"
]


# ============================================================
# LOAD DATA
# ============================================================

amazon = pd.read_csv(AMAZON_FILE)
flipkart = pd.read_csv(FLIPKART_FILE)


print("=" * 70)
print("MOBILE PRICE INTELLIGENCE - DATA VALIDATION")
print("=" * 70)


# ============================================================
# 1. BASIC INFORMATION
# ============================================================

print("\n1. BASIC DATASET INFORMATION")
print("-" * 70)

print(f"Amazon rows    : {len(amazon):,}")
print(f"Amazon columns : {len(amazon.columns):,}")

print(f"Flipkart rows    : {len(flipkart):,}")
print(f"Flipkart columns : {len(flipkart.columns):,}")


# ============================================================
# 2. SCHEMA VALIDATION
# ============================================================

print("\n2. SCHEMA VALIDATION")
print("-" * 70)


amazon_missing_columns = [
    col for col in EXPECTED_AMAZON_COLUMNS
    if col not in amazon.columns
]

flipkart_missing_columns = [
    col for col in EXPECTED_FLIPKART_COLUMNS
    if col not in flipkart.columns
]


if not amazon_missing_columns:
    print("Amazon schema: PASS")
else:
    print("Amazon schema: FAIL")
    print("Missing:", amazon_missing_columns)


if not flipkart_missing_columns:
    print("Flipkart schema: PASS")
else:
    print("Flipkart schema: FAIL")
    print("Missing:", flipkart_missing_columns)


# ============================================================
# 3. MISSING VALUE VALIDATION
# ============================================================

print("\n3. MISSING VALUE VALIDATION")
print("-" * 70)

print("\nAmazon missing values:")
print(amazon.isna().sum())

print("\nFlipkart missing values:")
print(flipkart.isna().sum())


# ============================================================
# 4. DUPLICATE VALIDATION
# ============================================================

print("\n4. DUPLICATE VALIDATION")
print("-" * 70)

print("Amazon duplicate rows:",
      amazon.duplicated().sum())

print("Flipkart duplicate rows:",
      flipkart.duplicated().sum())

print("\nAmazon duplicate URLs:",
      amazon["product_url"].duplicated().sum())

print("Flipkart duplicate URLs:",
      flipkart["product_url"].duplicated().sum())

print("\nAmazon duplicate titles:",
      amazon["title"].duplicated().sum())

print("Flipkart duplicate titles:",
      flipkart["title"].duplicated().sum())


# ============================================================
# 5. PLATFORM VALIDATION
# ============================================================

print("\n5. PLATFORM VALIDATION")
print("-" * 70)

print("Amazon platform values:")
print(amazon["platform"].value_counts())

print("\nFlipkart platform values:")
print(flipkart["platform"].value_counts())


# ============================================================
# 6. URL VALIDATION
# ============================================================

print("\n6. URL VALIDATION")
print("-" * 70)

amazon_invalid_urls = (
    ~amazon["product_url"].str.startswith(
        "https://www.amazon.in/"
    )
).sum()

flipkart_invalid_urls = (
    ~flipkart["product_url"].str.startswith(
        "https://www.flipkart.com/"
    )
).sum()


print("Invalid Amazon URLs:", amazon_invalid_urls)
print("Invalid Flipkart URLs:", flipkart_invalid_urls)


# ============================================================
# 7. TIMESTAMP VALIDATION
# ============================================================

print("\n7. TIMESTAMP VALIDATION")
print("-" * 70)

amazon_dates = pd.to_datetime(
    amazon["scrape_at"],
    format="%d-%m-%Y %H:%M",
    errors="coerce"
)

flipkart_dates = pd.to_datetime(
    flipkart["scrape_at"],
    format="%d-%m-%Y %H:%M",
    errors="coerce"
)

print("Invalid Amazon timestamps:",
      amazon_dates.isna().sum())

print("Invalid Flipkart timestamps:",
      flipkart_dates.isna().sum())

print("Amazon scrape date:",
      amazon_dates.dt.date.min())

print("Flipkart scrape date:",
      flipkart_dates.dt.date.min())


# ============================================================
# 8. PRICE VALIDATION
# ============================================================

print("\n8. PRICE VALIDATION")
print("-" * 70)


def extract_number(value):

    if pd.isna(value):
        return None

    match = re.search(
        r"[\d,]+(?:\.\d+)?",
        str(value)
    )

    if match:
        return float(
            match.group().replace(",", "")
        )

    return None


amazon["validated_current_price"] = (
    amazon["raw_current_price"]
    .apply(extract_number)
)

amazon["validated_mrp"] = (
    amazon["raw_list_price"]
    .apply(extract_number)
)

flipkart["validated_current_price"] = (
    flipkart["current_price"]
)

flipkart["validated_mrp"] = (
    flipkart["mrp"]
)


amazon_invalid_price = (
    amazon["validated_current_price"] <= 0
).sum()

flipkart_invalid_price = (
    flipkart["validated_current_price"] <= 0
).sum()


print("Invalid Amazon prices:",
      amazon_invalid_price)

print("Invalid Flipkart prices:",
      flipkart_invalid_price)


# MRP should not be lower than current price
amazon_bad_mrp = (
    amazon["validated_mrp"].notna()
    &
    (
        amazon["validated_mrp"]
        <
        amazon["validated_current_price"]
    )
).sum()

flipkart_bad_mrp = (
    flipkart["validated_mrp"].notna()
    &
    (
        flipkart["validated_mrp"]
        <
        flipkart["validated_current_price"]
    )
).sum()


print("Amazon MRP < Current Price:",
      amazon_bad_mrp)

print("Flipkart MRP < Current Price:",
      flipkart_bad_mrp)


# ============================================================
# 9. RATING VALIDATION
# ============================================================

print("\n9. RATING VALIDATION")
print("-" * 70)


def extract_rating(value):

    if pd.isna(value):
        return None

    match = re.search(
        r"\d+(?:\.\d+)?",
        str(value)
    )

    if match:
        return float(match.group())

    return None


amazon["validated_rating"] = (
    amazon["raw_rating"]
    .apply(extract_rating)
)

flipkart["validated_rating"] = (
    flipkart["rating"]
)


amazon_bad_rating = (
    (amazon["validated_rating"] < 0)
    |
    (amazon["validated_rating"] > 5)
).sum()

flipkart_bad_rating = (
    (flipkart["validated_rating"] < 0)
    |
    (flipkart["validated_rating"] > 5)
).sum()


print("Amazon invalid ratings:",
      amazon_bad_rating)

print("Flipkart invalid ratings:",
      flipkart_bad_rating)


# ============================================================
# 10. REVIEW COUNT VALIDATION
# ============================================================

print("\n10. REVIEW COUNT VALIDATION")
print("-" * 70)


def extract_review_count(value):

    if pd.isna(value):
        return None

    match = re.search(
        r"[\d,]+",
        str(value)
    )

    if match:
        return int(
            match.group().replace(",", "")
        )

    return None


amazon["validated_review_count"] = (
    amazon["raw_reviews_count"]
    .apply(extract_review_count)
)

flipkart["validated_review_count"] = (
    flipkart["review_count"]
)


amazon_missing_reviews = (
    amazon["validated_review_count"].isna()
).sum()

flipkart_missing_reviews = (
    flipkart["validated_review_count"].isna()
).sum()


print("Amazon missing review count:",
      amazon_missing_reviews)

print("Flipkart missing review count:",
      flipkart_missing_reviews)


# ============================================================
# 11. AVAILABILITY VALIDATION
# ============================================================

print("\n11. AVAILABILITY VALIDATION")
print("-" * 70)

print("Amazon availability values:")
print(
    amazon["raw_availability"]
    .value_counts(dropna=False)
)

print("\nFlipkart availability values:")
print(
    flipkart["availability"]
    .value_counts(dropna=False)
)


# ============================================================
# FINAL VALIDATION SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("VALIDATION COMPLETE")
print("=" * 70)

print("""
Raw datasets were validated without modifying the source files.

Next step:
DATA CLEANING
""")
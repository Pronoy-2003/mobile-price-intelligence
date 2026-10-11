"""
Purpose: Match identical mobile product variants across Amazon and Flipkart.

Main Tasks:
- Normalize brand names and product names for matching.
- Create matching keys using product identity, RAM, and storage capacity.
- Match iPhones using product name and storage because RAM is unavailable.
- Merge matched products into a cross-platform comparison dataset.
- Calculate price differences, absolute price gaps, discount differences,
  rating differences, and review count differences.
- Identify unmatched product variants and generate a matching report.
- Save the final comparison dataset for EDA and Power BI.
"""


import pandas as pd
from pathlib import Path

# ============================================================
# 1. File paths
# ============================================================

AMAZON_FILE = "data/processed/amazon_standardized.csv"
FLIPKART_FILE = "data/processed/flipkart_standardized.csv"

OUTPUT_FILE = "data/processed/final_mobile_price_comparison.csv"
REPORT_FILE = "data/processed/product_matching_report.csv"


# ============================================================
# 2. Load data
# ============================================================

amazon = pd.read_csv(AMAZON_FILE)
flipkart = pd.read_csv(FLIPKART_FILE)

print(f"Amazon records   : {len(amazon)}")
print(f"Flipkart records : {len(flipkart)}")


# ============================================================
# 3. Create normalized matching fields
# ============================================================

def normalize_text(series):
    return (
        series
        .fillna("")
        .astype(str)
        .str.strip()
        .str.lower()
    )


for df in [amazon, flipkart]:

    df["brand_match"] = normalize_text(df["brand"])
    df["product_match"] = normalize_text(df["product_name"])


# ============================================================
# 4. Create product matching key
# ============================================================

def create_match_key(df):

    # iPhone RAM is unavailable on both platforms,
    # so match iPhones using ROM instead of RAM.
    iphone_mask = df["brand_match"] == "apple"

    df["match_key"] = ""

    # iPhone key
    df.loc[iphone_mask, "match_key"] = (
        df.loc[iphone_mask, "brand_match"]
        + "|"
        + df.loc[iphone_mask, "product_match"]
        + "|"
        + df.loc[iphone_mask, "rom_gb"].astype(str)
    )

    # Non-iPhone key
    df.loc[~iphone_mask, "match_key"] = (
        df.loc[~iphone_mask, "brand_match"]
        + "|"
        + df.loc[~iphone_mask, "product_match"]
        + "|"
        + df.loc[~iphone_mask, "ram_gb"].astype(str)
        + "|"
        + df.loc[~iphone_mask, "rom_gb"].astype(str)
    )

    return df


amazon = create_match_key(amazon)
flipkart = create_match_key(flipkart)


# ============================================================
# 5. Identify exact product matches
# ============================================================

amazon_keys = set(amazon["match_key"])
flipkart_keys = set(flipkart["match_key"])

common_keys = amazon_keys.intersection(flipkart_keys)

print(f"\nExact matched variants: {len(common_keys)}")


# ============================================================
# 6. Create final comparison dataset
# ============================================================

amazon_matched = amazon[amazon["match_key"].isin(common_keys)].copy()
flipkart_matched = flipkart[flipkart["match_key"].isin(common_keys)].copy()


# Rename platform-specific columns

amazon_matched = amazon_matched.rename(columns={
    "current_price": "amazon_price",
    "mrp": "amazon_mrp",
    "discount_pct": "amazon_discount_pct",
    "rating": "amazon_rating",
    "review_count": "amazon_review_count",
    "availability": "amazon_availability",
    "product_url": "amazon_product_url",
    "scrape_at": "amazon_scrape_at"
})

flipkart_matched = flipkart_matched.rename(columns={
    "current_price": "flipkart_price",
    "mrp": "flipkart_mrp",
    "discount_pct": "flipkart_discount_pct",
    "rating": "flipkart_rating",
    "review_count": "flipkart_review_count",
    "availability": "flipkart_availability",
    "product_url": "flipkart_product_url",
    "scrape_at": "flipkart_scrape_at"
})


# ============================================================
# 7. Merge Amazon and Flipkart
# ============================================================

comparison = pd.merge(
    amazon_matched,
    flipkart_matched,
    on="match_key",
    how="inner",
    suffixes=("_amazon", "_flipkart")
)


# ============================================================
# 8. Keep clean business columns
# ============================================================

comparison = comparison[[
    "match_key",

    "product_name_amazon",
    "brand_amazon",
    "ram_gb_amazon",
    "rom_gb_amazon",

    "amazon_price",
    "amazon_mrp",
    "amazon_discount_pct",
    "amazon_rating",
    "amazon_review_count",
    "amazon_availability",
    "amazon_product_url",
    "amazon_scrape_at",

    "flipkart_price",
    "flipkart_mrp",
    "flipkart_discount_pct",
    "flipkart_rating",
    "flipkart_review_count",
    "flipkart_availability",
    "flipkart_product_url",
    "flipkart_scrape_at"
]]


# ============================================================
# 9. Create comparison metrics
# ============================================================

comparison["price_difference"] = (
    comparison["amazon_price"] - comparison["flipkart_price"]
)

comparison["absolute_price_difference"] = (
    comparison["price_difference"].abs()
)

comparison["cheaper_platform"] = comparison.apply(
    lambda row:
        "Amazon"
        if row["price_difference"] < 0
        else "Flipkart"
        if row["price_difference"] > 0
        else "Same Price",
    axis=1
)

comparison["discount_difference"] = (
    comparison["amazon_discount_pct"]
    - comparison["flipkart_discount_pct"]
)

comparison["rating_difference"] = (
    comparison["amazon_rating"]
    - comparison["flipkart_rating"]
)

comparison["review_difference"] = (
    comparison["amazon_review_count"]
    - comparison["flipkart_review_count"]
)


# ============================================================
# 10. Rename product columns
# ============================================================

comparison = comparison.rename(columns={
    "product_name_amazon": "product_name",
    "brand_amazon": "brand",
    "ram_gb_amazon": "ram_gb",
    "rom_gb_amazon": "rom_gb"
})


# ============================================================
# 11. Sort by product name
# ============================================================

comparison = comparison.sort_values(
    by=["brand", "product_name"]
).reset_index(drop=True)


# ============================================================
# 12. Save final comparison dataset
# ============================================================

Path("data/processed").mkdir(
    parents=True,
    exist_ok=True
)

comparison.to_csv(
    OUTPUT_FILE,
    index=False
)


# ============================================================
# 13. Create unmatched / variant mismatch report
# ============================================================

amazon_only = amazon[
    ~amazon["match_key"].isin(common_keys)
].copy()

flipkart_only = flipkart[
    ~flipkart["match_key"].isin(common_keys)
].copy()

amazon_only["match_status"] = "Amazon variant not matched"
flipkart_only["match_status"] = "Flipkart variant not matched"

report_columns = [
    "platform",
    "product_name",
    "brand",
    "ram_gb",
    "rom_gb",
    "current_price",
    "mrp",
    "discount_pct",
    "rating",
    "review_count",
    "availability",
    "match_status"
]

report = pd.concat(
    [
        amazon_only[report_columns],
        flipkart_only[report_columns]
    ],
    ignore_index=True
)

report.to_csv(
    REPORT_FILE,
    index=False
)


# ============================================================
# 14. Final validation
# ============================================================

print("\n========== MATCHING SUMMARY ==========")

print(f"Amazon products              : {len(amazon)}")
print(f"Flipkart products            : {len(flipkart)}")
print(f"Matched product variants     : {len(comparison)}")
print(f"Unmatched Amazon variants    : {len(amazon_only)}")
print(f"Unmatched Flipkart variants  : {len(flipkart_only)}")

print("\n========== CHEAPER PLATFORM ==========")

print(
    comparison["cheaper_platform"]
    .value_counts()
)

print("\n========== FINAL DATASET ==========")

print(
    comparison[
        [
            "brand",
            "product_name",
            "ram_gb",
            "rom_gb",
            "amazon_price",
            "flipkart_price",
            "price_difference",
            "cheaper_platform"
        ]
    ].to_string(index=False)
)

print("\nFiles created:")
print(f"1. {OUTPUT_FILE}")
print(f"2. {REPORT_FILE}")
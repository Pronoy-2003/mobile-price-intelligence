"""
Purpose: Standardize product information to support accurate cross-platform matching.

Main Tasks:
- Extract RAM and storage capacity from product titles.
- Standardize product names using brand-specific rules.
- Preserve original product titles for reference.
- Arrange product attributes into a consistent structure.
- Save standardized Amazon and Flipkart datasets.
"""


import pandas as pd
import re
from pathlib import Path


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

AMAZON_FILE = BASE_DIR / "data" / "processed" / "amazon_cleaned.csv"
FLIPKART_FILE = BASE_DIR / "data" / "processed" / "flipkart_cleaned.csv"

OUTPUT_DIR = BASE_DIR / "data" / "processed"

AMAZON_OUTPUT = OUTPUT_DIR / "amazon_standardized.csv"
FLIPKART_OUTPUT = OUTPUT_DIR / "flipkart_standardized.csv"


# ============================================================
# RAM EXTRACTION
# ============================================================

def extract_ram(title):

    if pd.isna(title):
        return None

    text = str(title)

    patterns = [

        # Example:
        # 12GB RAM
        # 12 GB RAM
        r'(\d+)\s*GB\s*RAM',

        # Example:
        # 256 GB) (12 GB ...more
        # 128 GB) (12 GB R...more
        r'\)\s*\(\s*(\d+)\s*GB',

        # Example:
        # 16GB+512GB
        # 12GB+256GB
        r'(\d+)\s*GB\s*\+\s*\d+\s*GB',

        # Example:
        # 12+256GB
        r'(\d+)\s*\+\s*\d+\s*GB',

        # Example:
        # 8GB, 256GB
        r'(\d+)\s*GB\s*,\s*\d+\s*GB'
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:
            return int(match.group(1))

    return None


# ============================================================
# ROM / STORAGE EXTRACTION
# ============================================================

def extract_rom(title):

    if pd.isna(title):
        return None

    text = str(title)

    # Explicit ROM
    match = re.search(
        r'(\d+)\s*GB\s*ROM',
        text,
        re.IGNORECASE
    )

    if match:
        return int(match.group(1))

    # Explicit Storage
    match = re.search(
        r'(\d+)\s*GB\s*Storage',
        text,
        re.IGNORECASE
    )

    if match:
        return int(match.group(1))

    # RAM + ROM
    # 16GB+512GB
    # 12+256GB
    match = re.search(
        r'\d+\s*GB?\s*\+\s*(\d+)\s*GB',
        text,
        re.IGNORECASE
    )

    if match:
        return int(match.group(1))

    # 8GB, 256GB
    match = re.search(
        r'\d+\s*GB\s*,\s*(\d+)\s*GB',
        text,
        re.IGNORECASE
    )

    if match:
        return int(match.group(1))

    # General storage fallback
    values = re.findall(
        r'(\d+)\s*GB',
        text,
        re.IGNORECASE
    )

    storage_values = [
        int(value)
        for value in values
        if int(value) in [
            64,
            128,
            256,
            512,
            1024
        ]
    ]

    if storage_values:
        return storage_values[-1]

    return None


# ============================================================
# STANDARDIZE PRODUCT TITLE
# ============================================================

def standardize_title(title, brand):

    if pd.isna(title):
        return None

    text = str(title).strip()

    brand = str(brand).strip()


    # ========================================================
    # APPLE
    # ========================================================

    if brand == "Apple":

        # IMPORTANT:
        # Check iPhone 17e BEFORE generic iPhone 17

        patterns = [

            r'(Apple\s+iPhone\s+\d+\s+Pro\s+Max)',

            r'(Apple\s+iPhone\s+\d+\s+Pro)',

            r'(Apple\s+iPhone\s+\d+e)',

            r'(Apple\s+iPhone\s+\d+)'
        ]

        for pattern in patterns:

            match = re.search(
                pattern,
                text,
                re.IGNORECASE
            )

            if match:
                return match.group(1).strip()

        return text


    # ========================================================
    # SAMSUNG
    # ========================================================

    if brand == "Samsung":

        patterns = [

            r'(Samsung\s+Galaxy\s+S\d+\s+Ultra)',

            r'(Samsung\s+Galaxy\s+S\d+)',

            r'(Galaxy\s+Z\s+Fold\d+)',

            r'(Samsung\s+Galaxy\s+Z\s+Flip\d+)',

            r'(Samsung\s+Galaxy\s+A\d+)',

            r'(Samsung\s+Galaxy\s+M\d+)',

            r'(Samsung\s+M\d+)'
        ]

        for pattern in patterns:

            match = re.search(
                pattern,
                text,
                re.IGNORECASE
            )

            if match:

                product = match.group(1)

                # Galaxy Z Fold6
                if re.match(
                    r'Galaxy\s+Z\s+Fold',
                    product,
                    re.IGNORECASE
                ):
                    product = "Samsung " + product

                # Samsung M36
                if re.match(
                    r'Samsung\s+M',
                    product,
                    re.IGNORECASE
                ):
                    product = product.replace(
                        "Samsung M",
                        "Samsung Galaxy M"
                    )

                return product.strip()

        return text


    # ========================================================
    # ONEPLUS
    # ========================================================

    if brand == "OnePlus":

        patterns = [

            r'(OnePlus\s+Nord\s+CE\d+)',

            r'(OnePlus\s+Nord\s+\d+)',

            r'(OnePlus\s+\d+R)',

            r'(OnePlus\s+\d+)'
        ]

        for pattern in patterns:

            match = re.search(
                pattern,
                text,
                re.IGNORECASE
            )

            if match:
                return match.group(1).strip()

        return text


    # ========================================================
    # REALME
    # ========================================================

    if brand == "realme":

        patterns = [

            r'(realme\s+GT\s+\d+T)',

            r'(realme\s+\d+\s+Pro)',

            r'(realme\s+P\d+)'
        ]

        for pattern in patterns:

            match = re.search(
                pattern,
                text,
                re.IGNORECASE
            )

            if match:
                return match.group(1).strip()

        return text


    # ========================================================
    # REDMI
    # ========================================================

    if brand == "Redmi":

        match = re.search(
            r'(?:Redmi|REDMI)\s+Note[-\s]*(\d+)\s+Pro\+?',
            text,
            re.IGNORECASE
        )

        if match:

            return (
                "Redmi Note "
                + match.group(1)
                + " Pro+"
            )

        return text


    # ========================================================
    # XIAOMI
    # ========================================================

    if brand == "Xiaomi":

        match = re.search(
            r'(?:XIAOMI|Mi)\s+(\d+\s+Civi)',
            text,
            re.IGNORECASE
        )

        if match:
            return (
                "Xiaomi "
                + match.group(1).strip()
            )

        return text


    # ========================================================
    # POCO
    # ========================================================

    if brand == "POCO":

        match = re.search(
            r'(?:Poco|POCO)\s+(F\d+)',
            text,
            re.IGNORECASE
        )

        if match:
            return (
                "POCO "
                + match.group(1).strip()
            )

        return text


    return text


# ============================================================
# PROCESS DATASET
# ============================================================

def process_dataset(df, platform):

    result = df.copy()

    # --------------------------------------------------------
    # IMPORTANT: Explicitly set platform
    # --------------------------------------------------------

    result["platform"] = platform

    # --------------------------------------------------------
    # Keep original title
    # --------------------------------------------------------

    result["original_title"] = result["title"]

    # --------------------------------------------------------
    # Extract RAM
    # --------------------------------------------------------

    result["ram_gb"] = result["title"].apply(
        extract_ram
    )

    # --------------------------------------------------------
    # Extract ROM
    # --------------------------------------------------------

    result["rom_gb"] = result["title"].apply(
        extract_rom
    )

    # --------------------------------------------------------
    # Standardize product name
    # --------------------------------------------------------

    result["product_name"] = result.apply(
        lambda row: standardize_title(
            row["title"],
            row["brand"]
        ),
        axis=1
    )

    # --------------------------------------------------------
    # Column order
    # --------------------------------------------------------

    columns = [
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
        "product_url",
        "scrape_at",
        "original_title"
    ]

    result = result[columns]

    return result


# ============================================================
# LOAD DATA
# ============================================================

print("=" * 70)
print("PRODUCT STANDARDIZATION")
print("=" * 70)

amazon = pd.read_csv(
    AMAZON_FILE
)

flipkart = pd.read_csv(
    FLIPKART_FILE
)

print("\nDatasets loaded.")

print("Amazon rows  :", len(amazon))
print("Flipkart rows:", len(flipkart))


# ============================================================
# PROCESS
# ============================================================

amazon_final = process_dataset(
    amazon,
    "Amazon"
)

flipkart_final = process_dataset(
    flipkart,
    "Flipkart"
)


# ============================================================
# SAVE
# ============================================================

amazon_final.to_csv(
    AMAZON_OUTPUT,
    index=False
)

flipkart_final.to_csv(
    FLIPKART_OUTPUT,
    index=False
)


# ============================================================
# DISPLAY RESULTS
# ============================================================

print("\n" + "=" * 70)
print("AMAZON RESULTS")
print("=" * 70)

print(
    amazon_final[
        [
            "platform",
            "product_name",
            "brand",
            "ram_gb",
            "rom_gb"
        ]
    ].to_string(index=False)
)


print("\n" + "=" * 70)
print("FLIPKART RESULTS")
print("=" * 70)

print(
    flipkart_final[
        [
            "platform",
            "product_name",
            "brand",
            "ram_gb",
            "rom_gb"
        ]
    ].to_string(index=False)
)


# ============================================================
# SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("EXTRACTION SUMMARY")
print("=" * 70)

print("\nAmazon:")
print(
    "Missing RAM:",
    amazon_final["ram_gb"].isna().sum()
)

print(
    "Missing ROM:",
    amazon_final["rom_gb"].isna().sum()
)

print("\nFlipkart:")
print(
    "Missing RAM:",
    flipkart_final["ram_gb"].isna().sum()
)

print(
    "Missing ROM:",
    flipkart_final["rom_gb"].isna().sum()
)


print("\n" + "=" * 70)
print("FILES CREATED")
print("=" * 70)

print("\nAmazon:")
print(AMAZON_OUTPUT)

print("\nFlipkart:")
print(FLIPKART_OUTPUT)

print("\nPrevious datasets were NOT modified.")

print("\nNext step:")
print("VERIFY STANDARDIZED DATA")
print("=" * 70)
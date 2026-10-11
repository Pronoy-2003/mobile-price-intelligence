# Data Dictionary — Mobile Price Intelligence

This document describes the principal fields used in the Mobile Price Intelligence project. The project contains raw marketplace extracts, cleaned and standardized listing files, and a final matched-product comparison dataset.

**Data collection date:** 7 October 2026  
**Platforms:** Amazon and Flipkart  
**Currency:** Indian rupees (₹)

> **Important:** Column names differ between raw, cleaned, standardized, and final comparison files. This dictionary documents the known field meanings and common names used in the workflow. Before publishing, compare each entry with the actual headers in your final CSV files and remove or rename any field that is not present.

## 1. Raw Marketplace Data

| Field / common column name | Description | Data type | Notes |
|---|---|---|---|
| `platform` | Marketplace from which the listing was collected | Text | Expected values include `Amazon` and `Flipkart`. |
| `title` | Product title as displayed on the marketplace | Text | Raw listing title; may contain model and configuration details. |
| `brand` | Product brand identified from the listing | Text | May be standardized in later processing. |
| `raw_current_price` / `current_price` | Current selling price captured during scraping | Numeric | Currency is INR. Amazon's raw field was named `raw_current_price`; Flipkart's source used `current_price` in the documented workflow. |
| `raw_list_price` / `mrp` | Listed MRP or list price | Numeric | May be missing. Do not replace missing values with zero. |
| `raw_discount_pct` / `discount_pct` | Listed discount percentage captured or derived from listing fields | Numeric | Confirm whether the source field was scraped or calculated. Missing values are possible. |
| `raw_rating` / `rating` | Customer rating displayed on the listing | Numeric | Rating scale should be interpreted as shown by the source marketplace. |
| `raw_reviews_count` / `reviews_count` | Number of customer reviews shown on the listing | Integer / numeric | May be missing and may be highly skewed. |
| `raw_availability` / `availability` | Availability status or text captured from the listing | Text | May be missing or unknown. |
| `product_url` | URL of the product listing | Text / URL | Keep for traceability; respect applicable website terms. |
| `scrape_at` | Timestamp when the listing was collected | Date/time or text | Collection metadata; the project snapshot date is 7 October 2026. |

## 2. Cleaned and Standardized Product Fields

| Field / common column name | Description | Data type | Notes |
|---|---|---|---|
| `product_name` | Normalized product/model name used for analysis | Text | Derived from the raw title; verify against the actual standardized file. |
| `brand`  | Standardized brand name | Text | Used for grouping and matching. |
| `ram_gb` | RAM capacity extracted from the product title | Numeric / nullable | May be unavailable, especially where titles do not state RAM. |
| `rom_gb` | Internal storage capacity extracted from the product title | Numeric / nullable | Naming varies by processing stage; verify the actual headers. |
| `platform` | Marketplace associated with the standardized listing | Text | Used to distinguish Amazon from Flipkart. |
| `current_price` | Cleaned current selling price | Numeric | INR. |
| `mrp` | Cleaned list price | Numeric / nullable | Null when the source did not provide a usable value. |
| `discount_pct` | Discount percentage used in Power BI or analysis | Numeric / nullable | In this project, values such as `13.8` represent 13.8%, not `0.138`. Format carefully to avoid multiplying by 100 twice. |
| `rating` | Cleaned listing rating | Numeric / nullable | Missing values should remain blank. |
| `review_count` | Cleaned review count | Integer / nullable | Check parsing and missing values before analysis. |
| `availability` | Cleaned availability status | Text / nullable | Reflects the captured listing, not guaranteed current stock. |

## 3. Final Matched Comparison Dataset

The final comparison dataset contains **16 matched product variants** and platform-specific comparison metrics. It may use wide-format columns, with separate Amazon and Flipkart values on each row.

| Column Name | Description | Data Type | Notes |
|---|---|---|---|
| `match_key` | Unique key used to match product variants across platforms | Text | Combines normalized product attributes for matching. |
| `product_name` | Standardized product/model name | Text | Used to identify and compare the same product. |
| `brand` | Product brand | Text | Used for brand-level analysis. |
| `ram_gb` | RAM capacity in GB | Numeric / nullable | May be missing when RAM is not available in product titles. |
| `rom_gb` | Storage capacity in GB | Numeric / nullable | Helps distinguish product variants. |
| `amazon_price` | Current selling price on Amazon | Numeric | Price in INR. |
| `amazon_mrp` | Listed maximum retail price on Amazon | Numeric / nullable | Missing when the listing does not provide MRP. |
| `amazon_discount_pct` | Discount percentage on Amazon | Numeric / nullable | Calculated from MRP and current price during cleaning. |
| `amazon_rating` | Customer rating on Amazon | Numeric / nullable | Typically on a 0–5 scale. |
| `amazon_review_count` | Number of customer reviews on Amazon | Integer / nullable | Extracted from the product listing. |
| `amazon_availability` | Product availability on Amazon | Text | Standardized availability category. |
| `amazon_product_url` | Amazon product page URL | Text | Used to identify and verify the listing. |
| `amazon_scrape_at` | Date and time the Amazon listing was scraped | DateTime | Records the data collection timestamp. |
| `flipkart_price` | Current selling price on Flipkart | Numeric | Price in INR. |
| `flipkart_mrp` | Listed maximum retail price on Flipkart | Numeric / nullable | Missing when the listing does not provide MRP. |
| `flipkart_discount_pct` | Discount percentage on Flipkart | Numeric / nullable | Calculated from MRP and current price during cleaning. |
| `flipkart_rating` | Customer rating on Flipkart | Numeric / nullable | Typically on a 0–5 scale. |
| `flipkart_review_count` | Number of customer reviews on Flipkart | Integer / nullable | Extracted from the product listing. |
| `flipkart_availability` | Product availability on Flipkart | Text | Standardized availability category. |
| `flipkart_product_url` | Flipkart product page URL | Text | Used to identify and verify the listing. |
| `flipkart_scrape_at` | Date and time the Flipkart listing was scraped | DateTime | Records the data collection timestamp. |
| `price_difference` | Amazon price minus Flipkart price | Numeric | Positive means Amazon is more expensive; negative means Amazon is cheaper. |
| `absolute_price_difference` | Absolute value of the price difference | Numeric | Measures the size of the price gap regardless of direction. |
| `cheaper_platform` | Platform with the lower current selling price | Text | Values: `Amazon`, `Flipkart`, or `Same Price`. |
| `discount_difference` | Amazon discount percentage minus Flipkart discount percentage | Numeric / nullable | Positive means Amazon's discount is higher; negative means Flipkart's is higher. |
| `rating_difference` | Amazon rating minus Flipkart rating | Numeric / nullable | Positive means Amazon has the higher rating; negative means Flipkart has the higher rating. |
| `review_difference` | Amazon review count minus Flipkart review count | Numeric / nullable | Positive means Amazon has more reviews; negative means Flipkart has more reviews. |

## 4. Power BI Model Fields

The Power BI report uses a star-schema-style model with product and platform dimensions linked to a product-platform fact table.

### `DimProduct`

| Field | Description |
|---|---|
| `ProductKey` | Product key used to relate product variants to fact rows. |
| `BrandName` / `Brand` | Product brand. |
| `ProductName` | Standardized product name. |
| `RAM_GB` | RAM configuration, where available. |
| `ROM_GB` / `Storage_GB` | Storage configuration, where available. |

### `DimPlatform`

| Field | Description |
|---|---|
| `PlatformKey` | Platform key used to relate platform names to fact rows. |
| `PlatformName` | Marketplace name, such as Amazon or Flipkart. |

### `FactProductPlatform`

| Field | Description |
|---|---|
| `ProductKey` | Foreign key to `DimProduct`. |
| `PlatformKey` | Foreign key to `DimPlatform`. |
| `CurrentPrice` | Current selling price in INR. |
| `MRP` | Listed MRP in INR; may be blank. |
| `DiscountPct` | Listed discount percentage; may be blank. |
| `Rating` | Listing rating; may be blank. |
| `ReviewCount` | Listing review count; may be blank. |
| `Availability` | Captured availability status. |

Expected grain: one row per product variant and platform. With 16 matched variants and two platforms, the model is expected to contain 32 fact rows, assuming each matched variant has one listing per platform.

## 5. Metric Definitions

| Metric | Definition | Interpretation |
|---|---|---|
| Matched Products | Count of distinct matched product keys | Number of comparable product variants. |
| Amazon Average Price | Average Amazon current price for the current filter context | Average selling price of included Amazon listings. |
| Flipkart Average Price | Average Flipkart current price for the current filter context | Average selling price of included Flipkart listings. |
| Average Absolute Price Gap | Average of each matched product's absolute Amazon–Flipkart price difference | Typical size of the gap without regard to direction. |
| Average Listed Discount | Average of non-missing discount percentages for one platform | Platforms may have different numbers of valid discount records. |
| Paired Average Discount | Average discount using only products with valid discount values on both platforms | A like-for-like comparison of the same products. |
| Average Rating | Average listing rating for the selected platform and filter context | Descriptive customer-feedback signal. |
| Median Review Count | Median listing review count for the selected platform and filter context | More robust to extreme review-count values than the mean. |
| Price Advantage | Count of matched products where Amazon is cheaper, Flipkart is cheaper, or both prices are equal | Describes the captured sample only. |

## 6. Data Quality Notes

- Missing MRP or discount values are unknown values, not zero discounts.
- A discount can only be derived from MRP and current price when both values are valid and MRP is greater than zero.
- Platform-level average discounts and paired-product discount comparisons use different populations; label them accordingly.
- Product matching is dependent on normalized titles and extracted RAM/storage information. Review unmatched records rather than forcing uncertain matches.
- Review counts, ratings, availability, prices, and discounts describe the captured snapshot and may change.
- Before publishing, confirm every column name against the actual CSV headers and Power BI model. This dictionary intentionally marks alternative names where the project has used different names at different stages.

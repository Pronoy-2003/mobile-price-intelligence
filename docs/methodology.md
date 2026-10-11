# Methodology — Mobile Price Intelligence

**Project:** Mobile Price Intelligence & Cross-Platform Competitive Analysis  
**Data collection date:** 7 October 2026  
**Platforms:** Amazon and Flipkart  
**Primary tools:** Python, Pandas, Jupyter Notebook, Power BI

## 1. Methodology Overview

The project follows a structured analytics workflow to compare equivalent mobile product variants across Amazon and Flipkart. The workflow moves from web-scraped source data through validation, cleaning, standardization, product matching, exploratory data analysis (EDA), and Power BI reporting.

The data represents a single-day snapshot collected on 7 October 2026. It is used to compare the listings captured on that date, not to infer long-term pricing trends.

## 2. Data Collection

Mobile product listings were collected from Amazon and Flipkart using Python-based web scraping.

The captured fields included listing title, brand, current selling price, listed MRP where available, discount percentage where available, rating, review count, availability, product URL, and scrape timestamp.

The raw datasets contained 22 rows each for Amazon and Flipkart, with 11 columns in each dataset according to the validation output.

**Output:** Raw source files saved separately for Amazon and Flipkart.

## 3. Data Validation

Before cleaning, the source files were checked for:
- Expected column schema.
- Row and column counts.
- Missing values in important fields.
- Fields that require numeric conversion or special parsing.

Both Amazon and Flipkart passed the documented schema checks.

Missing values were treated as missing information rather than automatically replaced with zero. This matters particularly for MRP and discount fields: a missing MRP does not mean that the discount is zero.

**Output:** Validation summaries used to identify fields requiring cleaning and review.

## 4. Data Cleaning

The cleaning process prepared the scraped fields for analysis.

Typical operations included:
- Converting current price, MRP, discount, rating, and review-count fields to suitable numeric types.
- Parsing rating and review information where it was captured as text.
- Handling missing MRP, discount, review count, and availability values.
- Preserving unknown values rather than inventing replacements.
- Reviewing invalid or incomplete values before downstream analysis.

The cleaned Amazon and Flipkart datasets were saved separately for subsequent standardization.

**Output:** Cleaned marketplace datasets.

## 5. Product Standardization and Configuration Extraction

Product titles on the two platforms may use different capitalization, wording, or configuration formats. The standardization step normalized product identity fields to improve matching.

The workflow included:
- Standardizing brand and product-name text.
- Extracting RAM and internal storage (ROM) capacity from titles when available.
- Normalizing text casing where needed.
- Retaining missing configuration values when they could not be reliably extracted.

Some product titles, including iPhone listings, did not provide reliable RAM information. For these cases, the matching logic relied on the available product identity and storage configuration rather than treating missing RAM as a known value.

**Output:** Standardized Amazon and Flipkart datasets with extracted configuration fields where available.

## 6. Product Matching

The matching process identified equivalent product variants listed on both platforms.

The main matching attributes were:
- Standardized brand.
- Normalized product/model name.
- RAM configuration, where available.
- Storage/ROM configuration, where available.

For products where RAM was unavailable on both listings, such as certain iPhone variants, the matching logic used product identity and storage configuration. Text normalization was used to handle differences such as capitalization.

Listings were not forced into a match when their configurations did not align. Unmatched records were retained in a matching report for transparency.

The documented matching outcome was:
- 16 matched product variants.
- 6 unmatched Amazon variants.
- 6 unmatched Flipkart variants.

**Output:** Final matched comparison dataset and product matching report.

## 7. Exploratory Data Analysis

The EDA was organized around the project's eight business questions.

### 7.1 Price competitiveness
For each matched product, compare Amazon and Flipkart current selling prices and identify the platform with the lower price or equal prices.

### 7.2 Typical price gap
Calculate the signed price difference and absolute price gap.

- **Signed price difference:** Amazon current price − Flipkart current price.
- **Absolute price gap:** Absolute value of the signed price difference.

A positive signed difference means Amazon is more expensive; a negative difference means Amazon is cheaper.

### 7.3 Largest product-level differences
Rank matched products by absolute price gap to identify the largest observed differences.

### 7.4 Brand-level pricing variation
Aggregate product-level signed price differences by brand to compare average observed gaps among brands in the matched sample.

### 7.5 Discount comparison
Discount analysis distinguishes between two populations:
- **Platform-level averages:** Calculate each platform's average using all non-missing discount values available for that platform. The current Power BI/EDA results show 13.8% for Amazon from 13 valid values and 24.5% for Flipkart from 12 valid values.
- **Paired comparison:** Use only products with non-missing discount percentages on both platforms. The documented paired subset contains 11 products.

These results should not be compared as if they use the same number of records. Missing discount values remain blank and are excluded from averages.

### 7.6 Rating and price relationship
Compare the rating of each matched listing with the platform offering the lower current price. Ratings are treated as contextual listing-level indicators, not definitive measures of quality.

### 7.7 Review volume
Compare review counts across platforms and use median review count to reduce the influence of highly skewed values. Review volume is a proxy for visible customer engagement, not a direct measure of sales.

### 7.8 Competitive opportunities
Identify products with large absolute price gaps and review the cheaper platform alongside available discount, rating, and availability information. These products are candidates for further investigation rather than automatic pricing recommendations.

**Output:** EDA notebook containing descriptive statistics, product-level comparisons, and business-question conclusions.

## 8. Power BI Data Model

The report uses a star-schema-style model with three tables:

### `DimProduct`
One row per matched product variant, with a product key, brand, standardized product name, RAM, and storage configuration where available.

### `DimPlatform`
One row per platform, identifying Amazon and Flipkart.

### `FactProductPlatform`
One row per product-platform combination, containing product and platform keys, current price, MRP, discount percentage, rating, review count, and availability.

Relationships:
- `DimProduct[ProductKey]` → `FactProductPlatform[ProductKey]` (one-to-many).
- `DimPlatform[PlatformKey]` → `FactProductPlatform[PlatformKey]` (one-to-many).

The dimension tables filter the fact table. With 16 matched variants and two platforms, the expected fact table grain is 32 rows, assuming one listing per product variant per platform.

## 9. Power BI Report Design

### Page 1 — Market Price Comparison
The first page provides the overview of matched products and pricing:
- Matched product count.
- Amazon and Flipkart average current prices.
- Average absolute price gap.
- Clustered price comparison by product.
- Average signed price difference by brand.
- Price-advantage breakdown.
- Brand and product slicers.

### Page 2 — Competitive Insights
The second page focuses on other marketplace signals:
- Amazon and Flipkart average listed discounts.
- Amazon and Flipkart average ratings.
- Average listed discount by platform.
- Average rating by platform.
- Median review count by platform.
- Top five products by absolute price gap, including the cheaper platform.
- Brand filter.

The report uses a consistent visual palette: navy `#23395B`, Amazon orange `#F59E0B`, Flipkart blue `#2874F0`, light blue `#DCEBFF`, and background `#F5F7FA`.

## 10. Data Quality and Interpretation Rules

- Missing MRP and discount values remain blank; they are not assumed to be zero.
- Platform-level discount averages use all valid discount values for each platform independently.
- Paired discount analysis uses only products with valid discounts on both platforms.
- A higher listed discount does not necessarily mean a lower current selling price.
- A positive signed price difference means Amazon is more expensive; a negative difference means Amazon is cheaper.
- Ratings and review counts are descriptive signals and should not be interpreted as direct measures of quality or sales.
- The report reflects a single collection date, and prices, discounts, ratings, review counts, and availability can change.

## 11. Limitations

- The analysis is based on one collection date, 7 October 2026.
- The raw sample contained 22 listings per platform, with 16 matched product variants.
- Some source fields, including MRP and discount percentages, were missing.
- Product matching depends on title normalization and configuration extraction; uncertain matches may remain unmatched.
- Marketplace page structures and scraping behavior may change.
- The sample is too small to generalize to all mobile listings or establish persistent platform-level pricing trends.

## 12. Reproducibility and Final Checks

Before publishing the repository:
1. Confirm the script filenames and run order match the actual project.
2. Confirm all CSV column names match the data dictionary.
3. Re-run validation, cleaning, standardization, matching, and EDA from the final raw data.
4. Confirm the discount averages and valid counts in EDA match the Power BI methodology.
5. Verify the Power BI model has the expected relationships and that slicers/navigation work.
6. Remove machine-specific absolute paths, credentials, cookies, and secrets.
7. Confirm the README and screenshots describe the final saved PBIX file.
8. Review website terms and only publish scraped data when redistribution is appropriate.

## 13. Summary

This methodology transforms scraped marketplace listings into a standardized, matched dataset and an interactive two-page Power BI report. The key analytical safeguard is comparing equivalent product variants and clearly distinguishing platform-level averages from paired product comparisons. The results provide a structured snapshot of cross-platform price differences while explicitly acknowledging missing data and the limits of a single-day sample.

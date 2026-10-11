# Mobile Price Intelligence & Cross-Platform Competitive Analysis

**Project type:** Data analytics portfolio project  
**Data collection date:** 7 October 2026  
**Marketplaces:** Amazon and Flipkart  
**Tools:** Python, Pandas, BeautifulSoup/requests (web scraping), Jupyter Notebook, Power BI  
**Primary deliverable:** Interactive two-page Power BI report

---

## 1. Executive Summary

This project compares mobile-phone listings on Amazon and Flipkart to understand how the current selling price, listed discount, customer rating, review count, and availability differ for equivalent product variants. Marketplace titles are not always consistent, and RAM/storage configurations can differ, so the analysis first standardizes product details and matches comparable variants before comparing prices.

The source data is a **single-day snapshot collected on 7 October 2026**. The analysis is useful for identifying pricing differences in the captured listings, but it does not establish long-term price trends or represent every mobile listing on either marketplace.

### Key findings from the captured sample

- **22 raw listings** were collected from Amazon and **22** from Flipkart.
- **16 product variants** were matched across the two platforms; six variants from each platform remained unmatched.
- Of the 16 matched variants, **Flipkart was cheaper for 11**, **Amazon was cheaper for 4**, and **one had the same price**.
- The average signed price difference (Amazon price minus Flipkart price) was approximately **₹6,243**. A positive value means Amazon was more expensive on average in the matched sample.
- The average absolute price gap was approximately **₹11,077**, while the median absolute gap was approximately **₹6,455**.
- Platform-level average listed discounts were **13.8% for Amazon** (13 valid values) and **24.5% for Flipkart** (12 valid values). These averages use all valid discount values available on each platform independently.
- Average listing ratings were approximately **4.29 for Amazon** and **4.45 for Flipkart**.
- Median review counts were **655 for Amazon** and **2,555 for Flipkart**.

These results describe the observed listings only. Prices, discounts, ratings, review counts, and availability can change over time.

## 2. Business Problem

Customers and e-commerce pricing teams may encounter different selling prices and listed discounts for the same mobile phone on Amazon and Flipkart. A direct comparison can be misleading when product titles use different wording or when listings refer to different RAM and storage configurations.

The business problem is:

> **How can equivalent mobile-phone variants listed on Amazon and Flipkart be compared consistently to identify observed price differences and potential competitive pricing opportunities?**

The project standardizes listing information, matches comparable product variants, analyzes price and marketplace signals, and presents the findings in Power BI.

## 3. Project Objectives

1. Collect mobile-phone listing data from Amazon and Flipkart.
2. Validate the structure and completeness of the raw datasets.
3. Clean numeric and text fields while preserving unknown values.
4. Standardize brand, product/model names, and RAM/storage configurations where possible.
5. Match equivalent product variants across the two marketplaces.
6. Analyze current selling prices, price gaps, listed discounts, ratings, and review counts.
7. Build an interactive Power BI report to communicate the results.
8. Identify products worth further pricing investigation without overstating conclusions from a small snapshot.

## 4. Business Questions

The analysis was organized around these eight questions:

1. Which platform is more price-competitive across comparable products?
2. What is the typical cross-platform price gap?
3. Which products have the largest pricing differences?
4. Which brands show the greatest pricing variation?
5. Do higher discounts translate into greater price competitiveness?
6. When one platform is cheaper, does it also have a lower customer rating?
7. Which platform has stronger customer engagement based on review volume?
8. Where are the biggest competitive pricing opportunities?

## 5. Data Collection and Scope

Python-based web scraping was used to collect mobile listing information from Amazon and Flipkart. Captured fields included listing title, brand, current selling price, MRP where available, listed discount percentage where available, rating, review count, availability, product URL, and scrape timestamp.

| Source | Raw rows | Raw columns | Schema validation |
|---|---:|---:|---|
| Amazon | 22 | 11 | Pass |
| Flipkart | 22 | 11 | Pass |

**Scope note:** The dataset contains one collection date, 7 October 2026. It is a snapshot, not a time series.

### Data files

The project workflow used separate raw and processed files. The expected project layout is:

```text
data/
├── raw/
│   ├── amazon_scraped_data.csv
│   └── flipkart_scraped_data.csv
└── processed/
    ├── amazon_cleaned.csv
    ├── flipkart_cleaned.csv
    ├── amazon_standardized.csv
    ├── flipkart_standardized.csv
    ├── final_mobile_price_comparison.csv
    ├── product_matching_report.csv
    └── final_mobile_price_comparison_eda.csv
```

Confirm these names against the final repository before publishing; filenames may differ in the working copy.

## 6. End-to-End Methodology

### Step 1 — Data validation

The raw files were checked for expected columns, row/column counts, and missing values. Both datasets passed the recorded schema checks. Missing values in fields such as MRP, discount, review count, and availability were identified for downstream handling.

### Step 2 — Data cleaning

The cleaning workflow prepared price, MRP, discount, rating, and review-count fields for analysis. Text-based values were parsed where necessary, and numeric fields were converted to appropriate types. Missing values were retained as unknown when the source did not provide reliable information.

**Important rule:** A missing MRP or discount is not equivalent to zero. Missing values were not filled with zero simply to make calculations possible.

### Step 3 — Product standardization

Brand and product/model text was normalized to reduce differences caused by capitalization and listing-title wording. RAM and ROM/storage capacities were extracted from product titles where possible. Configuration values were left missing when they could not be reliably identified.

Some iPhone titles did not provide reliable RAM values. For those products, matching relied on product identity and storage configuration rather than assuming an unknown RAM value.

### Step 4 — Cross-platform product matching

Equivalent product variants were matched using standardized brand, normalized product/model name, RAM where available, and storage/ROM configuration where available. Text normalization handled differences such as capitalization. Listings with different configurations were not forced into a match.

| Matching outcome | Variants |
|---|---:|
| Matched product variants | 16 |
| Unmatched Amazon variants | 6 |
| Unmatched Flipkart variants | 6 |

The final comparison dataset contains **16 matched product variants**. The unmatched records are documented separately in the product matching report.

### Step 5 — Exploratory data analysis (EDA)

The EDA notebook answers the eight business questions using descriptive statistics and product-level comparisons. It examines price differences, absolute gaps, brand-level variation, discounts, ratings, review counts, and potential pricing opportunities.

### Step 6 — Power BI reporting

The matched comparison data was modeled in Power BI and used to build a two-page report. The report provides high-level pricing comparisons on Page 1 and supporting competitive signals on Page 2.

## 7. Metric Definitions and Interpretation

### Price metrics

- **Signed price difference:** `Amazon Current Price − Flipkart Current Price`
- **Absolute price gap:** `ABS(Amazon Current Price − Flipkart Current Price)`
- **Positive signed difference:** Amazon's listed price is higher.
- **Negative signed difference:** Amazon's listed price is lower.
- **Zero signed difference:** The captured prices are equal.

The average signed difference was approximately ₹6,243. The mean absolute price gap was approximately ₹11,077, and the median absolute gap was approximately ₹6,455. The signed average indicates direction; the absolute measures show the size of the gap without regard to which platform is cheaper.

### Platform price advantage

Among the 16 matched variants:

| Price outcome | Product variants |
|---|---:|
| Flipkart cheaper | 11 |
| Amazon cheaper | 4 |
| Same price | 1 |

This describes the captured matched sample only and should not be generalized to the entire marketplace catalog.

### Largest observed price gaps

The EDA identified examples of substantial price differences, including:

| Product | Observed difference |
|---|---:|
| Samsung Galaxy Z Fold6 | Flipkart cheaper by ₹51,099 |
| Samsung Galaxy Z Flip6 | Amazon cheaper by ₹29,501 |
| Samsung Galaxy A35 | Flipkart cheaper by ₹19,000 |
| Apple iPhone 16 | Flipkart cheaper by ₹17,000 |
| Xiaomi 14 Civi | Flipkart cheaper by ₹15,401 |
| Apple iPhone 17e | Flipkart cheaper by ₹15,000 |

These are observed listing differences in the collected snapshot. Before acting on any unusually large gap, verify that the listings refer to the same exact variant and that price, seller, condition, and other listing details are comparable.

### Discount metrics

Two discount comparisons must be distinguished:

1. **Platform-level averages:** Each platform's average is calculated independently from all non-missing discount values available for that platform. The current results are Amazon **13.8%** from **13 valid values** and Flipkart **24.5%** from **12 valid values**.
2. **Paired product comparison:** To compare discounts for the same products, only products with a valid discount on both platforms are included. The documented paired subset contains **11 products**.

Because these calculations use different populations, the platform-level averages should not be described as a paired comparison. Missing discounts remain blank and are excluded from averages. A higher listed discount does not necessarily mean a lower current selling price.

### Rating and review-volume metrics

- Average listing rating: approximately **4.29 for Amazon** and **4.45 for Flipkart**.
- Median review count: **655 for Amazon** and **2,555 for Flipkart**.
- In the product-level rating comparison, the cheaper platform had the higher rating for 8 products, both platforms had the same rating for 4 products, and the cheaper platform had the lower rating for 4 products.
- Flipkart had a higher review count for 14 matched products, while Amazon had a higher review count for 2.

Ratings and review counts are contextual listing-level signals. Review volume is not a direct measure of sales, and ratings alone do not establish product quality.

## 8. Power BI Data Model

The report uses a three-table, star-schema-style model.

### `DimProduct`

One row per matched product variant. It contains `ProductKey`, brand, standardized product name, RAM, and storage configuration where available.

### `DimPlatform`

One row per marketplace: Amazon or Flipkart. It contains `PlatformKey` and `PlatformName`.

### `FactProductPlatform`

One row per product-platform listing, containing the product and platform keys plus current price, MRP, discount percentage, rating, review count, and availability.

### Relationships

- `DimProduct[ProductKey]` — one-to-many — `FactProductPlatform[ProductKey]`
- `DimPlatform[PlatformKey]` — one-to-many — `FactProductPlatform[PlatformKey]`

Both dimension tables filter the fact table. With 16 matched variants and two platforms, the expected fact-table grain is 32 rows if each matched variant has one listing on each platform.

## 9. Power BI Dashboard

### Page 1 — Market Price Comparison

The first page gives an overview of price competitiveness:

- Matched product count.
- Average current price on Amazon and Flipkart.
- Average absolute price gap.
- Product-level clustered price comparison.
- Average signed price difference by brand.
- Price-advantage donut chart.
- Brand and product slicers.

### Page 2 — Competitive Insights

The second page provides context beyond price:

- Average listed discount for Amazon and Flipkart.
- Average rating for Amazon and Flipkart.
- Average discount by platform.
- Average rating by platform.
- Median review count by platform.
- Top five products by absolute price gap, with cheaper platform.
- Brand slicer.

### Visual theme

| Use | Color |
|---|---|
| Navy | `#23395B` |
| Amazon orange | `#F59E0B` |
| Flipkart blue | `#2874F0` |
| Light blue | `#DCEBFF` |
| Background | `#F5F7FA` |

## 10. Business Interpretation and Recommendations

Based on this snapshot, the following actions are reasonable next steps for a pricing or marketplace analyst:

1. **Investigate large price gaps first.** Recheck the largest-gap products to confirm the exact model and RAM/storage variant match before drawing conclusions.
2. **Compare selling price as well as listed discount.** A larger discount percentage does not automatically make a product cheaper than the competitor.
3. **Use rating and review volume as context.** These metrics can help frame a comparison, but they should not be treated as direct sales or product-quality measures.
4. **Review missing listing information.** Missing MRP or discount fields reduce the number of products available for discount comparisons.
5. **Collect repeated snapshots before analyzing trends.** Repeated collection over several dates would help distinguish temporary price changes from persistent patterns.
6. **Expand the sample.** More product categories, brands, and matched variants would improve coverage and make the findings more representative.

These are investigation priorities, not definitive pricing recommendations, because the current dataset is small and covers one date only.

## 11. Data Quality Notes and Limitations

- The analysis uses 22 raw listings per platform and 16 matched product variants.
- It represents a single-day snapshot collected on 7 October 2026.
- Some MRP, discount, review-count, and availability values were missing in the source data.
- Product matching depends on title normalization and configuration extraction; uncertain listings may remain unmatched.
- The data validation output and cleaning summary previously recorded different Amazon missing-discount counts. Reconcile this count against the final raw and cleaned CSV files before publishing a definitive missing-value table.
- Marketplace prices, discounts, ratings, review counts, availability, and page structures can change.
- The sample is too small to generalize to all mobile listings or establish persistent platform-level pricing trends.
- Scraped data should only be redistributed where permitted; credentials, cookies, and other secrets must not be committed to the repository.

## 12. Reproducibility Checklist

Before publishing the GitHub repository:

- [ ] Confirm script filenames and execution order match the actual project.
- [ ] Confirm all CSV column names match the data dictionary.
- [ ] Re-run validation, cleaning, standardization, matching, and EDA from the final raw data.
- [ ] Reconcile the Amazon missing-discount count between validation and cleaning outputs.
- [ ] Confirm the 13.8% Amazon and 24.5% Flipkart discount averages use the documented independent platform-level method.
- [ ] Confirm paired discount comparison uses only the 11 products with discounts available on both platforms.
- [ ] Confirm Power BI relationships and measures are correct.
- [ ] Test slicers, page navigation, and visual formatting.
- [ ] Ensure screenshots and README match the final saved Power BI report.
- [ ] Remove machine-specific absolute paths, credentials, cookies, and secrets.
- [ ] Review website terms and data redistribution restrictions before committing scraped records.

## 13. Conclusion

This project demonstrates an end-to-end analytics workflow: collecting marketplace data, validating and cleaning it, standardizing product attributes, matching equivalent variants, analyzing cross-platform pricing, and communicating findings in Power BI. Its main strength is the focus on comparable product configurations and transparent treatment of missing values. The results suggest that Flipkart was cheaper for more of the matched products in this snapshot, while several products showed substantial price gaps worth verifying. Additional data collection across more products and dates would be required to determine whether these patterns persist.

---

**Related documentation:** `business_problem.md`, `data_dictionary.md`, and `methodology.md`.

# Mobile Price Intelligence & Cross-Platform Competitive Analysis

A data analytics portfolio project that compares mobile-phone listings on **Amazon and Flipkart** to understand cross-platform price differences, listed discounts, customer ratings, and review volume.

> **Data snapshot:** 7 October 2026  
> **Tools:** Python, Pandas, BeautifulSoup/web scraping, Jupyter Notebook, Power BI

## Business Problem

The same mobile phone can be listed at different prices on different e-commerce platforms. However, product titles and RAM/storage configurations may vary, so comparing listings without standardization can produce misleading results.

This project cleans and standardizes scraped mobile listings, matches equivalent product variants across Amazon and Flipkart, and analyzes the observed differences to support competitive-pricing decisions.

## Project Objectives

- Collect mobile-phone listing data from Amazon and Flipkart.
- Validate source schemas and identify missing or inconsistent values.
- Clean prices, discounts, ratings, review counts, and other relevant fields.
- Standardize brands, product names, and RAM/storage configurations.
- Match equivalent product variants across the two platforms.
- Analyze price gaps, discounts, ratings, and review volume.
- Present the findings in an interactive Power BI report.

## Key Findings

The following findings describe the captured sample only; they should not be interpreted as long-term marketplace trends.

- **44 raw listings** were collected: 22 from Amazon and 22 from Flipkart.
- **16 product variants** were matched across both platforms; 6 listings per platform remained unmatched in the matching report.
- Among the 16 matched variants, **Flipkart was cheaper for 11**, **Amazon was cheaper for 4**, and **1 had the same price**.
- The mean signed price gap (Amazon price − Flipkart price) was approximately **₹6,243**; the mean absolute price gap was approximately **₹11,077**.
- Average listed discount was **13.8% for Amazon** (13 valid values) and **24.5% for Flipkart** (12 valid values), calculated separately using each platform's available non-missing values.
- Average rating measures were approximately **4.29 for Amazon** and **4.45 for Flipkart**.
- Median review counts were **655 for Amazon** and **2,555 for Flipkart**.

**Important interpretation note:** Discount averages use all valid values available on each platform. For an apples-to-apples paired discount comparison, use only the 11 matched products with a valid discount on both platforms. Missing discounts are treated as unknown, not as zero.

## Business Questions

1. Which platform is more price-competitive across comparable products?
2. What is the typical cross-platform price gap?
3. Which products have the largest pricing differences?
4. Which brands show the greatest pricing variation?
5. Do higher discounts translate into greater price competitiveness?
6. When one platform is cheaper, does it also have a lower customer rating?
7. Which platform has stronger customer engagement based on review volume?
8. Where are the biggest competitive pricing opportunities?

## Power BI Dashboard

### Page 1 — Market Price Comparison

- Matched product count and platform average prices
- Average absolute price gap
- Amazon versus Flipkart price comparison by product
- Average signed price difference by brand
- Product price-advantage breakdown
- Brand and product slicers

![Market Price Comparison dashboard](images/01_market_price_comparison.png)

### Page 2 — Competitive Insights

- Average listed discount by platform
- Average customer rating by platform
- Median review count by platform
- Top five products by absolute price gap
- Brand slicer

![Competitive Insights dashboard](images/02_competitive_insights.png)

> Add the two dashboard screenshots to the repository at the paths shown above. If you use different filenames or folders, update these links.

## Methodology

1. **Data collection:** Scraped mobile listings from Amazon and Flipkart on 7 October 2026.
2. **Data validation:** Checked dataset schemas, row counts, and missing values.
3. **Data cleaning:** Converted fields to appropriate types and preserved unavailable values as null rather than replacing them with zero.
4. **Product standardization:** Normalized brand and product naming and extracted RAM/storage configuration where possible.
5. **Product matching:** Matched equivalent variants using standardized product attributes and configuration details. Where RAM was not available for iPhones, matching relied on product name and storage capacity.
6. **EDA:** Analyzed pricing differences, discounts, ratings, review counts, and competitive opportunities.
7. **Power BI reporting:** Built a two-page report to communicate the results.
8. **Recommendations:** Identified products worth further price investigation and documented the limits of the snapshot.

See [`methodology.md`](methodology.md) for the detailed workflow, metric definitions, data quality notes, and reproducibility checks. See [`business_problem.md`](business_problem.md) for the business framing and [`data_dictionary.md`](data_dictionary.md) for field descriptions.

## Repository Structure

Update this example to match the exact files and folders you publish to GitHub.

```text
mobile-price-intelligence/
├── data/
│   ├── raw/
│   │   ├── amazon_scraped_data.csv
│   │   ├── amazon_scraped_data.json
│   │   └── flipkart_scraped_data.csv
│   ├── processed/
│   │   ├── amazon_cleaned.csv
│   │   ├── amazon_standardized.csv
│   │   ├── flipkart_cleaned.csv
│   │   ├── flipkart_standardized.csv
│   │   ├── final_mobile_price_comparison.csv
│   │   ├── final_mobile_price_comparison_eda.csv
│   │   └── product_matching_report.csv
│   └── .gitkeep
├── docs/
│   ├── Project_Documentation.md
│   ├── business_problem.md
│   ├── data_dictionary.md
│   └── methodology.md
├── images/
│   ├── 01_market_price_comparison.png
│   └── 02_competitive_insights.png
├── notebooks/
│   └── mobile_price_eda.ipynb
├── powerbi/
│   └── mobile_price_intelligence.pbix
├── python/
│   ├── 01_amazon_scraper.py
│   ├── 02_flipkart_scraper.py
│   ├── 03_validate_data.py
│   ├── 04_clean_data.py
│   ├── 05_standardize_products.py
│   ├── 06_product_matching.py
│   └── __init__.py
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

Only include files that actually exist in your repository. Avoid committing generated or raw data if website terms or redistribution restrictions do not permit it.

## Run the Project

### 1. Clone the repository

```bash
git clone <your-github-repository-url>
cd mobile-price-intelligence
```


### 2. Install dependencies

If `requirements.txt` is present:

```bash
pip install -r requirements.txt
```

If you do not have a requirements file yet, create one from the packages actually used by your scripts and notebook. Do not add guessed dependencies.

### 3. Run the analysis

Run the Python pipeline scripts in their documented order, then open `notebooks/mobile_price_eda.ipynb` in Jupyter Notebook or JupyterLab. Use the paths configured in the scripts, and confirm that the required input CSV files are available.

### 4. Open the dashboard

Open `powerbi/mobile_price_intelligence.pbix` in Power BI Desktop. The report uses a product dimension, a platform dimension, and a product-platform fact table.

## Metric Definitions

- **Signed price difference:** Amazon current price − Flipkart current price. A positive value means Amazon is more expensive; a negative value means Amazon is cheaper.
- **Absolute price gap:** Absolute value of the signed price difference.
- **Platform-level average discount:** Mean of the non-missing discount values available for that platform.
- **Paired discount comparison:** Compares only matched products with non-missing discount values on both platforms.
- **Median review count:** Median review count for a platform, reducing the influence of unusually large review counts.

## Limitations

- This is a **single-day snapshot**, not a time-series study.
- The matched sample contains only 16 product variants.
- Some MRP and discount values are missing; this limits the products included in discount comparisons.
- Matching accuracy depends on product-title standardization and configuration extraction.
- Prices, discounts, ratings, and availability may change after collection.
- A larger listed discount does not necessarily mean a lower final selling price.
- Scraping methods may need maintenance when website structures change.

## Recommendations

- Investigate products with the largest observed absolute price gaps.
- Compare actual selling prices in addition to listed discounts.
- Use ratings and review counts as context, not as proof of product quality or customer satisfaction.
- Collect repeated snapshots before making claims about price trends or volatility.
- Expand the product sample and monitor the percentage of listings that can be matched reliably.

## Documentation

- [`Project_Documentation.md`](Project_Documentation.md) — full project narrative, findings, model, dashboard, and limitations.
- [`business_problem.md`](business_problem.md) — business problem, objectives, and questions.
- [`data_dictionary.md`](data_dictionary.md) — descriptions of dataset fields and model fields.
- [`methodology.md`](methodology.md) — detailed workflow, metric definitions, and validation notes.

## Responsible Use

Respect the applicable website terms and access restrictions. Do not commit passwords, API keys, cookies, session tokens, or other secrets. Publish scraped data only when redistribution is appropriate; otherwise, share schemas, permitted sample data, and instructions for reproducing the collection process.

## Future Work

1. Collect price data regularly to analyze price trends over time.
2. Expand the dataset to include more mobile models and brands.
3. Improve product matching to handle differences in product titles and configurations.
4. Add more e-commerce platforms for broader price comparisons.
5. Automate data collection, validation, and dashboard refreshes.

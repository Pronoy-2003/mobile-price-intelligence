# Business Problem — Mobile Price Intelligence

## Business Problem Statement

The same mobile phone can be listed at different selling prices across Amazon and Flipkart. However, differences in product titles, RAM/storage configurations, listed discounts, customer ratings, and review counts can make direct comparisons unreliable.

This project builds a data analytics workflow to compare **equivalent mobile product variants** across both platforms. The analysis focuses on current selling prices, price gaps, listed discounts, customer ratings, and review volume to identify where each platform is more price-competitive and where notable pricing differences exist.

The analysis uses a **single-day data snapshot collected on 7 October 2026**. The results describe the listings captured on that date and should not be interpreted as long-term pricing trends.

## Project Objective

To collect, validate, clean, standardize, and match mobile listings from Amazon and Flipkart, then analyze cross-platform pricing and related listing metrics using Python and Power BI.

## Final Business Questions

### Business Question 1: Which platform is more price-competitive across comparable products?

Compare current selling prices for matched product variants to determine how often Amazon or Flipkart offers the lower price, and how many products have the same price.

### Business Question 2: What is the typical cross-platform price gap?

Measure the signed price difference and absolute price gap across matched products to understand the direction and typical magnitude of price differences.

**Metric definitions**
- **Signed price difference:** Amazon current price − Flipkart current price. A positive value means Amazon is more expensive; a negative value means Amazon is cheaper.
- **Absolute price gap:** The absolute value of the signed price difference, regardless of which platform is cheaper.

### Business Question 3: Which products have the largest pricing differences?

Rank matched product variants by absolute price gap to identify the products with the largest observed differences in current selling price.

### Business Question 4: Which brands show the greatest pricing variation?

Aggregate product-level price differences by brand to compare the observed cross-platform pricing gap among brands represented in the matched dataset.

### Business Question 5: Do higher discounts translate into greater price competitiveness?

Compare listed discount percentages across platforms and examine whether the platform offering the higher listed discount also has the lower current selling price. Discount availability can differ between platforms, so platform-level averages and same-product paired comparisons must be clearly distinguished.

### Business Question 6: When one platform is cheaper, does it also have a lower customer rating?

Compare customer ratings for matched product variants and assess whether the lower-priced listing tends to have a lower, similar, or higher rating. Ratings are contextual listing indicators and do not by themselves establish product quality.

### Business Question 7: Which platform has stronger customer engagement based on review volume?

Compare review counts for matched listings, using median review count to reduce the influence of highly skewed counts. Review volume is used as a proxy for visible customer engagement, not as a direct measure of sales.

### Business Question 8: Where are the biggest competitive pricing opportunities?

Combine the size of the price gap with the cheaper platform and available listing context—such as ratings, discounts, and availability where captured—to highlight products that may warrant further pricing review.

## Project Scope

### Included
- Mobile listings collected from Amazon and Flipkart.
- Data validation and missing-value assessment.
- Data cleaning and numeric conversion.
- Standardization of brand, product name, and RAM/storage configuration where available.
- Matching equivalent product variants across platforms.
- Exploratory data analysis for the eight business questions.
- A two-page Power BI report:
  - **Page 1 — Market Price Comparison**
  - **Page 2 — Competitive Insights**

### Out of Scope
- Claiming that the results represent every mobile listing on either marketplace.
- Drawing conclusions about long-term pricing trends from one collection date.
- Treating listed discounts as proof that a platform has the lowest final selling price.
- Treating review count as a direct sales or revenue measure.
- Making recommendations that assume prices or availability remain unchanged after collection.

## Intended Business Value

The project demonstrates how web-scraped marketplace data can be transformed into a structured comparison dataset and an interactive report. It can help an analyst identify observed price differences, compare discounts and customer feedback signals, and prioritize products for further investigation.

Because the sample is small and based on one day of collection, any business action should be validated with a larger dataset and repeated observations over time.

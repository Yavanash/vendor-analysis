# Data Audit Report
**D2C Fashion Customer Intelligence Project**

**Date:** 2026-08-27
**Analyst:** Analytics Engineering Team
**Source:** `Raw_Data/Dataset.csv`

---

## Executive Summary

This audit examines a dataset of **3,900 records** with **18 variables** representing customer transactions from a D2C fashion retailer.

**Key Findings:**
- Dataset grain: One row per customer (customer-level)
- Unique customers: 3,900
- Data quality: Good overall quality
- Semantic duplications: Yes
- Missing values: 37 (0.05% of all values)

---

## 1. Dataset Profile

### Basic Metrics
| Metric | Value |
|--------|-------|
| Number of rows | 3,900 |
| Number of columns | 18 |
| Unique Customer IDs | 3,900 |
| Customer ID is unique | True |
| **Dataset grain** | **One row per customer (customer-level)** |

### Column List
1. Customer ID
2. Age
3. Gender
4. Item Purchased
5. Category
6. Purchase Amount (USD)
7. Location
8. Size
9. Color
10. Season
11. Review Rating
12. Subscription Status
13. Shipping Type
14. Discount Applied
15. Promo Code Used
16. Previous Purchases
17. Payment Method
18. Frequency of Purchases

---

## 2. Data Types

| Column | Data Type | Non-Null Count | Null Count |
|--------|-----------|----------------|------------|
| Customer ID | int64 | 3,900 | 0 |
| Age | int64 | 3,900 | 0 |
| Gender | str | 3,900 | 0 |
| Item Purchased | str | 3,900 | 0 |
| Category | str | 3,900 | 0 |
| Purchase Amount (USD) | int64 | 3,900 | 0 |
| Location | str | 3,900 | 0 |
| Size | str | 3,900 | 0 |
| Color | str | 3,900 | 0 |
| Season | str | 3,900 | 0 |
| Review Rating | float64 | 3,863 | 37 |
| Subscription Status | str | 3,900 | 0 |
| Shipping Type | str | 3,900 | 0 |
| Discount Applied | str | 3,900 | 0 |
| Promo Code Used | str | 3,900 | 0 |
| Previous Purchases | int64 | 3,900 | 0 |
| Payment Method | str | 3,900 | 0 |
| Frequency of Purchases | str | 3,900 | 0 |

---

## 3. Missing Values Analysis

| Column | Missing Count | Missing % |
|--------|---------------|----------|
| Review Rating | 37 | 0.95% |

**Impact Assessment:**
- **Review Rating**: 37 missing (0.95%). May indicate not all customers leave reviews. Consider this bias in satisfaction analysis.

---

## 4. Duplicate Records

- **Full duplicate rows:** 0
- **Duplicate Customer IDs:** 0

**Interpretation:** Each row represents a unique customer.

---

## 5. Categorical Variables


### Gender
**Unique values:** 2

| Value | Count | % |
|-------|-------|---|
| Male | 2,652 | 68.0% |
| Female | 1,248 | 32.0% |

### Item Purchased
**Unique values:** 25

| Value | Count | % |
|-------|-------|---|
| Blouse | 171 | 4.4% |
| Pants | 171 | 4.4% |
| Jewelry | 171 | 4.4% |
| Shirt | 169 | 4.3% |
| Dress | 166 | 4.3% |
| Sweater | 164 | 4.2% |
| Jacket | 163 | 4.2% |
| Coat | 161 | 4.1% |
| Sunglasses | 161 | 4.1% |
| Belt | 161 | 4.1% |
| Sandals | 160 | 4.1% |
| Socks | 159 | 4.1% |
| Skirt | 158 | 4.1% |
| Shorts | 157 | 4.0% |
| Scarf | 157 | 4.0% |
| Hat | 154 | 3.9% |
| Handbag | 153 | 3.9% |
| Hoodie | 151 | 3.9% |
| Shoes | 150 | 3.8% |
| T-shirt | 147 | 3.8% |
| Sneakers | 145 | 3.7% |
| Boots | 144 | 3.7% |
| Backpack | 143 | 3.7% |
| Gloves | 140 | 3.6% |
| Jeans | 124 | 3.2% |

### Category
**Unique values:** 4

| Value | Count | % |
|-------|-------|---|
| Clothing | 1,737 | 44.5% |
| Accessories | 1,240 | 31.8% |
| Footwear | 599 | 15.4% |
| Outerwear | 324 | 8.3% |

### Location
**Unique values:** 50

| Value | Count | % |
|-------|-------|---|
| Montana | 96 | 2.5% |
| California | 95 | 2.4% |
| Idaho | 93 | 2.4% |
| Illinois | 92 | 2.4% |
| Alabama | 89 | 2.3% |
| Minnesota | 88 | 2.3% |
| New York | 87 | 2.2% |
| Nevada | 87 | 2.2% |
| Nebraska | 87 | 2.2% |
| Delaware | 86 | 2.2% |
| Maryland | 86 | 2.2% |
| Vermont | 85 | 2.2% |
| Louisiana | 84 | 2.2% |
| North Dakota | 83 | 2.1% |
| West Virginia | 81 | 2.1% |
| Missouri | 81 | 2.1% |
| New Mexico | 81 | 2.1% |
| Mississippi | 80 | 2.1% |
| Kentucky | 79 | 2.0% |
| Arkansas | 79 | 2.0% |
| Indiana | 79 | 2.0% |
| Georgia | 79 | 2.0% |
| North Carolina | 78 | 2.0% |
| Connecticut | 78 | 2.0% |
| Maine | 77 | 2.0% |
| Texas | 77 | 2.0% |
| Tennessee | 77 | 2.0% |
| Ohio | 77 | 2.0% |
| Virginia | 77 | 2.0% |
| South Carolina | 76 | 1.9% |
| Oklahoma | 75 | 1.9% |
| Colorado | 75 | 1.9% |
| Wisconsin | 75 | 1.9% |
| Oregon | 74 | 1.9% |
| Pennsylvania | 74 | 1.9% |
| Washington | 73 | 1.9% |
| Michigan | 73 | 1.9% |
| Massachusetts | 72 | 1.8% |
| Alaska | 72 | 1.8% |
| Wyoming | 71 | 1.8% |
| New Hampshire | 71 | 1.8% |
| Utah | 71 | 1.8% |
| South Dakota | 70 | 1.8% |
| Iowa | 69 | 1.8% |
| Florida | 68 | 1.7% |
| New Jersey | 67 | 1.7% |
| Hawaii | 65 | 1.7% |
| Arizona | 65 | 1.7% |
| Rhode Island | 63 | 1.6% |
| Kansas | 63 | 1.6% |

### Size
**Unique values:** 4

| Value | Count | % |
|-------|-------|---|
| M | 1,755 | 45.0% |
| L | 1,053 | 27.0% |
| S | 663 | 17.0% |
| XL | 429 | 11.0% |

### Color
**Unique values:** 25

| Value | Count | % |
|-------|-------|---|
| Olive | 177 | 4.5% |
| Yellow | 174 | 4.5% |
| Silver | 173 | 4.4% |
| Teal | 172 | 4.4% |
| Green | 169 | 4.3% |
| Black | 167 | 4.3% |
| Violet | 166 | 4.3% |
| Cyan | 166 | 4.3% |
| Gray | 159 | 4.1% |
| Maroon | 158 | 4.1% |
| Orange | 154 | 3.9% |
| Charcoal | 153 | 3.9% |
| Pink | 153 | 3.9% |
| Magenta | 152 | 3.9% |
| Blue | 152 | 3.9% |
| Purple | 151 | 3.9% |
| Peach | 149 | 3.8% |
| Red | 148 | 3.8% |
| Lavender | 147 | 3.8% |
| Beige | 147 | 3.8% |
| Indigo | 147 | 3.8% |
| Turquoise | 145 | 3.7% |
| White | 142 | 3.6% |
| Brown | 141 | 3.6% |
| Gold | 138 | 3.5% |

### Season
**Unique values:** 4

| Value | Count | % |
|-------|-------|---|
| Spring | 999 | 25.6% |
| Fall | 975 | 25.0% |
| Winter | 971 | 24.9% |
| Summer | 955 | 24.5% |

### Subscription Status
**Unique values:** 2

| Value | Count | % |
|-------|-------|---|
| No | 2,847 | 73.0% |
| Yes | 1,053 | 27.0% |

### Shipping Type
**Unique values:** 6

| Value | Count | % |
|-------|-------|---|
| Free Shipping | 675 | 17.3% |
| Standard | 654 | 16.8% |
| Store Pickup | 650 | 16.7% |
| Next Day Air | 648 | 16.6% |
| Express | 646 | 16.6% |
| 2-Day Shipping | 627 | 16.1% |

### Discount Applied
**Unique values:** 2

| Value | Count | % |
|-------|-------|---|
| No | 2,223 | 57.0% |
| Yes | 1,677 | 43.0% |

### Promo Code Used
**Unique values:** 2

| Value | Count | % |
|-------|-------|---|
| No | 2,223 | 57.0% |
| Yes | 1,677 | 43.0% |

### Payment Method
**Unique values:** 6

| Value | Count | % |
|-------|-------|---|
| PayPal | 677 | 17.4% |
| Credit Card | 671 | 17.2% |
| Cash | 670 | 17.2% |
| Debit Card | 636 | 16.3% |
| Venmo | 634 | 16.3% |
| Bank Transfer | 612 | 15.7% |

### Frequency of Purchases
**Unique values:** 7

| Value | Count | % |
|-------|-------|---|
| Every 3 Months | 584 | 15.0% |
| Annually | 572 | 14.7% |
| Quarterly | 563 | 14.4% |
| Monthly | 553 | 14.2% |
| Bi-Weekly | 547 | 14.0% |
| Fortnightly | 542 | 13.9% |
| Weekly | 539 | 13.8% |

---

## 6. Numeric Variables


### Customer ID

| Statistic | Value |
|-----------|-------|
| Count | 3900 |
| Mean | 1950.50 |
| Std Dev | 1125.98 |
| Min | 1.00 |
| 25th percentile | 975.75 |
| Median | 1950.50 |
| 75th percentile | 2925.25 |
| Max | 3900.00 |

### Age

| Statistic | Value |
|-----------|-------|
| Count | 3900 |
| Mean | 44.07 |
| Std Dev | 15.21 |
| Min | 18.00 |
| 25th percentile | 31.00 |
| Median | 44.00 |
| 75th percentile | 57.00 |
| Max | 70.00 |

### Purchase Amount (USD)

| Statistic | Value |
|-----------|-------|
| Count | 3900 |
| Mean | 59.76 |
| Std Dev | 23.69 |
| Min | 20.00 |
| 25th percentile | 39.00 |
| Median | 60.00 |
| 75th percentile | 81.00 |
| Max | 100.00 |

### Review Rating

| Statistic | Value |
|-----------|-------|
| Count | 3863 |
| Mean | 3.75 |
| Std Dev | 0.72 |
| Min | 2.50 |
| 25th percentile | 3.10 |
| Median | 3.80 |
| 75th percentile | 4.40 |
| Max | 5.00 |

### Previous Purchases

| Statistic | Value |
|-----------|-------|
| Count | 3900 |
| Mean | 25.35 |
| Std Dev | 14.45 |
| Min | 1.00 |
| 25th percentile | 13.00 |
| Median | 25.00 |
| 75th percentile | 38.00 |
| Max | 50.00 |

---

## 7. Semantic Duplication Analysis

### Investigation 1: Discount Applied vs Promo Code Used

**Matching records:** 3,900 (100.0%)  
**Mismatching records:** 0 (0.0%)  

⚠️ **FINDING:** These fields are perfectly correlated. They appear to represent the same information.

**Implication:** One field may be redundant unless they represent conceptually different things (offer received vs offer used).

### Investigation 2: Quarterly vs Every 3 Months

- **'Quarterly':** 563 records
- **'Every 3 Months':** 584 records

⚠️ **FINDING:** Semantic duplication detected. These represent identical frequencies.

**Recommendation:** Normalize to 'Quarterly' before analysis.

### Investigation 3: Bi-Weekly vs Fortnightly

- **'Bi-Weekly':** 547 records
- **'Fortnightly':** 542 records

⚠️ **FINDING:** Semantic duplication detected. These represent identical frequencies.

**Recommendation:** Normalize to 'Bi-Weekly' before analysis.

---

## 8. Data Quality Issues

✓ **No major data quality issues detected.**

---

## 9. Fields Requiring Normalization


**Frequency of Purchases**
- Issue: Quarterly vs Every 3 Months
- Recommended action: Standardize to single term (recommend: Quarterly)

**Frequency of Purchases**
- Issue: Bi-Weekly vs Fortnightly
- Recommended action: Standardize to single term (recommend: Bi-Weekly)

**Discount Applied / Promo Code Used**
- Issue: Perfectly correlated - appears to be duplicate information
- Recommended action: Evaluate if one field can be removed or if they represent different concepts

---

## 10. Analytical Capability Mapping

### Customer Value Analysis
**Available variables:**
- Purchase Amount (USD) - transaction value
- Previous Purchases - historical transaction count
- Frequency of Purchases - stated purchase cadence
- Subscription Status - recurring relationship indicator

### Loyalty Proxies
**Available variables:**
- Previous Purchases - engagement depth
- Frequency of Purchases - purchase regularity
- Subscription Status - commitment indicator
- Review Rating - satisfaction/engagement proxy

### Promotional Exposure Analysis
**Available variables:**
- Discount Applied - promotional offer received
- Promo Code Used - promotional offer utilized

### Satisfaction Analysis
**Available variables:**
- Review Rating - explicit satisfaction measure

### Geography Analysis
**Available variables:**
- Location - state-level geography

### Category Analysis
**Available variables:**
- Category - product category
- Item Purchased - specific item
- Size - product size
- Color - product color
- Season - seasonal attribution

### Fulfillment Analysis
**Available variables:**
- Shipping Type - delivery method preference

### Payment Analysis
**Available variables:**
- Payment Method - payment type

### Demographic Analysis
**Available variables:**
- Age - customer age
- Gender - customer gender

---

## 11. Analytical Limitations

**Critical limitations that constrain analysis:**

1. **TEMPORAL:** No transaction date - cannot analyze trends over time
2. **TEMPORAL:** Cannot determine recency of purchases
3. **TEMPORAL:** Cannot calculate time between purchases
4. **TEMPORAL:** Cannot perform cohort analysis
5. **TEMPORAL:** Frequency of Purchases is stated preference, not observed behavior
6. **FINANCIAL:** No cost/margin data - cannot calculate profitability
7. **FINANCIAL:** Cannot separate discount amount from base price
8. **BEHAVIORAL:** Previous Purchases is a count only - no detail on what was purchased
9. **BEHAVIORAL:** No cart/browse data - cannot analyze conversion
10. **CAUSAL:** Cannot establish causation between discount and purchase
11. **CAUSAL:** Cannot determine if subscription drives higher spend or vice versa
12. **GRANULARITY:** Location is state-level only - cannot analyze by city/region
13. **GRANULARITY:** Season may be purchase season or product season (ambiguous)

---

## 12. Questions That CANNOT Be Legitimately Answered

These questions require data not present in the dataset:

1. What is customer lifetime value? (no time dimension or future projection capability)
2. Are customers becoming more or less engaged over time? (no dates)
3. What is the customer churn rate? (no dates, no way to define churn window)
4. How long does it take customers to make a repeat purchase? (no dates)
5. What is the year-over-year growth? (no dates)
6. Which marketing campaign drove the most sales? (no campaign identifier)
7. What is the return/refund rate? (no return data)
8. What is the customer acquisition cost efficiency? (no cost data)
9. What is the profit margin by customer? (no cost data)
10. Did discounts cause increased purchase amounts? (correlation ≠ causation, no experiment)
11. Will subscription customers spend more in the future? (no predictive features)
12. Why do customers choose specific payment methods? (no survey/preference data)
13. What is the impact of shipping type on satisfaction? (confounded by many factors)
14. Which product categories are growing? (no time dimension)
15. What is the customer journey? (single snapshot per customer)

---

## 13. Analytical Opportunities

Despite limitations, this dataset enables:

1. **Descriptive profiling** of customer purchase behavior
2. **Segmentation** by demographics, purchase patterns, and product preferences
3. **Association analysis** between variables (not causation)
4. **Distribution analysis** of purchase amounts, ratings, and frequencies
5. **Geographic distribution** analysis at state level
6. **Product category** performance comparison
7. **Correlation analysis** between customer characteristics and purchase behavior
8. **Promotional exposure** association with purchase patterns

---

## 14. Recommended Next Steps

1. **Normalize** Frequency of Purchases field to eliminate semantic duplicates
2. **Investigate** whether Discount Applied and Promo Code Used represent distinct concepts
3. **Handle** missing values in Review Rating (impute or analyze separately)
4. **Document** assumptions about Season (purchase season vs product season)
5. **Create** standardized geographic groupings if regional analysis is needed
6. **Validate** age range and review rating ranges with business stakeholders
7. **Establish** clear definitions for any derived metrics before creating them

---

## Appendix: Validation Checklist

- [x] Raw data file not modified
- [x] All columns inventoried
- [x] Data types documented
- [x] Missing values quantified
- [x] Duplicates checked
- [x] Categorical distributions profiled
- [x] Numeric summaries calculated
- [x] Outliers identified
- [x] Semantic duplications investigated
- [x] Data quality issues flagged
- [x] Normalization needs identified
- [x] Analytical capabilities mapped
- [x] Limitations documented
- [x] Unanswerable questions listed
- [x] No loyalty scores created
- [x] No customer segments created
- [x] No marketing recommendations made
- [x] No causal claims made
- [x] No invented fields

---

**End of Report**

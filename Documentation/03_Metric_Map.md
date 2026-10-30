# Metric Map
**D2C Fashion Customer Intelligence Project**

**Date:** 2026-08-27  
**Phase:** Metric Definition & Business Alignment  
**Purpose:** Define decision-useful metrics traceable to raw fields

---

## Overview

This metric map translates business questions into measurable metrics using available raw data fields. Every metric is designed to support a specific business decision while respecting data constraints.

**Critical Constraints:**
- No transaction timestamps → Cannot measure actual retention, churn, or time-based patterns
- No longitudinal data → Cannot measure historical promotional dependency
- Customer-level snapshot only → Observed behavior at one point in time
- No cost/margin data → Cannot measure profitability

---

## Business Questions → Metrics Framework

### 1. Who are the genuinely loyal customers vs promotion-oriented customers?

**Approach:** Combine repeat-purchase history, frequency, satisfaction, and observed promotional exposure into loyalty proxies.

### 2. What observable behavioral patterns are associated with high customer value?

**Approach:** Analyze purchase amount, purchase history, frequency, satisfaction, subscription status, and demographic patterns.

### 3. Which geographies and demographics appear commercially underlevered?

**Approach:** Identify locations with high spend per customer but low observed promotional exposure (brand-pull proxy).

### 4. Which product categories are associated with lower vs higher purchase history?

**Approach:** Compare average previous purchases across categories; identify categories overrepresented in low-history vs high-history segments.

### 5. How should promotional activity be reduced selectively?

**Approach:** Identify customer segments with high observed value and satisfaction but also high observed promotional exposure.

### 6. What does the ideal customer profile look like?

**Approach:** Profile characteristics of high-value, high-history, high-frequency, high-satisfaction customers.

---

## A. CUSTOMER VALUE METRICS

| Metric Name | Raw Field(s) | Formula | Metric Type | Why It Matters | Decision Enabled | Limitations | Priority |
|-------------|--------------|---------|-------------|----------------|------------------|-------------|----------|
| **Current Observed Spend** | Purchase Amount (USD) | Direct value (sum of Purchase Amount) | Core KPI | Immediate transaction value | Spend segmentation | Single transaction only, not lifetime; NOT CLV | P0 |
| **Previous Purchase History** | Previous Purchases | Direct count | Core KPI | Depth of engagement | Loyalty proxy, customer segmentation | Count only, no purchase detail or timing | P0 |
| **Estimated Cumulative Observed Value (NOT CLV)** | Purchase Amount (USD), Previous Purchases | current_spend + (previous_purchases × avg_historical_spend_proxy) | Core KPI | Directional proxy for cumulative spend contribution | Value-based segmentation | Assumes uniform historical spend; NOT Customer Lifetime Value — cannot project future or account for margins | P1 |
| **Purchase Frequency Score** | Frequency of Purchases | Ordinal mapping: Weekly=7, Bi-Weekly/Fortnightly=3.5, Monthly=2, Quarterly/Every 3 Months=1, Annually=0.5 | Core KPI | Purchase regularity indicator | Loyalty proxy, engagement scoring | Stated preference, not observed behavior | P0 |
| **High-Value Flag** | Purchase Amount (USD) | Top 25% or data-driven threshold | Segmentation Feature | Identifies premium transactions | High-value customer identification | Threshold requires justification | P1 |
| **High-History Flag** | Previous Purchases | Top 25% or data-driven threshold | Segmentation Feature | Identifies repeat customers | Loyalty segmentation | Threshold requires justification | P0 |

---

## B. LOYALTY / REPEAT BEHAVIOR METRICS

| Metric Name | Raw Field(s) | Formula | Metric Type | Why It Matters | Decision Enabled | Limitations | Priority |
|-------------|--------------|---------|-------------|----------------|------------------|-------------|----------|
| **Loyalty Proxy A** | Previous Purchases, Frequency of Purchases, Review Rating, Discount Applied | Composite score combining history, frequency, satisfaction, low promo exposure | Core KPI | Behavioral loyalty indicator | Customer segmentation, retention strategy | No causal validation, proxy only | P0 |
| **Loyalty Proxy B** | Previous Purchases, Purchase Amount (USD), Frequency of Purchases, Review Rating | Composite score emphasizing value and engagement | Core KPI | Commercial value-oriented loyalty | Customer segmentation, value prioritization | No causal validation, proxy only | P0 |
| **High-Frequency Flag** | Frequency of Purchases | Weekly or Bi-Weekly/Fortnightly | Segmentation Feature | Identifies frequent purchasers | Engagement segmentation | Stated preference, not observed | P1 |
| **Subscription Flag** | Subscription Status | Yes/No | Segmentation Feature | Commitment indicator | Subscription vs transactional analysis | Cannot determine causation with value | P1 |
| **Engagement Score** | Previous Purchases, Frequency of Purchases | Normalized composite of history and frequency | Diagnostic | Overall engagement indicator | Loyalty input, segmentation | Does not account for satisfaction | P1 |

---

## C. PROMOTIONAL BEHAVIOR METRICS

| Metric Name | Raw Field(s) | Formula | Metric Type | Why It Matters | Decision Enabled | Limitations | Priority |
|-------------|--------------|---------|-------------|----------------|------------------|-------------|----------|
| **Observed Promo Exposure** | Discount Applied, Promo Code Used | Yes/No flag (either field = Yes) | Core KPI | Indicates promotional association | Promo dependency identification | Single observation, not historical pattern | P0 |
| **Promo-Exposed Customer Count** | Discount Applied | COUNT(Discount Applied = 'Yes') | Diagnostic | Promotional penetration | Budget reallocation decisions | Does not indicate dependency | P0 |
| **Current Observed Spend from Promo-Exposed Customers** | Purchase Amount (USD), Discount Applied | SUM(Purchase Amount WHERE Discount Applied = 'Yes') | Diagnostic | Current observed spend associated with promo exposure | ROI assessment (directional only) | Cannot establish causation; current observed only | P1 |
| **Promo Exposure Rate by Segment** | Discount Applied, Customer Segment | % customers with promo exposure per segment | Diagnostic | Segment-level promotional patterns | Selective promo reduction strategy | Correlation, not causation | P0 |
| **High-Value / High-Promo Flag** | Purchase Amount (USD), Previous Purchases, Discount Applied | High value AND high history AND promo-exposed | Segmentation Feature | Identifies over-promoted loyalists | Promo reduction opportunity | Threshold-dependent | P1 |

**CRITICAL NOTE:** Because this is a customer-level snapshot, we CANNOT calculate:
- Historical promotional dependency (e.g., % of orders with promo)
- Promotional frequency over time
- Whether promotions drove the purchase

We can only observe: "This customer's record is associated with promotional exposure at the time of observation."

---

## D. SATISFACTION METRICS

| Metric Name | Raw Field(s) | Formula | Metric Type | Why It Matters | Decision Enabled | Limitations | Priority |
|-------------|--------------|---------|-------------|----------------|------------------|-------------|----------|
| **Satisfaction Score** | Review Rating | Direct value (2.5-5.0 scale) | Core KPI | Explicit satisfaction measure | Quality monitoring, loyalty input | 37 missing values (0.95%) | P0 |
| **High Satisfaction Flag** | Review Rating | Rating ≥ 4.0 or data-driven threshold | Segmentation Feature | Identifies satisfied customers | Retention prioritization | Threshold requires justification | P1 |
| **Satisfaction Missing Flag** | Review Rating | Is NULL | Diagnostic | Indicates non-reviewers | Selection bias awareness | Cannot assume satisfaction level | P2 |
| **Average Satisfaction by Segment** | Review Rating, Customer Segment | AVG(Review Rating) per segment | Diagnostic | Segment quality indicator | Segment validation | Missing values may bias | P1 |

---

## E. CUSTOMER PROFILE METRICS

| Metric Name | Raw Field(s) | Formula | Metric Type | Why It Matters | Decision Enabled | Limitations | Priority |
|-------------|--------------|---------|-------------|----------------|------------------|-------------|----------|
| **Age Band** | Age | Bins: 18-24, 25-34, 35-44, 45-54, 55-64, 65+ | Segmentation Feature | Demographic segmentation | Targeted marketing, ICP definition | Age alone does not predict behavior | P1 |
| **Gender** | Gender | Male/Female | Segmentation Feature | Demographic pattern analysis | Product strategy, marketing | Binary only in dataset | P1 |
| **Subscription Status** | Subscription Status | Yes/No | Segmentation Feature | Recurring relationship indicator | Subscription program effectiveness | Cannot determine if it drives value | P1 |
| **Payment Method** | Payment Method | Categorical | Supporting Metric | Payment preference pattern | Operational insight | Weak predictor of loyalty | P2 |
| **Shipping Type** | Shipping Type | Categorical | Supporting Metric | Fulfillment preference | Operational insight | Weak predictor of loyalty | P2 |
| **Location** | Location | US State | Segmentation Feature | Geographic distribution | Geographic strategy, expansion | State-level only, no city/region | P0 |
| **Category** | Category | Clothing/Accessories/Footwear/Outerwear | Segmentation Feature | Product preference | Product strategy, cross-sell | Single purchase observed | P0 |
| **Item Purchased** | Item Purchased | 25 distinct items | Supporting Metric | Granular product preference | Product-level insight | High cardinality, single observation | P2 |

---

## F. GEOGRAPHY METRICS

| Metric Name | Raw Field(s) | Formula | Metric Type | Why It Matters | Decision Enabled | Limitations | Priority |
|-------------|--------------|---------|-------------|----------------|------------------|-------------|----------|
| **Customers per Location** | Location | COUNT(Customer ID) by Location | Core KPI | Market penetration indicator | Geographic prioritization | Cannot determine market share | P0 |
| **Average Spend by Location** | Purchase Amount (USD), Location | AVG(Purchase Amount) by Location | Core KPI | Geographic revenue quality | High-value market identification | Single transaction per customer | P0 |
| **Average Previous Purchases by Location** | Previous Purchases, Location | AVG(Previous Purchases) by Location | Diagnostic | Geographic loyalty proxy | Retention by market | Count only, no detail | P0 |
| **Average Frequency by Location** | Frequency of Purchases, Location | AVG(Frequency Score) by Location | Diagnostic | Geographic engagement pattern | Market health assessment | Stated preference | P1 |
| **Promo Exposure Rate by Location** | Discount Applied, Location | % promo-exposed by Location | Core KPI | Geographic promotional dependency | Selective promo strategy by market | Correlation, not causation | P0 |
| **Average Satisfaction by Location** | Review Rating, Location | AVG(Review Rating) by Location | Diagnostic | Geographic quality indicator | Market satisfaction monitoring | Missing values may bias | P1 |
| **Subscription Rate by Location** | Subscription Status, Location | % subscribed by Location | Diagnostic | Geographic subscription penetration | Subscription program effectiveness | Cannot determine causation | P1 |
| **Geographic Opportunity Score** | Multiple | High spend + low promo exposure | Core KPI | Brand-pull proxy markets | Expansion/investment prioritization | Observational only | P0 |

---

## G. CATEGORY METRICS

| Metric Name | Raw Field(s) | Formula | Metric Type | Why It Matters | Decision Enabled | Limitations | Priority |
|-------------|--------------|---------|-------------|----------------|------------------|-------------|----------|
| **Customers per Category** | Category | COUNT(Customer ID) by Category | Core KPI | Category popularity | Product strategy | Single purchase per customer | P0 |
| **Average Spend by Category** | Purchase Amount (USD), Category | AVG(Purchase Amount) by Category | Core KPI | Category revenue quality | Pricing strategy, product mix | Single transaction per customer | P0 |
| **Average Previous Purchases by Category** | Previous Purchases, Category | AVG(Previous Purchases) by Category | Core KPI | Category-loyalty association | Category funnel analysis | Association, not causation | P0 |
| **Average Frequency by Category** | Frequency of Purchases, Category | AVG(Frequency Score) by Category | Diagnostic | Category-frequency association | Product strategy | Stated preference | P1 |
| **Promo Exposure Rate by Category** | Discount Applied, Category | % promo-exposed by Category | Diagnostic | Category promotional patterns | Pricing strategy | Single observation | P1 |
| **Average Satisfaction by Category** | Review Rating, Category | AVG(Review Rating) by Category | Diagnostic | Category quality indicator | Product quality monitoring | Missing values may bias | P1 |
| **Purchase History Band Distribution** | Previous Purchases, Category | % Low/Mid/High history per category | Core KPI | Entry vs retention category indicator | Category funnel strategy | Association, not causation | P0 |

**Category Interpretation:**
- Categories **associated with lower purchase history**: May represent entry points or lower engagement
- Categories **associated with higher purchase history**: May represent retention categories or higher engagement
- DO NOT claim causation (e.g., "buying X causes loyalty")

---

## Metric Type Definitions

- **Core KPI**: Essential metric directly supporting a primary business decision
- **Diagnostic**: Supporting metric providing context or validation
- **Segmentation Feature**: Input to customer segmentation logic
- **Supporting Metric**: Secondary metric for operational or exploratory insight

---

## Priority Definitions

- **P0 (Essential)**: Required for core business questions; project cannot succeed without these
- **P1 (Important)**: Materially improves decision quality; should be included
- **P2 (Optional)**: Nice-to-have; include if time/resources permit

---

## Redundant Metrics Identified

1. **Discount Applied vs Promo Code Used**: Perfectly correlated (100% match). Use single field: `observed_promo_exposure`
2. **Quarterly vs Every 3 Months**: Semantic duplicates. Normalize to "Quarterly"
3. **Bi-Weekly vs Fortnightly**: Semantic duplicates. Normalize to "Bi-Weekly"

---

## Metrics That CANNOT Be Legitimately Calculated

| Metric Name | Why It Cannot Be Calculated |
|-------------|------------------------------|
| Customer Lifetime Value (CLV) | No transaction dates, no future projection capability |
| Actual Retention Rate | No time dimension, no cohort structure |
| Actual Churn Rate | No exit dates, no time dimension |
| Time to Second Purchase | No transaction timestamps |
| Historical Promo Dependency | Single customer-level snapshot, not transaction history |
| Promo-Incremental Revenue | No control group, no causal design |
| Category Migration Patterns | Single purchase per customer |
| Purchase Seasonality | No transaction dates |
| Customer Acquisition Cost (CAC) | No cost data |
| Profit Margin by Customer | No cost/margin data |

---

## Misleading Metrics to AVOID

| Metric Name | Why It Is Misleading |
|-------------|----------------------|
| "Churn Risk Score" | No actual churn labels or temporal data to validate |
| "Lifetime Value" | Implies predictive accuracy we cannot achieve |
| "Promo-Caused Revenue" | Implies causation from observational data |
| "True Loyalty Score" | No validation data; should be called "loyalty proxy" |
| "Historical Promo Rate" | Single snapshot; cannot calculate historical rate |
| "Next Purchase Date" | No temporal data for prediction |

---

## Minimum Viable Metric Set

For initial business diagnostics, focus on:

### Customer Value
1. Current Spend
2. Previous Purchase History
3. Purchase Frequency Score

### Loyalty Proxy
4. Loyalty Proxy A (behavior-focused)
5. Loyalty Proxy B (value-focused)

### Promotional Analysis
6. Observed Promo Exposure
7. Promo Exposure Rate by Segment

### Satisfaction
8. Satisfaction Score
9. High Satisfaction Flag

### Segmentation
10. Customer Segments (derived from loyalty proxies)
11. Age Band
12. Location
13. Category

### Geographic Opportunity
14. Customers per Location
15. Average Spend by Location
16. Promo Exposure Rate by Location
17. Geographic Opportunity Score

### Category Analysis
18. Average Previous Purchases by Category
19. Purchase History Band Distribution by Category

**Total Core Metrics: 19**

---

## Founder Dashboard Recommendation

**Panel 1: Customer Value Pyramid**
- Segment
- Customer Count
- Customer Share %
- Current Observed Spend
- Spend Share %
- Average Spend
- Average Previous Purchases

**Panel 2: Promo Exposure vs Loyalty**
- Segment
- Observed Promo Exposure %
- Loyalty Score (avg)
- Average Spend
- Customer Count

**Panel 3: Geographic Opportunity**
- Location (top 15 by opportunity score)
- Customers
- Average Spend
- Promo Exposure %
- Opportunity Classification

**Panel 4: Category Funnel**
- Category
- Purchase History Band (Low/Mid/High)
- Customer Share %
- Average Spend
- Average Satisfaction

---

## Assumptions & Limitations

1. **Frequency of Purchases** is stated preference, not observed behavior from transaction history
2. **Previous Purchases** is a count only; no detail on what was purchased or when
3. **Discount Applied** indicates promotional exposure at observation time; does not indicate historical dependency
4. **Review Rating** has 37 missing values (0.95%); may introduce selection bias
5. **Season** field is ambiguous (purchase season or product season?)
6. All metrics are observational; no causal claims can be made
7. Customer-level snapshot; no longitudinal tracking capability

## Final Methodology Constraints

The following apply to all outputs derived from this metric map:

- **No timestamps:** Transaction dates are not available; true time-to-event, recency, and trend metrics cannot be calculated
- **No true churn:** Cannot measure customer departure; no exit dates or churn window definition is possible
- **No true retention:** Cannot measure whether customers continued purchasing over time; observed snapshot only
- **No historical promo dependency:** Single customer-level observation; cannot calculate what share of a customer's purchase history involved promotions
- **No causal inference:** All observed associations between promo exposure, spend, and loyalty proxies are correlational; promotional impact on behavior cannot be established from this data

---

## Next Steps

1. Validate metric definitions with business stakeholders
2. Confirm frequency score ordinal mapping is acceptable
3. Confirm satisfaction threshold for "high satisfaction"
4. Confirm purchase history thresholds for Low/Mid/High bands
5. Proceed to data cleaning phase
6. Develop loyalty proxy methodologies for A and B definitions

---

**End of Metric Map**

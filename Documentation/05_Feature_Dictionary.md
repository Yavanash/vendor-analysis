# Feature Dictionary
**D2C Fashion Customer Intelligence Project**

**Date:** 2026-08-27
**Phase:** Feature Engineering
**Purpose:** Document all engineered features for customer value analysis

**Input:** `Raw_Data/cleaned/customer_cleaned.csv`
**Output:** `Outputs/analytical/customer_features.csv`

---

## Overview

This dictionary documents all features created for customer value and loyalty analysis. Every feature is traceable to raw data fields and supports specific business decisions.

**Total Features:** 24
**Customer Records:** 3,900

---

## Feature Categories

1. **Core Value Features** (3): Spend, purchase history, frequency
2. **Promotional Features** (2): Promo exposure indicators
3. **Satisfaction Features** (3): Rating, missing flag, high satisfaction
4. **Engagement Features** (2): High history, high frequency flags
5. **Profile Features** (7): Demographics, subscription, location, category, preferences
6. **Reference Fields** (6): Original fields preserved for validation

---

## 1. CORE VALUE FEATURES

### current_spend

**Definition:** Customer's observed purchase amount in USD

**Source Field:** `Purchase Amount (USD)`

**Formula:** Direct mapping

**Data Type:** Numeric (integer)

**Range:** $20 - $100

**Mean:** $59.76

**Business Use:**
- Revenue segmentation
- High-value customer identification
- Value-based prioritization

**Interpretation:** Immediate transaction value; single observation per customer

**Limitations:**
- Single transaction only; not lifetime value
- Cannot determine if this is typical or anomalous for the customer

---

### previous_purchase_history

**Definition:** Count of purchases made prior to observed transaction

**Source Field:** `Previous Purchases`

**Formula:** Direct mapping

**Data Type:** Numeric (integer)

**Range:** 1 - 50

**Mean:** 25.35

**Distribution:**
- 25th percentile: 13
- Median: 25
- 75th percentile: 38

**Business Use:**
- Loyalty proxy
- Customer segmentation
- Repeat behavior indicator

**Interpretation:** Higher count suggests deeper engagement and repeat purchase behavior

**Limitations:**
- Count only; no detail on what was purchased or when
- No way to determine time span of these purchases
- Cannot distinguish between 10 purchases in 1 month vs 10 purchases over 5 years

---

### purchase_frequency_score

**Definition:** Ordinal score representing stated purchase frequency

**Source Field:** `frequency_normalized`

**Formula:** Ordinal mapping
- Weekly = 7.0
- Bi-Weekly = 3.5
- Monthly = 2.0
- Quarterly = 1.0
- Annually = 0.5

**Data Type:** Numeric (float)

**Range:** 0.5 - 7.0

**Mean:** 2.60

**Distribution:**
- Quarterly (1.0): 1,147 (29.4%)
- Bi-Weekly (3.5): 1,089 (27.9%)
- Annually (0.5): 572 (14.7%)
- Monthly (2.0): 553 (14.2%)
- Weekly (7.0): 539 (13.8%)


**Business Use:**
- Loyalty proxy input
- Engagement indicator
- Purchase pattern analysis

**Interpretation:** Higher scores indicate more frequent stated purchase behavior

**Limitations:**
- Stated preference, NOT observed behavior from transaction history
- Cannot validate if actual behavior matches stated frequency
- Self-reported data may not reflect reality

---

## 2. PROMOTIONAL FEATURES

### observed_promo_exposure

**Definition:** Whether customer's record is associated with promotional activity

**Source Field:** `Discount Applied`

**Formula:** Direct mapping (Yes/No)

**Data Type:** Categorical (Yes/No)

**Distribution:**
- Yes: 1,677 (43.0%)
- No: 2,223 (57.0%)

**Business Use:**
- Promo-exposure identification
- Promotional strategy analysis
- Selective promo reduction targeting

**Interpretation:** "Yes" indicates promotional exposure at time of observation

**Limitations:**
- Single snapshot; does NOT indicate historical promotional dependency
- Cannot calculate "% of orders with promo" (no transaction history)
- Cannot determine causation (promo → purchase vs purchase → promo applied)

---

### observed_promo_exposure_flag

**Definition:** Binary indicator of promotional exposure

**Source Field:** `Discount Applied`

**Formula:** 1 if Discount Applied = 'Yes', else 0

**Data Type:** Numeric (integer, 0/1)

**Distribution:**
- 1 (promo-exposed): 1,677 (43.0%)
- 0 (non-promo): 2,223

**Business Use:**
- Numeric calculations
- Segmentation logic
- Correlation analysis

**Interpretation:** Same as observed_promo_exposure, numeric format for analysis

---

## 3. SATISFACTION FEATURES

### satisfaction_score

**Definition:** Customer's review rating of their experience

**Source Field:** `Review Rating`

**Formula:** Direct mapping

**Data Type:** Numeric (float)

**Range:** 2.5 - 5.0

**Mean:** 3.75 (excluding missing)

**Distribution:**
- Valid ratings: 3,863
- Missing ratings: 37
- Median: 3.80
- 75th percentile: 4.40

**Business Use:**
- Satisfaction monitoring
- Loyalty proxy input
- Quality indicator

**Interpretation:** Higher ratings indicate greater satisfaction (scale 2.5-5.0)

**Limitations:**
- 37 missing values (0.95%)
- Selection bias: only customers who chose to leave reviews
- May not represent overall satisfaction; could skew toward extremes

---

### satisfaction_missing_flag

**Definition:** Indicator that customer did not leave a review

**Source Field:** `Review Rating` (derived)

**Formula:** 1 if Review Rating is NULL, else 0

**Data Type:** Numeric (integer, 0/1)

**Distribution:**
- 1 (missing): 37
- 0 (present): 3,863

**Business Use:**
- Selection bias awareness
- Segment non-reviewers
- Behavioral pattern analysis

**Interpretation:** Flag enables separate analysis of reviewer vs non-reviewer segments

**Limitations:**
- Cannot infer satisfaction level from missing reviews
- Missing may indicate neutrality, apathy, or other factors

---

### high_satisfaction_flag

**Definition:** Indicator of high customer satisfaction

**Source Field:** `satisfaction_score`

**Formula:** 1 if satisfaction_score ≥ 4.0, else 0 (NULL if satisfaction_score is NULL)

**Threshold:** 4.0 (business-relevant cutoff: 80% on 5-point scale)

**Data Type:** Numeric (integer, 0/1, with NULLs)

**Distribution:**
- 1 (high satisfaction): 1,634 (42.3% of valid ratings)
- 0 (lower satisfaction): 2,266
- NULL (no rating): 0

**Business Use:**
- Satisfied customer identification
- Retention prioritization
- Loyalty segmentation

**Interpretation:** Customers meeting or exceeding quality expectations

**Limitations:**
- Threshold is business judgment, not data-driven optimization
- Only applies to 3,863 customers with ratings

---

## 4. ENGAGEMENT FEATURES

### high_purchase_history_flag

**Definition:** Indicator of high repeat-purchase behavior

**Source Field:** `previous_purchase_history`

**Formula:** 1 if previous_purchase_history ≥ 38 (75th percentile), else 0

**Threshold:** 38 purchases (75th percentile, data-driven)

**Data Type:** Numeric (integer, 0/1)

**Distribution:**
- 1 (high history): 998 (25.6%)
- 0 (lower history): 2,902

**Business Use:**
- Loyalty segmentation
- High-value customer identification
- Retention targeting

**Interpretation:** Top 25% of customers by historical purchase count

**Limitations:**
- Threshold is arbitrary percentile; business may prefer different cutoff
- Count only; no purchase detail or timing

---

### high_frequency_flag

**Definition:** Indicator of frequent stated purchase behavior

**Source Field:** `frequency_normalized`

**Formula:** 1 if frequency is 'Weekly' or 'Bi-Weekly', else 0

**Data Type:** Numeric (integer, 0/1)

**Distribution:**
- 1 (high frequency): 1,628 (41.7%)
- 0 (lower frequency): 2,272

**Business Use:**
- Engagement segmentation
- Loyalty proxy input
- Cadence analysis

**Interpretation:** Customers stating weekly or bi-weekly purchase patterns

**Limitations:**
- Stated preference, NOT observed behavior
- Cannot validate actual purchase frequency
- Definition of "high" is business judgment

---

## 5. CUSTOMER PROFILE FEATURES

### age_band

**Definition:** Customer age grouped into business-relevant segments

**Source Field:** `Age`

**Formula:** Binned age ranges

**Data Type:** Categorical

**Categories & Distribution:**
- 18-24: 486 (12.5%)
- 25-34: 755 (19.4%)
- 35-44: 729 (18.7%)
- 45-54: 752 (19.3%)
- 55-64: 751 (19.3%)
- 65+: 427 (10.9%)


**Business Use:**
- Demographic segmentation
- ICP definition
- Targeted marketing

**Interpretation:** Standard age cohorts for customer profiling

**Limitations:**
- Age alone is weak predictor of behavior
- Binning loses granularity

---

### subscription_flag

**Definition:** Indicator of active subscription relationship

**Source Field:** `Subscription Status`

**Formula:** 1 if Subscription Status = 'Yes', else 0

**Data Type:** Numeric (integer, 0/1)

**Distribution:**
- 1 (subscriber): 1,053 (27.0%)
- 0 (non-subscriber): 2,847

**Business Use:**
- Subscription program analysis
- Commitment indicator
- Loyalty proxy input

**Interpretation:** Recurring relationship vs transactional

**Limitations:**
- Cannot determine causation (does subscription drive value or vice versa?)
- No subscription tenure or value information

---

### gender

**Definition:** Customer gender

**Source Field:** `Gender`

**Formula:** Direct mapping

**Data Type:** Categorical (Male/Female)

**Distribution:**
- Male: 2,652 (68.0%)
- Female: 1,248 (32.0%)

**Business Use:**
- Demographic analysis
- Product strategy
- Marketing targeting

**Limitations:**
- Binary only in dataset
- Gender alone is weak predictor of value

---

### location

**Definition:** Customer's US state

**Source Field:** `Location`

**Formula:** Direct mapping

**Data Type:** Categorical (50 states)

**Business Use:**
- Geographic analysis
- Market penetration
- Regional strategy
- Opportunity identification

**Limitations:**
- State-level only; no city/region/ZIP
- Cannot determine market share

---

### category

**Definition:** Product category of observed purchase

**Source Field:** `Category`

**Formula:** Direct mapping

**Data Type:** Categorical

**Distribution:**
- Clothing: 1,737 (44.5%)
- Accessories: 1,240 (31.8%)
- Footwear: 599 (15.4%)
- Outerwear: 324 (8.3%)


**Business Use:**
- Product strategy
- Category-loyalty association
- Cross-sell opportunities

**Interpretation:** Categories may be associated with different loyalty patterns

**Limitations:**
- Single purchase observed per customer
- Cannot determine category migration or preferences

---

### payment_method

**Definition:** Payment method used for observed transaction

**Source Field:** `Payment Method`

**Formula:** Direct mapping

**Data Type:** Categorical (6 methods)

**Business Use:**
- Payment preference analysis
- Operational insight

**Limitations:**
- Weak predictor of loyalty
- Single observation; preferences may vary

---

### shipping_type

**Definition:** Shipping method selected for observed transaction

**Source Field:** `Shipping Type`

**Formula:** Direct mapping

**Data Type:** Categorical (6 types)

**Business Use:**
- Fulfillment preference analysis
- Operational insight

**Limitations:**
- Weak predictor of loyalty
- Single observation; preferences may vary

---

## 6. REFERENCE FIELDS

The following original fields are preserved for validation and drill-down analysis:

- **Age:** Original age value
- **Item Purchased:** Specific item (25 unique items)
- **Size:** Product size (S/M/L/XL)
- **Color:** Product color (25 unique colors)
- **Season:** Seasonal attribution (Spring/Summer/Fall/Winter)
- **frequency_normalized:** Cleaned frequency text

---

## Feature Engineering Decisions

### Data-Driven Thresholds

1. **high_purchase_history_flag:** 75th percentile (38 purchases)
   - Rationale: Identifies top quartile of repeat customers
   - Alternative: Business could define absolute threshold (e.g., ≥30 purchases)

2. **high_satisfaction_flag:** 4.0 rating
   - Rationale: Business-relevant cutoff (80% on 5-point scale)
   - Alternative: Could use 75th percentile (4.40)

3. **high_frequency_flag:** Weekly or Bi-Weekly
   - Rationale: Clear separation of high-frequency segments
   - Alternative: Could include Monthly (top 3 frequencies)

### Frequency Score Mapping

The ordinal mapping (Weekly=7.0, Bi-Weekly=3.5, etc.) approximates relative purchase frequency:
- Weekly ≈ 52 purchases/year → 7.0
- Bi-Weekly ≈ 26 purchases/year → 3.5
- Monthly ≈ 12 purchases/year → 2.0
- Quarterly ≈ 4 purchases/year → 1.0
- Annually ≈ 1 purchase/year → 0.5

**Limitation:** This is a linear approximation; actual purchase behavior may not be linear.

### Fields NOT Created (By Design)

- **Loyalty scores:** Reserved for Phase 4 & 5
- **Customer segments:** Reserved for Phase 7
- **Lifetime value:** Cannot calculate (no time dimension, no predictive model)
- **Churn risk:** Cannot calculate (no churn labels, no temporal data)
- **Promo dependency rate:** Cannot calculate (single snapshot, not transaction history)

---

## Usage Guidelines

### For Analysis

1. **Customer Value:** Use `current_spend` + `previous_purchase_history` + `purchase_frequency_score`
2. **Loyalty Proxy:** Combine `previous_purchase_history`, `purchase_frequency_score`, `satisfaction_score`, `observed_promo_exposure_flag`
3. **Segmentation:** Use engagement flags, profile features, and value metrics
4. **Geographic Opportunity:** Analyze `location` with value and promo metrics
5. **Category Analysis:** Cross `category` with `previous_purchase_history` bands

### For Business Decisions

- **High-value retention:** Focus on `high_purchase_history_flag=1` AND `high_satisfaction_flag=1`
- **Promo reduction opportunity:** Target `high_purchase_history_flag=1` AND `observed_promo_exposure_flag=1`
- **Growth segments:** Identify demographics/geographies with high value, low promo exposure

### Interpretive Caution

- All metrics are **observational proxies**, not validated predictors
- **Correlation ≠ causation**: Cannot claim promo exposure "causes" anything
- **Stated ≠ observed**: Frequency scores are self-reported, not transaction-derived
- **Single snapshot**: No way to determine trends, changes, or trajectories

---

## Validation Results

**Critical features:** No missing values in core metrics
**Expected nulls:** satisfaction_score (37), high_satisfaction_flag (0)
**Data integrity:** All 3,900 customer records preserved

---

## Next Steps

1. Proceed to Phase 4: Loyalty Definition A
2. Proceed to Phase 5: Loyalty Definition B
3. Compare loyalty frameworks in Phase 6
4. Create customer segments in Phase 7

---

**End of Feature Dictionary**

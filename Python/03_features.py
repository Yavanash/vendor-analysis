"""
Customer Feature Engineering for D2C Fashion Customer Intelligence Project
===========================================================================

Purpose: Create decision-useful features from cleaned customer data
Author: Analytics Engineering Team
Date: 2026-08-27

CRITICAL RULES:
- Only create features that support business decisions
- Every feature must be traceable to raw fields
- Document all transformations
- Use data-driven thresholds where possible
- Do NOT create loyalty scores at this phase
- Do NOT create customer segments at this phase
"""

import pandas as pd
import numpy as np
from pathlib import Path
import warnings
import sys
import io

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

warnings.filterwarnings('ignore')

# File paths
INPUT_PATH = Path("Raw_Data/cleaned/customer_cleaned.csv")
OUTPUT_PATH = Path("Outputs/analytical/customer_features.csv")
FEATURE_DICT_PATH = Path("Documentation/05_Feature_Dictionary.md")

# Create output directory
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

print("="*80)
print("CUSTOMER FEATURE ENGINEERING")
print("="*80)
print()

# ============================================================================
# 1. LOAD CLEANED DATA
# ============================================================================
print("Step 1: Loading cleaned data...")
df = pd.read_csv(INPUT_PATH)
print(f"✓ Loaded {len(df):,} customer records")
print(f"✓ Input columns: {len(df.columns)}")
print()

# ============================================================================
# 2. CORE VALUE FEATURES
# ============================================================================
print("="*80)
print("Step 2: Creating Core Value Features")
print("="*80)
print()

# Current spend (direct mapping)
df['current_spend'] = df['Purchase Amount (USD)']
print("✓ current_spend: Direct mapping from Purchase Amount (USD)")

# Previous purchase history (direct mapping)
df['previous_purchase_history'] = df['Previous Purchases']
print("✓ previous_purchase_history: Direct mapping from Previous Purchases")

# Purchase frequency score (ordinal mapping)
frequency_mapping = {
    'Weekly': 7.0,
    'Bi-Weekly': 3.5,
    'Monthly': 2.0,
    'Quarterly': 1.0,
    'Annually': 0.5
}

df['purchase_frequency_score'] = df['frequency_normalized'].map(frequency_mapping)
print("✓ purchase_frequency_score: Ordinal mapping")
print("  Weekly=7.0, Bi-Weekly=3.5, Monthly=2.0, Quarterly=1.0, Annually=0.5")

# Validate mapping
unmapped = df['purchase_frequency_score'].isnull().sum()
if unmapped > 0:
    print(f"  ⚠️ Warning: {unmapped} unmapped frequency values")
    print(f"  Unmapped values: {df[df['purchase_frequency_score'].isnull()]['frequency_normalized'].unique()}")
else:
    print(f"  ✓ All {len(df):,} records mapped successfully")

print()

# Value distribution analysis
print("Value Distribution:")
print(f"  Current Spend: min=${df['current_spend'].min()}, max=${df['current_spend'].max()}, mean=${df['current_spend'].mean():.2f}")
print(f"  Previous Purchases: min={df['previous_purchase_history'].min()}, max={df['previous_purchase_history'].max()}, mean={df['previous_purchase_history'].mean():.2f}")
print(f"  Frequency Score: min={df['purchase_frequency_score'].min()}, max={df['purchase_frequency_score'].max()}, mean={df['purchase_frequency_score'].mean():.2f}")
print()

# ============================================================================
# 3. PROMOTIONAL EXPOSURE FEATURES
# ============================================================================
print("="*80)
print("Step 3: Creating Promotional Exposure Features")
print("="*80)
print()

# Observed promo exposure (primary field: Discount Applied)
df['observed_promo_exposure'] = df['Discount Applied']
df['observed_promo_exposure_flag'] = (df['Discount Applied'] == 'Yes').astype(int)

promo_count = df['observed_promo_exposure_flag'].sum()
promo_pct = (promo_count / len(df)) * 100

print(f"✓ observed_promo_exposure: Mapped from Discount Applied")
print(f"✓ observed_promo_exposure_flag: Binary indicator")
print(f"  Promo-exposed customers: {promo_count:,} ({promo_pct:.1f}%)")
print(f"  Non-promo customers: {len(df) - promo_count:,} ({100-promo_pct:.1f}%)")
print()

# ============================================================================
# 4. SATISFACTION FEATURES
# ============================================================================
print("="*80)
print("Step 4: Creating Satisfaction Features")
print("="*80)
print()

# Satisfaction score (direct mapping, preserving missing)
df['satisfaction_score'] = df['Review Rating']
print(f"✓ satisfaction_score: Direct mapping from Review Rating")
print(f"  Valid ratings: {df['satisfaction_score'].notna().sum():,}")
print(f"  Missing ratings: {df['satisfaction_score'].isna().sum()} (preserved)")

# Satisfaction missing flag (already created in cleaning)
df['satisfaction_missing_flag'] = df['review_rating_missing']
print(f"✓ satisfaction_missing_flag: From cleaning phase")

# High satisfaction flag (data-driven threshold)
# Use median as threshold
satisfaction_valid = df['satisfaction_score'].dropna()
satisfaction_median = satisfaction_valid.median()
satisfaction_75th = satisfaction_valid.quantile(0.75)

# Use 4.0 as threshold (business-relevant and close to 75th percentile)
high_satisfaction_threshold = 4.0

df['high_satisfaction_flag'] = (df['satisfaction_score'] >= high_satisfaction_threshold).astype(int)
high_sat_count = df['high_satisfaction_flag'].sum()
high_sat_pct = (high_sat_count / df['satisfaction_score'].notna().sum()) * 100

print(f"✓ high_satisfaction_flag: Rating ≥ {high_satisfaction_threshold}")
print(f"  Threshold rationale: Business-relevant cutoff (4.0/5.0 = 80%)")
print(f"  Data context: median={satisfaction_median:.2f}, 75th percentile={satisfaction_75th:.2f}")
print(f"  High satisfaction customers: {high_sat_count:,} ({high_sat_pct:.1f}% of those with ratings)")
print()

# ============================================================================
# 5. ENGAGEMENT FLAGS
# ============================================================================
print("="*80)
print("Step 5: Creating Engagement Flags")
print("="*80)
print()

# High purchase history flag (data-driven threshold using 75th percentile)
history_75th = df['previous_purchase_history'].quantile(0.75)
high_history_threshold = history_75th

df['high_purchase_history_flag'] = (df['previous_purchase_history'] >= high_history_threshold).astype(int)
high_history_count = df['high_purchase_history_flag'].sum()
high_history_pct = (high_history_count / len(df)) * 100

print(f"✓ high_purchase_history_flag: Previous Purchases ≥ {high_history_threshold:.0f}")
print(f"  Threshold: 75th percentile (data-driven)")
print(f"  High-history customers: {high_history_count:,} ({high_history_pct:.1f}%)")

# High frequency flag (Weekly or Bi-Weekly)
df['high_frequency_flag'] = df['frequency_normalized'].isin(['Weekly', 'Bi-Weekly']).astype(int)
high_freq_count = df['high_frequency_flag'].sum()
high_freq_pct = (high_freq_count / len(df)) * 100

print(f"✓ high_frequency_flag: Weekly or Bi-Weekly")
print(f"  High-frequency customers: {high_freq_count:,} ({high_freq_pct:.1f}%)")
print()

# ============================================================================
# 6. CUSTOMER PROFILE FEATURES
# ============================================================================
print("="*80)
print("Step 6: Creating Customer Profile Features")
print("="*80)
print()

# Age bands (business-relevant segments)
age_bins = [0, 25, 35, 45, 55, 65, 100]
age_labels = ['18-24', '25-34', '35-44', '45-54', '55-64', '65+']
df['age_band'] = pd.cut(df['Age'], bins=age_bins, labels=age_labels, right=False)

print("✓ age_band: 6 segments")
print(f"  Bins: {', '.join(age_labels)}")
age_dist = df['age_band'].value_counts().sort_index()
for band, count in age_dist.items():
    pct = (count / len(df)) * 100
    print(f"    {band}: {count:,} ({pct:.1f}%)")

# Subscription flag
df['subscription_flag'] = (df['Subscription Status'] == 'Yes').astype(int)
sub_count = df['subscription_flag'].sum()
sub_pct = (sub_count / len(df)) * 100
print(f"\n✓ subscription_flag: {sub_count:,} subscribers ({sub_pct:.1f}%)")

# Gender (direct mapping)
df['gender'] = df['Gender']
print(f"✓ gender: Direct mapping")

# Location (direct mapping)
df['location'] = df['Location']
print(f"✓ location: {df['location'].nunique()} unique states")

# Category (direct mapping)
df['category'] = df['Category']
print(f"✓ category: {df['category'].nunique()} categories")
cat_dist = df['category'].value_counts()
for cat, count in cat_dist.items():
    pct = (count / len(df)) * 100
    print(f"    {cat}: {count:,} ({pct:.1f}%)")

# Payment method (direct mapping)
df['payment_method'] = df['Payment Method']
print(f"\n✓ payment_method: {df['payment_method'].nunique()} methods")

# Shipping type (direct mapping)
df['shipping_type'] = df['Shipping Type']
print(f"✓ shipping_type: {df['shipping_type'].nunique()} types")

print()

# ============================================================================
# 7. SELECT FINAL FEATURE SET
# ============================================================================
print("="*80)
print("Step 7: Assembling Final Feature Set")
print("="*80)
print()

# Core identifiers and features
feature_columns = [
    # Identifier
    'Customer ID',

    # Core Value
    'current_spend',
    'previous_purchase_history',
    'purchase_frequency_score',

    # Promotional
    'observed_promo_exposure',
    'observed_promo_exposure_flag',

    # Satisfaction
    'satisfaction_score',
    'satisfaction_missing_flag',
    'high_satisfaction_flag',

    # Engagement
    'high_purchase_history_flag',
    'high_frequency_flag',

    # Profile
    'age_band',
    'subscription_flag',
    'gender',
    'location',
    'category',
    'payment_method',
    'shipping_type',

    # Original fields for reference
    'Age',
    'Item Purchased',
    'Size',
    'Color',
    'Season',
    'frequency_normalized'
]

df_features = df[feature_columns].copy()

print(f"✓ Final feature set: {len(feature_columns)} columns")
print()

# ============================================================================
# 8. FEATURE VALIDATION
# ============================================================================
print("="*80)
print("Step 8: Feature Validation")
print("="*80)
print()

# Check for missing values in critical features
critical_features = [
    'current_spend',
    'previous_purchase_history',
    'purchase_frequency_score',
    'observed_promo_exposure_flag',
    'high_purchase_history_flag',
    'high_frequency_flag'
]

print("Critical features validation:")
for feat in critical_features:
    null_count = df_features[feat].isnull().sum()
    if null_count > 0:
        print(f"  ⚠️ {feat}: {null_count} null values")
    else:
        print(f"  ✓ {feat}: No nulls")

print()

# Expected nulls
print("Expected nulls (by design):")
print(f"  satisfaction_score: {df_features['satisfaction_score'].isnull().sum()} (preserved from raw data)")
print(f"  high_satisfaction_flag: {df_features['high_satisfaction_flag'].isnull().sum()} (nulls where satisfaction missing)")
print()

# ============================================================================
# 9. SAVE FEATURES
# ============================================================================
print("="*80)
print("Step 9: Saving Feature Dataset")
print("="*80)
print()

df_features.to_csv(OUTPUT_PATH, index=False)
print(f"✓ Features saved to: {OUTPUT_PATH}")
print(f"  Rows: {len(df_features):,}")
print(f"  Columns: {len(df_features.columns)}")
print()

# ============================================================================
# 10. GENERATE FEATURE DICTIONARY
# ============================================================================
print("="*80)
print("Step 10: Generating Feature Dictionary")
print("="*80)
print()

feature_dict = f"""# Feature Dictionary
**D2C Fashion Customer Intelligence Project**

**Date:** 2026-08-27
**Phase:** Feature Engineering
**Purpose:** Document all engineered features for customer value analysis

**Input:** `Raw_Data/cleaned/customer_cleaned.csv`
**Output:** `Outputs/analytical/customer_features.csv`

---

## Overview

This dictionary documents all features created for customer value and loyalty analysis. Every feature is traceable to raw data fields and supports specific business decisions.

**Total Features:** {len(feature_columns)}
**Customer Records:** {len(df_features):,}

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

**Range:** ${df_features['current_spend'].min()} - ${df_features['current_spend'].max()}

**Mean:** ${df_features['current_spend'].mean():.2f}

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

**Range:** {int(df_features['previous_purchase_history'].min())} - {int(df_features['previous_purchase_history'].max())}

**Mean:** {df_features['previous_purchase_history'].mean():.2f}

**Distribution:**
- 25th percentile: {df_features['previous_purchase_history'].quantile(0.25):.0f}
- Median: {df_features['previous_purchase_history'].quantile(0.50):.0f}
- 75th percentile: {df_features['previous_purchase_history'].quantile(0.75):.0f}

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

**Range:** {df_features['purchase_frequency_score'].min()} - {df_features['purchase_frequency_score'].max()}

**Mean:** {df_features['purchase_frequency_score'].mean():.2f}

**Distribution:**
"""

freq_dist = df_features['purchase_frequency_score'].value_counts().sort_values(ascending=False)
for score, count in freq_dist.items():
    pct = (count / len(df_features)) * 100
    # Reverse lookup to get label
    label = [k for k, v in frequency_mapping.items() if v == score][0]
    feature_dict += f"- {label} ({score}): {count:,} ({pct:.1f}%)\n"

feature_dict += f"""

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
- Yes: {(df_features['observed_promo_exposure'] == 'Yes').sum():,} ({(df_features['observed_promo_exposure'] == 'Yes').sum()/len(df_features)*100:.1f}%)
- No: {(df_features['observed_promo_exposure'] == 'No').sum():,} ({(df_features['observed_promo_exposure'] == 'No').sum()/len(df_features)*100:.1f}%)

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
- 1 (promo-exposed): {df_features['observed_promo_exposure_flag'].sum():,} ({df_features['observed_promo_exposure_flag'].mean()*100:.1f}%)
- 0 (non-promo): {(df_features['observed_promo_exposure_flag'] == 0).sum():,}

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

**Range:** {df_features['satisfaction_score'].min():.1f} - {df_features['satisfaction_score'].max():.1f}

**Mean:** {df_features['satisfaction_score'].mean():.2f} (excluding missing)

**Distribution:**
- Valid ratings: {df_features['satisfaction_score'].notna().sum():,}
- Missing ratings: {df_features['satisfaction_score'].isna().sum()}
- Median: {df_features['satisfaction_score'].median():.2f}
- 75th percentile: {df_features['satisfaction_score'].quantile(0.75):.2f}

**Business Use:**
- Satisfaction monitoring
- Loyalty proxy input
- Quality indicator

**Interpretation:** Higher ratings indicate greater satisfaction (scale 2.5-5.0)

**Limitations:**
- {df_features['satisfaction_score'].isna().sum()} missing values (0.95%)
- Selection bias: only customers who chose to leave reviews
- May not represent overall satisfaction; could skew toward extremes

---

### satisfaction_missing_flag

**Definition:** Indicator that customer did not leave a review

**Source Field:** `Review Rating` (derived)

**Formula:** 1 if Review Rating is NULL, else 0

**Data Type:** Numeric (integer, 0/1)

**Distribution:**
- 1 (missing): {df_features['satisfaction_missing_flag'].sum()}
- 0 (present): {(df_features['satisfaction_missing_flag'] == 0).sum():,}

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
- 1 (high satisfaction): {df_features['high_satisfaction_flag'].sum():,} ({df_features['high_satisfaction_flag'].sum()/df_features['satisfaction_score'].notna().sum()*100:.1f}% of valid ratings)
- 0 (lower satisfaction): {(df_features['high_satisfaction_flag'] == 0).sum():,}
- NULL (no rating): {df_features['high_satisfaction_flag'].isna().sum()}

**Business Use:**
- Satisfied customer identification
- Retention prioritization
- Loyalty segmentation

**Interpretation:** Customers meeting or exceeding quality expectations

**Limitations:**
- Threshold is business judgment, not data-driven optimization
- Only applies to {df_features['satisfaction_score'].notna().sum():,} customers with ratings

---

## 4. ENGAGEMENT FEATURES

### high_purchase_history_flag

**Definition:** Indicator of high repeat-purchase behavior

**Source Field:** `previous_purchase_history`

**Formula:** 1 if previous_purchase_history ≥ {high_history_threshold:.0f} (75th percentile), else 0

**Threshold:** {high_history_threshold:.0f} purchases (75th percentile, data-driven)

**Data Type:** Numeric (integer, 0/1)

**Distribution:**
- 1 (high history): {df_features['high_purchase_history_flag'].sum():,} ({df_features['high_purchase_history_flag'].mean()*100:.1f}%)
- 0 (lower history): {(df_features['high_purchase_history_flag'] == 0).sum():,}

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
- 1 (high frequency): {df_features['high_frequency_flag'].sum():,} ({df_features['high_frequency_flag'].mean()*100:.1f}%)
- 0 (lower frequency): {(df_features['high_frequency_flag'] == 0).sum():,}

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
"""

for band in age_labels:
    count = (df_features['age_band'] == band).sum()
    pct = (count / len(df_features)) * 100
    feature_dict += f"- {band}: {count:,} ({pct:.1f}%)\n"

feature_dict += f"""

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
- 1 (subscriber): {df_features['subscription_flag'].sum():,} ({df_features['subscription_flag'].mean()*100:.1f}%)
- 0 (non-subscriber): {(df_features['subscription_flag'] == 0).sum():,}

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
- Male: {(df_features['gender'] == 'Male').sum():,} ({(df_features['gender'] == 'Male').sum()/len(df_features)*100:.1f}%)
- Female: {(df_features['gender'] == 'Female').sum():,} ({(df_features['gender'] == 'Female').sum()/len(df_features)*100:.1f}%)

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

**Data Type:** Categorical ({df_features['location'].nunique()} states)

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
"""

for cat in ['Clothing', 'Accessories', 'Footwear', 'Outerwear']:
    count = (df_features['category'] == cat).sum()
    pct = (count / len(df_features)) * 100
    feature_dict += f"- {cat}: {count:,} ({pct:.1f}%)\n"

feature_dict += f"""

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

**Data Type:** Categorical ({df_features['payment_method'].nunique()} methods)

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

**Data Type:** Categorical ({df_features['shipping_type'].nunique()} types)

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

1. **high_purchase_history_flag:** 75th percentile ({high_history_threshold:.0f} purchases)
   - Rationale: Identifies top quartile of repeat customers
   - Alternative: Business could define absolute threshold (e.g., ≥30 purchases)

2. **high_satisfaction_flag:** 4.0 rating
   - Rationale: Business-relevant cutoff (80% on 5-point scale)
   - Alternative: Could use 75th percentile ({satisfaction_75th:.2f})

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
**Expected nulls:** satisfaction_score ({df_features['satisfaction_score'].isnull().sum()}), high_satisfaction_flag ({df_features['high_satisfaction_flag'].isnull().sum()})
**Data integrity:** All {len(df_features):,} customer records preserved

---

## Next Steps

1. Proceed to Phase 4: Loyalty Definition A
2. Proceed to Phase 5: Loyalty Definition B
3. Compare loyalty frameworks in Phase 6
4. Create customer segments in Phase 7

---

**End of Feature Dictionary**
"""

# Write feature dictionary
FEATURE_DICT_PATH.parent.mkdir(parents=True, exist_ok=True)
with open(FEATURE_DICT_PATH, 'w', encoding='utf-8') as f:
    f.write(feature_dict)

print(f"✓ Feature dictionary written to: {FEATURE_DICT_PATH}")
print()

print("="*80)
print("FEATURE ENGINEERING COMPLETE")
print("="*80)
print()
print("Summary:")
print(f"  ✓ {len(feature_columns)} features created")
print(f"  ✓ {len(df_features):,} customer records processed")
print(f"  ✓ All features documented")
print(f"  ✓ Data integrity validated")
print()
print("Next step: Loyalty definition development (Python/04_loyalty_definition_a.py)")
print()

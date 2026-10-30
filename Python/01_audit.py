"""
Data Audit Script for D2C Fashion Customer Intelligence Project
================================================================

Purpose: Comprehensive audit of raw customer transaction dataset
Author: Analytics Engineering Team
Date: 2026-08-27

CRITICAL RULES:
- DO NOT modify raw data
- DO NOT create loyalty scores
- DO NOT create customer segments
- DO NOT recommend marketing actions
- DO NOT make causal claims
"""

import pandas as pd
import numpy as np
from pathlib import Path
import warnings
import sys
import io

# Fix Windows console encoding issues
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

warnings.filterwarnings('ignore')

# File paths
RAW_DATA_PATH = Path("Raw_Data/Dataset.csv")
OUTPUT_PATH = Path("Documentation/02_Data_Audit.md")

print("="*80)
print("D2C FASHION CUSTOMER DATA AUDIT")
print("="*80)
print()

# ============================================================================
# 1. LOAD DATA
# ============================================================================
print("Loading dataset...")
df = pd.read_csv(RAW_DATA_PATH)
print(f"✓ Dataset loaded successfully\n")

# ============================================================================
# 2. BASIC DATASET PROFILE
# ============================================================================
print("="*80)
print("BASIC DATASET PROFILE")
print("="*80)

n_rows = len(df)
n_cols = len(df.columns)
n_unique_customers = df['Customer ID'].nunique()
is_customer_id_unique = df['Customer ID'].is_unique

print(f"Number of rows: {n_rows:,}")
print(f"Number of columns: {n_cols}")
print(f"Unique Customer IDs: {n_unique_customers:,}")
print(f"Is Customer ID unique? {is_customer_id_unique}")
print()

# Determine grain
if is_customer_id_unique:
    grain = "One row per customer (customer-level)"
else:
    transactions_per_customer = df.groupby('Customer ID').size()
    print(f"Min transactions per customer: {transactions_per_customer.min()}")
    print(f"Max transactions per customer: {transactions_per_customer.max()}")
    print(f"Mean transactions per customer: {transactions_per_customer.mean():.2f}")
    grain = "One row per transaction (transaction-level)"

print(f"\nLikely grain: {grain}")
print()

# ============================================================================
# 3. COLUMN INVENTORY
# ============================================================================
print("="*80)
print("COLUMN INVENTORY")
print("="*80)
print(f"\nColumns ({n_cols}):")
for i, col in enumerate(df.columns, 1):
    print(f"{i:2d}. {col}")
print()

# ============================================================================
# 4. DATA TYPES
# ============================================================================
print("="*80)
print("DATA TYPES")
print("="*80)
print()
dtype_summary = pd.DataFrame({
    'Column': df.columns,
    'Data Type': df.dtypes.values,
    'Non-Null Count': df.count().values,
    'Null Count': df.isnull().sum().values
})
print(dtype_summary.to_string(index=False))
print()

# ============================================================================
# 5. MISSING VALUES ANALYSIS
# ============================================================================
print("="*80)
print("MISSING VALUES ANALYSIS")
print("="*80)
print()

missing_summary = pd.DataFrame({
    'Column': df.columns,
    'Missing Count': df.isnull().sum().values,
    'Missing %': (df.isnull().sum() / len(df) * 100).values
})
missing_summary = missing_summary[missing_summary['Missing Count'] > 0].sort_values('Missing Count', ascending=False)

if len(missing_summary) > 0:
    print("Columns with missing values:")
    print(missing_summary.to_string(index=False))
else:
    print("No missing values found in any column")
print()

# ============================================================================
# 6. DUPLICATE RECORDS
# ============================================================================
print("="*80)
print("DUPLICATE RECORDS ANALYSIS")
print("="*80)
print()

# Full row duplicates
full_duplicates = df.duplicated().sum()
print(f"Full duplicate rows: {full_duplicates}")

# Customer ID duplicates
customer_id_duplicates = df['Customer ID'].duplicated().sum()
print(f"Duplicate Customer IDs: {customer_id_duplicates}")

if customer_id_duplicates > 0:
    print(f"\nCustomers with multiple records: {df['Customer ID'].value_counts().gt(1).sum()}")
    print("\nTop 10 customers by transaction count:")
    print(df['Customer ID'].value_counts().head(10))
print()

# ============================================================================
# 7. CATEGORICAL VARIABLES ANALYSIS
# ============================================================================
print("="*80)
print("CATEGORICAL VARIABLES ANALYSIS")
print("="*80)
print()

categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
# Remove Customer ID from categorical analysis
if 'Customer ID' in categorical_cols:
    categorical_cols.remove('Customer ID')

for col in categorical_cols:
    n_unique = df[col].nunique()
    print(f"\n{col}")
    print("-" * len(col))
    print(f"Unique values: {n_unique}")

    if n_unique <= 50:  # Show value counts for reasonable cardinality
        value_counts = df[col].value_counts()
        print("\nValue distribution:")
        for val, count in value_counts.items():
            pct = (count / len(df)) * 100
            print(f"  {val}: {count:,} ({pct:.1f}%)")
    else:
        print(f"(Too many unique values to display - showing top 10)")
        value_counts = df[col].value_counts().head(10)
        for val, count in value_counts.items():
            pct = (count / len(df)) * 100
            print(f"  {val}: {count:,} ({pct:.1f}%)")

print()

# ============================================================================
# 8. NUMERIC VARIABLES ANALYSIS
# ============================================================================
print("="*80)
print("NUMERIC VARIABLES ANALYSIS")
print("="*80)
print()

numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

for col in numeric_cols:
    print(f"\n{col}")
    print("-" * len(col))

    stats = df[col].describe()
    print(f"Count: {stats['count']:.0f}")
    print(f"Mean: {stats['mean']:.2f}")
    print(f"Std Dev: {stats['std']:.2f}")
    print(f"Min: {stats['min']:.2f}")
    print(f"25th percentile: {stats['25%']:.2f}")
    print(f"Median (50th): {stats['50%']:.2f}")
    print(f"75th percentile: {stats['75%']:.2f}")
    print(f"Max: {stats['max']:.2f}")

    # Outlier detection using IQR method
    Q1 = stats['25%']
    Q3 = stats['75%']
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    outliers_low = (df[col] < lower_bound).sum()
    outliers_high = (df[col] > upper_bound).sum()
    total_outliers = outliers_low + outliers_high

    if total_outliers > 0:
        print(f"\nPotential outliers (IQR method):")
        print(f"  Below {lower_bound:.2f}: {outliers_low}")
        print(f"  Above {upper_bound:.2f}: {outliers_high}")
        print(f"  Total: {total_outliers} ({(total_outliers/len(df)*100):.1f}%)")

print()

# ============================================================================
# 9. SEMANTIC DUPLICATION INVESTIGATION
# ============================================================================
print("="*80)
print("SEMANTIC DUPLICATION INVESTIGATION")
print("="*80)
print()

print("INVESTIGATION 1: Discount Applied vs Promo Code Used")
print("-" * 60)
discount_promo_crosstab = pd.crosstab(
    df['Discount Applied'],
    df['Promo Code Used'],
    margins=True
)
print(discount_promo_crosstab)
print()

# Check if they're identical
discount_promo_match = (df['Discount Applied'] == df['Promo Code Used']).sum()
discount_promo_mismatch = (df['Discount Applied'] != df['Promo Code Used']).sum()
print(f"Matching values: {discount_promo_match:,} ({discount_promo_match/len(df)*100:.1f}%)")
print(f"Mismatching values: {discount_promo_mismatch:,} ({discount_promo_mismatch/len(df)*100:.1f}%)")
print()

if discount_promo_mismatch > 0:
    print("Sample mismatches:")
    mismatches = df[df['Discount Applied'] != df['Promo Code Used']][
        ['Customer ID', 'Discount Applied', 'Promo Code Used']
    ].head(10)
    print(mismatches.to_string(index=False))
print()

print("\nINVESTIGATION 2: Quarterly vs Every 3 Months")
print("-" * 60)
freq_counts = df['Frequency of Purchases'].value_counts()
print("Frequency of Purchases distribution:")
print(freq_counts)
print()

has_quarterly = 'Quarterly' in df['Frequency of Purchases'].values
has_every_3_months = 'Every 3 Months' in df['Frequency of Purchases'].values
print(f"Has 'Quarterly': {has_quarterly}")
print(f"Has 'Every 3 Months': {has_every_3_months}")

if has_quarterly and has_every_3_months:
    quarterly_count = (df['Frequency of Purchases'] == 'Quarterly').sum()
    every_3_months_count = (df['Frequency of Purchases'] == 'Every 3 Months').sum()
    print(f"\n'Quarterly': {quarterly_count:,}")
    print(f"'Every 3 Months': {every_3_months_count:,}")
    print("\n⚠️  SEMANTIC DUPLICATION: These represent the same frequency")
print()

print("\nINVESTIGATION 3: Bi-Weekly vs Fortnightly")
print("-" * 60)
has_biweekly = 'Bi-Weekly' in df['Frequency of Purchases'].values
has_fortnightly = 'Fortnightly' in df['Frequency of Purchases'].values
print(f"Has 'Bi-Weekly': {has_biweekly}")
print(f"Has 'Fortnightly': {has_fortnightly}")

if has_biweekly and has_fortnightly:
    biweekly_count = (df['Frequency of Purchases'] == 'Bi-Weekly').sum()
    fortnightly_count = (df['Frequency of Purchases'] == 'Fortnightly').sum()
    print(f"\n'Bi-Weekly': {biweekly_count:,}")
    print(f"'Fortnightly': {fortnightly_count:,}")
    print("\n⚠️  SEMANTIC DUPLICATION: These represent the same frequency")
print()

# ============================================================================
# 10. DATA QUALITY ISSUES
# ============================================================================
print("="*80)
print("DATA QUALITY ISSUES")
print("="*80)
print()

quality_issues = []

# Check for inconsistent categorical values
print("Checking for data quality issues...\n")

# Age range check
age_min = df['Age'].min()
age_max = df['Age'].max()
if age_min < 0 or age_max > 120:
    quality_issues.append(f"Age: Suspicious range ({age_min} to {age_max})")
    print(f"⚠️  Age range: {age_min} to {age_max}")

# Purchase Amount check
purchase_min = df['Purchase Amount (USD)'].min()
purchase_max = df['Purchase Amount (USD)'].max()
if purchase_min < 0:
    quality_issues.append(f"Purchase Amount: Negative values found")
    print(f"⚠️  Purchase Amount: Contains negative values")

# Review Rating check
if 'Review Rating' in df.columns:
    rating_min = df['Review Rating'].min()
    rating_max = df['Review Rating'].max()
    print(f"Review Rating range: {rating_min} to {rating_max}")
    if rating_min < 0 or rating_max > 5:
        quality_issues.append(f"Review Rating: Out of typical 0-5 range")
        print(f"⚠️  Review Rating outside typical range")

# Previous Purchases check
prev_purchases_negative = (df['Previous Purchases'] < 0).sum()
if prev_purchases_negative > 0:
    quality_issues.append(f"Previous Purchases: {prev_purchases_negative} negative values")
    print(f"⚠️  Previous Purchases: {prev_purchases_negative} negative values")

# Check for whitespace issues in categorical columns
for col in categorical_cols:
    if df[col].dtype == 'object':
        has_leading_space = df[col].astype(str).str.startswith(' ').sum()
        has_trailing_space = df[col].astype(str).str.endswith(' ').sum()
        if has_leading_space > 0 or has_trailing_space > 0:
            quality_issues.append(f"{col}: Whitespace issues detected")
            print(f"⚠️  {col}: Leading/trailing whitespace found")

if len(quality_issues) == 0:
    print("✓ No major data quality issues detected")

print()

# ============================================================================
# 11. FIELDS REQUIRING NORMALIZATION
# ============================================================================
print("="*80)
print("FIELDS REQUIRING NORMALIZATION")
print("="*80)
print()

normalization_candidates = []

# Semantic duplicates in Frequency of Purchases
if has_quarterly and has_every_3_months:
    normalization_candidates.append({
        'Field': 'Frequency of Purchases',
        'Issue': 'Quarterly vs Every 3 Months',
        'Action': 'Standardize to single term (recommend: Quarterly)'
    })

if has_biweekly and has_fortnightly:
    normalization_candidates.append({
        'Field': 'Frequency of Purchases',
        'Issue': 'Bi-Weekly vs Fortnightly',
        'Action': 'Standardize to single term (recommend: Bi-Weekly)'
    })

# Check if Discount Applied and Promo Code Used are redundant
if discount_promo_match == len(df):
    normalization_candidates.append({
        'Field': 'Discount Applied / Promo Code Used',
        'Issue': 'Perfectly correlated - appears to be duplicate information',
        'Action': 'Evaluate if one field can be removed or if they represent different concepts'
    })

for candidate in normalization_candidates:
    print(f"Field: {candidate['Field']}")
    print(f"  Issue: {candidate['Issue']}")
    print(f"  Recommended action: {candidate['Action']}")
    print()

if len(normalization_candidates) == 0:
    print("No normalization issues identified")
    print()

# ============================================================================
# 12. ANALYTICAL CAPABILITY MAPPING
# ============================================================================
print("="*80)
print("ANALYTICAL CAPABILITY MAPPING")
print("="*80)
print()

print("CUSTOMER VALUE ANALYSIS")
print("-" * 40)
print("Available variables:")
print("  • Purchase Amount (USD) - transaction value")
print("  • Previous Purchases - historical count")
print("  • Frequency of Purchases - purchase cadence")
print("  • Subscription Status - indicates recurring relationship")
print()

print("LOYALTY PROXIES")
print("-" * 40)
print("Available variables:")
print("  • Previous Purchases - engagement depth")
print("  • Frequency of Purchases - purchase regularity")
print("  • Subscription Status - commitment indicator")
print("  • Review Rating - satisfaction/engagement proxy")
print()

print("PROMOTIONAL EXPOSURE ANALYSIS")
print("-" * 40)
print("Available variables:")
print("  • Discount Applied - promotional offer received")
print("  • Promo Code Used - promotional offer utilized")
print()

print("SATISFACTION ANALYSIS")
print("-" * 40)
print("Available variables:")
print("  • Review Rating - explicit satisfaction measure")
print()

print("GEOGRAPHY ANALYSIS")
print("-" * 40)
print("Available variables:")
print("  • Location - state-level geography")
print()

print("CATEGORY ANALYSIS")
print("-" * 40)
print("Available variables:")
print("  • Category - product category")
print("  • Item Purchased - specific item")
print("  • Size - product size")
print("  • Color - product color")
print("  • Season - seasonal attribution")
print()

print("FULFILLMENT ANALYSIS")
print("-" * 40)
print("Available variables:")
print("  • Shipping Type - delivery method")
print()

print("PAYMENT ANALYSIS")
print("-" * 40)
print("Available variables:")
print("  • Payment Method - payment type")
print()

print("DEMOGRAPHIC ANALYSIS")
print("-" * 40)
print("Available variables:")
print("  • Age - customer age")
print("  • Gender - customer gender")
print()

# ============================================================================
# 13. ANALYTICAL LIMITATIONS
# ============================================================================
print("="*80)
print("ANALYTICAL LIMITATIONS")
print("="*80)
print()

limitations = [
    "TEMPORAL: No transaction date - cannot analyze trends over time",
    "TEMPORAL: Cannot determine recency of purchases",
    "TEMPORAL: Cannot calculate time between purchases",
    "TEMPORAL: Cannot perform cohort analysis",
    "TEMPORAL: Frequency of Purchases is stated preference, not observed behavior",
    "FINANCIAL: No cost/margin data - cannot calculate profitability",
    "FINANCIAL: Cannot separate discount amount from base price",
    "BEHAVIORAL: Previous Purchases is a count only - no detail on what was purchased",
    "BEHAVIORAL: No cart/browse data - cannot analyze conversion",
    "CAUSAL: Cannot establish causation between discount and purchase",
    "CAUSAL: Cannot determine if subscription drives higher spend or vice versa",
    "GRANULARITY: Location is state-level only - cannot analyze by city/region",
    "GRANULARITY: Season may be purchase season or product season (ambiguous)"
]

for i, limitation in enumerate(limitations, 1):
    print(f"{i:2d}. {limitation}")

print()

# ============================================================================
# 14. QUESTIONS THAT CANNOT BE ANSWERED
# ============================================================================
print("="*80)
print("QUESTIONS THAT CANNOT BE LEGITIMATELY ANSWERED")
print("="*80)
print()

unanswerable = [
    "What is customer lifetime value? (no time dimension or future projection capability)",
    "Are customers becoming more or less engaged over time? (no dates)",
    "What is the customer churn rate? (no dates, no way to define churn window)",
    "How long does it take customers to make a repeat purchase? (no dates)",
    "What is the year-over-year growth? (no dates)",
    "Which marketing campaign drove the most sales? (no campaign identifier)",
    "What is the return/refund rate? (no return data)",
    "What is the customer acquisition cost efficiency? (no cost data)",
    "What is the profit margin by customer? (no cost data)",
    "Did discounts cause increased purchase amounts? (correlation ≠ causation, no experiment)",
    "Will subscription customers spend more in the future? (no predictive features)",
    "Why do customers choose specific payment methods? (no survey/preference data)",
    "What is the impact of shipping type on satisfaction? (confounded by many factors)",
    "Which product categories are growing? (no time dimension)",
    "What is the customer journey? (single transaction per customer if grain is customer-level)"
]

for i, question in enumerate(unanswerable, 1):
    print(f"{i:2d}. {question}")

print()
print("="*80)
print("AUDIT COMPLETE")
print("="*80)
print()

# ============================================================================
# GENERATE MARKDOWN DOCUMENTATION
# ============================================================================
print("Generating markdown documentation...")

md_content = f"""# Data Audit Report
**D2C Fashion Customer Intelligence Project**

**Date:** 2026-08-27
**Analyst:** Analytics Engineering Team
**Source:** `Raw_Data/Dataset.csv`

---

## Executive Summary

This audit examines a dataset of **{n_rows:,} records** with **{n_cols} variables** representing customer transactions from a D2C fashion retailer.

**Key Findings:**
- Dataset grain: {grain}
- Unique customers: {n_unique_customers:,}
- Data quality: {"Minor issues identified" if len(quality_issues) > 0 else "Good overall quality"}
- Semantic duplications: {"Yes" if len(normalization_candidates) > 0 else "None found"}
- Missing values: {missing_summary['Missing Count'].sum() if len(missing_summary) > 0 else 0} ({(missing_summary['Missing Count'].sum() / (n_rows * n_cols) * 100):.2f}% of all values)

---

## 1. Dataset Profile

### Basic Metrics
| Metric | Value |
|--------|-------|
| Number of rows | {n_rows:,} |
| Number of columns | {n_cols} |
| Unique Customer IDs | {n_unique_customers:,} |
| Customer ID is unique | {is_customer_id_unique} |
| **Dataset grain** | **{grain}** |

### Column List
"""

for i, col in enumerate(df.columns, 1):
    md_content += f"{i}. {col}\n"

md_content += """
---

## 2. Data Types

| Column | Data Type | Non-Null Count | Null Count |
|--------|-----------|----------------|------------|
"""

for _, row in dtype_summary.iterrows():
    md_content += f"| {row['Column']} | {row['Data Type']} | {row['Non-Null Count']:,} | {row['Null Count']} |\n"

md_content += """
---

## 3. Missing Values Analysis

"""

if len(missing_summary) > 0:
    md_content += "| Column | Missing Count | Missing % |\n"
    md_content += "|--------|---------------|----------|\n"
    for _, row in missing_summary.iterrows():
        md_content += f"| {row['Column']} | {row['Missing Count']} | {row['Missing %']:.2f}% |\n"

    md_content += "\n**Impact Assessment:**\n"
    for _, row in missing_summary.iterrows():
        if row['Column'] == 'Review Rating':
            md_content += f"- **{row['Column']}**: {row['Missing Count']} missing ({row['Missing %']:.2f}%). May indicate not all customers leave reviews. Consider this bias in satisfaction analysis.\n"
else:
    md_content += "✓ **No missing values detected in any column.**\n"

md_content += """
---

## 4. Duplicate Records

"""

if customer_id_duplicates > 0:
    md_content += f"- **Full duplicate rows:** {full_duplicates}\n"
    md_content += f"- **Duplicate Customer IDs:** {customer_id_duplicates:,}\n"
    md_content += f"- **Customers with multiple records:** {df['Customer ID'].value_counts().gt(1).sum():,}\n\n"
    md_content += "**Interpretation:** This is a transaction-level dataset, not customer-level.\n"
else:
    md_content += f"- **Full duplicate rows:** {full_duplicates}\n"
    md_content += f"- **Duplicate Customer IDs:** {customer_id_duplicates}\n\n"
    md_content += "**Interpretation:** Each row represents a unique customer.\n"

md_content += """
---

## 5. Categorical Variables

"""

for col in categorical_cols:
    n_unique = df[col].nunique()
    md_content += f"\n### {col}\n"
    md_content += f"**Unique values:** {n_unique}\n\n"

    if n_unique <= 50:
        md_content += "| Value | Count | % |\n"
        md_content += "|-------|-------|---|\n"
        value_counts = df[col].value_counts()
        for val, count in value_counts.items():
            pct = (count / len(df)) * 100
            md_content += f"| {val} | {count:,} | {pct:.1f}% |\n"
    else:
        md_content += "*(High cardinality - showing top 10)*\n\n"
        md_content += "| Value | Count | % |\n"
        md_content += "|-------|-------|---|\n"
        value_counts = df[col].value_counts().head(10)
        for val, count in value_counts.items():
            pct = (count / len(df)) * 100
            md_content += f"| {val} | {count:,} | {pct:.1f}% |\n"

md_content += """
---

## 6. Numeric Variables

"""

for col in numeric_cols:
    stats = df[col].describe()
    Q1 = stats['25%']
    Q3 = stats['75%']
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    outliers_low = (df[col] < lower_bound).sum()
    outliers_high = (df[col] > upper_bound).sum()
    total_outliers = outliers_low + outliers_high

    md_content += f"\n### {col}\n\n"
    md_content += "| Statistic | Value |\n"
    md_content += "|-----------|-------|\n"
    md_content += f"| Count | {stats['count']:.0f} |\n"
    md_content += f"| Mean | {stats['mean']:.2f} |\n"
    md_content += f"| Std Dev | {stats['std']:.2f} |\n"
    md_content += f"| Min | {stats['min']:.2f} |\n"
    md_content += f"| 25th percentile | {stats['25%']:.2f} |\n"
    md_content += f"| Median | {stats['50%']:.2f} |\n"
    md_content += f"| 75th percentile | {stats['75%']:.2f} |\n"
    md_content += f"| Max | {stats['max']:.2f} |\n"

    if total_outliers > 0:
        md_content += f"\n**Outliers (IQR method):**\n"
        md_content += f"- Below {lower_bound:.2f}: {outliers_low}\n"
        md_content += f"- Above {upper_bound:.2f}: {outliers_high}\n"
        md_content += f"- Total: {total_outliers} ({(total_outliers/len(df)*100):.1f}%)\n"

md_content += """
---

## 7. Semantic Duplication Analysis

### Investigation 1: Discount Applied vs Promo Code Used

"""

md_content += f"**Matching records:** {discount_promo_match:,} ({discount_promo_match/len(df)*100:.1f}%)  \n"
md_content += f"**Mismatching records:** {discount_promo_mismatch:,} ({discount_promo_mismatch/len(df)*100:.1f}%)  \n\n"

if discount_promo_match == len(df):
    md_content += "⚠️ **FINDING:** These fields are perfectly correlated. They appear to represent the same information.\n\n"
    md_content += "**Implication:** One field may be redundant unless they represent conceptually different things (offer received vs offer used).\n"
elif discount_promo_mismatch > 0:
    md_content += "**FINDING:** These fields are distinct and carry different information.\n"

md_content += "\n### Investigation 2: Quarterly vs Every 3 Months\n\n"

if has_quarterly and has_every_3_months:
    quarterly_count = (df['Frequency of Purchases'] == 'Quarterly').sum()
    every_3_months_count = (df['Frequency of Purchases'] == 'Every 3 Months').sum()
    md_content += f"- **'Quarterly':** {quarterly_count:,} records\n"
    md_content += f"- **'Every 3 Months':** {every_3_months_count:,} records\n\n"
    md_content += "⚠️ **FINDING:** Semantic duplication detected. These represent identical frequencies.\n\n"
    md_content += "**Recommendation:** Normalize to 'Quarterly' before analysis.\n"
else:
    md_content += "✓ No duplication found.\n"

md_content += "\n### Investigation 3: Bi-Weekly vs Fortnightly\n\n"

if has_biweekly and has_fortnightly:
    biweekly_count = (df['Frequency of Purchases'] == 'Bi-Weekly').sum()
    fortnightly_count = (df['Frequency of Purchases'] == 'Fortnightly').sum()
    md_content += f"- **'Bi-Weekly':** {biweekly_count:,} records\n"
    md_content += f"- **'Fortnightly':** {fortnightly_count:,} records\n\n"
    md_content += "⚠️ **FINDING:** Semantic duplication detected. These represent identical frequencies.\n\n"
    md_content += "**Recommendation:** Normalize to 'Bi-Weekly' before analysis.\n"
else:
    md_content += "✓ No duplication found.\n"

md_content += """
---

## 8. Data Quality Issues

"""

if len(quality_issues) > 0:
    for issue in quality_issues:
        md_content += f"- ⚠️ {issue}\n"
else:
    md_content += "✓ **No major data quality issues detected.**\n"

md_content += """
---

## 9. Fields Requiring Normalization

"""

if len(normalization_candidates) > 0:
    for candidate in normalization_candidates:
        md_content += f"\n**{candidate['Field']}**\n"
        md_content += f"- Issue: {candidate['Issue']}\n"
        md_content += f"- Recommended action: {candidate['Action']}\n"
else:
    md_content += "✓ **No normalization requirements identified.**\n"

md_content += """
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
"""

# Write markdown file
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
    f.write(md_content)

print(f"✓ Documentation written to: {OUTPUT_PATH}")
print()
print("="*80)
print("All outputs generated successfully!")
print("="*80)

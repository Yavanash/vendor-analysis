"""
Category Analysis
==================

Purpose: Profile customer value, loyalty, and behavior by product category
Author: Analytics Engineering Team
Date: 2026-08-27

Analyzes:
- Customer distribution across categories
- Average spend, history, and loyalty by category
- Promo exposure by category
- Subscription rate by category
- Segment composition by category
- Cross-tab of category with key demographic and behavioral variables
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
SEGMENTS_PATH = Path("Outputs/analytical/customer_segments.csv")
OUTPUT_PATH = Path("Outputs/analytical/category_analysis.csv")
DOC_PATH = Path("Documentation/09_Category_Analysis.md")

print("="*80)
print("CATEGORY ANALYSIS")
print("="*80)
print()

# Load data
print("Loading data...")
df = pd.read_csv(SEGMENTS_PATH)
print(f"✓ Loaded {len(df):,} customers")
print(f"  Categories: {df['category'].nunique()}")
print()

# ============================================================================
# CATEGORY OVERVIEW
# ============================================================================
print("="*80)
print("CATEGORY OVERVIEW")
print("="*80)
print()

category_stats = []

for category in sorted(df['category'].unique()):
    cat_df = df[df['category'] == category]

    stats = {
        'Category': category,
        'Customer_Count': len(cat_df),
        'Customer_Pct': len(cat_df) / len(df) * 100,
        'Total_Current_Observed_Spend': cat_df['current_spend'].sum(),
        'Spend_Pct': cat_df['current_spend'].sum() / df['current_spend'].sum() * 100,
        'Avg_Spend': cat_df['current_spend'].mean(),
        'Avg_Previous_Purchases': cat_df['previous_purchase_history'].mean(),
        'Avg_Frequency_Score': cat_df['purchase_frequency_score'].mean(),
        'Promo_Exposure_Pct': cat_df['observed_promo_exposure_flag'].mean() * 100,
        'Avg_Satisfaction': cat_df['satisfaction_score'].mean(),
        'Subscription_Pct': cat_df['subscription_flag'].mean() * 100,
        'Avg_Loyalty_Score': cat_df['loyalty_score_a'].mean()
    }

    category_stats.append(stats)

    print(f"\n{category}")
    print("-" * 60)
    print(f"Customers: {stats['Customer_Count']:,} ({stats['Customer_Pct']:.1f}%)")
    print(f"Current observed spend: ${stats['Total_Current_Observed_Spend']:,.0f} ({stats['Spend_Pct']:.1f}%)")
    print(f"Avg spend: ${stats['Avg_Spend']:.2f}")
    print(f"Avg previous purchases: {stats['Avg_Previous_Purchases']:.1f}")
    print(f"Promo exposure: {stats['Promo_Exposure_Pct']:.1f}%")
    print(f"Avg satisfaction: {stats['Avg_Satisfaction']:.2f}")
    print(f"Subscription rate: {stats['Subscription_Pct']:.1f}%")
    print(f"Avg loyalty score (A): {stats['Avg_Loyalty_Score']:.2f}")

print()

df_category_stats = pd.DataFrame(category_stats)

# ============================================================================
# CATEGORY RANKINGS
# ============================================================================
print("="*80)
print("CATEGORY RANKINGS")
print("="*80)
print()

print("Ranked by Average Previous Purchase History (higher = more repeat behavior):")
history_rank = df_category_stats.sort_values('Avg_Previous_Purchases', ascending=False)
for _, row in history_rank.iterrows():
    print(f"  {row['Category']:>15}: {row['Avg_Previous_Purchases']:.1f}")
print()

print("Ranked by Avg Loyalty Score (Definition A):")
loyal_rank = df_category_stats.sort_values('Avg_Loyalty_Score', ascending=False)
for _, row in loyal_rank.iterrows():
    print(f"  {row['Category']:>15}: {row['Avg_Loyalty_Score']:.2f}")
print()

print("Ranked by Promo Exposure (lowest = most brand-pull):")
promo_rank = df_category_stats.sort_values('Promo_Exposure_Pct')
for _, row in promo_rank.iterrows():
    print(f"  {row['Category']:>15}: {row['Promo_Exposure_Pct']:.1f}%")
print()

print("Ranked by Subscription Rate:")
sub_rank = df_category_stats.sort_values('Subscription_Pct', ascending=False)
for _, row in sub_rank.iterrows():
    print(f"  {row['Category']:>15}: {row['Subscription_Pct']:.1f}%")
print()

# ============================================================================
# SEGMENT COMPOSITION BY CATEGORY
# ============================================================================
print("="*80)
print("SEGMENT COMPOSITION BY CATEGORY")
print("="*80)
print()

segment_order = [
    'Core Loyalists',
    'Emerging Loyalists',
    'Developing Loyalists',
    'Promo-Engaged Repeaters',
    'Early-Stage Customers',
    'Promo-Exposed Transactors'
]

ct = pd.crosstab(df['category'], df['segment'], normalize='index') * 100
ct = ct[segment_order]

print("Segment % within each category:")
print("-" * 80)
print(ct.round(1).to_string())
print()

# ============================================================================
# CATEGORY × DEMOGRAPHIC CROSS-TABS
# ============================================================================
print("="*80)
print("CATEGORY × AGE BAND")
print("="*80)
print()

age_cat = pd.crosstab(df['category'], df['age_band'], normalize='index') * 100
print(age_cat.round(1).to_string())
print()

print("="*80)
print("CATEGORY × GENDER")
print("="*80)
print()

gender_cat = pd.crosstab(df['category'], df['gender'], normalize='index') * 100
print(gender_cat.round(1).to_string())
print()

# ============================================================================
# SAVE OUTPUTS
# ============================================================================
print("="*80)
print("SAVING OUTPUTS")
print("="*80)
print()

# Save category stats
df_category_stats.to_csv(OUTPUT_PATH, index=False)
print(f"✓ Category analysis saved to: {OUTPUT_PATH}")

# Save segment composition
segment_comp_path = Path("Archive/legacy_compositions/category_segment_composition.csv")
ct.to_csv(segment_comp_path)
print(f"✓ Segment composition saved to: {segment_comp_path}")

# Save age cross-tab
age_path = Path("Archive/legacy_compositions/category_age_composition.csv")
age_cat.to_csv(age_path)
print(f"✓ Age composition saved to: {age_path}")

# Save gender cross-tab
gender_path = Path("Archive/legacy_compositions/category_gender_composition.csv")
gender_cat.to_csv(gender_path)
print(f"✓ Gender composition saved to: {gender_path}")
print()

# ============================================================================
# GENERATE DOCUMENTATION
# ============================================================================

doc_content = f"""# Category Analysis
**D2C Fashion Customer Intelligence Project**

**Date:** 2026-08-27
**Framework:** Loyalty Definition A + Segmentation

---

## Overview

Category profiling of {len(df):,} customers across {df['category'].nunique()} product categories.

**Key Questions:**
- Which categories attract highest-value repeat customers?
- Which categories are most/least promo-driven?
- Where is subscription penetration strongest?

---

## Category Profiles

"""

for stats in sorted(category_stats, key=lambda x: x['Customer_Count'], reverse=True):
    doc_content += f"""### {stats['Category']}

| Metric | Value |
|--------|-------|
| Customers | {stats['Customer_Count']:,} ({stats['Customer_Pct']:.1f}%) |
| Total Current Observed Spend | ${stats['Total_Current_Observed_Spend']:,.0f} ({stats['Spend_Pct']:.1f}%) |
| Avg Spend | ${stats['Avg_Spend']:.2f} |
| Avg Previous Purchases | {stats['Avg_Previous_Purchases']:.1f} |
| Avg Frequency Score | {stats['Avg_Frequency_Score']:.2f} |
| Promo Exposure | {stats['Promo_Exposure_Pct']:.1f}% |
| Avg Satisfaction | {stats['Avg_Satisfaction']:.2f} |
| Subscription Rate | {stats['Subscription_Pct']:.1f}% |
| Avg Loyalty Score (A) | {stats['Avg_Loyalty_Score']:.2f} |

"""

doc_content += f"""---

## Key Findings

### Highest Repeat Purchase History

| Category | Avg Previous Purchases |
|----------|----------------------|
"""
for _, row in history_rank.iterrows():
    doc_content += f"| {row['Category']} | {row['Avg_Previous_Purchases']:.1f} |\n"

doc_content += f"""
### Highest Loyalty Score (Definition A)

| Category | Avg Loyalty Score |
|----------|------------------|
"""
for _, row in loyal_rank.iterrows():
    doc_content += f"| {row['Category']} | {row['Avg_Loyalty_Score']:.2f} |\n"

doc_content += f"""
### Lowest Promo Exposure (Highest Brand Pull)

| Category | Promo Exposure |
|----------|---------------|
"""
for _, row in promo_rank.iterrows():
    doc_content += f"| {row['Category']} | {row['Promo_Exposure_Pct']:.1f}% |\n"

doc_content += f"""
### Highest Subscription Rate

| Category | Subscription Rate |
|----------|------------------|
"""
for _, row in sub_rank.iterrows():
    doc_content += f"| {row['Category']} | {row['Subscription_Pct']:.1f}% |\n"

doc_content += f"""
---

## Segment Composition by Category

| Category | { ' | '.join(segment_order) } |
|----------|{'|'.join(['---'] * len(segment_order))}|
"""

for category in sorted(df['category'].unique()):
    row = ct.loc[category]
    doc_content += f"| {category} | { ' | '.join([f'{row[s]:.1f}%' for s in segment_order]) } |\n"

doc_content += f"""
---

## Category × Demographics

### Category × Age Band

| Category | { ' | '.join(sorted(df['age_band'].dropna().unique())) } |
|----------|{'|'.join(['---'] * len(df['age_band'].dropna().unique()))}|
"""

for category in sorted(df['category'].unique()):
    row = age_cat.loc[category]
    doc_content += f"| {category} | { ' | '.join([f'{row[b]:.1f}%' for b in sorted(df['age_band'].dropna().unique())]) } |\n"

doc_content += f"""
### Category × Gender

| Category | { ' | '.join(sorted(df['gender'].unique())) } |
|----------|{'|'.join(['---'] * len(df['gender'].unique()))}|
"""

for category in sorted(df['category'].unique()):
    row = gender_cat.loc[category]
    doc_content += f"| {category} | { ' | '.join([f'{row[g]:.1f}%' for g in sorted(df['gender'].unique())]) } |\n"

doc_content += f"""
---

## Strategic Implications

### High-Engagement Categories
- Categories with high repeat purchase history and loyalty scores indicate strong customer attachment
- Lower promo exposure in these categories suggests organic demand
- Candidates for premium positioning and reduced discounting

### Promo-Dependent Categories
- High promo exposure rates indicate reliance on discounts to drive transactions
- Risk of revenue volatility if promotional strategy shifts
- Consider gradual value-building alternatives (bundles, loyalty programs)

### Subscription Categories
- High subscription rates indicate recurring revenue potential
- Strong candidates for subscription expansion
- Prioritize retention in these categories

### Cross-Category Insights
- Underleveraged categories may benefit from targeted engagement
- Avoid blanket promo strategies across all categories
- Consider category-specific marketing approaches

---

## Limitations

1. **Single transaction per customer:** Cannot track cross-category purchase behavior
2. **No category migration data:** Cannot identify customers shifting between categories
3. **Self-reported satisfaction:** Single rating, not category-specific
4. **No revenue cost data:** Cannot calculate category margin or true CLV
5. **No seasonality:** Cannot identify category-specific seasonal patterns

---

## Usage Guidelines

### For Strategy
- Use high-loyalty categories to test selective promo reduction
- Avoid promo cuts in promo-dependent categories
- Prioritize subscription growth in high-subscription categories

### For Analysis
- Cross-reference with geographic and demographic patterns
- Track category mix over time (requires future snapshots)
- Investigate satisfaction drivers within categories

### For Reporting
- Frame category findings as observed associations
- Avoid causal claims about category → loyalty
- Include sample sizes in all category comparisons

---

**End of Category Analysis**
"""

DOC_PATH.parent.mkdir(parents=True, exist_ok=True)
with open(DOC_PATH, 'w', encoding='utf-8') as f:
    f.write(doc_content)

print(f"✓ Category analysis saved to: {DOC_PATH}")
print()

print("="*80)
print("CATEGORY ANALYSIS COMPLETE")
print("="*80)
print()
print(f"✓ {df['category'].nunique()} categories profiled")
print(f"✓ Segment composition mapped")
print(f"✓ Demographic cross-tabs generated")
print()
print("Next: SQL scripts (Phase 10)")
print()

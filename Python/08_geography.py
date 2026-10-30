"""
Geographic Analysis
====================

Purpose: Profile customer value, loyalty, and promo behavior by location
Author: Analytics Engineering Team
Date: 2026-08-27

Analyzes:
- Customer distribution across geographies
- Average spend, history, and loyalty score by location
- Promo exposure rates by location
- Segment composition by location
- Identification of underleveraged geographies
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
OUTPUT_PATH = Path("Outputs/analytical/geographic_analysis.csv")
DOC_PATH = Path("Documentation/08_Geographic_Analysis.md")

print("="*80)
print("GEOGRAPHIC ANALYSIS")
print("="*80)
print()

# Load data
print("Loading data...")
df = pd.read_csv(SEGMENTS_PATH)
print(f"✓ Loaded {len(df):,} customers")
print(f"  Locations: {df['location'].nunique()}")
print()

# ============================================================================
# LOCATION OVERVIEW
# ============================================================================
print("="*80)
print("LOCATION OVERVIEW")
print("="*80)
print()

location_stats = []

for location in sorted(df['location'].unique()):
    loc_df = df[df['location'] == location]

    stats = {
        'Location': location,
        'Customer_Count': len(loc_df),
        'Customer_Pct': len(loc_df) / len(df) * 100,
        'Total_Revenue': loc_df['current_spend'].sum(),
        'Revenue_Pct': loc_df['current_spend'].sum() / df['current_spend'].sum() * 100,
        'Avg_Spend': loc_df['current_spend'].mean(),
        'Avg_Previous_Purchases': loc_df['previous_purchase_history'].mean(),
        'Avg_Frequency_Score': loc_df['purchase_frequency_score'].mean(),
        'Promo_Exposure_Pct': loc_df['observed_promo_exposure_flag'].mean() * 100,
        'Avg_Satisfaction': loc_df['satisfaction_score'].mean(),
        'Subscription_Pct': loc_df['subscription_flag'].mean() * 100,
        'Avg_Loyalty_Score': loc_df['loyalty_score_a'].mean()
    }

    location_stats.append(stats)

    print(f"\n{location}")
    print("-" * 60)
    print(f"Customers: {stats['Customer_Count']:,} ({stats['Customer_Pct']:.1f}%)")
    print(f"Revenue: ${stats['Total_Revenue']:,.0f} ({stats['Revenue_Pct']:.1f}%)")
    print(f"Avg spend: ${stats['Avg_Spend']:.2f}")
    print(f"Avg previous purchases: {stats['Avg_Previous_Purchases']:.1f}")
    print(f"Promo exposure: {stats['Promo_Exposure_Pct']:.1f}%")
    print(f"Avg satisfaction: {stats['Avg_Satisfaction']:.2f}")
    print(f"Subscription rate: {stats['Subscription_Pct']:.1f}%")
    print(f"Avg loyalty score (A): {stats['Avg_Loyalty_Score']:.2f}")

print()

df_location_stats = pd.DataFrame(location_stats)

# ============================================================================
# LOCATION RANKINGS
# ============================================================================
print("="*80)
print("LOCATION RANKINGS")
print("="*80)
print()

print("Top 3 by Customer Count:")
top_count = df_location_stats.nlargest(3, 'Customer_Count')[['Location', 'Customer_Count', 'Customer_Pct']]
for _, row in top_count.iterrows():
    print(f"  {row['Location']}: {row['Customer_Count']:,} ({row['Customer_Pct']:.1f}%)")
print()

print("Top 3 by Average Spend:")
top_spend = df_location_stats.nlargest(3, 'Avg_Spend')[['Location', 'Avg_Spend']]
for _, row in top_spend.iterrows():
    print(f"  {row['Location']}: ${row['Avg_Spend']:.2f}")
print()

print("Top 3 by Average Loyalty Score (Definition A):")
top_loyal = df_location_stats.nlargest(3, 'Avg_Loyalty_Score')[['Location', 'Avg_Loyalty_Score']]
for _, row in top_loyal.iterrows():
    print(f"  {row['Location']}: {row['Avg_Loyalty_Score']:.2f}")
print()

print("Top 3 by Promo Exposure (lowest = most brand-pull):")
low_promo = df_location_stats.nsmallest(3, 'Promo_Exposure_Pct')[['Location', 'Promo_Exposure_Pct']]
for _, row in low_promo.iterrows():
    print(f"  {row['Location']}: {row['Promo_Exposure_Pct']:.1f}%")
print()

print("Top 3 by Subscription Rate:")
top_sub = df_location_stats.nlargest(3, 'Subscription_Pct')[['Location', 'Subscription_Pct']]
for _, row in top_sub.iterrows():
    print(f"  {row['Location']}: {row['Subscription_Pct']:.1f}%")
print()

# ============================================================================
# SEGMENT COMPOSITION BY LOCATION
# ============================================================================
print("="*80)
print("SEGMENT COMPOSITION BY LOCATION")
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

# Cross-tab
ct = pd.crosstab(df['location'], df['segment'], normalize='index') * 100
ct = ct[segment_order]

print("Segment % within each location:")
print("-" * 80)
print(ct.round(1).to_string())
print()

# ============================================================================
# COMMERCIAL VALUE OPPORTUNITY
# ============================================================================
print("="*80)
print("COMMERCIAL VALUE OPPORTUNITY ANALYSIS")
print("="*80)
print()

# Calculate: Core Loyalists + Emerging Loyalists share by location
df_location_stats['High_Loyalty_Pct'] = df_location_stats['Location'].apply(
    lambda loc: ((df[df['location'] == loc]['segment'].isin(['Core Loyalists', 'Emerging Loyalists'])).mean()) * 100
)

print("Locations ranked by High-Loyalty Segment Share:")
print("-" * 60)
for _, row in df_location_stats.sort_values('High_Loyalty_Pct', ascending=False).iterrows():
    print(f"  {row['Location']:>12}: {row['High_Loyalty_Pct']:.1f}% high-loyalty")
print()

# ============================================================================
# SAVE OUTPUTS
# ============================================================================
print("="*80)
print("SAVING OUTPUTS")
print("="*80)
print()

# Save location stats
df_location_stats.to_csv(OUTPUT_PATH, index=False)
print(f"✓ Location analysis saved to: {OUTPUT_PATH}")

# Save segment composition
segment_comp_path = Path("Archive/legacy_compositions/geographic_segment_composition.csv")
ct.to_csv(segment_comp_path)
print(f"✓ Segment composition saved to: {segment_comp_path}")
print()

# ============================================================================
# GENERATE DOCUMENTATION
# ============================================================================

doc_content = f"""# Geographic Analysis
**D2C Fashion Customer Intelligence Project**

**Date:** 2026-08-27
**Framework:** Loyalty Definition A + Segmentation

---

## Overview

Geographic profiling of {len(df):,} customers across {df['location'].nunique()} locations.

**Key Questions:**
- Which locations show highest customer value and loyalty?
- Where is promotional exposure highest/lowest?
- Which geographies are commercially underleveraged?

---

## Location Profiles

"""

for stats in sorted(location_stats, key=lambda x: x['Customer_Count'], reverse=True):
    doc_content += f"""### {stats['Location']}

| Metric | Value |
|--------|-------|
| Customers | {stats['Customer_Count']:,} ({stats['Customer_Pct']:.1f}%) |
| Total Revenue | ${stats['Total_Revenue']:,.0f} ({stats['Revenue_Pct']:.1f}%) |
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

### Customer Distribution
"""

top_3_count = df_location_stats.nlargest(3, 'Customer_Count')
for _, row in top_3_count.iterrows():
    doc_content += f"- **{row['Location']}**: {row['Customer_Count']:,} customers ({row['Customer_Pct']:.1f}%)\n"

doc_content += f"""
### Average Spend Leaders
"""
top_3_spend = df_location_stats.nlargest(3, 'Avg_Spend')
for _, row in top_3_spend.iterrows():
    doc_content += f"- **{row['Location']}**: ${row['Avg_Spend']:.2f}\n"

doc_content += f"""
### Loyalty Score Leaders (Definition A)
"""
top_3_loy = df_location_stats.nlargest(3, 'Avg_Loyalty_Score')
for _, row in top_3_loy.iterrows():
    doc_content += f"- **{row['Location']}**: {row['Avg_Loyalty_Score']:.2f}\n"

doc_content += f"""
### Lowest Promo Exposure (Highest Brand Pull)
"""
low_3_promo = df_location_stats.nsmallest(3, 'Promo_Exposure_Pct')
for _, row in low_3_promo.iterrows():
    doc_content += f"- **{row['Location']}**: {row['Promo_Exposure_Pct']:.1f}% promo\n"

doc_content += f"""
### Subscription Leaders
"""
top_3_sub = df_location_stats.nlargest(3, 'Subscription_Pct')
for _, row in top_3_sub.iterrows():
    doc_content += f"- **{row['Location']}**: {row['Subscription_Pct']:.1f}% subscription\n"

doc_content += f"""
---

## Segment Composition by Location

| Location | { ' | '.join(segment_order) } |
|----------|{'|'.join(['---'] * len(segment_order))}|
"""

for location in sorted(df['location'].unique()):
    row = ct.loc[location]
    doc_content += f"| {location} | { ' | '.join([f'{row[s]:.1f}%' for s in segment_order]) } |\n"

doc_content += f"""
---

## High-Loyalty Segment Share

Locations ranked by share of Core Loyalists + Emerging Loyalists (Definition A's top tiers):

| Location | High-Loyalty % |
|----------|---------------|
"""

for _, row in df_location_stats.sort_values('High_Loyalty_Pct', ascending=False).iterrows():
    doc_content += f"| {row['Location']} | {row['High_Loyalty_Pct']:.1f}% |\n"

doc_content += f"""
---

## Strategic Implications

### Mature Markets
- Locations with high Core Loyalists share indicate strong brand pull
- Lower promo exposure in these markets suggests organic retention
- Selective promo reduction may be feasible

### Underleveraged Geographies
- Lower average loyalty scores suggest untapped potential
- May benefit from targeted engagement campaigns
- Avoid heavy discounting to prevent promo dependency

### Promo-Dependent Markets
- High promo exposure rates suggest reliance on discounting
- Risk of revenue volatility if promos reduced
- Gradual value-building strategies recommended

---

## Limitations

1. **No revenue-by-location cost data:** Cannot calculate true margin or LTV
2. **Single snapshot:** No trend analysis possible
3. **Self-reported satisfaction:** Single rating, not validated behavior
4. **No channel data:** Online/offline split unknown
5. **Geographic granularity:** Location-level only, no city/region drilldown

---

## Usage Guidelines

### For Strategy
- Use high-loyalty locations to test selective promo reduction
- Target underleveraged locations with value-driven engagement
- Avoid blanket promo changes across all geographies

### For Analysis
- Cross-reference with category preferences
- Track segment composition changes over time
- Investigate satisfaction drivers in high-promo markets

### For Reporting
- Frame geography findings as observed associations
- Avoid causal claims about location → loyalty relationships
- Include sample sizes in all geographic comparisons

---

**End of Geographic Analysis**
"""

DOC_PATH.parent.mkdir(parents=True, exist_ok=True)
with open(DOC_PATH, 'w', encoding='utf-8') as f:
    f.write(doc_content)

print(f"✓ Geographic analysis saved to: {DOC_PATH}")
print()

print("="*80)
print("GEOGRAPHIC ANALYSIS COMPLETE")
print("="*80)
print()
print(f"✓ {df['location'].nunique()} locations profiled")
print(f"✓ Segment composition mapped")
print(f"✓ Strategic implications documented")
print()
print("Next: Category analysis (Python/09_category.py)")
print()

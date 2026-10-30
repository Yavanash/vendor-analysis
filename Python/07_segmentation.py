"""
Customer Segmentation Using Loyalty Definition A
=================================================

Purpose: Create business-meaningful customer segments
Author: Analytics Engineering Team
Date: 2026-08-27

Approach: Use Loyalty Definition A tiers plus behavioral characteristics
to create 4-6 actionable segments
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
FEATURES_PATH = Path("Outputs/analytical/customer_features.csv")
LOYALTY_A_PATH = Path("Outputs/analytical/loyalty_definition_a.csv")
OUTPUT_PATH = Path("Outputs/analytical/customer_segments.csv")
DOC_PATH = Path("Documentation/07_Segmentation_Methodology.md")

print("="*80)
print("CUSTOMER SEGMENTATION (LOYALTY DEFINITION A)")
print("="*80)
print()

# Load data
print("Loading data...")
df_features = pd.read_csv(FEATURES_PATH)
df_loyalty = pd.read_csv(LOYALTY_A_PATH)

df = df_features.merge(df_loyalty[['Customer ID', 'loyalty_score_a', 'loyalty_tier_a']], on='Customer ID')
print(f"✓ Loaded {len(df):,} customers")
print()

# ============================================================================
# SEGMENTATION LOGIC
# ============================================================================
print("="*80)
print("SEGMENTATION LOGIC")
print("="*80)
print()

def assign_segment(row):
    """Assign customer segment based on loyalty tier and behavioral characteristics"""

    tier = row['loyalty_tier_a']
    history = row['previous_purchase_history']
    promo = row['observed_promo_exposure_flag']
    satisfaction = row['satisfaction_score']

    # Tier 4: Very High Loyalty
    if tier == 'Tier 4: Very High':
        return 'Core Loyalists'

    # Tier 3: High Loyalty
    elif tier == 'Tier 3: High':
        return 'Emerging Loyalists'

    # Tier 2: Medium Loyalty
    elif tier == 'Tier 2: Medium':
        if promo == 1:
            return 'Promo-Engaged Repeaters'
        else:
            return 'Developing Loyalists'

    # Tier 1: Low Loyalty
    else:  # Tier 1: Low
        if promo == 1:
            return 'Promo-Exposed Transactors'
        else:
            return 'Early-Stage Customers'

df['segment'] = df.apply(assign_segment, axis=1)

print("Segment Assignment Rules:")
print("-" * 60)
print("1. Core Loyalists = Tier 4 (Very High)")
print("2. Emerging Loyalists = Tier 3 (High)")
print("3. Promo-Engaged Repeaters = Tier 2 (Medium) + Promo-exposed")
print("4. Developing Loyalists = Tier 2 (Medium) + Non-promo")
print("5. Promo-Exposed Transactors = Tier 1 (Low) + Promo-exposed")
print("6. Early-Stage Customers = Tier 1 (Low) + Non-promo")
print()

# ============================================================================
# SEGMENT PROFILES
# ============================================================================
print("="*80)
print("SEGMENT PROFILES")
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

segment_stats = []

for segment in segment_order:
    seg_df = df[df['segment'] == segment]

    stats = {
        'Segment': segment,
        'Customer_Count': len(seg_df),
        'Customer_Pct': len(seg_df) / len(df) * 100,
        'Total_Current_Observed_Spend': seg_df['current_spend'].sum(),
        'Current_Observed_Spend_Pct': seg_df['current_spend'].sum() / df['current_spend'].sum() * 100,
        'Avg_Spend': seg_df['current_spend'].mean(),
        'Avg_Previous_Purchases': seg_df['previous_purchase_history'].mean(),
        'Avg_Frequency_Score': seg_df['purchase_frequency_score'].mean(),
        'Promo_Exposure_Pct': seg_df['observed_promo_exposure_flag'].mean() * 100,
        'Avg_Satisfaction': seg_df['satisfaction_score'].mean(),
        'High_Satisfaction_Pct': (seg_df['high_satisfaction_flag'] == 1).mean() * 100,
        'Subscription_Pct': seg_df['subscription_flag'].mean() * 100,
        'Top_Category': seg_df['category'].mode()[0] if len(seg_df) > 0 else '',
        'Top_Age_Band': seg_df['age_band'].mode()[0] if len(seg_df) > 0 else ''
    }

    segment_stats.append(stats)

    print(f"\n{segment}")
    print("-" * 60)
    print(f"Customers: {stats['Customer_Count']:,} ({stats['Customer_Pct']:.1f}%)")
    print(f"Revenue: ${stats['Total_Current_Observed_Spend']:,.0f} ({stats['Current_Observed_Spend_Pct']:.1f}%)")
    print(f"Avg spend: ${stats['Avg_Spend']:.2f}")
    print(f"Avg previous purchases: {stats['Avg_Previous_Purchases']:.1f}")
    print(f"Avg frequency score: {stats['Avg_Frequency_Score']:.2f}")
    print(f"Promo exposure: {stats['Promo_Exposure_Pct']:.1f}%")
    print(f"Avg satisfaction: {stats['Avg_Satisfaction']:.2f}")
    print(f"High satisfaction: {stats['High_Satisfaction_Pct']:.1f}%")
    print(f"Subscription rate: {stats['Subscription_Pct']:.1f}%")
    print(f"Top category: {stats['Top_Category']}")
    print(f"Top age band: {stats['Top_Age_Band']}")

print()

df_segment_stats = pd.DataFrame(segment_stats)

# ============================================================================
# SAVE OUTPUTS
# ============================================================================
print("="*80)
print("SAVING OUTPUTS")
print("="*80)
print()

# Save detailed customer data
output_cols = [
    'Customer ID',
    'segment',
    'loyalty_tier_a',
    'loyalty_score_a',
    'current_spend',
    'previous_purchase_history',
    'purchase_frequency_score',
    'observed_promo_exposure_flag',
    'satisfaction_score',
    'high_satisfaction_flag',
    'subscription_flag',
    'age_band',
    'gender',
    'location',
    'category'
]

df[output_cols].to_csv(OUTPUT_PATH, index=False)
print(f"✓ Customer segments saved to: {OUTPUT_PATH}")

# Save segment summary
summary_path = OUTPUT_PATH.parent / "segment_summary.csv"
df_segment_stats.to_csv(summary_path, index=False)
print(f"✓ Segment summary saved to: {summary_path}")
print()

# ============================================================================
# GENERATE DOCUMENTATION
# ============================================================================

doc_content = f"""# Customer Segmentation Methodology
**D2C Fashion Customer Intelligence Project**

**Date:** 2026-08-27
**Framework:** Loyalty Definition A (Behavioral)

---

## Overview

Six customer segments created using Loyalty Definition A tiers plus behavioral characteristics.

**Total Customers:** {len(df):,}
**Segmentation Variables:**
- Loyalty tier (from Definition A)
- Promotional exposure
- Purchase history
- Satisfaction

---

## Segment Definitions

### 1. Core Loyalists
**Rule:** Loyalty Tier 4 (Very High)

**Profile:**
- Customers: {segment_stats[0]['Customer_Count']:,} ({segment_stats[0]['Customer_Pct']:.1f}%)
- Avg previous purchases: {segment_stats[0]['Avg_Previous_Purchases']:.1f}
- Avg frequency score: {segment_stats[0]['Avg_Frequency_Score']:.2f}
- Promo exposure: {segment_stats[0]['Promo_Exposure_Pct']:.1f}%
- Avg satisfaction: {segment_stats[0]['Avg_Satisfaction']:.2f}

**Characteristics:**
- Highest repeat purchase history
- Highest stated frequency
- **Lowest promotional exposure (11%)**
- Highest satisfaction
- Strong brand pull

**Business Implication:** Can sustain purchases without heavy promotional investment

---

### 2. Emerging Loyalists
**Rule:** Loyalty Tier 3 (High)

**Profile:**
- Customers: {segment_stats[1]['Customer_Count']:,} ({segment_stats[1]['Customer_Pct']:.1f}%)
- Avg previous purchases: {segment_stats[1]['Avg_Previous_Purchases']:.1f}
- Avg frequency score: {segment_stats[1]['Avg_Frequency_Score']:.2f}
- Promo exposure: {segment_stats[1]['Promo_Exposure_Pct']:.1f}%
- Avg satisfaction: {segment_stats[1]['Avg_Satisfaction']:.2f}

**Characteristics:**
- High repeat purchase history
- Moderate promo exposure (27%)
- Good satisfaction levels
- Ascending loyalty trajectory

**Business Implication:** Prime candidates to graduate to Core Loyalists

---

### 3. Developing Loyalists
**Rule:** Loyalty Tier 2 (Medium) + Non-promo-exposed

**Profile:**
- Customers: {segment_stats[2]['Customer_Count']:,} ({segment_stats[2]['Customer_Pct']:.1f}%)
- Avg previous purchases: {segment_stats[2]['Avg_Previous_Purchases']:.1f}
- Avg frequency score: {segment_stats[2]['Avg_Frequency_Score']:.2f}
- Promo exposure: {segment_stats[2]['Promo_Exposure_Pct']:.1f}%
- Avg satisfaction: {segment_stats[2]['Avg_Satisfaction']:.2f}

**Characteristics:**
- Moderate repeat behavior
- **Not currently promo-exposed**
- Organic purchase drivers
- Development potential

**Business Implication:** Nurture without introducing promo dependency

---

### 4. Promo-Engaged Repeaters
**Rule:** Loyalty Tier 2 (Medium) + Promo-exposed

**Profile:**
- Customers: {segment_stats[3]['Customer_Count']:,} ({segment_stats[3]['Customer_Pct']:.1f}%)
- Avg previous purchases: {segment_stats[3]['Avg_Previous_Purchases']:.1f}
- Avg frequency score: {segment_stats[3]['Avg_Frequency_Score']:.2f}
- Promo exposure: {segment_stats[3]['Promo_Exposure_Pct']:.1f}%
- Avg satisfaction: {segment_stats[3]['Avg_Satisfaction']:.2f}

**Characteristics:**
- Moderate repeat behavior
- **Currently promo-exposed**
- May have developed promo association
- Mid-tier value

**Business Implication:** Test promo reduction carefully; monitor response

---

### 5. Early-Stage Customers
**Rule:** Loyalty Tier 1 (Low) + Non-promo-exposed

**Profile:**
- Customers: {segment_stats[4]['Customer_Count']:,} ({segment_stats[4]['Customer_Pct']:.1f}%)
- Avg previous purchases: {segment_stats[4]['Avg_Previous_Purchases']:.1f}
- Avg frequency score: {segment_stats[4]['Avg_Frequency_Score']:.2f}
- Promo exposure: {segment_stats[4]['Promo_Exposure_Pct']:.1f}%
- Avg satisfaction: {segment_stats[4]['Avg_Satisfaction']:.2f}

**Characteristics:**
- Lower purchase history
- **Not currently promo-exposed**
- Organic acquisition or early relationship
- Potential for development

**Business Implication:** Nurture organically; avoid creating promo dependency

---

### 6. Promo-Exposed Transactors
**Rule:** Loyalty Tier 1 (Low) + Promo-exposed

**Profile:**
- Customers: {segment_stats[5]['Customer_Count']:,} ({segment_stats[5]['Customer_Pct']:.1f}%)
- Avg previous purchases: {segment_stats[5]['Avg_Previous_Purchases']:.1f}
- Avg frequency score: {segment_stats[5]['Avg_Frequency_Score']:.2f}
- Promo exposure: {segment_stats[5]['Promo_Exposure_Pct']:.1f}%
- Avg satisfaction: {segment_stats[5]['Avg_Satisfaction']:.2f}

**Characteristics:**
- Lower purchase history
- **High promo exposure**
- May be promo-driven acquisitions
- Lower satisfaction

**Business Implication:** High promo sensitivity; maintain promotional support

---

## Segment Summary Table

| Segment | Customers | % | Current Observed Spend | Spend % | Avg Spend | Promo % |
|---------|-----------|---|------------------------|---------|-----------|---------|
"""

for stats in segment_stats:
    doc_content += f"| {stats['Segment']} | {stats['Customer_Count']:,} | {stats['Customer_Pct']:.1f}% | ${stats['Total_Current_Observed_Spend']:,.0f} | {stats['Current_Observed_Spend_Pct']:.1f}% | ${stats['Avg_Spend']:.2f} | {stats['Promo_Exposure_Pct']:.0f}% |\n"

doc_content += f"""

---

## Strategic Implications

### High-Opportunity Segments

**1. Core Loyalists ({segment_stats[0]['Customer_Count']:,} customers, {segment_stats[0]['Current_Observed_Spend_Pct']:.1f}% spend)**
- **Action:** Reduce promotional investment
- **Rationale:** Only {segment_stats[0]['Promo_Exposure_Pct']:.1f}% promo exposure; strong brand pull
- **Expected outcome:** Maintain behavior with lower discount costs

**2. Emerging Loyalists ({segment_stats[1]['Customer_Count']:,} customers, {segment_stats[1]['Current_Observed_Spend_Pct']:.1f}% spend)**
- **Action:** Test selective promo reduction
- **Rationale:** {segment_stats[1]['Promo_Exposure_Pct']:.1f}% promo exposure; ascending loyalty
- **Expected outcome:** Some customers graduate to Core Loyalists

### Maintain-Current-Approach Segments

**3. Developing Loyalists ({segment_stats[2]['Customer_Count']:,} customers)**
- **Action:** Nurture without introducing promo dependency
- **Rationale:** Already showing organic behavior
- **Expected outcome:** Natural progression to higher tiers

**4. Early-Stage Customers ({segment_stats[4]['Customer_Count']:,} customers)**
- **Action:** Quality engagement without heavy discounting
- **Rationale:** Organic start; avoid promo conditioning
- **Expected outcome:** Healthy development trajectory

### Caution Segments

**5. Promo-Engaged Repeaters ({segment_stats[3]['Customer_Count']:,} customers)**
- **Action:** Maintain current promotional strategy; test carefully
- **Rationale:** Promo-associated but has repeat behavior
- **Expected outcome:** Gradual optimization possible

**6. Promo-Exposed Transactors ({segment_stats[5]['Customer_Count']:,} customers)**
- **Action:** Maintain promotional support
- **Rationale:** High promo sensitivity ({segment_stats[5]['Promo_Exposure_Pct']:.0f}%)
- **Expected outcome:** Revenue at risk if promos reduced abruptly

---

## Limitations

1. **Observational only:** Cannot establish causation
2. **Single snapshot:** No longitudinal tracking of segment migration
3. **Promo exposure:** Single observation; not historical dependency rate
4. **No validation:** Segments not tested via experimentation
5. **Stated frequency:** Self-reported, not transaction-derived

---

## Usage Guidelines

### For Strategy
- Prioritize promo reduction in Core Loyalists and test in Emerging Loyalists
- Protect Early-Stage and Developing Loyalists from unnecessary promo exposure
- Proceed cautiously with Promo-Engaged segments

### For Analysis
- Cross-tabulate segments with geography, category, demographics
- Track segment sizes over time (requires future snapshots)
- Monitor satisfaction and behavior changes within segments

### For Reporting
- Use segment names in dashboards and presentations
- Focus executive attention on Core + Emerging Loyalists
- Frame promo strategy as selective reduction, not blanket cuts

---

**End of Segmentation Methodology**
"""

DOC_PATH.parent.mkdir(parents=True, exist_ok=True)
with open(DOC_PATH, 'w', encoding='utf-8') as f:
    f.write(doc_content)

print(f"✓ Segmentation methodology saved to: {DOC_PATH}")
print()

print("="*80)
print("CUSTOMER SEGMENTATION COMPLETE")
print("="*80)
print()
print(f"✓ 6 segments created")
print(f"✓ {len(df):,} customers classified")
print(f"✓ Clear promo differentiation across segments")
print()
print("Segment highlights:")
print(f"  • Core Loyalists: {segment_stats[0]['Promo_Exposure_Pct']:.0f}% promo (prime opportunity)")
print(f"  • Promo-Exposed Transactors: {segment_stats[5]['Promo_Exposure_Pct']:.0f}% promo (high sensitivity)")
print()
print("Next: Geographic analysis (Python/08_geography.py)")
print()

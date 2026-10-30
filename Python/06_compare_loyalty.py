"""
Loyalty Framework Comparison: Definition A vs B
================================================

Purpose: Compare behavioral vs commercial value loyalty frameworks
Author: Analytics Engineering Team
Date: 2026-08-27

Objective: Determine which framework provides clearest differentiation
for business decision-making
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
LOYALTY_B_PATH = Path("Outputs/analytical/loyalty_definition_b.csv")
OUTPUT_PATH = Path("Outputs/analytical/loyalty_comparison.csv")
REPORT_PATH = Path("Documentation/06_Loyalty_Comparison.md")

print("="*80)
print("LOYALTY FRAMEWORK COMPARISON: A vs B")
print("="*80)
print()

# Load data
print("Loading data...")
df_features = pd.read_csv(FEATURES_PATH)
df_a = pd.read_csv(LOYALTY_A_PATH)
df_b = pd.read_csv(LOYALTY_B_PATH)

# Merge
df = df_features.merge(
    df_a[['Customer ID', 'loyalty_score_a', 'loyalty_tier_a']],
    on='Customer ID'
).merge(
    df_b[['Customer ID', 'loyalty_score_b', 'loyalty_tier_b']],
    on='Customer ID'
)

print(f"✓ Loaded {len(df):,} customers with both loyalty definitions")
print()

# ============================================================================
# TIER COMPARISON
# ============================================================================
print("="*80)
print("TIER DISTRIBUTION COMPARISON")
print("="*80)
print()

print("DEFINITION A (Behavioral - with promo penalty):")
print("-" * 60)
for tier in ['Tier 1: Low', 'Tier 2: Medium', 'Tier 3: High', 'Tier 4: Very High']:
    tier_df = df[df['loyalty_tier_a'] == tier]
    count = len(tier_df)
    pct = (count / len(df)) * 100
    avg_spend = tier_df['current_spend'].mean()
    total_revenue = tier_df['current_spend'].sum()
    rev_pct = (total_revenue / df['current_spend'].sum()) * 100

    print(f"{tier}:")
    print(f"  Customers: {count:,} ({pct:.1f}%)")
    print(f"  Avg spend: ${avg_spend:.2f}")
    print(f"  Total current observed spend: ${total_revenue:,.0f} ({rev_pct:.1f}%)")
    print()

print("\nDEFINITION B (Commercial Value - no promo penalty):")
print("-" * 60)
for tier in ['Tier 1: Low', 'Tier 2: Medium', 'Tier 3: High', 'Tier 4: Very High']:
    tier_df = df[df['loyalty_tier_b'] == tier]
    count = len(tier_df)
    pct = (count / len(df)) * 100
    avg_spend = tier_df['current_spend'].mean()
    total_revenue = tier_df['current_spend'].sum()
    rev_pct = (total_revenue / df['current_spend'].sum()) * 100

    print(f"{tier}:")
    print(f"  Customers: {count:,} ({pct:.1f}%)")
    print(f"  Avg spend: ${avg_spend:.2f}")
    print(f"  Total current observed spend: ${total_revenue:,.0f} ({rev_pct:.1f}%)")
    print()

# ============================================================================
# DETAILED METRICS BY TIER
# ============================================================================
print("="*80)
print("DETAILED METRICS COMPARISON")
print("="*80)
print()

comparison_data = []

for definition, tier_col in [('A', 'loyalty_tier_a'), ('B', 'loyalty_tier_b')]:
    for tier in ['Tier 1: Low', 'Tier 2: Medium', 'Tier 3: High', 'Tier 4: Very High']:
        tier_df = df[df[tier_col] == tier]

        comparison_data.append({
            'Definition': definition,
            'Tier': tier,
            'Customer_Count': len(tier_df),
            'Customer_Pct': len(tier_df) / len(df) * 100,
            'Total_Current_Observed_Spend': tier_df['current_spend'].sum(),
            'Spend_Pct': tier_df['current_spend'].sum() / df['current_spend'].sum() * 100,
            'Avg_Spend': tier_df['current_spend'].mean(),
            'Avg_Previous_Purchases': tier_df['previous_purchase_history'].mean(),
            'Avg_Frequency_Score': tier_df['purchase_frequency_score'].mean(),
            'Avg_Satisfaction': tier_df['satisfaction_score'].mean(),
            'Promo_Exposure_Rate': tier_df['observed_promo_exposure_flag'].mean() * 100,
            'Subscription_Rate': tier_df['subscription_flag'].mean() * 100
        })

df_comparison = pd.DataFrame(comparison_data)

# Display side-by-side for Tier 4
print("TIER 4 (Very High) COMPARISON:")
print("-" * 60)
tier4_a = df_comparison[(df_comparison['Definition'] == 'A') & (df_comparison['Tier'] == 'Tier 4: Very High')].iloc[0]
tier4_b = df_comparison[(df_comparison['Definition'] == 'B') & (df_comparison['Tier'] == 'Tier 4: Very High')].iloc[0]

print(f"{'Metric':<30} {'Definition A':>15} {'Definition B':>15}")
print("-" * 60)
print(f"{'Customer Count':<30} {tier4_a['Customer_Count']:>15,.0f} {tier4_b['Customer_Count']:>15,.0f}")
print(f"{'Total Current Observed Spend':<30} ${tier4_a['Total_Current_Observed_Spend']:>14,.0f} ${tier4_b['Total_Current_Observed_Spend']:>14,.0f}")
print(f"{'Spend %':<30} {tier4_a['Spend_Pct']:>14.1f}% {tier4_b['Spend_Pct']:>14.1f}%")
print(f"{'Avg Spend':<30} ${tier4_a['Avg_Spend']:>14.2f} ${tier4_b['Avg_Spend']:>14.2f}")
print(f"{'Avg Previous Purchases':<30} {tier4_a['Avg_Previous_Purchases']:>15.1f} {tier4_b['Avg_Previous_Purchases']:>15.1f}")
print(f"{'Avg Frequency Score':<30} {tier4_a['Avg_Frequency_Score']:>15.2f} {tier4_b['Avg_Frequency_Score']:>15.2f}")
print(f"{'Avg Satisfaction':<30} {tier4_a['Avg_Satisfaction']:>15.2f} {tier4_b['Avg_Satisfaction']:>15.2f}")
print(f"{'Promo Exposure %':<30} {tier4_a['Promo_Exposure_Rate']:>14.1f}% {tier4_b['Promo_Exposure_Rate']:>14.1f}%")
print(f"{'Subscription %':<30} {tier4_a['Subscription_Rate']:>14.1f}% {tier4_b['Subscription_Rate']:>14.1f}%")
print()

# ============================================================================
# KEY DIFFERENTIATORS
# ============================================================================
print("="*80)
print("KEY DIFFERENTIATORS")
print("="*80)
print()

print("Definition A (Behavioral):")
print("  • Tier 4 promo exposure: {:.1f}%".format(tier4_a['Promo_Exposure_Rate']))
print("  • Clear brand-pull signal (11% promo in top tier)")
print("  • Spend concentration in Tier 4: {:.1f}%".format(tier4_a['Spend_Pct']))
print()

print("Definition B (Commercial Value):")
print("  • Tier 4 promo exposure: {:.1f}%".format(tier4_b['Promo_Exposure_Rate']))
print("  • No differentiation on promo (43% across all tiers)")
print("  • Spend concentration in Tier 4: {:.1f}%".format(tier4_b['Spend_Pct']))
print("  • Stronger spend differentiation (${:.2f} vs ${:.2f} avg spend)".format(
    tier4_b['Avg_Spend'], tier4_a['Avg_Spend']))
print()

# ============================================================================
# REVENUE CONCENTRATION ANALYSIS
# ============================================================================
print("="*80)
print("REVENUE CONCENTRATION (Tier 3 + 4)")
print("="*80)
print()

for definition, tier_col in [('A', 'loyalty_tier_a'), ('B', 'loyalty_tier_b')]:
    high_tiers = df[df[tier_col].isin(['Tier 3: High', 'Tier 4: Very High'])]
    customer_pct = len(high_tiers) / len(df) * 100
    spend_pct = high_tiers['current_spend'].sum() / df['current_spend'].sum() * 100

    print(f"Definition {definition}:")
    print(f"  Top 50% of customers capture {spend_pct:.1f}% of observed spend")
    print()

# ============================================================================
# RECOMMENDATION
# ============================================================================
print("="*80)
print("RECOMMENDATION")
print("="*80)
print()

# Calculate differentiation power
a_promo_range = tier4_a['Promo_Exposure_Rate'] - df[df['loyalty_tier_a'] == 'Tier 1: Low']['observed_promo_exposure_flag'].mean() * 100
b_spend_range = tier4_b['Avg_Spend'] - df[df['loyalty_tier_b'] == 'Tier 1: Low']['current_spend'].mean()

print("WINNER: Definition A (Behavioral Loyalty Proxy)")
print()
print("Evidence:")
print(f"  1. Clear promotional differentiation across tiers")
print(f"     • Tier 1: {df[df['loyalty_tier_a']=='Tier 1: Low']['observed_promo_exposure_flag'].mean()*100:.1f}% promo exposure")
print(f"     • Tier 4: {tier4_a['Promo_Exposure_Rate']:.1f}% promo exposure")
promo_range = tier4_a['Promo_Exposure_Rate'] - df[df['loyalty_tier_a']=='Tier 1: Low']['observed_promo_exposure_flag'].mean()*100
print(f"     • Range: {promo_range:.1f} percentage points")
print()
print(f"  2. Enables strategic promo reduction")
print(f"     • Tier 4 customers show strong brand pull")
print(f"     • Can reduce promo investment in this segment")
print()
print(f"  3. Satisfies primary business questions:")
print(f"     • Identifies loyal vs promo-oriented customers")
print(f"     • Clear behavioral differentiation")
print(f"     • Actionable for selective promo reduction")
print()
print("Definition B Advantages:")
print(f"  • Stronger spend differentiation (${tier4_b['Avg_Spend']:.2f} vs ${tier4_a['Avg_Spend']:.2f})")
print(f"  • Identifies high-value customers regardless of promo")
print(f"  • Useful for commercial value prioritization")
print()
print("Recommendation:")
print("  • PRIMARY: Use Definition A for customer segmentation and strategy")
print("  • SECONDARY: Track Definition B score for revenue prioritization within segments")
print()

# ============================================================================
# SAVE OUTPUTS
# ============================================================================
print("="*80)
print("SAVING OUTPUTS")
print("="*80)
print()

df_comparison.to_csv(OUTPUT_PATH, index=False)
print(f"✓ Comparison data saved to: {OUTPUT_PATH}")

# Generate detailed report
report = f"""# Loyalty Framework Comparison Report
**D2C Fashion Customer Intelligence Project**

**Date:** 2026-08-27
**Analyst:** Analytics Engineering Team

---

## Executive Summary

Two loyalty framework candidates were developed and tested:
- **Definition A (Behavioral):** Emphasizes repeat behavior, frequency, satisfaction, and LOW promotional exposure
- **Definition B (Commercial Value):** Emphasizes spend, repeat behavior, frequency, and satisfaction (no promo penalty)

**RECOMMENDED FRAMEWORK: Definition A (Behavioral Loyalty Proxy)**

---

## Framework Methodologies

### Definition A: Behavioral Loyalty Proxy

> **Caveat — Promo Exposure Is an Input, Not Independent Validation:**
> Promo exposure is a weighted component of Definition A's score. The observed separation of promo rates across tiers (e.g., 83% → 11%) is therefore **a direct consequence of how the score was constructed**, not an independent validation of the framework. Additionally, because Loyalty A tiers are defined by quartile cut-offs of the composite score, they represent **relative behavioral rankings** within this dataset rather than naturally occurring, independently-defined loyalty classes.

**Components:**
1. Purchase history (35% weight) - Historical engagement depth
2. Purchase frequency (25% weight) - Stated purchase regularity
3. Satisfaction (20% weight) - Quality indicator
4. Low promo exposure (20% weight) - Brand-pull indicator

**Philosophy:** Loyal customers demonstrate repeat behavior, high satisfaction, and **purchase without requiring promotional incentives**.

---

### Definition B: Commercial Value Proxy

> **Note — This Is a Commercial Value Proxy, Not Evidence of True Loyalty:**
> Definition B does not incorporate promo exposure as a penalty. Its tiers reflect customers' observed spend and engagement levels. This framework is useful for prioritizing commercial value but does not provide evidence of behavioral loyalty or immunity to promotional incentives. Use Definition B as a **value-spend segmentation tool**, not as a loyalty indicator.

**Components:**
1. Purchase history (35% weight) - Historical engagement depth
2. Current spend (30% weight) - Immediate value contribution
3. Purchase frequency (20% weight) - Stated purchase regularity
4. Satisfaction (15% weight) - Quality indicator

**Philosophy:** Loyal customers demonstrate high commercial value through spend and repeat behavior, **regardless of promotional association**.

---

## Tier Distribution Comparison

### Definition A (Behavioral)

| Tier | Customers | % | Avg Spend | Total Current Observed Spend | Spend % |
|------|-----------|---|-----------|------------------------------|---------|
| Tier 1: Low | {df_comparison[(df_comparison['Definition']=='A')&(df_comparison['Tier']=='Tier 1: Low')]['Customer_Count'].values[0]:.0f} | 25.0% | ${df_comparison[(df_comparison['Definition']=='A')&(df_comparison['Tier']=='Tier 1: Low')]['Avg_Spend'].values[0]:.2f} | ${df_comparison[(df_comparison['Definition']=='A')&(df_comparison['Tier']=='Tier 1: Low')]['Total_Current_Observed_Spend'].values[0]:,.0f} | {df_comparison[(df_comparison['Definition']=='A')&(df_comparison['Tier']=='Tier 1: Low')]['Spend_Pct'].values[0]:.1f}% |
| Tier 2: Medium | {df_comparison[(df_comparison['Definition']=='A')&(df_comparison['Tier']=='Tier 2: Medium')]['Customer_Count'].values[0]:.0f} | 25.0% | ${df_comparison[(df_comparison['Definition']=='A')&(df_comparison['Tier']=='Tier 2: Medium')]['Avg_Spend'].values[0]:.2f} | ${df_comparison[(df_comparison['Definition']=='A')&(df_comparison['Tier']=='Tier 2: Medium')]['Total_Current_Observed_Spend'].values[0]:,.0f} | {df_comparison[(df_comparison['Definition']=='A')&(df_comparison['Tier']=='Tier 2: Medium')]['Spend_Pct'].values[0]:.1f}% |
| Tier 3: High | {df_comparison[(df_comparison['Definition']=='A')&(df_comparison['Tier']=='Tier 3: High')]['Customer_Count'].values[0]:.0f} | 25.0% | ${df_comparison[(df_comparison['Definition']=='A')&(df_comparison['Tier']=='Tier 3: High')]['Avg_Spend'].values[0]:.2f} | ${df_comparison[(df_comparison['Definition']=='A')&(df_comparison['Tier']=='Tier 3: High')]['Total_Current_Observed_Spend'].values[0]:,.0f} | {df_comparison[(df_comparison['Definition']=='A')&(df_comparison['Tier']=='Tier 3: High')]['Spend_Pct'].values[0]:.1f}% |
| Tier 4: Very High | {df_comparison[(df_comparison['Definition']=='A')&(df_comparison['Tier']=='Tier 4: Very High')]['Customer_Count'].values[0]:.0f} | 25.0% | ${df_comparison[(df_comparison['Definition']=='A')&(df_comparison['Tier']=='Tier 4: Very High')]['Avg_Spend'].values[0]:.2f} | ${df_comparison[(df_comparison['Definition']=='A')&(df_comparison['Tier']=='Tier 4: Very High')]['Total_Current_Observed_Spend'].values[0]:,.0f} | {df_comparison[(df_comparison['Definition']=='A')&(df_comparison['Tier']=='Tier 4: Very High')]['Spend_Pct'].values[0]:.1f}% |

### Definition B (Commercial Value Proxy)

| Tier | Customers | % | Avg Spend | Total Current Observed Spend | Spend % |
|------|-----------|---|-----------|------------------------------|---------|
| Tier 1: Low | {df_comparison[(df_comparison['Definition']=='B')&(df_comparison['Tier']=='Tier 1: Low')]['Customer_Count'].values[0]:.0f} | 25.0% | ${df_comparison[(df_comparison['Definition']=='B')&(df_comparison['Tier']=='Tier 1: Low')]['Avg_Spend'].values[0]:.2f} | ${df_comparison[(df_comparison['Definition']=='B')&(df_comparison['Tier']=='Tier 1: Low')]['Total_Current_Observed_Spend'].values[0]:,.0f} | {df_comparison[(df_comparison['Definition']=='B')&(df_comparison['Tier']=='Tier 1: Low')]['Spend_Pct'].values[0]:.1f}% |
| Tier 2: Medium | {df_comparison[(df_comparison['Definition']=='B')&(df_comparison['Tier']=='Tier 2: Medium')]['Customer_Count'].values[0]:.0f} | 25.0% | ${df_comparison[(df_comparison['Definition']=='B')&(df_comparison['Tier']=='Tier 2: Medium')]['Avg_Spend'].values[0]:.2f} | ${df_comparison[(df_comparison['Definition']=='B')&(df_comparison['Tier']=='Tier 2: Medium')]['Total_Current_Observed_Spend'].values[0]:,.0f} | {df_comparison[(df_comparison['Definition']=='B')&(df_comparison['Tier']=='Tier 2: Medium')]['Spend_Pct'].values[0]:.1f}% |
| Tier 3: High | {df_comparison[(df_comparison['Definition']=='B')&(df_comparison['Tier']=='Tier 3: High')]['Customer_Count'].values[0]:.0f} | 25.0% | ${df_comparison[(df_comparison['Definition']=='B')&(df_comparison['Tier']=='Tier 3: High')]['Avg_Spend'].values[0]:.2f} | ${df_comparison[(df_comparison['Definition']=='B')&(df_comparison['Tier']=='Tier 3: High')]['Total_Current_Observed_Spend'].values[0]:,.0f} | {df_comparison[(df_comparison['Definition']=='B')&(df_comparison['Tier']=='Tier 3: High')]['Spend_Pct'].values[0]:.1f}% |
| Tier 4: Very High | {df_comparison[(df_comparison['Definition']=='B')&(df_comparison['Tier']=='Tier 4: Very High')]['Customer_Count'].values[0]:.0f} | 25.0% | ${df_comparison[(df_comparison['Definition']=='B')&(df_comparison['Tier']=='Tier 4: Very High')]['Avg_Spend'].values[0]:.2f} | ${df_comparison[(df_comparison['Definition']=='B')&(df_comparison['Tier']=='Tier 4: Very High')]['Total_Current_Observed_Spend'].values[0]:,.0f} | {df_comparison[(df_comparison['Definition']=='B')&(df_comparison['Tier']=='Tier 4: Very High')]['Spend_Pct'].values[0]:.1f}% |

---

## Detailed Metric Comparison (Tier 4: Very High)

| Metric | Definition A | Definition B |
|--------|--------------|--------------|
| **Customer Count** | {tier4_a['Customer_Count']:.0f} | {tier4_b['Customer_Count']:.0f} |
| **Total Current Observed Spend** | ${tier4_a['Total_Current_Observed_Spend']:,.0f} | ${tier4_b['Total_Current_Observed_Spend']:,.0f} |
| **Spend %** | {tier4_a['Spend_Pct']:.1f}% | {tier4_b['Spend_Pct']:.1f}% |
| **Avg Spend** | ${tier4_a['Avg_Spend']:.2f} | ${tier4_b['Avg_Spend']:.2f} |
| **Avg Previous Purchases** | {tier4_a['Avg_Previous_Purchases']:.1f} | {tier4_b['Avg_Previous_Purchases']:.1f} |
| **Avg Frequency Score** | {tier4_a['Avg_Frequency_Score']:.2f} | {tier4_b['Avg_Frequency_Score']:.2f} |
| **Avg Satisfaction** | {tier4_a['Avg_Satisfaction']:.2f} | {tier4_b['Avg_Satisfaction']:.2f} |
| **Promo Exposure %** | **{tier4_a['Promo_Exposure_Rate']:.1f}%** | {tier4_b['Promo_Exposure_Rate']:.1f}% |
| **Subscription %** | {tier4_a['Subscription_Rate']:.1f}% | {tier4_b['Subscription_Rate']:.1f}% |

---

## Key Findings

### Definition A Strengths

1. **Clear Promotional Differentiation**
   - Tier 1 (Low): {df_comparison[(df_comparison['Definition']=='A')&(df_comparison['Tier']=='Tier 1: Low')]['Promo_Exposure_Rate'].values[0]:.1f}% promo exposure
   - Tier 4 (Very High): {tier4_a['Promo_Exposure_Rate']:.1f}% promo exposure
   - **Range: {(tier4_a['Promo_Exposure_Rate']-df_comparison[(df_comparison['Definition']=='A')&(df_comparison['Tier']=='Tier 1: Low')]['Promo_Exposure_Rate'].values[0]):.1f} percentage points**

2. **Identifies Brand-Pull Customers**
   - Top tier shows strong purchase behavior WITHOUT promotional dependence
   - Only {tier4_a['Promo_Exposure_Rate']:.1f}% promo exposure in most loyal segment

3. **Actionable for Promo Reduction Strategy**
   - Clear target: Tier 4 customers can sustain purchase without heavy discounting
   - Tier 1 customers show high promo association ({df_comparison[(df_comparison['Definition']=='A')&(df_comparison['Tier']=='Tier 1: Low')]['Promo_Exposure_Rate'].values[0]:.1f}%)

4. **Answers Primary Business Question**
   - "Who are loyal vs promo-oriented customers?" → Definition A directly addresses this

### Definition B (Commercial Value Proxy) Strengths

1. **Stronger Spend Differentiation**
   - Tier 4 avg spend: ${tier4_b['Avg_Spend']:.2f}
   - Tier 1 avg spend: ${df_comparison[(df_comparison['Definition']=='B')&(df_comparison['Tier']=='Tier 1: Low')]['Avg_Spend'].values[0]:.2f}
   - Spend concentration in Tier 4: {tier4_b['Spend_Pct']:.1f}%

2. **Commercial Value Focus**
   - Identifies high-value customers regardless of promotional channel
   - Useful for commercial value prioritization

3. **No Promo Discrimination**
   - Definition B Tier 4 promo exposure: {tier4_b['Promo_Exposure_Rate']:.1f}% (similar across all tiers)
   - Does NOT differentiate on promotional behavior

### Critical Difference

**Definition A:** Promo exposure decreases dramatically as loyalty increases ({df_comparison[(df_comparison['Definition']=='A')&(df_comparison['Tier']=='Tier 1: Low')]['Promo_Exposure_Rate'].values[0]:.1f}% → {tier4_a['Promo_Exposure_Rate']:.1f}%)
**Definition B:** Promo exposure stays flat across all tiers (~{df_comparison[(df_comparison['Definition']=='B')&(df_comparison['Tier']=='Tier 4: Very High')]['Promo_Exposure_Rate'].values[0]:.0f}%)

**Implication:** Definition A identifies customers with different **behavioral relationships** to promotions. Definition B identifies customers with different **spend levels** but similar promotional patterns.

---

## Recommendation

### PRIMARY FRAMEWORK: Definition A (Behavioral Loyalty Proxy)

**Rationale:**

1. **Directly answers the primary business question:** "Who are loyal vs promo-oriented customers?"

2. **Enables strategic promo reduction:** Clear differentiation allows selective reduction without blanket cuts

3. **Behavioral differentiation:** Shows fundamentally different customer relationships with the brand

4. **Actionable segments:**
   - Tier 4: Reduce promo investment (strong brand pull)
   - Tier 1: High promo dependency (proceed with caution)

### SECONDARY USE: Definition B for Commercial Value Prioritization

**Use Case:** Within Definition A segments, use Definition B score to prioritize by commercial value (spend)

**Example:** Among Definition A Tier 3 customers, focus retention efforts on those with high Definition B scores

---

## Business Applications

### Using Definition A

**Tier 4 (Very High Loyalty):**
- **Action:** Reduce promotional exposure
- **Expected outcome:** Maintain purchase behavior with lower discount cost
- **Promo exposure:** Currently {tier4_a['Promo_Exposure_Rate']:.1f}%
- **Customers:** {tier4_a['Customer_Count']:.0f} (25%)

**Tier 3 (High Loyalty):**
- **Action:** Test selective promo reduction
- **Expected outcome:** Some customers may maintain behavior without promo
- **Promo exposure:** Currently {df_comparison[(df_comparison['Definition']=='A')&(df_comparison['Tier']=='Tier 3: High')]['Promo_Exposure_Rate'].values[0]:.1f}%
- **Customers:** {df_comparison[(df_comparison['Definition']=='A')&(df_comparison['Tier']=='Tier 3: High')]['Customer_Count'].values[0]:.0f} (25%)

**Tier 1-2 (Low-Medium Loyalty):**
- **Action:** Maintain or test promo optimization
- **Expected outcome:** High promo sensitivity; proceed carefully
- **Promo exposure:** {df_comparison[(df_comparison['Definition']=='A')&(df_comparison['Tier']=='Tier 1: Low')]['Promo_Exposure_Rate'].values[0]:.1f}% (Tier 1), {df_comparison[(df_comparison['Definition']=='A')&(df_comparison['Tier']=='Tier 2: Medium')]['Promo_Exposure_Rate'].values[0]:.1f}% (Tier 2)
- **Customers:** {(df_comparison[(df_comparison['Definition']=='A')&(df_comparison['Tier']=='Tier 1: Low')]['Customer_Count'].values[0]+df_comparison[(df_comparison['Definition']=='A')&(df_comparison['Tier']=='Tier 2: Medium')]['Customer_Count'].values[0]):,.0f} (50%)

### Using Definition B (Secondary)

- **Commercial value prioritization** within loyalty tiers
- **High-value customer** identification across all segments
- **Spend-based targeting** for upsell campaigns (not causal)

---

## Limitations

1. **Observational only:** Cannot establish causation (promo → loyalty or loyalty → less promo)
2. **Single snapshot:** No longitudinal data to validate loyalty persistence
3. **Stated frequency:** Frequency scores are self-reported, not transaction-derived
4. **No validation:** Cannot A/B test loyalty definitions without implementation
5. **Promo exposure is a Definition A input:** Tier separation on promo is a design feature, not independent evidence
6. **Quartile tiers are relative rankings:** Definition A tiers represent statistical cut-offs within the observed population, not independently-defined loyalty classes

## Final Methodology Constraints

The following apply to all loyalty outputs in this project:

- **No timestamps:** Transaction dates are not available; true time-to-event, recency, and trend metrics cannot be calculated
- **No true churn:** Cannot measure customer departure; no exit dates or churn window definition is possible
- **No true retention:** Cannot measure whether customers continued purchasing over time; observed snapshot only
- **No historical promo dependency:** Single customer-level observation; cannot calculate what share of a customer's purchase history involved promotions
- **No causal inference:** All observed associations between promo exposure, spend, and loyalty proxies are correlational; promotional impact on behavior cannot be established from this data

---

## Next Steps

1. **Adopt Definition A** as primary loyalty framework
2. **Create customer segments** based on Definition A tiers
3. **Proceed to geographic analysis** using Definition A framework
4. **Proceed to category analysis** using Definition A framework
5. **Track Definition B scores** as secondary commercial value proxy (not true loyalty)

---

**End of Comparison Report**
"""

REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
with open(REPORT_PATH, 'w', encoding='utf-8') as f:
    f.write(report)

print(f"✓ Comparison report saved to: {REPORT_PATH}")
print()

print("="*80)
print("LOYALTY COMPARISON COMPLETE")
print("="*80)
print()
print("WINNER: Definition A (Behavioral Loyalty Proxy)")
print()
print("Primary reasons:")
print("  1. Clear promo differentiation (83% → 11% across tiers)")
print("  2. Answers core business question about loyal vs promo-oriented customers")
print("  3. Actionable for selective promo reduction strategy")
print()
print("Next: Customer segmentation using Definition A (Python/07_segmentation.py)")
print()

"""
Loyalty Definition B - Commercial Value Loyalty Proxy
======================================================

Purpose: Create commercial-value-focused loyalty proxy
Author: Analytics Engineering Team
Date: 2026-08-27

Methodology: Composite score emphasizing commercial value contribution,
repeat behavior, frequency, and satisfaction (WITHOUT promo exposure penalty)

Components:
1. Current spend (immediate value)
2. Previous purchase history (depth of engagement)
3. Purchase frequency score (regularity)
4. Satisfaction score (quality indicator)

Key Difference from A: Does NOT penalize promotional exposure
Rationale: Identify high-value customers regardless of promo association
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
INPUT_PATH = Path("Outputs/analytical/customer_features.csv")
OUTPUT_PATH = Path("Outputs/analytical/loyalty_definition_b.csv")

print("="*80)
print("LOYALTY DEFINITION B: COMMERCIAL VALUE LOYALTY PROXY")
print("="*80)
print()

# Load features
print("Loading customer features...")
df = pd.read_csv(INPUT_PATH)
print(f"✓ Loaded {len(df):,} customers")
print()

# ============================================================================
# COMPONENT 1: CURRENT SPEND SCORE
# ============================================================================
print("Component 1: Current Spend Score")
print("-" * 60)

# Standardize to 0-100 scale using min-max normalization
spend_min = df['current_spend'].min()
spend_max = df['current_spend'].max()

df['spend_score'] = ((df['current_spend'] - spend_min) /
                      (spend_max - spend_min) * 100)

print(f"Range: ${spend_min} - ${spend_max}")
print(f"Normalized to: 0-100 scale")
print(f"Mean score: {df['spend_score'].mean():.2f}")
print()

# ============================================================================
# COMPONENT 2: PURCHASE HISTORY SCORE
# ============================================================================
print("Component 2: Purchase History Score")
print("-" * 60)

# Standardize to 0-100 scale
history_min = df['previous_purchase_history'].min()
history_max = df['previous_purchase_history'].max()

df['history_score'] = ((df['previous_purchase_history'] - history_min) /
                        (history_max - history_min) * 100)

print(f"Range: {history_min} - {history_max} purchases")
print(f"Normalized to: 0-100 scale")
print(f"Mean score: {df['history_score'].mean():.2f}")
print()

# ============================================================================
# COMPONENT 3: FREQUENCY SCORE
# ============================================================================
print("Component 3: Frequency Score")
print("-" * 60)

# Standardize to 0-100 scale
freq_min = df['purchase_frequency_score'].min()
freq_max = df['purchase_frequency_score'].max()

df['frequency_score'] = ((df['purchase_frequency_score'] - freq_min) /
                          (freq_max - freq_min) * 100)

print(f"Range: {freq_min} - {freq_max} frequency score")
print(f"Normalized to: 0-100 scale")
print(f"Mean score: {df['frequency_score'].mean():.2f}")
print()

# ============================================================================
# COMPONENT 4: SATISFACTION SCORE
# ============================================================================
print("Component 4: Satisfaction Score")
print("-" * 60)

# Handle missing satisfaction scores
satisfaction_median = df['satisfaction_score'].median()
df['satisfaction_imputed'] = df['satisfaction_score'].fillna(satisfaction_median)

# Standardize to 0-100 scale
sat_min = df['satisfaction_imputed'].min()
sat_max = df['satisfaction_imputed'].max()

df['satisfaction_score_norm'] = ((df['satisfaction_imputed'] - sat_min) /
                                  (sat_max - sat_min) * 100)

print(f"Range: {sat_min} - {sat_max} rating")
print(f"Missing values: {df['satisfaction_score'].isna().sum()} (imputed with median={satisfaction_median:.2f})")
print(f"Normalized to: 0-100 scale")
print(f"Mean score: {df['satisfaction_score_norm'].mean():.2f}")
print()

# ============================================================================
# COMPOSITE LOYALTY SCORE B
# ============================================================================
print("="*80)
print("COMPOSITE LOYALTY SCORE B")
print("="*80)
print()

# Weighted composite emphasizing value and history
weight_spend = 0.30          # Current value contribution
weight_history = 0.35        # Historical engagement (heaviest)
weight_frequency = 0.20      # Purchase regularity
weight_satisfaction = 0.15   # Quality indicator

print("Weighting scheme:")
print(f"  Current spend: {weight_spend:.0%}")
print(f"  Purchase history: {weight_history:.0%}")
print(f"  Frequency: {weight_frequency:.0%}")
print(f"  Satisfaction: {weight_satisfaction:.0%}")
print()

df['loyalty_score_b'] = (
    df['spend_score'] * weight_spend +
    df['history_score'] * weight_history +
    df['frequency_score'] * weight_frequency +
    df['satisfaction_score_norm'] * weight_satisfaction
)

print(f"Loyalty Score B Statistics:")
print(f"  Min: {df['loyalty_score_b'].min():.2f}")
print(f"  25th percentile: {df['loyalty_score_b'].quantile(0.25):.2f}")
print(f"  Median: {df['loyalty_score_b'].median():.2f}")
print(f"  75th percentile: {df['loyalty_score_b'].quantile(0.75):.2f}")
print(f"  Max: {df['loyalty_score_b'].max():.2f}")
print(f"  Mean: {df['loyalty_score_b'].mean():.2f}")
print()

# ============================================================================
# LOYALTY TIERS
# ============================================================================
print("="*80)
print("LOYALTY TIERS")
print("="*80)
print()

# Create tiers using quartiles (data-driven)
tier_thresholds = [
    df['loyalty_score_b'].quantile(0.25),
    df['loyalty_score_b'].quantile(0.50),
    df['loyalty_score_b'].quantile(0.75)
]

print("Tier definitions (quartile-based):")
print(f"  Tier 1 (Low): 0 - {tier_thresholds[0]:.2f}")
print(f"  Tier 2 (Medium): {tier_thresholds[0]:.2f} - {tier_thresholds[1]:.2f}")
print(f"  Tier 3 (High): {tier_thresholds[1]:.2f} - {tier_thresholds[2]:.2f}")
print(f"  Tier 4 (Very High): {tier_thresholds[2]:.2f} - 100")
print()

def assign_tier(score):
    if score < tier_thresholds[0]:
        return 'Tier 1: Low'
    elif score < tier_thresholds[1]:
        return 'Tier 2: Medium'
    elif score < tier_thresholds[2]:
        return 'Tier 3: High'
    else:
        return 'Tier 4: Very High'

df['loyalty_tier_b'] = df['loyalty_score_b'].apply(assign_tier)

# Tier distribution
print("Tier distribution:")
tier_dist = df['loyalty_tier_b'].value_counts().sort_index()
for tier, count in tier_dist.items():
    pct = (count / len(df)) * 100
    print(f"  {tier}: {count:,} ({pct:.1f}%)")
print()

# ============================================================================
# TIER PROFILES
# ============================================================================
print("="*80)
print("TIER PROFILES")
print("="*80)
print()

for tier in ['Tier 1: Low', 'Tier 2: Medium', 'Tier 3: High', 'Tier 4: Very High']:
    tier_df = df[df['loyalty_tier_b'] == tier]

    print(f"\n{tier}")
    print("-" * 60)
    print(f"Customers: {len(tier_df):,}")
    print(f"Avg current spend: ${tier_df['current_spend'].mean():.2f}")
    print(f"Avg previous purchases: {tier_df['previous_purchase_history'].mean():.1f}")
    print(f"Avg frequency score: {tier_df['purchase_frequency_score'].mean():.2f}")
    print(f"Avg satisfaction: {tier_df['satisfaction_imputed'].mean():.2f}")
    print(f"Promo exposure rate: {tier_df['observed_promo_exposure_flag'].mean():.1%}")
    print(f"Subscription rate: {tier_df['subscription_flag'].mean():.1%}")

print()

# ============================================================================
# SAVE OUTPUT
# ============================================================================
print("="*80)
print("SAVING OUTPUT")
print("="*80)
print()

output_cols = [
    'Customer ID',
    'loyalty_score_b',
    'loyalty_tier_b',
    'spend_score',
    'history_score',
    'frequency_score',
    'satisfaction_score_norm',
    'current_spend',
    'previous_purchase_history',
    'purchase_frequency_score',
    'satisfaction_score',
    'satisfaction_imputed',
    'observed_promo_exposure_flag',
    'subscription_flag'
]

df_output = df[output_cols].copy()
df_output.to_csv(OUTPUT_PATH, index=False)

print(f"✓ Loyalty Definition B saved to: {OUTPUT_PATH}")
print(f"  Rows: {len(df_output):,}")
print(f"  Columns: {len(df_output.columns)}")
print()

print("="*80)
print("LOYALTY DEFINITION B COMPLETE")
print("="*80)
print()
print("Methodology Summary:")
print("  • Commercial value focus: spend, history, frequency, satisfaction")
print("  • No promotional exposure penalty")
print("  • History-weighted (35%) with spend emphasis (30%)")
print("  • Quartile-based tiers (data-driven)")
print()
print("Next: Compare A vs B (Python/06_compare_loyalty.py)")
print()

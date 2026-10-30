"""
Dashboard CSV Outputs
======================

Purpose: Generate CSV outputs for dashboard consumption
Author: Analytics Engineering Team
Date: 2026-08-27

Outputs:
1. Executive Summary - High-level KPIs
2. Segment Performance - Segment-level metrics
3. Geographic Performance - Location-level metrics
4. Category Performance - Category-level metrics
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
SEGMENTS_PATH = Path("Outputs/analytical/customer_segments.csv")
GEO_PATH = Path("Outputs/analytical/geographic_analysis.csv")
CAT_PATH = Path("Outputs/analytical/category_analysis.csv")
LOYALTY_A_PATH = Path("Outputs/analytical/loyalty_definition_a.csv")

DASHBOARD_DIR = Path("Outputs/dashboards")
LEGACY_DASHBOARD_DIR = Path("Archive/legacy_dashboards")
DASHBOARD_DIR.mkdir(parents=True, exist_ok=True)
LEGACY_DASHBOARD_DIR.mkdir(parents=True, exist_ok=True)

print("="*80)
print("DASHBOARD CSV GENERATION")
print("="*80)
print()

# Load data
print("Loading data...")
df_features = pd.read_csv(FEATURES_PATH)
df_segments = pd.read_csv(SEGMENTS_PATH)
df_geo = pd.read_csv(GEO_PATH)
df_cat = pd.read_csv(CAT_PATH)
df_loyalty = pd.read_csv(LOYALTY_A_PATH)
print(f"✓ Loaded {len(df_features):,} customers")
print()

# ============================================================================
# DASHBOARD 1: EXECUTIVE SUMMARY
# ============================================================================
print("="*80)
print("EXECUTIVE SUMMARY DASHBOARD")
print("="*80)
print()

# Calculate core KPIs
total_customers = len(df_features)
total_revenue = df_features['current_spend'].sum()
avg_spend = df_features['current_spend'].mean()
avg_previous_purchases = df_features['previous_purchase_history'].mean()
avg_satisfaction = df_features['satisfaction_score'].mean()
promo_exposure_rate = df_features['observed_promo_exposure_flag'].mean() * 100
subscription_rate = df_features['subscription_flag'].mean() * 100
avg_loyalty_score = df_loyalty['loyalty_score_a'].mean()

# Tier distribution
tier_dist = df_loyalty['loyalty_tier_a'].value_counts()
tier_4_pct = tier_dist.get('Tier 4: Very High', 0) / len(df_loyalty) * 100
tier_1_pct = tier_dist.get('Tier 1: Low', 0) / len(df_loyalty) * 100

# Segment distribution
segment_counts = df_segments['segment'].value_counts()
core_loyalists_pct = segment_counts.get('Core Loyalists', 0) / len(df_segments) * 100

# Top metrics
top_locations = df_geo.nlargest(5, 'Customer_Count')[['Location', 'Customer_Count', 'Avg_Spend', 'Promo_Exposure_Pct', 'Avg_Loyalty_Score']]
top_categories = df_cat.nlargest(4, 'Customer_Count')[['Category', 'Customer_Count', 'Avg_Spend', 'Promo_Exposure_Pct', 'Subscription_Pct']]

# Create executive summary dataframe
exec_summary = pd.DataFrame({
    'Metric': [
        'Total Customers',
        'Total Revenue',
        'Average Spend',
        'Average Previous Purchases',
        'Average Review Rating',
        'Promotional Exposure Rate',
        'Subscription Rate',
        'Average Loyalty Score (A)',
        'Tier 4 (Very High Loyalty) %',
        'Tier 1 (Low Loyalty) %',
        'Core Loyalists %'
    ],
    'Value': [
        f"{total_customers:,}",
        f"${total_revenue:,.2f}",
        f"${avg_spend:.2f}",
        f"{avg_previous_purchases:.1f}",
        f"{avg_satisfaction:.2f}",
        f"{promo_exposure_rate:.1f}%",
        f"{subscription_rate:.1f}%",
        f"{avg_loyalty_score:.2f}",
        f"{tier_4_pct:.1f}%",
        f"{tier_1_pct:.1f}%",
        f"{core_loyalists_pct:.1f}%"
    ]
})

exec_path = LEGACY_DASHBOARD_DIR / "01_executive_summary.csv"
exec_summary.to_csv(exec_path, index=False)
print(f"✓ Executive summary saved to: {exec_path}")

# Top locations
top_loc_path = LEGACY_DASHBOARD_DIR / "01a_top_locations.csv"
top_locations.to_csv(top_loc_path, index=False)
print(f"✓ Top locations saved to: {top_loc_path}")

# Top categories
top_cat_path = LEGACY_DASHBOARD_DIR / "01b_top_categories.csv"
top_categories.to_csv(top_cat_path, index=False)
print(f"✓ Top categories saved to: {top_cat_path}")
print()

# ============================================================================
# DASHBOARD 2: SEGMENT PERFORMANCE
# ============================================================================
print("="*80)
print("SEGMENT PERFORMANCE DASHBOARD")
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

segment_dashboard = []

for segment in segment_order:
    seg_df = df_segments[df_segments['segment'] == segment]

    metrics = {
        'Segment': segment,
        'Customer_Count': len(seg_df),
        'Customer_Pct': len(seg_df) / len(df_segments) * 100,
        'Total_Revenue': seg_df['current_spend'].sum(),
        'Revenue_Pct': seg_df['current_spend'].sum() / df_segments['current_spend'].sum() * 100,
        'Avg_Spend': seg_df['current_spend'].mean(),
        'Avg_Previous_Purchases': seg_df['previous_purchase_history'].mean(),
        'Avg_Frequency_Score': seg_df['purchase_frequency_score'].mean(),
        'Promo_Exposure_Pct': seg_df['observed_promo_exposure_flag'].mean() * 100,
        'Avg_Satisfaction': seg_df['satisfaction_score'].mean(),
        'High_Satisfaction_Pct': (seg_df['high_satisfaction_flag'] == 1).mean() * 100,
        'Subscription_Pct': seg_df['subscription_flag'].mean() * 100,
        'Avg_Loyalty_Score': seg_df['loyalty_score_a'].mean(),
        'Avg_Age': seg_df['age'].mean() if 'age' in seg_df.columns else None
    }

    segment_dashboard.append(metrics)

    print(f"{segment}: {metrics['Customer_Count']:,} customers | {metrics['Revenue_Pct']:.1f}% revenue | {metrics['Promo_Exposure_Pct']:.0f}% promo")

print()

df_segment_dash = pd.DataFrame(segment_dashboard)
seg_path = DASHBOARD_DIR / "02_segment_performance.csv"
df_segment_dash.to_csv(seg_path, index=False)
print(f"✓ Segment performance saved to: {seg_path}")

# Segment × Location cross-tab
seg_loc = pd.crosstab(
    df_segments['location'],
    df_segments['segment'],
    normalize='index'
) * 100
seg_loc = seg_loc[segment_order]
seg_loc_path = DASHBOARD_DIR / "02a_segment_by_location.csv"
seg_loc.to_csv(seg_loc_path)
print(f"✓ Segment × Location saved to: {seg_loc_path}")

# Segment × Category cross-tab
seg_cat = pd.crosstab(
    df_segments['category'],
    df_segments['segment'],
    normalize='index'
) * 100
seg_cat = seg_cat[segment_order]
# No CSV is written: this grain is fully reproducible from the retained
# customer-level customer_segments.csv table.
print()

# ============================================================================
# DASHBOARD 3: GEOGRAPHIC PERFORMANCE
# ============================================================================
print("="*80)
print("GEOGRAPHIC PERFORMANCE DASHBOARD")
print("="*80)
print()

# Add high-loyalty % to geographic dashboard
df_geo_full = df_geo.copy()
df_geo_full['High_Loyalty_Pct'] = df_geo_full['Location'].apply(
    lambda loc: ((df_segments[df_segments['location'] == loc]['segment'].isin(['Core Loyalists', 'Emerging Loyalists'])).mean()) * 100
)

# Top 20 locations by customer count
top20_geo = df_geo_full.nlargest(20, 'Customer_Count')
top20_geo_path = LEGACY_DASHBOARD_DIR / "03_top_20_locations.csv"
top20_geo.to_csv(top20_geo_path, index=False)
print(f"✓ Top 20 locations saved to: {top20_geo_path}")

# All locations summary
all_geo_path = DASHBOARD_DIR / "03_all_locations.csv"
df_geo_full.to_csv(all_geo_path, index=False)
print(f"✓ All locations saved to: {all_geo_path}")

# Geographic tier summary
df_geo_full['Geo_Tier'] = pd.qcut(df_geo_full['Customer_Count'], q=3, labels=['Small', 'Medium', 'Large'])
geo_tier_summary = df_geo_full.groupby('Geo_Tier').agg({
    'Location': 'count',
    'Customer_Count': 'sum',
    'Total_Revenue': 'sum',
    'Avg_Spend': 'mean',
    'Promo_Exposure_Pct': 'mean',
    'Avg_Loyalty_Score': 'mean',
    'Subscription_Pct': 'mean',
    'High_Loyalty_Pct': 'mean'
}).reset_index()
geo_tier_summary.columns = ['Geo_Tier', 'Location_Count', 'Total_Customers', 'Total_Revenue', 'Avg_Spend', 'Avg_Promo_Exposure', 'Avg_Loyalty_Score', 'Avg_Subscription_Pct', 'Avg_High_Loyalty_Pct']
geo_tier_path = DASHBOARD_DIR / "03_geographic_tier_summary.csv"
geo_tier_summary.to_csv(geo_tier_path, index=False)
print(f"✓ Geographic tier summary saved to: {geo_tier_path}")
print()

# ============================================================================
# DASHBOARD 4: CATEGORY PERFORMANCE
# ============================================================================
print("="*80)
print("CATEGORY PERFORMANCE DASHBOARD")
print("="*80)
print()

# Full category dashboard
cat_dashboard = df_cat.copy()
cat_path_full = DASHBOARD_DIR / "04_category_performance.csv"
cat_dashboard.to_csv(cat_path_full, index=False)
print(f"✓ Category performance saved to: {cat_path_full}")

# Category × Segment cross-tab
cat_seg = pd.crosstab(
    df_segments['category'],
    df_segments['segment'],
    normalize='index'
) * 100
cat_seg = cat_seg[segment_order]
cat_seg_path = LEGACY_DASHBOARD_DIR / "04a_category_by_segment.csv"
cat_seg.to_csv(cat_seg_path)
print(f"✓ Category × Segment saved to: {cat_seg_path}")

# Category × Age cross-tab
df_segments['age_band'] = pd.cut(
    df_segments['age'],
    bins=[0, 25, 35, 45, 55, 65, 100],
    labels=['18-24', '25-34', '35-44', '45-54', '55-64', '65+']
) if 'age' in df_segments.columns else df_segments['age_band']

cat_age = pd.crosstab(
    df_segments['category'],
    df_segments['age_band'],
    normalize='index'
) * 100
cat_age_path = LEGACY_DASHBOARD_DIR / "04b_category_by_age.csv"
cat_age.to_csv(cat_age_path)
print(f"✓ Category × Age saved to: {cat_age_path}")

# Category × Gender cross-tab
cat_gender = pd.crosstab(
    df_segments['category'],
    df_segments['gender'],
    normalize='index'
) * 100
cat_gender_path = LEGACY_DASHBOARD_DIR / "04c_category_by_gender.csv"
cat_gender.to_csv(cat_gender_path)
print(f"✓ Category × Gender saved to: {cat_gender_path}")
print()

# ============================================================================
# SUMMARY
# ============================================================================
print("="*80)
print("DASHBOARD GENERATION COMPLETE")
print("="*80)
print()
print(f"Output directory: {DASHBOARD_DIR}")
print()
print("Files created:")
for f in sorted(DASHBOARD_DIR.iterdir()):
    print(f"  • {f.name}")
print()
print("Next: QA validation (Python/11_validation.py)")
print()

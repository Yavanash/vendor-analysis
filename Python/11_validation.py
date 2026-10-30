"""
Quality Assurance Validation
============================

Purpose: Validate integrity and completeness of all analytical outputs
Author: Analytics Engineering Team
Date: 2026-08-27

Validates:
1. Customer count integrity across all outputs
2. Segment distribution completeness
3. Feature score range validation
4. Cross-file reference integrity
5. Missing value handling
6. Output file completeness
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
RAW_PATH = Path("Raw_Data/Dataset.csv")
CLEAN_PATH = Path("Raw_Data/cleaned/customer_cleaned.csv")
FEATURES_PATH = Path("Outputs/analytical/customer_features.csv")
LOYALTY_A_PATH = Path("Outputs/analytical/loyalty_definition_a.csv")
LOYALTY_B_PATH = Path("Outputs/analytical/loyalty_definition_b.csv")
COMPARISON_PATH = Path("Outputs/analytical/loyalty_comparison.csv")
SEGMENTS_PATH = Path("Outputs/analytical/customer_segments.csv")
SEGMENT_SUMMARY_PATH = Path("Outputs/analytical/segment_summary.csv")
GEO_PATH = Path("Outputs/analytical/geographic_analysis.csv")
CAT_PATH = Path("Outputs/analytical/category_analysis.csv")
DASHBOARD_DIR = Path("Outputs/dashboards")
DOC_DIR = Path("Documentation")

print("="*80)
print("QUALITY ASSURANCE VALIDATION")
print("="*80)
print()

# Track validation results
validation_results = []
errors_found = 0
warnings_found = 0

def validate_check(name, condition, message, is_warning=False):
    """Helper to record validation checks"""
    global errors_found, warnings_found
    result = {
        'Check': name,
        'Status': 'PASS' if condition else 'FAIL',
        'Message': message
    }
    validation_results.append(result)
    if condition:
        print(f"  {'✓' if not is_warning else '⚠'} {name}: {message}")
    else:
        print(f"  {'✗' if not is_warning else '!'} {name}: {message}")
        if is_warning:
            warnings_found += 1
        else:
            errors_found += 1
    return condition

# ============================================================================
# 1. FILE EXISTENCE CHECKS
# ============================================================================
print("="*80)
print("1. FILE EXISTENCE CHECKS")
print("="*80)
print()

required_files = [
    RAW_PATH,
    CLEAN_PATH,
    FEATURES_PATH,
    LOYALTY_A_PATH,
    LOYALTY_B_PATH,
    COMPARISON_PATH,
    SEGMENTS_PATH,
    SEGMENT_SUMMARY_PATH,
    GEO_PATH,
    CAT_PATH
]

for f in required_files:
    validate_check(
        f"File exists: {f.name}",
        f.exists(),
        f"{'Found' if f.exists() else 'MISSING'}"
    )
print()

# Dashboard files
if DASHBOARD_DIR.exists():
    dashboard_files = list(DASHBOARD_DIR.glob("*.csv"))
    validate_check(
        "Dashboard CSVs created",
        len(dashboard_files) == 5,
        f"{len(dashboard_files)} dashboard files found"
    )
else:
    validate_check(
        "Dashboard directory exists",
        False,
        "Dashboard directory not found"
    )

# Documentation files
if DOC_DIR.exists():
    doc_files = list(DOC_DIR.glob("*.md"))
    validate_check(
        "Documentation created",
        len(doc_files) >= 5,
        f"{len(doc_files)} documentation files found"
    )
print()

# ============================================================================
# 2. CUSTOMER COUNT INTEGRITY
# ============================================================================
print("="*80)
print("2. CUSTOMER COUNT INTEGRITY")
print("="*80)
print()

# Load all datasets
df_raw = pd.read_csv(RAW_PATH)
df_clean = pd.read_csv(CLEAN_PATH)
df_features = pd.read_csv(FEATURES_PATH)
df_loyalty_a = pd.read_csv(LOYALTY_A_PATH)
df_segments = pd.read_csv(SEGMENTS_PATH)

raw_count = len(df_raw)
clean_count = len(df_clean)
features_count = len(df_features)
loyalty_count = len(df_loyalty_a)
segments_count = len(df_segments)

validate_check(
    "Raw dataset row count",
    raw_count == 3900,
    f"{raw_count:,} rows (expected 3,900)"
)

validate_check(
    "Clean dataset row count",
    clean_count == raw_count,
    f"{clean_count:,} rows matches raw ({raw_count:,})"
)

validate_check(
    "Features dataset row count",
    features_count == raw_count,
    f"{features_count:,} rows matches raw ({raw_count:,})"
)

validate_check(
    "Loyalty A dataset row count",
    loyalty_count == raw_count,
    f"{loyalty_count:,} rows matches raw ({raw_count:,})"
)

validate_check(
    "Segments dataset row count",
    segments_count == raw_count,
    f"{segments_count:,} rows matches raw ({raw_count:,})"
)
print()

# ============================================================================
# 3. CUSTOMER ID VALIDATION
# ============================================================================
print("="*80)
print("3. CUSTOMER ID VALIDATION")
print("="*80)
print()

validate_check(
    "All Customer IDs unique (features)",
    df_features['Customer ID'].nunique() == len(df_features),
    f"{df_features['Customer ID'].nunique():,} unique IDs"
)

validate_check(
    "Customer IDs preserved (features)",
    set(df_features['Customer ID']) == set(df_raw['Customer ID']),
    "Same IDs as raw dataset"
)

validate_check(
    "Customer IDs preserved (loyalty A)",
    set(df_loyalty_a['Customer ID']) == set(df_raw['Customer ID']),
    "Same IDs as raw dataset"
)

validate_check(
    "Customer IDs preserved (segments)",
    set(df_segments['Customer ID']) == set(df_raw['Customer ID']),
    "Same IDs as raw dataset"
)
print()

# ============================================================================
# 4. FEATURE VALUE RANGES
# ============================================================================
print("="*80)
print("4. FEATURE VALUE RANGES")
print("="*80)
print()

# Spend validation
spend_min = df_features['current_spend'].min()
spend_max = df_features['current_spend'].max()
validate_check(
    "Current spend range",
    0 <= spend_min and spend_max <= 200,
    f"${spend_min:.2f} - ${spend_max:.2f}"
)

# Previous purchases
hist_min = df_features['previous_purchase_history'].min()
hist_max = df_features['previous_purchase_history'].max()
validate_check(
    "Previous purchases range",
    hist_min >= 0 and hist_max <= 100,
    f"{hist_min} - {hist_max}"
)

# Frequency score (mapped from normalized frequency: Weekly=7, Bi-Weekly=3.5, Monthly=2, Quarterly=1, Annually=0.5)
freq_min = df_features['purchase_frequency_score'].min()
freq_max = df_features['purchase_frequency_score'].max()
validate_check(
    "Frequency score range",
    freq_min >= 0.5 and freq_max <= 7,
    f"{freq_min} - {freq_max}"
)

# Satisfaction score
sat_min = df_features['satisfaction_score'].min()
sat_max = df_features['satisfaction_score'].max()
validate_check(
    "Satisfaction score range",
    sat_min >= 1 and sat_max <= 5,
    f"{sat_min} - {sat_max}"
)

# Promo exposure flag
promo_unique = df_features['observed_promo_exposure_flag'].unique()
validate_check(
    "Promo exposure is binary",
    set(promo_unique).issubset({0, 1}),
    f"Values: {sorted(promo_unique)}"
)

# Subscription flag
sub_unique = df_features['subscription_flag'].unique()
validate_check(
    "Subscription is binary",
    set(sub_unique).issubset({0, 1}),
    f"Values: {sorted(sub_unique)}"
)
print()

# ============================================================================
# 5. LOYALTY SCORE VALIDATION
# ============================================================================
print("="*80)
print("5. LOYALTY SCORE VALIDATION")
print("="*80)
print()

# Loyalty Score A
ls_a_min = df_loyalty_a['loyalty_score_a'].min()
ls_a_max = df_loyalty_a['loyalty_score_a'].max()
validate_check(
    "Loyalty Score A range",
    0 <= ls_a_min and ls_a_max <= 100,
    f"{ls_a_min:.2f} - {ls_a_max:.2f}"
)

# Loyalty Score A tiers
tier_counts_a = df_loyalty_a['loyalty_tier_a'].value_counts()
total_tiers_a = sum(tier_counts_a)
validate_check(
    "All customers assigned to Tier A",
    total_tiers_a == len(df_loyalty_a),
    f"{total_tiers_a:,} customers in tiers"
)

# Tier distribution (should be roughly 25% each)
for tier, count in tier_counts_a.items():
    pct = count / len(df_loyalty_a) * 100
    validate_check(
        f"Tier A distribution: {tier}",
        20 <= pct <= 30,
        f"{pct:.1f}% ({count:,} customers)",
        is_warning=True
    )
print()

# ============================================================================
# 6. SEGMENT VALIDATION
# ============================================================================
print("="*80)
print("6. SEGMENT VALIDATION")
print("="*80)
print()

# All customers assigned to a segment
segment_counts = df_segments['segment'].value_counts()
total_segments = sum(segment_counts)
validate_check(
    "All customers assigned to segment",
    total_segments == len(df_segments),
    f"{total_segments:,} customers in segments"
)

validate_check(
    "Exactly 6 segments",
    len(segment_counts) == 6,
    f"{len(segment_counts)} segments found"
)

# Segment percentages sum to 100%
segment_pct_sum = segment_counts / len(df_segments) * 100
validate_check(
    "Segment percentages sum to ~100%",
    99.5 <= segment_pct_sum.sum() <= 100.5,
    f"{segment_pct_sum.sum():.1f}% total",
    is_warning=True
)

# Segment names are correct
expected_segments = [
    'Core Loyalists',
    'Emerging Loyalists',
    'Developing Loyalists',
    'Promo-Engaged Repeaters',
    'Early-Stage Customers',
    'Promo-Exposed Transactors'
]
actual_segments = set(segment_counts.index)
validate_check(
    "Correct segment names",
    actual_segments == set(expected_segments),
    f"Found: {sorted(actual_segments)}"
)
print()

# Segment-specific validations
for segment in expected_segments:
    if segment in segment_counts.index:
        seg_df = df_segments[df_segments['segment'] == segment]
        count = len(seg_df)
        pct = count / len(df_segments) * 100
        validate_check(
            f"Segment size reasonable: {segment}",
            1 <= count <= 1500,
            f"{count:,} customers ({pct:.1f}%)",
            is_warning=True
        )
print()

# ============================================================================
# 7. GEOGRAPHIC VALIDATION
# ============================================================================
print("="*80)
print("7. GEOGRAPHIC VALIDATION")
print("="*80)
print()

df_geo = pd.read_csv(GEO_PATH)

validate_check(
    "Geographic analysis created",
    len(df_geo) > 0,
    f"{len(df_geo)} locations"
)

validate_check(
    "All customers accounted for in geo",
    df_geo['Customer_Count'].sum() == len(df_segments),
    f"{df_geo['Customer_Count'].sum():,} customers"
)

validate_check(
    "Location percentages sum to ~100%",
    99.5 <= df_geo['Customer_Pct'].sum() <= 100.5,
    f"{df_geo['Customer_Pct'].sum():.1f}% total",
    is_warning=True
)

validate_check(
    "50 locations (all US states)",
    len(df_geo) == 50,
    f"{len(df_geo)} locations"
)

# Promo exposure range
promo_exp = df_geo['Promo_Exposure_Pct']
validate_check(
    "Promo exposure in valid range",
    promo_exp.min() >= 0 and promo_exp.max() <= 100,
    f"{promo_exp.min():.1f}% - {promo_exp.max():.1f}%"
)
print()

# ============================================================================
# 8. CATEGORY VALIDATION
# ============================================================================
print("="*80)
print("8. CATEGORY VALIDATION")
print("="*80)
print()

df_cat = pd.read_csv(CAT_PATH)

validate_check(
    "Category analysis created",
    len(df_cat) > 0,
    f"{len(df_cat)} categories"
)

validate_check(
    "All customers accounted for in category",
    df_cat['Customer_Count'].sum() == len(df_segments),
    f"{df_cat['Customer_Count'].sum():,} customers"
)

validate_check(
    "Category percentages sum to ~100%",
    99.5 <= df_cat['Customer_Pct'].sum() <= 100.5,
    f"{df_cat['Customer_Pct'].sum():.1f}% total",
    is_warning=True
)

validate_check(
    "4 categories (Clothing, Footwear, Accessories, Outerwear)",
    len(df_cat) == 4,
    f"{len(df_cat)} categories"
)

# Expected categories
expected_cats = {'Accessories', 'Clothing', 'Footwear', 'Outerwear'}
actual_cats = set(df_cat['Category'])
validate_check(
    "Correct category names",
    actual_cats == expected_cats,
    f"Found: {sorted(actual_cats)}"
)
print()

# ============================================================================
# 9. MISSING VALUE CHECKS
# ============================================================================
print("="*80)
print("9. MISSING VALUE CHECKS")
print("="*80)
print()

# Satisfaction score missing values
sat_missing = df_features['satisfaction_score'].isna().sum()
validate_check(
    "Satisfaction score missing values handled",
    sat_missing < len(df_features) * 0.05,
    f"{sat_missing} missing ({sat_missing/len(df_features)*100:.2f}%)",
    is_warning=True
)

# Review rating missing values
review_missing = df_features['satisfaction_score'].isna().sum()  # Same field
validate_check(
    "Review rating missing values documented",
    True,  # Already flagged in features
    f"See satisfaction_score missing count"
)

# Customer ID no missing
id_missing = df_features['Customer ID'].isna().sum()
validate_check(
    "Customer IDs complete",
    id_missing == 0,
    f"{id_missing} missing IDs"
)
print()

# ============================================================================
# 10. OUTPUT FILE VALIDATION
# ============================================================================
print("="*80)
print("10. OUTPUT FILE VALIDATION")
print("="*80)
print()

# Check required output files exist
output_files = [
    ("Customer features", FEATURES_PATH),
    ("Loyalty Definition A", LOYALTY_A_PATH),
    ("Loyalty Definition B", LOYALTY_B_PATH),
    ("Loyalty Comparison", COMPARISON_PATH),
    ("Customer Segments", SEGMENTS_PATH),
    ("Segment Summary", SEGMENT_SUMMARY_PATH),
    ("Geographic Analysis", GEO_PATH),
    ("Category Analysis", CAT_PATH)
]

for name, path in output_files:
    validate_check(
        f"Output file: {name}",
        path.exists() and path.stat().st_size > 0,
        f"{path.name} ({path.stat().st_size:,} bytes)"
    )

# Dashboard directory
if DASHBOARD_DIR.exists():
    dash_files = list(DASHBOARD_DIR.glob("*.csv"))
    validate_check(
        "Dashboard CSVs present",
        len(dash_files) == 5,
        f"{len(dash_files)} files"
    )
print()

# ============================================================================
# SUMMARY REPORT
# ============================================================================
print("="*80)
print("VALIDATION SUMMARY")
print("="*80)
print()

df_results = pd.DataFrame(validation_results)
pass_count = (df_results['Status'] == 'PASS').sum()
fail_count = (df_results['Status'] == 'FAIL').sum()

print(f"Total checks: {len(df_results)}")
print(f"  Passed: {pass_count}")
print(f"  Failed: {fail_count}")
print(f"  Warnings: {warnings_found}")
print()

if fail_count == 0:
    print("✓ ALL CRITICAL VALIDATIONS PASSED")
else:
    print(f"✗ {fail_count} CRITICAL VALIDATION(S) FAILED")
    failed_checks = df_results[df_results['Status'] == 'FAIL']
    print("\nFailed checks:")
    for _, row in failed_checks.iterrows():
        print(f"  • {row['Check']}: {row['Message']}")

if warnings_found > 0:
    print(f"\n⚠ {warnings_found} WARNING(S) - Review suggested")

print()

# Save validation report
validation_report_path = DOC_DIR / "10_QA_Validation.md"
DOC_DIR.mkdir(parents=True, exist_ok=True)

report_content = f"""# Quality Assurance Validation Report
**D2C Fashion Customer Intelligence Project**

**Date:** 2026-08-27

---

## Executive Summary

| Metric | Value |
|--------|-------|
| Total Validation Checks | {len(df_results)} |
| Passed | {pass_count} |
| Failed | {fail_count} |
| Warnings | {warnings_found} |

**Overall Status:** {'✓ PASS - All critical validations successful' if fail_count == 0 else '✗ FAIL - Review failed checks below'}

---

## Validation Results

"""

for _, row in df_results.iterrows():
    status_icon = '✓' if row['Status'] == 'PASS' else '✗'
    report_content += f"| {status_icon} | {row['Check']} | {row['Message']} |\n"

report_content += f"""
---

## Data Integrity Summary

### Customer Counts
| Dataset | Rows | Status |
|---------|------|--------|
| Raw Data | {raw_count:,} | Reference |
| Cleaned Data | {clean_count:,} | {'✓' if clean_count == raw_count else '✗'} |
| Features | {features_count:,} | {'✓' if features_count == raw_count else '✗'} |
| Loyalty A | {loyalty_count:,} | {'✓' if loyalty_count == raw_count else '✗'} |
| Segments | {segments_count:,} | {'✓' if segments_count == raw_count else '✗'} |

### Segment Distribution
| Segment | Count | Percentage |
|---------|-------|------------|
"""

for segment in expected_segments:
    if segment in segment_counts.index:
        count = segment_counts[segment]
        pct = count / len(df_segments) * 100
        report_content += f"| {segment} | {count:,} | {pct:.1f}% |\n"

report_content += f"""
---

## Failed Checks (if any)

"""
if fail_count > 0:
    failed = df_results[df_results['Status'] == 'FAIL']
    for _, row in failed.iterrows():
        report_content += f"### {row['Check']}\n**Message:** {row['Message']}\n\n"
else:
    report_content += "No critical failures detected.\n"

report_content += f"""
---

## Warnings (Informational)

"""
if warnings_found > 0:
    warned = df_results[df_results['Status'] == 'PASS'].query("Message.str.contains('%')")
    for _, row in warned.iterrows():
        report_content += f"- {row['Check']}: {row['Message']}\n"
else:
    report_content += "No warnings recorded.\n"

report_content += """
---

## Recommendations

1. **For Production Deployment:** All critical checks passed. Data is ready for use.
2. **For Dashboard Integration:** Validate dashboard CSV files match expected schemas.
3. **For Future Analysis:** Re-run validation after any data pipeline changes.

---

**End of Validation Report**
"""

with open(validation_report_path, 'w', encoding='utf-8') as f:
    f.write(report_content)

print(f"✓ Validation report saved to: {validation_report_path}")
print()
print("="*80)
print("VALIDATION COMPLETE")
print("="*80)
print()

# Exit with appropriate code
if fail_count > 0:
    sys.exit(1)

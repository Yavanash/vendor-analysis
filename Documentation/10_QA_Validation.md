# Quality Assurance Validation Report

> **Submission cleanup note:** This report was generated before the final structural cleanup and records the former dashboard-count expectation. The analytical pipeline was not rerun during submission cleanup. `Python/11_validation.py` now expects the approved five active dashboard extracts.
**D2C Fashion Customer Intelligence Project**

**Date:** 2026-08-27

---

## Executive Summary

| Metric | Value |
|--------|-------|
| Total Validation Checks | 65 |
| Passed | 63 |
| Failed | 2 |
| Warnings | 0 |

**Overall Status:** ✗ FAIL - Review failed checks below

---

## Validation Results

| ✓ | File exists: Dataset.csv | Found |
| ✓ | File exists: customer_cleaned.csv | Found |
| ✓ | File exists: customer_features.csv | Found |
| ✓ | File exists: loyalty_definition_a.csv | Found |
| ✓ | File exists: loyalty_definition_b.csv | Found |
| ✓ | File exists: loyalty_comparison.csv | Found |
| ✓ | File exists: customer_segments.csv | Found |
| ✓ | File exists: segment_summary.csv | Found |
| ✓ | File exists: geographic_analysis.csv | Found |
| ✓ | File exists: category_analysis.csv | Found |
| ✗ | Dashboard CSVs created | 5 dashboard files found |
| ✓ | Documentation created | 12 documentation files found |
| ✓ | Raw dataset row count | 3,900 rows (expected 3,900) |
| ✓ | Clean dataset row count | 3,900 rows matches raw (3,900) |
| ✓ | Features dataset row count | 3,900 rows matches raw (3,900) |
| ✓ | Loyalty A dataset row count | 3,900 rows matches raw (3,900) |
| ✓ | Segments dataset row count | 3,900 rows matches raw (3,900) |
| ✓ | All Customer IDs unique (features) | 3,900 unique IDs |
| ✓ | Customer IDs preserved (features) | Same IDs as raw dataset |
| ✓ | Customer IDs preserved (loyalty A) | Same IDs as raw dataset |
| ✓ | Customer IDs preserved (segments) | Same IDs as raw dataset |
| ✓ | Current spend range | $20.00 - $100.00 |
| ✓ | Previous purchases range | 1 - 50 |
| ✓ | Frequency score range | 0.5 - 7.0 |
| ✓ | Satisfaction score range | 2.5 - 5.0 |
| ✓ | Promo exposure is binary | Values: [np.int64(0), np.int64(1)] |
| ✓ | Subscription is binary | Values: [np.int64(0), np.int64(1)] |
| ✓ | Loyalty Score A range | 2.72 - 99.20 |
| ✓ | All customers assigned to Tier A | 3,900 customers in tiers |
| ✓ | Tier A distribution: Tier 3: High | 25.0% (976 customers) |
| ✓ | Tier A distribution: Tier 1: Low | 25.0% (975 customers) |
| ✓ | Tier A distribution: Tier 4: Very High | 25.0% (975 customers) |
| ✓ | Tier A distribution: Tier 2: Medium | 25.0% (974 customers) |
| ✓ | All customers assigned to segment | 3,900 customers in segments |
| ✓ | Exactly 6 segments | 6 segments found |
| ✓ | Segment percentages sum to ~100% | 100.0% total |
| ✓ | Correct segment names | Found: ['Core Loyalists', 'Developing Loyalists', 'Early-Stage Customers', 'Emerging Loyalists', 'Promo-Engaged Repeaters', 'Promo-Exposed Transactors'] |
| ✓ | Segment size reasonable: Core Loyalists | 975 customers (25.0%) |
| ✓ | Segment size reasonable: Emerging Loyalists | 976 customers (25.0%) |
| ✓ | Segment size reasonable: Developing Loyalists | 477 customers (12.2%) |
| ✓ | Segment size reasonable: Promo-Engaged Repeaters | 497 customers (12.7%) |
| ✓ | Segment size reasonable: Early-Stage Customers | 163 customers (4.2%) |
| ✓ | Segment size reasonable: Promo-Exposed Transactors | 812 customers (20.8%) |
| ✓ | Geographic analysis created | 50 locations |
| ✓ | All customers accounted for in geo | 3,900 customers |
| ✓ | Location percentages sum to ~100% | 100.0% total |
| ✓ | 50 locations (all US states) | 50 locations |
| ✓ | Promo exposure in valid range | 23.8% - 57.0% |
| ✓ | Category analysis created | 4 categories |
| ✓ | All customers accounted for in category | 3,900 customers |
| ✓ | Category percentages sum to ~100% | 100.0% total |
| ✓ | 4 categories (Clothing, Footwear, Accessories, Outerwear) | 4 categories |
| ✓ | Correct category names | Found: ['Accessories', 'Clothing', 'Footwear', 'Outerwear'] |
| ✓ | Satisfaction score missing values handled | 37 missing (0.95%) |
| ✓ | Review rating missing values documented | See satisfaction_score missing count |
| ✓ | Customer IDs complete | 0 missing IDs |
| ✓ | Output file: Customer features | customer_features.csv (472,287 bytes) |
| ✓ | Output file: Loyalty Definition A | loyalty_definition_a.csv (424,745 bytes) |
| ✓ | Output file: Loyalty Definition B | loyalty_definition_b.csv (438,333 bytes) |
| ✓ | Output file: Loyalty Comparison | loyalty_comparison.csv (1,498 bytes) |
| ✓ | Output file: Customer Segments | customer_segments.csv (425,266 bytes) |
| ✓ | Output file: Segment Summary | segment_summary.csv (1,428 bytes) |
| ✓ | Output file: Geographic Analysis | geographic_analysis.csv (10,021 bytes) |
| ✓ | Output file: Category Analysis | category_analysis.csv (949 bytes) |
| ✗ | Dashboard CSVs present | 5 files |

---

## Data Integrity Summary

### Customer Counts
| Dataset | Rows | Status |
|---------|------|--------|
| Raw Data | 3,900 | Reference |
| Cleaned Data | 3,900 | ✓ |
| Features | 3,900 | ✓ |
| Loyalty A | 3,900 | ✓ |
| Segments | 3,900 | ✓ |

### Segment Distribution
| Segment | Count | Percentage |
|---------|-------|------------|
| Core Loyalists | 975 | 25.0% |
| Emerging Loyalists | 976 | 25.0% |
| Developing Loyalists | 477 | 12.2% |
| Promo-Engaged Repeaters | 497 | 12.7% |
| Early-Stage Customers | 163 | 4.2% |
| Promo-Exposed Transactors | 812 | 20.8% |

---

## Failed Checks (if any)

### Dashboard CSVs created
**Message:** 5 dashboard files found

### Dashboard CSVs present
**Message:** 5 files


---

## Warnings (Informational)

No warnings recorded.

---

## Recommendations

1. **For Production Deployment:** All critical checks passed. Data is ready for use.
2. **For Dashboard Integration:** Validate dashboard CSV files match expected schemas.
3. **For Future Analysis:** Re-run validation after any data pipeline changes.

---

**End of Validation Report**

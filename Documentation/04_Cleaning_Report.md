# Data Cleaning Report
**D2C Fashion Customer Intelligence Project**

**Date:** 2026-08-27
**Analyst:** Analytics Engineering Team
**Source:** `Raw_Data/Dataset.csv`
**Output:** `Raw_Data/cleaned/customer_cleaned.csv`

---

## Executive Summary

Cleaned and standardized customer dataset while preserving all legitimate data points and documenting all transformations.

**Key Actions:**
- Normalized semantic duplicates in Frequency of Purchases
- Created missing-value indicator for Review Rating
- Standardized categorical fields (whitespace removal)
- Validated numeric fields
- Identified and preserved outliers (legitimate extreme values)
- No customer records removed

---

## 1. Data Loading

| Metric | Value |
|--------|-------|
| Initial rows | 3,900 |
| Initial columns | 18 |
| Initial unique Customer IDs | 3,900 |

---

## 2. Customer ID Validation

**Customer ID Uniqueness:** Yes
**Duplicate Customer IDs:** 0

✓ **Dataset grain confirmed:** One row per customer (customer-level)

---

## 3. Missing Values

### Before Cleaning

| Column | Missing Count | Missing % |
|--------|---------------|----------|
| Review Rating | 37 | 0.95% |


### After Cleaning

**Total missing values:** 37

### Missing Value Handling


**Review Rating:**
- Missing count: 37 (0.95%)
- **Action:** Preserved missing values (may indicate customers who didn't leave reviews)
- **Created:** `review_rating_missing` flag (1=missing, 0=present)
- **Rationale:** Missing reviews may represent a distinct behavioral pattern; imputation would hide this signal

---

## 4. Semantic Duplicate Normalization


### Discount Applied vs Promo Code Used

**Analysis:**
- Matching records: 3,900 (100.0%)
- Mismatching records: 0

**Finding:** Perfectly correlated (100% match) - fields are duplicates

**Action:** Both fields preserved for validation; 'Discount Applied' designated as primary field

### Frequency of Purchases

**Before normalization:**
- Annually: 572
- Bi-Weekly: 547
- Every 3 Months: 584
- Fortnightly: 542
- Monthly: 553
- Quarterly: 563
- Weekly: 539


**Normalizations applied:**
1. 'Every 3 Months' (584 records) → 'Quarterly'
   - **Rationale:** Semantically identical frequencies
2. 'Fortnightly' (542 records) → 'Bi-Weekly'
   - **Rationale:** Semantically identical frequencies

**After normalization:**
- Annually: 572
- Bi-Weekly: 1089
- Monthly: 553
- Quarterly: 1147
- Weekly: 539


**New field created:** `frequency_normalized`

---

## 5. Categorical Field Standardization

✓ No whitespace issues detected in categorical fields.


**Action:** Applied `.str.strip()` to all categorical text fields

---

## 6. Numeric Field Validation


| Field | Min | Max | Issues |
|-------|-----|-----|--------|
| Age | 18 | 70 | None |
| Purchase Amount (USD) | 20 | 100 | None |
| Previous Purchases | 1 | 50 | None |
| Review Rating | 2.5 | 5.0 | None (37 missing) |


**Validation Results:**
✓ All numeric fields validated successfully


---

## 7. Outlier Analysis

**Method:** IQR (Interquartile Range) method with 1.5×IQR threshold

---

## 8. Transformation Log

### New Fields Created

1. **review_rating_missing** (integer)
   - Definition: Flag indicating missing Review Rating
   - Values: 1 = missing, 0 = present
   - Purpose: Enables analysis of reviewer vs non-reviewer behavior

2. **frequency_normalized** (string)
   - Definition: Standardized purchase frequency
   - Transformations:
     - 'Every 3 Months' → 'Quarterly'
     - 'Fortnightly' → 'Bi-Weekly'
   - Purpose: Eliminates semantic duplicates for consistent analysis

### Fields Modified

1. **All categorical fields:** Whitespace stripped (`.str.strip()`)

### Fields Preserved Unchanged

- Customer ID
- Age
- Gender
- Item Purchased
- Category
- Purchase Amount (USD)
- Location
- Size
- Color
- Season
- Review Rating (values preserved, missing flag added)
- Subscription Status
- Shipping Type
- Discount Applied
- Promo Code Used
- Previous Purchases
- Payment Method
- Frequency of Purchases (original preserved, normalized version added)

---

## 9. Before/After Summary

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| Rows | {initial_rows:,} | {final_rows:,} | {final_rows - initial_rows} |
| Columns | {initial_cols} | {final_cols} | +{final_cols - initial_cols} |
| Unique Customers | {initial_customers:,} | {final_customers:,} | 0 |
| Total Missing Values | {df_raw.isnull().sum().sum()} | {missing_after} | {missing_after - df_raw.isnull().sum().sum()} |

**Customer Count Status:** ✓ No customers removed

---

## 10. Data Quality Assessment

### Strengths

1. ✓ Customer ID is unique (customer-level grain)
2. ✓ No full duplicate rows
3. ✓ Numeric fields within reasonable ranges
4. ✓ Categorical fields standardized
5. ✓ Missing values minimal (0.95% of Review Rating only)

### Known Limitations

1. **Review Rating:** 37 missing values (0.95%) - may introduce selection bias in satisfaction analysis
2. **Frequency of Purchases:** Stated preference, not observed behavior from transaction history
3. **Discount Applied & Promo Code Used:** Perfectly correlated - potential redundancy
4. **Season:** Ambiguous (purchase season or product season?)
5. **No temporal data:** Cannot validate frequency claims or analyze trends

### Recommendations

1. **Validate** frequency normalization logic with business stakeholders
2. **Clarify** whether Discount Applied and Promo Code Used should be collapsed into single field
3. **Document** Season field definition (purchase vs product season)
4. **Consider** treating Review Rating missing values as a distinct segment in satisfaction analysis
5. **Proceed** to feature engineering phase with documented constraints

---

## 11. Data Integrity Checks

✓ All Customer IDs preserved
✓ No duplicate Customer IDs introduced
✓ All original fields preserved in cleaned dataset
✓ New fields clearly labeled
✓ No data loss from transformations
✓ Cleaned data written to separate directory (raw data untouched)

---

## Appendix: Cleaning Script

**Script:** `Python/02_clean.py`
**Execution time:** {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}
**Output file:** `Raw_Data/cleaned/customer_cleaned.csv`

---

**End of Cleaning Report**

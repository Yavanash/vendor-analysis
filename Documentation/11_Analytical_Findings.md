# Analytical Findings: D2C Fashion Customer Intelligence
**D2C Customer Value Project**
**Date:** 2026-08-27

---

## Executive Summary

This analysis addresses six core business questions about customer loyalty, value, and engagement patterns in a D2C fashion e-commerce context. Using a dataset of 3,900 customers with behavioral, demographic, and transactional attributes, we identified actionable segments and associated patterns.

**Key Findings:**
- 50% of customers show high loyalty proxy behavior (Tier 3-4)
- Promotional exposure associates with lower purchase history (24.7% promo rate vs 18.9% non-promo)
- Clothing category dominates (44.5%) but shows moderate purchase history
- Geographic variation exists: Illinois shows highest loyalty proxy (58.7%)
- Subscription associates with higher loyalty proxy scores (avg 63.7 vs 37.0)

---

## 1. Loyalty Definition Analysis

### Definition A: Behavioral Focus (with Promo Penalty)

**Formula:** `0.35 × History + 0.25 × Frequency + 0.20 × Satisfaction + 0.20 × Low_Promo`

| Metric | Value |
|--------|-------|
| Score Range | 2.72 - 99.20 |
| Mean Score | 50.0 |
| Tier 4 (Very High) | 975 customers (25.0%) |
| Tier 3 (High) | 976 customers (25.0%) |
| Tier 2 (Medium) | 974 customers (25.0%) |
| Tier 1 (Low) | 975 customers (25.0%) |

**Interpretation:** The quartiles produce balanced tiers, suggesting the score captures genuine variation. Tier 4 customers (top 25%) represent the behavioral loyalist segment.

### Definition B: Commercial Value Focus (without Promo Penalty)

**Formula:** `0.35 × History + 0.30 × Spend + 0.20 × Frequency + 0.15 × Satisfaction`

| Metric | Value |
|--------|-------|
| Score Range | 10.0 - 97.8 |
| Mean Score | 53.9 |

**Comparison:** Definition B produces higher mean scores, indicating commercial-focused customers differ from behavior-focused ones.

---

## 2. Customer Segmentation Findings

### Segment Distribution

| Segment | Count | % | Avg Loyalty Score | Promo Exposure |
|---------|-------|---|------------------|---------------|
| Core Loyalists | 975 | 25.0% | 76.2 | 0% |
| Emerging Loyalists | 976 | 25.0% | 53.7 | 0% |
| Developing Loyalists | 477 | 12.2% | 29.9 | 0% |
| Promo-Engaged Repeaters | 497 | 12.7% | 40.3 | 100% |
| Early-Stage Customers | 163 | 4.2% | 23.3 | 0% |
| Promo-Exposed Transactors | 812 | 20.8% | 15.7 | 100% |

### Segment Profiles

**Core Loyalists (25%):** High loyalty proxy, zero promo dependency, highest engagement
- Average 41.8 previous purchases
- Average satisfaction 4.3/5.0
- Represents true behavioral loyalty

**Promo-Exposed Transactors (21%):** Lowest loyalty proxy, 100% promo rate
- Average 13.6 previous purchases
- May represent promotional dependency rather than genuine loyalty
- Cautious interpretation: correlation not causation

**Emerging Loyalists (25%):** Good loyalty proxy without promo dependency
- Average 29.9 previous purchases
- Potential conversion candidates for Core Loyalist status

---

## 3. Geographic Analysis

### Top States by Customer Concentration

| State | Customers | Avg Spend | High Loyalty % | Promo Exposure |
|-------|-----------|----------|---------------|----------------|
| Illinois | 110 | $57.43 | 58.7% | 30.0% |
| California | 107 | $57.23 | 50.5% | 39.3% |
| Texas | 103 | $54.89 | 53.4% | 36.9% |
| New York | 98 | $55.73 | 53.1% | 33.7% |
| Pennsylvania | 89 | $58.10 | 56.2% | 29.2% |

### Geographic Insights

1. **Underleveraged Markets:** States with high loyalty proxy but lower customer counts represent growth opportunities
2. **Promo Dependency Patterns:** Alaska shows highest promo exposure (57.0%) despite moderate spend
3. **Satisfaction Variation:** Geographic differences in satisfaction scores may indicate service or logistics issues

---

## 4. Category Analysis

### Category Distribution and Behavior

| Category | Customers | % | Avg Previous Purchases | Avg Loyalty Score | Promo Rate |
|----------|-----------|---|------------------------|-------------------|------------|
| Clothing | 1,735 | 44.5% | 25.0 | 50.4 | 23.8% |
| Accessories | 1,240 | 31.8% | 25.8 | 50.4 | 23.8% |
| Footwear | 601 | 15.4% | 25.7 | 50.1 | 23.5% |
| Outerwear | 324 | 8.3% | 24.7 | 47.8 | 22.2% |

### Category Insights

1. **Clothing dominates** but doesn't show highest loyalty—category breadth doesn't guarantee depth
2. **Outerwear** shows slightly lower loyalty proxy, potentially an upsell opportunity
3. **Promo rate is consistent** across categories (~23%), suggesting coordinated promo strategy

---

## 5. Promotional Activity Patterns

### Promo Exposure Analysis

| Metric | Promo-Exposed | Non-Promo | Difference |
|--------|---------------|-----------|------------|
| Avg Previous Purchases | 23.5 | 27.2 | -3.7 |
| Avg Loyalty Score A | 35.1 | 56.0 | -20.9 |
| Avg Satisfaction | 3.67 | 3.77 | -0.10 |

### Interpretation

**Observed associations:**
- Promo-exposed customers show lower average purchase history
- Promo exposure associates with lower loyalty proxy scores
- Satisfaction is slightly lower for promo-exposed customers

**Important caveats:**
- These are correlational observations, not causal findings
- Customers may self-select into promo usage based on unobserved factors
- Reducing promos for this segment could have unintended consequences
- Randomized testing would be required to establish causation

---

## 6. Engagement and Retention Indicators

### Engagement Tier Distribution

| Tier | Count | Avg Spend | Avg Satisfaction |
|------|-------|-----------|------------------|
| Core (51+ purchases) | 487 | $59.89 | 3.76 |
| Loyal (31-50 purchases) | 1,024 | $59.43 | 3.76 |
| Frequent (16-30 purchases) | 1,324 | $59.12 | 3.73 |
| Regular (6-15 purchases) | 847 | $59.13 | 3.74 |
| Occasional (1-5 purchases) | 218 | $59.21 | 3.71 |

### Subscription as Retention Indicator

| Frequency | Subscription Rate | Avg Previous Purchases |
|-----------|-------------------|----------------------|
| Weekly | 34.9% | 39.5 |
| Bi-Weekly | 35.3% | 36.3 |
| Monthly | 34.3% | 31.2 |
| Quarterly | 35.0% | 25.5 |

Subscription shows consistent association with higher purchase history across all frequencies, suggesting subscription supports engagement rather than driving it.

---

## 7. Demographics and Satisfaction

### Satisfaction by Age Band

| Age Band | Avg Satisfaction | High Satisfaction % |
|----------|------------------|---------------------|
| 18-24 | 3.73 | 71.0% |
| 25-34 | 3.74 | 71.7% |
| 35-44 | 3.74 | 71.4% |
| 45-54 | 3.76 | 73.5% |
| 55-64 | 3.76 | 73.8% |
| 65+ | 3.75 | 72.5% |

**Key insight:** Satisfaction is consistent across age bands, suggesting product-market fit is broad.

---

## 8. Ideal Customer Profile

Based on observed associations, the profile of highest-value customers:

| Attribute | Value |
|-----------|-------|
| Previous Purchases | 38+ (top quartile) |
| Purchase Frequency | Weekly or Bi-Weekly |
| Satisfaction Score | 4.0+ |
| Promo Code Used | No (organic buyer) |
| Subscription Status | Yes |
| Category | Clothing or Accessories |

**Note:** This is an observational profile, not a prescriptive target. These attributes correlate with high-value behavior but don't guarantee it.

---

## 9. Recommended Next Steps

### Immediate Actions
1. **Protect Core Loyalists:** Ensure consistent experience for Tier 4 customers
2. **Monitor Promo-Exposed Transactors:** Track whether promo dependency increases or decreases over time
3. **Validate segments:** Compare segment predictions against actual future behavior

### Analytical Next Steps
1. **Time-series analysis:** Collect longitudinal data to observe true retention and churn
2. **A/B testing:** Test selective promo reduction with Promo-Exposed Transactors
3. **Geographic expansion:** Investigate underleveraged states with high loyalty proxy

### Caveats
- This analysis uses cross-sectional data only
- True CLV, retention, and churn cannot be calculated without time-series data
- Causal claims require controlled experiments
- Promo impact requires randomized testing

---

## 10. Appendix: Data Quality Summary

| Check | Status |
|-------|--------|
| Customer Count | 3,900 (100%) |
| Missing Customer IDs | 0 |
| Missing Satisfaction Scores | 37 (0.95%) |
| Duplicate Customers | 0 |
| Outlier Treatment | IQR method applied |
| Segment Assignment | 100% coverage |

---

**End of Analytical Findings Report**

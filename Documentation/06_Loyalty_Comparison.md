# Loyalty Framework Comparison Report
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
| Tier 1: Low | 975 | 25.0% | $59.52 | $58,030 | 24.9% |
| Tier 2: Medium | 974 | 25.0% | $59.63 | $58,079 | 24.9% |
| Tier 3: High | 976 | 25.0% | $59.53 | $58,097 | 24.9% |
| Tier 4: Very High | 975 | 25.0% | $60.38 | $58,875 | 25.3% |

### Definition B (Commercial Value Proxy)

| Tier | Customers | % | Avg Spend | Total Current Observed Spend | Spend % |
|------|-----------|---|-----------|------------------------------|---------|
| Tier 1: Low | 975 | 25.0% | $42.19 | $41,137 | 17.6% |
| Tier 2: Medium | 975 | 25.0% | $55.41 | $54,027 | 23.2% |
| Tier 3: High | 975 | 25.0% | $64.11 | $62,507 | 26.8% |
| Tier 4: Very High | 975 | 25.0% | $77.34 | $75,410 | 32.4% |

---

## Detailed Metric Comparison (Tier 4: Very High)

| Metric | Definition A | Definition B |
|--------|--------------|--------------|
| **Customer Count** | 975 | 975 |
| **Total Current Observed Spend** | $58,875 | $75,410 |
| **Spend %** | 25.3% | 32.4% |
| **Avg Spend** | $60.38 | $77.34 |
| **Avg Previous Purchases** | 36.6 | 37.7 |
| **Avg Frequency Score** | 3.93 | 3.76 |
| **Avg Satisfaction** | 4.10 | 4.01 |
| **Promo Exposure %** | **11.0%** | 43.3% |
| **Subscription %** | 7.1% | 28.3% |

---

## Key Findings

### Definition A Strengths

1. **Clear Promotional Differentiation**
   - Tier 1 (Low): 83.3% promo exposure
   - Tier 4 (Very High): 11.0% promo exposure
   - **Range: -72.3 percentage points**

2. **Identifies Brand-Pull Customers**
   - Top tier shows strong purchase behavior WITHOUT promotional dependence
   - Only 11.0% promo exposure in most loyal segment

3. **Actionable for Promo Reduction Strategy**
   - Clear target: Tier 4 customers can sustain purchase without heavy discounting
   - Tier 1 customers show high promo association (83.3%)

4. **Answers Primary Business Question**
   - "Who are loyal vs promo-oriented customers?" → Definition A directly addresses this

### Definition B (Commercial Value Proxy) Strengths

1. **Stronger Spend Differentiation**
   - Tier 4 avg spend: $77.34
   - Tier 1 avg spend: $42.19
   - Spend concentration in Tier 4: 32.4%

2. **Commercial Value Focus**
   - Identifies high-value customers regardless of promotional channel
   - Useful for commercial value prioritization

3. **No Promo Discrimination**
   - Definition B Tier 4 promo exposure: 43.3% (similar across all tiers)
   - Does NOT differentiate on promotional behavior

### Critical Difference

**Definition A:** Promo exposure decreases dramatically as loyalty increases (83.3% → 11.0%)
**Definition B:** Promo exposure stays flat across all tiers (~43%)

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
- **Promo exposure:** Currently 11.0%
- **Customers:** 975 (25%)

**Tier 3 (High Loyalty):**
- **Action:** Test selective promo reduction
- **Expected outcome:** Some customers may maintain behavior without promo
- **Promo exposure:** Currently 26.7%
- **Customers:** 976 (25%)

**Tier 1-2 (Low-Medium Loyalty):**
- **Action:** Maintain or test promo optimization
- **Expected outcome:** High promo sensitivity; proceed carefully
- **Promo exposure:** 83.3% (Tier 1), 51.0% (Tier 2)
- **Customers:** 1,949 (50%)

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

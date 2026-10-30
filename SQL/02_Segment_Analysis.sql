-- ============================================================================
-- Segment Analysis SQL
-- Purpose: Customer segmentation analysis using derived loyalty metrics
-- Author: Analytics Engineering Team
-- Date: 2026-08-27
-- ============================================================================

-- Assumes customer_segments table has been created with segment assignments
-- See: Outputs/analytical/customer_segments.csv

-- ============================================================================
-- 1. Segment Distribution Summary
-- ============================================================================
SELECT
    segment,
    COUNT(*) AS customer_count,
    COUNT(*) * 100.0 / SUM(COUNT(*)) OVER() AS pct_of_customers,
    SUM(current_spend) AS total_revenue,
    SUM(current_spend) * 100.0 / SUM(SUM(current_spend)) OVER() AS pct_of_revenue,
    AVG(current_spend) AS avg_spend,
    AVG(loyalty_score_a) AS avg_loyalty_score
FROM customer_segments
GROUP BY segment
ORDER BY SUM(current_spend) DESC;

-- ============================================================================
-- 2. Segment Value Metrics
-- ============================================================================
SELECT
    segment,
    COUNT(*) AS customer_count,
    AVG(current_spend) AS avg_spend,
    AVG(previous_purchase_history) AS avg_previous_purchases,
    AVG(purchase_frequency_score) AS avg_frequency_score,
    AVG(satisfaction_score) AS avg_satisfaction,
    SUM(CASE WHEN observed_promo_exposure_flag = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS promo_exposure_pct
FROM customer_segments
GROUP BY segment
ORDER BY AVG(loyalty_score_a) DESC;

-- ============================================================================
-- 3. Segment by Promo Exposure
-- ============================================================================
SELECT
    segment,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN observed_promo_exposure_flag = 1 THEN 1 ELSE 0 END) AS promo_customers,
    SUM(CASE WHEN observed_promo_exposure_flag = 0 THEN 1 ELSE 0 END) AS non_promo_customers,
    SUM(CASE WHEN observed_promo_exposure_flag = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS promo_pct,
    SUM(CASE WHEN observed_promo_exposure_flag = 0 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS non_promo_pct
FROM customer_segments
GROUP BY segment
ORDER BY promo_pct DESC;

-- ============================================================================
-- 4. Segment by Subscription Status
-- ============================================================================
SELECT
    segment,
    COUNT(*) AS total_customers,
    SUM(subscription_flag) AS subscribers,
    SUM(1 - subscription_flag) AS non_subscribers,
    SUM(subscription_flag) * 100.0 / COUNT(*) AS subscription_rate_pct
FROM customer_segments
GROUP BY segment
ORDER BY subscription_rate_pct DESC;

-- ============================================================================
-- 5. Segment by Satisfaction Level
-- ============================================================================
SELECT
    segment,
    AVG(satisfaction_score) AS avg_satisfaction,
    MIN(satisfaction_score) AS min_satisfaction,
    MAX(satisfaction_score) AS max_satisfaction,
    SUM(CASE WHEN satisfaction_score >= 4 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS high_satisfaction_pct,
    SUM(CASE WHEN satisfaction_score < 3 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS low_satisfaction_pct
FROM customer_segments
GROUP BY segment
ORDER BY avg_satisfaction DESC;

-- ============================================================================
-- 6. Segment by Location (Cross-tab approach)
-- ============================================================================
SELECT
    location,
    SUM(CASE WHEN segment = 'Core Loyalists' THEN 1 ELSE 0 END) AS core_loyalists,
    SUM(CASE WHEN segment = 'Emerging Loyalists' THEN 1 ELSE 0 END) AS emerging_loyalists,
    SUM(CASE WHEN segment = 'Developing Loyalists' THEN 1 ELSE 0 END) AS developing_loyalists,
    SUM(CASE WHEN segment = 'Promo-Engaged Repeaters' THEN 1 ELSE 0 END) AS promo_engaged,
    SUM(CASE WHEN segment = 'Early-Stage Customers' THEN 1 ELSE 0 END) AS early_stage,
    SUM(CASE WHEN segment = 'Promo-Exposed Transactors' THEN 1 ELSE 0 END) AS promo_transactors,
    COUNT(*) AS total_customers
FROM customer_segments
GROUP BY location
ORDER BY COUNT(*) DESC;

-- ============================================================================
-- 7. Segment by Category
-- ============================================================================
SELECT
    category,
    SUM(CASE WHEN segment = 'Core Loyalists' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS core_loyalists_pct,
    SUM(CASE WHEN segment = 'Emerging Loyalists' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS emerging_loyalists_pct,
    SUM(CASE WHEN segment = 'Developing Loyalists' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS developing_loyalists_pct,
    SUM(CASE WHEN segment = 'Promo-Engaged Repeaters' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS promo_engaged_pct,
    SUM(CASE WHEN segment = 'Early-Stage Customers' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS early_stage_pct,
    SUM(CASE WHEN segment = 'Promo-Exposed Transactors' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS promo_transactors_pct,
    COUNT(*) AS total_customers
FROM customer_segments
GROUP BY category
ORDER BY COUNT(*) DESC;

-- ============================================================================
-- 8. Segment by Age Band
-- ============================================================================
SELECT
    age_band,
    SUM(CASE WHEN segment = 'Core Loyalists' THEN 1 ELSE 0 END) AS core_loyalists,
    SUM(CASE WHEN segment = 'Emerging Loyalists' THEN 1 ELSE 0 END) AS emerging_loyalists,
    SUM(CASE WHEN segment = 'Promo-Exposed Transactors' THEN 1 ELSE 0 END) AS promo_transactors,
    COUNT(*) AS total_customers
FROM customer_segments
GROUP BY age_band
ORDER BY
    CASE age_band
        WHEN '18-24' THEN 1
        WHEN '25-34' THEN 2
        WHEN '35-44' THEN 3
        WHEN '45-54' THEN 4
        WHEN '55-64' THEN 5
        ELSE 6
    END;

-- ============================================================================
-- 9. High-Loyalty Segment Deep Dive (Core + Emerging)
-- ============================================================================
SELECT
    CASE
        WHEN segment IN ('Core Loyalists', 'Emerging Loyalists') THEN 'High-Loyalty'
        ELSE 'Other'
    END AS loyalty_group,
    COUNT(*) AS customer_count,
    AVG(current_spend) AS avg_spend,
    AVG(previous_purchase_history) AS avg_previous_purchases,
    SUM(observed_promo_exposure_flag) * 100.0 / COUNT(*) AS promo_exposure_pct,
    AVG(satisfaction_score) AS avg_satisfaction
FROM customer_segments
GROUP BY
    CASE
        WHEN segment IN ('Core Loyalists', 'Emerging Loyalists') THEN 'High-Loyalty'
        ELSE 'Other'
    END;

-- ============================================================================
-- 10. Segment Transition Potential (Customers Near Tier Boundaries)
-- ============================================================================
-- Identify Tier 3 customers close to Tier 4 (potential Core Loyalist candidates)
SELECT
    loyalty_tier_a,
    COUNT(*) AS customer_count,
    AVG(loyalty_score_a) AS avg_score,
    MIN(loyalty_score_a) AS min_score,
    MAX(loyalty_score_a) AS max_score
FROM customer_segments
GROUP BY loyalty_tier_a
ORDER BY MIN(loyalty_score_a);

-- ============================================================================
-- End of Segment Analysis SQL
-- ============================================================================

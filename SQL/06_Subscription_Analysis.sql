-- ============================================================================
-- Subscription Analysis SQL
-- Purpose: Subscription status analysis and value assessment
-- Author: Analytics Engineering Team
-- Date: 2026-08-27
-- ============================================================================

-- ============================================================================
-- 1. Subscription Overview
-- ============================================================================
SELECT
    [Subscription Status],
    COUNT(*) AS customer_count,
    COUNT(*) * 100.0 / SUM(COUNT(*)) OVER() AS pct_of_customers,
    SUM([Purchase Amount (USD)]) AS total_revenue,
    AVG([Purchase Amount (USD)]) AS avg_spend
FROM customer_cleaned
GROUP BY [Subscription Status];

-- ============================================================================
-- 2. Subscriber vs Non-Subscriber Value Comparison
-- ============================================================================
SELECT
    [Subscription Status],
    COUNT(*) AS customer_count,
    AVG([Purchase Amount (USD)]) AS avg_spend,
    AVG([Previous Purchases]) AS avg_previous_purchases,
    AVG([Review Rating]) AS avg_review_rating,
    SUM(CASE WHEN [Promo Code Used] = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS promo_rate
FROM customer_cleaned
GROUP BY [Subscription Status];

-- ============================================================================
-- 3. Subscription by Gender
-- ============================================================================
SELECT
    [Gender],
    SUM(CASE WHEN [Subscription Status] = 'Yes' THEN 1 ELSE 0 END) AS subscribers,
    SUM(CASE WHEN [Subscription Status] = 'No' THEN 1 ELSE 0 END) AS non_subscribers,
    SUM(CASE WHEN [Subscription Status] = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS subscription_rate
FROM customer_cleaned
GROUP BY [Gender];

-- ============================================================================
-- 4. Subscription by Age Band
-- ============================================================================
SELECT
    CASE
        WHEN Age < 25 THEN '18-24'
        WHEN Age BETWEEN 25 AND 34 THEN '25-34'
        WHEN Age BETWEEN 35 AND 44 THEN '35-44'
        WHEN Age BETWEEN 45 AND 54 THEN '45-54'
        WHEN Age BETWEEN 55 AND 64 THEN '55-64'
        ELSE '65+'
    END AS age_band,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN [Subscription Status] = 'Yes' THEN 1 ELSE 0 END) AS subscribers,
    SUM(CASE WHEN [Subscription Status] = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS subscription_rate
FROM customer_cleaned
GROUP BY
    CASE
        WHEN Age < 25 THEN '18-24'
        WHEN Age BETWEEN 25 AND 34 THEN '25-34'
        WHEN Age BETWEEN 35 AND 44 THEN '35-44'
        WHEN Age BETWEEN 45 AND 54 THEN '45-54'
        WHEN Age BETWEEN 55 AND 64 THEN '55-64'
        ELSE '65+'
    END
ORDER BY subscription_rate DESC;

-- ============================================================================
-- 5. Subscription by Location (Top 10)
-- ============================================================================
SELECT TOP 10
    [Location],
    COUNT(*) AS customer_count,
    SUM(CASE WHEN [Subscription Status] = 'Yes' THEN 1 ELSE 0 END) AS subscribers,
    SUM(CASE WHEN [Subscription Status] = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS subscription_rate
FROM customer_cleaned
GROUP BY [Location]
ORDER BY subscription_rate DESC;

-- ============================================================================
-- 6. Subscription by Category
-- ============================================================================
SELECT
    [Category],
    COUNT(*) AS customer_count,
    SUM(CASE WHEN [Subscription Status] = 'Yes' THEN 1 ELSE 0 END) AS subscribers,
    SUM(CASE WHEN [Subscription Status] = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS subscription_rate
FROM customer_cleaned
GROUP BY [Category]
ORDER BY subscription_rate DESC;

-- ============================================================================
-- 7. Subscription by Purchase Frequency
-- ============================================================================
SELECT
    [Purchase Frequency],
    COUNT(*) AS customer_count,
    SUM(CASE WHEN [Subscription Status] = 'Yes' THEN 1 ELSE 0 END) AS subscribers,
    SUM(CASE WHEN [Subscription Status] = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS subscription_rate
FROM customer_cleaned
GROUP BY [Purchase Frequency]
ORDER BY subscription_rate DESC;

-- ============================================================================
-- 8. Subscription by Purchase History Band
-- ============================================================================
SELECT
    CASE
        WHEN [Previous Purchases] = 0 THEN 'New (0)'
        WHEN [Previous Purchases] BETWEEN 1 AND 10 THEN '1-10'
        WHEN [Previous Purchases] BETWEEN 11 AND 25 THEN '11-25'
        WHEN [Previous Purchases] BETWEEN 26 AND 50 THEN '26-50'
        ELSE '51+'
    END AS history_band,
    COUNT(*) AS customer_count,
    SUM(CASE WHEN [Subscription Status] = 'Yes' THEN 1 ELSE 0 END) AS subscribers,
    SUM(CASE WHEN [Subscription Status] = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS subscription_rate
FROM customer_cleaned
GROUP BY
    CASE
        WHEN [Previous Purchases] = 0 THEN 'New (0)'
        WHEN [Previous Purchases] BETWEEN 1 AND 10 THEN '1-10'
        WHEN [Previous Purchases] BETWEEN 11 AND 25 THEN '11-25'
        WHEN [Previous Purchases] BETWEEN 26 AND 50 THEN '26-50'
        ELSE '51+'
    END
ORDER BY MIN([Previous Purchases]);

-- ============================================================================
-- 9. Subscriber Profile Analysis
-- ============================================================================
SELECT
    CASE
        WHEN [Previous Purchases] >= 38 AND [Subscription Status] = 'Yes' THEN 'High History + Subscriber'
        WHEN [Previous Purchases] >= 38 AND [Subscription Status] = 'No' THEN 'High History + Non-Subscriber'
        WHEN [Previous Purchases] < 38 AND [Subscription Status] = 'Yes' THEN 'Low History + Subscriber'
        ELSE 'Low History + Non-Subscriber'
    END AS customer_segment,
    COUNT(*) AS customer_count,
    AVG([Purchase Amount (USD)]) AS avg_spend
FROM customer_cleaned
GROUP BY
    CASE
        WHEN [Previous Purchases] >= 38 AND [Subscription Status] = 'Yes' THEN 'High History + Subscriber'
        WHEN [Previous Purchases] >= 38 AND [Subscription Status] = 'No' THEN 'High History + Non-Subscriber'
        WHEN [Previous Purchases] < 38 AND [Subscription Status] = 'Yes' THEN 'Low History + Subscriber'
        ELSE 'Low History + Non-Subscriber'
    END
ORDER BY COUNT(*) DESC;

-- ============================================================================
-- 10. Subscription and Promo Interaction
-- ============================================================================
SELECT
    [Subscription Status],
    [Promo Code Used],
    COUNT(*) AS customer_count,
    AVG([Purchase Amount (USD)]) AS avg_spend,
    AVG([Previous Purchases]) AS avg_previous_purchases
FROM customer_cleaned
GROUP BY [Subscription Status], [Promo Code Used]
ORDER BY [Subscription Status], [Promo Code Used];

-- ============================================================================
-- 11. Subscription Rate by Channel
-- ============================================================================
SELECT
    [Preferred Login Device],
    COUNT(*) AS customer_count,
    SUM(CASE WHEN [Subscription Status] = 'Yes' THEN 1 ELSE 0 END) AS subscribers,
    SUM(CASE WHEN [Subscription Status] = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS subscription_rate
FROM customer_cleaned
GROUP BY [Preferred Login Device]
ORDER BY subscription_rate DESC;

-- ============================================================================
-- 12. Subscription by Review Rating Band
-- ============================================================================
SELECT
    CASE
        WHEN [Review Rating] >= 4.5 THEN 'Very High (4.5+)'
        WHEN [Review Rating] >= 4 THEN 'High (4-4.4)'
        WHEN [Review Rating] >= 3 THEN 'Medium (3-3.9)'
        ELSE 'Low (<3)'
    END AS rating_band,
    COUNT(*) AS customer_count,
    SUM(CASE WHEN [Subscription Status] = 'Yes' THEN 1 ELSE 0 END) AS subscribers,
    SUM(CASE WHEN [Subscription Status] = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS subscription_rate
FROM customer_cleaned
GROUP BY
    CASE
        WHEN [Review Rating] >= 4.5 THEN 'Very High (4.5+)'
        WHEN [Review Rating] >= 4 THEN 'High (4-4.4)'
        WHEN [Review Rating] >= 3 THEN 'Medium (3-3.9)'
        ELSE 'Low (<3)'
    END
ORDER BY MIN([Review Rating]) DESC;

-- ============================================================================
-- 13. Geographic Hotspots for Subscription Growth
-- ============================================================================
WITH location_sub AS (
    SELECT
        [Location],
        COUNT(*) AS customer_count,
        SUM(CASE WHEN [Subscription Status] = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS sub_rate
    FROM customer_cleaned
    GROUP BY [Location]
)
SELECT
    [Location],
    customer_count,
    sub_rate,
    CASE
        WHEN sub_rate < 20 THEN 'Low Subscription Opportunity'
        WHEN sub_rate < 30 THEN 'Moderate Subscription Opportunity'
        ELSE 'High Subscription Penetration'
    END AS opportunity_tier
FROM location_sub
WHERE customer_count >= 70
ORDER BY sub_rate;

-- ============================================================================
-- End of Subscription Analysis SQL
-- ============================================================================

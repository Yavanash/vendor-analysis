-- ============================================================================
-- Promo Analysis SQL
-- Purpose: Promotional activity analysis and impact assessment
-- Author: Analytics Engineering Team
-- Date: 2026-08-27
-- ============================================================================

-- ============================================================================
-- 1. Promo Code Usage Overview
-- ============================================================================
SELECT
    [Promo Code Used],
    COUNT(*) AS customer_count,
    COUNT(*) * 100.0 / SUM(COUNT(*)) OVER() AS pct_of_customers,
    AVG([Purchase Amount (USD)]) AS avg_spend,
    SUM([Purchase Amount (USD)]) AS total_revenue
FROM customer_cleaned
GROUP BY [Promo Code Used];

-- ============================================================================
-- 2. Discount Applied Overview
-- ============================================================================
SELECT
    [Discount Applied],
    COUNT(*) AS customer_count,
    COUNT(*) * 100.0 / SUM(COUNT(*)) OVER() AS pct_of_customers,
    AVG([Purchase Amount (USD)]) AS avg_spend,
    SUM([Purchase Amount (USD)]) AS total_revenue
FROM customer_cleaned
GROUP BY [Discount Applied];

-- ============================================================================
-- 3. Promo Code vs Discount Cross-tabulation
-- ============================================================================
SELECT
    [Promo Code Used],
    [Discount Applied],
    COUNT(*) AS customer_count,
    AVG([Purchase Amount (USD)]) AS avg_spend
FROM customer_cleaned
GROUP BY [Promo Code Used], [Discount Applied]
ORDER BY [Promo Code Used], [Discount Applied];

-- ============================================================================
-- 4. Promo Usage by Gender
-- ============================================================================
SELECT
    [Gender],
    SUM(CASE WHEN [Promo Code Used] = 'Yes' THEN 1 ELSE 0 END) AS promo_users,
    SUM(CASE WHEN [Promo Code Used] = 'No' THEN 1 ELSE 0 END) AS non_promo_users,
    SUM(CASE WHEN [Promo Code Used] = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS promo_rate_pct,
    AVG(CASE WHEN [Promo Code Used] = 'Yes' THEN [Purchase Amount (USD)] END) AS promo_avg_spend,
    AVG(CASE WHEN [Promo Code Used] = 'No' THEN [Purchase Amount (USD)] END) AS non_promo_avg_spend
FROM customer_cleaned
GROUP BY [Gender];

-- ============================================================================
-- 5. Promo Usage by Age Band
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
    SUM(CASE WHEN [Promo Code Used] = 'Yes' THEN 1 ELSE 0 END) AS promo_users,
    SUM(CASE WHEN [Promo Code Used] = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS promo_rate_pct
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
-- 6. Promo Usage by Location (Top 10)
-- ============================================================================
SELECT TOP 10
    [Location],
    COUNT(*) AS customer_count,
    SUM(CASE WHEN [Promo Code Used] = 'Yes' THEN 1 ELSE 0 END) AS promo_users,
    SUM(CASE WHEN [Promo Code Used] = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS promo_rate_pct
FROM customer_cleaned
GROUP BY [Location]
ORDER BY promo_rate_pct DESC;

-- ============================================================================
-- 7. Promo Usage by Category
-- ============================================================================
SELECT
    [Category],
    COUNT(*) AS customer_count,
    SUM(CASE WHEN [Promo Code Used] = 'Yes' THEN 1 ELSE 0 END) AS promo_users,
    SUM(CASE WHEN [Promo Code Used] = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS promo_rate_pct
FROM customer_cleaned
GROUP BY [Category]
ORDER BY promo_rate_pct DESC;

-- ============================================================================
-- 8. Promo Usage by Purchase History Band
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
    SUM(CASE WHEN [Promo Code Used] = 'Yes' THEN 1 ELSE 0 END) AS promo_users,
    SUM(CASE WHEN [Promo Code Used] = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS promo_rate_pct
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
-- 9. Promo Usage by Subscription Status
-- ============================================================================
SELECT
    [Subscription Status],
    COUNT(*) AS customer_count,
    SUM(CASE WHEN [Promo Code Used] = 'Yes' THEN 1 ELSE 0 END) AS promo_users,
    SUM(CASE WHEN [Promo Code Used] = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS promo_rate_pct,
    AVG([Purchase Amount (USD)]) AS avg_spend
FROM customer_cleaned
GROUP BY [Subscription Status];

-- ============================================================================
-- 10. Promo Usage by Frequency
-- ============================================================================
SELECT
    [Purchase Frequency],
    COUNT(*) AS customer_count,
    SUM(CASE WHEN [Promo Code Used] = 'Yes' THEN 1 ELSE 0 END) AS promo_users,
    SUM(CASE WHEN [Promo Code Used] = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS promo_rate_pct
FROM customer_cleaned
GROUP BY [Purchase Frequency]
ORDER BY COUNT(*) DESC;

-- ============================================================================
-- 11. Promo Users vs Non-Promo Users Comparison
-- ============================================================================
SELECT
    'Promo Users' AS customer_group,
    COUNT(*) AS customer_count,
    AVG([Purchase Amount (USD)]) AS avg_spend,
    AVG([Previous Purchases]) AS avg_previous_purchases,
    AVG([Review Rating]) AS avg_review_rating
FROM customer_cleaned
WHERE [Promo Code Used] = 'Yes'
UNION ALL
SELECT
    'Non-Promo Users' AS customer_group,
    COUNT(*) AS customer_count,
    AVG([Purchase Amount (USD)]) AS avg_spend,
    AVG([Previous Purchases]) AS avg_previous_purchases,
    AVG([Review Rating]) AS avg_review_rating
FROM customer_cleaned
WHERE [Promo Code Used] = 'No';

-- ============================================================================
-- 12. High vs Low Purchase History Promo Analysis
-- ============================================================================
SELECT
    CASE
        WHEN [Previous Purchases] >= 38 THEN 'High History (38+)'
        ELSE 'Low History (<38)'
    END AS history_segment,
    COUNT(*) AS customer_count,
    SUM(CASE WHEN [Promo Code Used] = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS promo_rate_pct,
    AVG([Purchase Amount (USD)]) AS avg_spend
FROM customer_cleaned
GROUP BY
    CASE
        WHEN [Previous Purchases] >= 38 THEN 'High History (38+)'
        ELSE 'Low History (<38)'
    END;

-- ============================================================================
-- 13. Promo Intensity by Location (Locations with >40% promo rate)
-- ============================================================================
WITH location_promo AS (
    SELECT
        [Location],
        COUNT(*) AS customer_count,
        SUM(CASE WHEN [Promo Code Used] = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS promo_rate
    FROM customer_cleaned
    GROUP BY [Location]
)
SELECT
    [Location],
    customer_count,
    promo_rate
FROM location_promo
WHERE promo_rate > 40
ORDER BY promo_rate DESC;

-- ============================================================================
-- End of Promo Analysis SQL
-- ============================================================================

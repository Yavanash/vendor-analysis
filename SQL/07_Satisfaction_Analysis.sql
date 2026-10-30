-- ============================================================================
-- Satisfaction Analysis SQL
-- Purpose: Customer satisfaction analysis and satisfaction drivers
-- Author: Analytics Engineering Team
-- Date: 2026-08-27
-- ============================================================================

-- ============================================================================
-- 1. Review Rating Distribution
-- ============================================================================
SELECT
    [Review Rating],
    COUNT(*) AS customer_count,
    COUNT(*) * 100.0 / SUM(COUNT(*)) OVER() AS pct_of_customers
FROM customer_cleaned
GROUP BY [Review Rating]
ORDER BY [Review Rating];

-- ============================================================================
-- 2. Review Rating Band Distribution
-- ============================================================================
SELECT
    CASE
        WHEN [Review Rating] >= 4.5 THEN 'Very High (4.5+)'
        WHEN [Review Rating] >= 4 THEN 'High (4-4.4)'
        WHEN [Review Rating] >= 3 THEN 'Medium (3-3.9)'
        ELSE 'Low (<3)'
    END AS rating_band,
    COUNT(*) AS customer_count,
    COUNT(*) * 100.0 / SUM(COUNT(*)) OVER() AS pct_of_customers
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
-- 3. Average Rating by Segment
-- ============================================================================
SELECT
    CASE
        WHEN [Review Rating] >= 4.5 THEN 'Very High (4.5+)'
        WHEN [Review Rating] >= 4 THEN 'High (4-4.4)'
        WHEN [Review Rating] >= 3 THEN 'Medium (3-3.9)'
        ELSE 'Low (<3)'
    END AS rating_band,
    AVG([Purchase Amount (USD)]) AS avg_spend,
    AVG([Previous Purchases]) AS avg_previous_purchases,
    SUM(CASE WHEN [Promo Code Used] = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS promo_rate
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
-- 4. Satisfaction by Gender
-- ============================================================================
SELECT
    [Gender],
    COUNT(*) AS customer_count,
    AVG([Review Rating]) AS avg_review_rating,
    MIN([Review Rating]) AS min_rating,
    MAX([Review Rating]) AS max_rating,
    SUM(CASE WHEN [Review Rating] >= 4 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS high_rating_pct
FROM customer_cleaned
GROUP BY [Gender];

-- ============================================================================
-- 5. Satisfaction by Age Band
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
    COUNT(*) AS customer_count,
    AVG([Review Rating]) AS avg_review_rating,
    SUM(CASE WHEN [Review Rating] >= 4 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS high_rating_pct
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
-- 6. Satisfaction by Location (Top 10)
-- ============================================================================
SELECT TOP 10
    [Location],
    COUNT(*) AS customer_count,
    AVG([Review Rating]) AS avg_review_rating,
    MIN([Review Rating]) AS min_rating,
    MAX([Review Rating]) AS max_rating,
    SUM(CASE WHEN [Review Rating] >= 4 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS high_rating_pct
FROM customer_cleaned
GROUP BY [Location]
ORDER BY avg_review_rating DESC;

-- ============================================================================
-- 7. Satisfaction by Category
-- ============================================================================
SELECT
    [Category],
    COUNT(*) AS customer_count,
    AVG([Review Rating]) AS avg_review_rating,
    SUM(CASE WHEN [Review Rating] >= 4 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS high_rating_pct
FROM customer_cleaned
GROUP BY [Category]
ORDER BY avg_review_rating DESC;

-- ============================================================================
-- 8. Satisfaction by Subscription Status
-- ============================================================================
SELECT
    [Subscription Status],
    COUNT(*) AS customer_count,
    AVG([Review Rating]) AS avg_review_rating,
    MIN([Review Rating]) AS min_rating,
    MAX([Review Rating]) AS max_rating,
    SUM(CASE WHEN [Review Rating] >= 4 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS high_rating_pct
FROM customer_cleaned
GROUP BY [Subscription Status];

-- ============================================================================
-- 9. Satisfaction by Promo Usage
-- ============================================================================
SELECT
    [Promo Code Used],
    COUNT(*) AS customer_count,
    AVG([Review Rating]) AS avg_review_rating,
    SUM(CASE WHEN [Review Rating] >= 4 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS high_rating_pct
FROM customer_cleaned
GROUP BY [Promo Code Used];

-- ============================================================================
-- 10. Satisfaction by Purchase History
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
    AVG([Review Rating]) AS avg_review_rating,
    SUM(CASE WHEN [Review Rating] >= 4 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS high_rating_pct
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
-- 11. Satisfaction by Frequency
-- ============================================================================
SELECT
    [Purchase Frequency],
    COUNT(*) AS customer_count,
    AVG([Review Rating]) AS avg_review_rating,
    SUM(CASE WHEN [Review Rating] >= 4 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS high_rating_pct
FROM customer_cleaned
GROUP BY [Purchase Frequency]
ORDER BY avg_review_rating DESC;

-- ============================================================================
-- 12. Low Satisfaction Customer Profile
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
    [Gender],
    [Category],
    COUNT(*) AS customer_count,
    AVG([Previous Purchases]) AS avg_previous_purchases,
    AVG([Purchase Amount (USD)]) AS avg_spend
FROM customer_cleaned
WHERE [Review Rating] < 3
GROUP BY
    CASE
        WHEN Age < 25 THEN '18-24'
        WHEN Age BETWEEN 25 AND 34 THEN '25-34'
        WHEN Age BETWEEN 35 AND 44 THEN '35-44'
        WHEN Age BETWEEN 45 AND 54 THEN '45-54'
        WHEN Age BETWEEN 55 AND 64 THEN '55-64'
        ELSE '65+'
    END, [Gender], [Category]
ORDER BY COUNT(*) DESC;

-- ============================================================================
-- 13. High Satisfaction Customer Profile
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
    [Gender],
    [Category],
    COUNT(*) AS customer_count,
    AVG([Previous Purchases]) AS avg_previous_purchases,
    AVG([Purchase Amount (USD)]) AS avg_spend
FROM customer_cleaned
WHERE [Review Rating] >= 4
GROUP BY
    CASE
        WHEN Age < 25 THEN '18-24'
        WHEN Age BETWEEN 25 AND 34 THEN '25-34'
        WHEN Age BETWEEN 35 AND 44 THEN '35-44'
        WHEN Age BETWEEN 45 AND 54 THEN '45-54'
        WHEN Age BETWEEN 55 AND 64 THEN '55-64'
        ELSE '65+'
    END, [Gender], [Category]
ORDER BY COUNT(*) DESC;

-- ============================================================================
-- 14. Missing Review Rating Analysis
-- ============================================================================
SELECT
    [Subscription Status],
    [Promo Code Used],
    [Category],
    COUNT(*) AS customer_count,
    SUM(CASE WHEN [Review Rating] IS NULL THEN 1 ELSE 0 END) AS missing_ratings,
    SUM(CASE WHEN [Review Rating] IS NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS missing_pct
FROM customer_cleaned
GROUP BY [Subscription Status], [Promo Code Used], [Category]
HAVING SUM(CASE WHEN [Review Rating] IS NULL THEN 1 ELSE 0 END) > 0
ORDER BY missing_pct DESC;

-- ============================================================================
-- End of Satisfaction Analysis SQL
-- ============================================================================

-- ============================================================================
-- Geographic Analysis SQL
-- Purpose: Location-based customer profiling and segmentation
-- Author: Analytics Engineering Team
-- Date: 2026-08-27
-- ============================================================================

-- ============================================================================
-- 1. Location Overview Statistics
-- ============================================================================
SELECT
    [Location],
    COUNT(*) AS customer_count,
    COUNT(*) * 100.0 / SUM(COUNT(*)) OVER() AS pct_of_customers,
    AVG([Purchase Amount (USD)]) AS avg_spend,
    SUM([Purchase Amount (USD)]) AS total_revenue,
    SUM([Purchase Amount (USD)]) * 100.0 / SUM(SUM([Purchase Amount (USD)])) OVER() AS pct_of_revenue
FROM customer_cleaned
GROUP BY [Location]
ORDER BY COUNT(*) DESC;

-- ============================================================================
-- 2. Location Ranked by Average Spend
-- ============================================================================
SELECT
    [Location],
    COUNT(*) AS customer_count,
    AVG([Purchase Amount (USD)]) AS avg_spend,
    MIN([Purchase Amount (USD)]) AS min_spend,
    MAX([Purchase Amount (USD)]) AS max_spend,
    SUM([Purchase Amount (USD)]) AS total_revenue
FROM customer_cleaned
GROUP BY [Location]
ORDER BY AVG([Purchase Amount (USD)]) DESC;

-- ============================================================================
-- 3. Location Ranked by Purchase History (Repeat Behavior)
-- ============================================================================
SELECT
    [Location],
    COUNT(*) AS customer_count,
    AVG([Previous Purchases]) AS avg_previous_purchases,
    MEDIAN([Previous Purchases]) AS median_previous_purchases,
    SUM(CASE WHEN [Previous Purchases] >= 38 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS high_history_pct
FROM customer_cleaned
GROUP BY [Location]
ORDER BY AVG([Previous Purchases]) DESC;

-- ============================================================================
-- 4. Location by Promo Code Usage
-- ============================================================================
SELECT
    [Location],
    COUNT(*) AS customer_count,
    SUM(CASE WHEN [Promo Code Used] = 'Yes' THEN 1 ELSE 0 END) AS promo_customers,
    SUM(CASE WHEN [Promo Code Used] = 'No' THEN 1 ELSE 0 END) AS non_promo_customers,
    SUM(CASE WHEN [Promo Code Used] = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS promo_rate_pct
FROM customer_cleaned
GROUP BY [Location]
ORDER BY promo_rate_pct DESC;

-- ============================================================================
-- 5. Location by Discount Usage
-- ============================================================================
SELECT
    [Location],
    COUNT(*) AS customer_count,
    SUM(CASE WHEN [Discount Applied] = 'Yes' THEN 1 ELSE 0 END) AS discount_customers,
    SUM(CASE WHEN [Discount Applied] = 'No' THEN 1 ELSE 0 END) AS no_discount_customers,
    SUM(CASE WHEN [Discount Applied] = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS discount_rate_pct,
    AVG([Purchase Amount (USD)]) AS avg_spend
FROM customer_cleaned
GROUP BY [Location]
ORDER BY discount_rate_pct DESC;

-- ============================================================================
-- 6. Location by Subscription Status
-- ============================================================================
SELECT
    [Location],
    COUNT(*) AS customer_count,
    SUM(CASE WHEN [Subscription Status] = 'Yes' THEN 1 ELSE 0 END) AS subscribers,
    SUM(CASE WHEN [Subscription Status] = 'No' THEN 1 ELSE 0 END) AS non_subscribers,
    SUM(CASE WHEN [Subscription Status] = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS subscription_rate_pct
FROM customer_cleaned
GROUP BY [Location]
ORDER BY subscription_rate_pct DESC;

-- ============================================================================
-- 7. Location by Review Rating
-- ============================================================================
SELECT
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
-- 8. Location by Category Preference
-- ============================================================================
SELECT
    [Location],
    [Category],
    COUNT(*) AS customer_count,
    COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(PARTITION BY [Location]) AS pct_within_location
FROM customer_cleaned
GROUP BY [Location], [Category]
ORDER BY [Location], COUNT(*) DESC;

-- ============================================================================
-- 9. Location by Gender Distribution
-- ============================================================================
SELECT
    [Location],
    SUM(CASE WHEN [Gender] = 'Male' THEN 1 ELSE 0 END) AS male_count,
    SUM(CASE WHEN [Gender] = 'Female' THEN 1 ELSE 0 END) AS female_count,
    SUM(CASE WHEN [Gender] = 'Male' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS male_pct,
    AVG(CASE WHEN [Gender] = 'Male' THEN [Purchase Amount (USD)] END) AS male_avg_spend,
    AVG(CASE WHEN [Gender] = 'Female' THEN [Purchase Amount (USD)] END) AS female_avg_spend
FROM customer_cleaned
GROUP BY [Location]
ORDER BY COUNT(*) DESC;

-- ============================================================================
-- 10. Location by Age Band
-- ============================================================================
SELECT
    [Location],
    SUM(CASE WHEN Age < 25 THEN 1 ELSE 0 END) AS age_18_24,
    SUM(CASE WHEN Age BETWEEN 25 AND 34 THEN 1 ELSE 0 END) AS age_25_34,
    SUM(CASE WHEN Age BETWEEN 35 AND 44 THEN 1 ELSE 0 END) AS age_35_44,
    SUM(CASE WHEN Age BETWEEN 45 AND 54 THEN 1 ELSE 0 END) AS age_45_54,
    SUM(CASE WHEN Age BETWEEN 55 AND 64 THEN 1 ELSE 0 END) AS age_55_64,
    SUM(CASE WHEN Age >= 65 THEN 1 ELSE 0 END) AS age_65_plus,
    COUNT(*) AS total_customers
FROM customer_cleaned
GROUP BY [Location]
ORDER BY COUNT(*) DESC;

-- ============================================================================
-- 11. High-Value Location Analysis (Spend + History)
-- ============================================================================
WITH location_metrics AS (
    SELECT
        [Location],
        AVG([Purchase Amount (USD)]) AS avg_spend,
        AVG([Previous Purchases]) AS avg_history,
        COUNT(*) AS customer_count
    FROM customer_cleaned
    GROUP BY [Location]
)
SELECT
    [Location],
    customer_count,
    avg_spend,
    avg_history,
    CASE
        WHEN avg_spend >= 60 AND avg_history >= 25 THEN 'High Spend + High History'
        WHEN avg_spend >= 60 AND avg_history < 25 THEN 'High Spend + Low History'
        WHEN avg_spend < 60 AND avg_history >= 25 THEN 'Low Spend + High History'
        ELSE 'Low Spend + Low History'
    END AS value_segment
FROM location_metrics
ORDER BY avg_spend DESC, avg_history DESC;

-- ============================================================================
-- 12. Geographic Concentration Analysis
-- ============================================================================
WITH location_rank AS (
    SELECT
        [Location],
        SUM([Purchase Amount (USD)]) AS total_revenue,
        RANK() OVER (ORDER BY SUM([Purchase Amount (USD)]) DESC) AS revenue_rank
    FROM customer_cleaned
    GROUP BY [Location]
)
SELECT
    CASE
        WHEN revenue_rank <= 10 THEN 'Top 10'
        WHEN revenue_rank <= 25 THEN 'Middle 15'
        ELSE 'Bottom 25'
    END AS geographic_tier,
    COUNT(*) AS location_count,
    SUM(total_revenue) AS combined_revenue,
    SUM(total_revenue) * 100.0 / SUM(SUM(total_revenue)) OVER() AS pct_of_total
FROM location_rank
GROUP BY
    CASE
        WHEN revenue_rank <= 10 THEN 'Top 10'
        WHEN revenue_rank <= 25 THEN 'Middle 15'
        ELSE 'Bottom 25'
    END;

-- ============================================================================
-- End of Geographic Analysis SQL
-- ============================================================================

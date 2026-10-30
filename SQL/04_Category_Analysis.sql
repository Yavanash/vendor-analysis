-- ============================================================================
-- Category Analysis SQL
-- Purpose: Product category profiling and cross-category insights
-- Author: Analytics Engineering Team
-- Date: 2026-08-27
-- ============================================================================

-- ============================================================================
-- 1. Category Overview Statistics
-- ============================================================================
SELECT
    [Category],
    COUNT(*) AS customer_count,
    COUNT(*) * 100.0 / SUM(COUNT(*)) OVER() AS pct_of_customers,
    SUM([Purchase Amount (USD)]) AS total_revenue,
    SUM([Purchase Amount (USD)]) * 100.0 / SUM(SUM([Purchase Amount (USD)])) OVER() AS pct_of_revenue,
    AVG([Purchase Amount (USD)]) AS avg_spend
FROM customer_cleaned
GROUP BY [Category]
ORDER BY COUNT(*) DESC;

-- ============================================================================
-- 2. Category by Purchase History (Repeat Behavior)
-- ============================================================================
SELECT
    [Category],
    COUNT(*) AS customer_count,
    AVG([Previous Purchases]) AS avg_previous_purchases,
    MEDIAN([Previous Purchases]) AS median_previous_purchases,
    MIN([Previous Purchases]) AS min_purchases,
    MAX([Previous Purchases]) AS max_purchases,
    SUM(CASE WHEN [Previous Purchases] >= 38 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS high_history_pct
FROM customer_cleaned
GROUP BY [Category]
ORDER BY AVG([Previous Purchases]) DESC;

-- ============================================================================
-- 3. Category by Promo Code Usage
-- ============================================================================
SELECT
    [Category],
    COUNT(*) AS customer_count,
    SUM(CASE WHEN [Promo Code Used] = 'Yes' THEN 1 ELSE 0 END) AS promo_customers,
    SUM(CASE WHEN [Promo Code Used] = 'No' THEN 1 ELSE 0 END) AS non_promo_customers,
    SUM(CASE WHEN [Promo Code Used] = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS promo_rate_pct
FROM customer_cleaned
GROUP BY [Category]
ORDER BY promo_rate_pct DESC;

-- ============================================================================
-- 4. Category by Discount Applied
-- ============================================================================
SELECT
    [Category],
    COUNT(*) AS customer_count,
    SUM(CASE WHEN [Discount Applied] = 'Yes' THEN 1 ELSE 0 END) AS discount_customers,
    SUM(CASE WHEN [Discount Applied] = 'No' THEN 1 ELSE 0 END) AS no_discount,
    SUM(CASE WHEN [Discount Applied] = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS discount_rate_pct
FROM customer_cleaned
GROUP BY [Category]
ORDER BY discount_rate_pct DESC;

-- ============================================================================
-- 5. Category by Subscription Status
-- ============================================================================
SELECT
    [Category],
    COUNT(*) AS customer_count,
    SUM(CASE WHEN [Subscription Status] = 'Yes' THEN 1 ELSE 0 END) AS subscribers,
    SUM(CASE WHEN [Subscription Status] = 'No' THEN 1 ELSE 0 END) AS non_subscribers,
    SUM(CASE WHEN [Subscription Status] = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS subscription_rate_pct
FROM customer_cleaned
GROUP BY [Category]
ORDER BY subscription_rate_pct DESC;

-- ============================================================================
-- 6. Category by Review Rating
-- ============================================================================
SELECT
    [Category],
    COUNT(*) AS customer_count,
    AVG([Review Rating]) AS avg_review_rating,
    MIN([Review Rating]) AS min_rating,
    MAX([Review Rating]) AS max_rating,
    SUM(CASE WHEN [Review Rating] >= 4 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS high_rating_pct
FROM customer_cleaned
GROUP BY [Category]
ORDER BY avg_review_rating DESC;

-- ============================================================================
-- 7. Category by Gender Distribution
-- ============================================================================
SELECT
    [Category],
    SUM(CASE WHEN [Gender] = 'Male' THEN 1 ELSE 0 END) AS male_count,
    SUM(CASE WHEN [Gender] = 'Female' THEN 1 ELSE 0 END) AS female_count,
    SUM(CASE WHEN [Gender] = 'Male' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS male_pct,
    SUM(CASE WHEN [Gender] = 'Female' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS female_pct
FROM customer_cleaned
GROUP BY [Category]
ORDER BY COUNT(*) DESC;

-- ============================================================================
-- 8. Category by Age Band
-- ============================================================================
SELECT
    [Category],
    SUM(CASE WHEN Age < 25 THEN 1 ELSE 0 END) AS age_18_24,
    SUM(CASE WHEN Age BETWEEN 25 AND 34 THEN 1 ELSE 0 END) AS age_25_34,
    SUM(CASE WHEN Age BETWEEN 35 AND 44 THEN 1 ELSE 0 END) AS age_35_44,
    SUM(CASE WHEN Age BETWEEN 45 AND 54 THEN 1 ELSE 0 END) AS age_45_54,
    SUM(CASE WHEN Age BETWEEN 55 AND 64 THEN 1 ELSE 0 END) AS age_55_64,
    SUM(CASE WHEN Age >= 65 THEN 1 ELSE 0 END) AS age_65_plus,
    COUNT(*) AS total_customers
FROM customer_cleaned
GROUP BY [Category]
ORDER BY COUNT(*) DESC;

-- ============================================================================
-- 9. Category × Promo Code Usage (Cross-tab)
-- ============================================================================
SELECT
    [Category],
    SUM(CASE WHEN [Promo Code Used] = 'Yes' THEN 1 ELSE 0 END) AS promo_yes,
    SUM(CASE WHEN [Promo Code Used] = 'No' THEN 1 ELSE 0 END) AS promo_no,
    AVG(CASE WHEN [Promo Code Used] = 'Yes' THEN [Purchase Amount (USD)] END) AS promo_avg_spend,
    AVG(CASE WHEN [Promo Code Used] = 'No' THEN [Purchase Amount (USD)] END) AS non_promo_avg_spend,
    AVG(CASE WHEN [Promo Code Used] = 'Yes' THEN [Previous Purchases] END) AS promo_avg_history,
    AVG(CASE WHEN [Promo Code Used] = 'No' THEN [Previous Purchases] END) AS non_promo_avg_history
FROM customer_cleaned
GROUP BY [Category];

-- ============================================================================
-- 10. Category × Subscription Status (Cross-tab)
-- ============================================================================
SELECT
    [Category],
    SUM(CASE WHEN [Subscription Status] = 'Yes' THEN 1 ELSE 0 END) AS sub_yes,
    SUM(CASE WHEN [Subscription Status] = 'No' THEN 1 ELSE 0 END) AS sub_no,
    AVG(CASE WHEN [Subscription Status] = 'Yes' THEN [Purchase Amount (USD)] END) AS subscriber_avg_spend,
    AVG(CASE WHEN [Subscription Status] = 'No' THEN [Purchase Amount (USD)] END) AS non_subscriber_avg_spend,
    AVG(CASE WHEN [Subscription Status] = 'Yes' THEN [Previous Purchases] END) AS subscriber_avg_history,
    AVG(CASE WHEN [Subscription Status] = 'No' THEN [Previous Purchases] END) AS non_subscriber_avg_history
FROM customer_cleaned
GROUP BY [Category];

-- ============================================================================
-- 11. Category Value Analysis (Spend + History Combined)
-- ============================================================================
WITH category_metrics AS (
    SELECT
        [Category],
        AVG([Purchase Amount (USD)]) AS avg_spend,
        AVG([Previous Purchases]) AS avg_history,
        COUNT(*) AS customer_count
    FROM customer_cleaned
    GROUP BY [Category]
)
SELECT
    [Category],
    customer_count,
    avg_spend,
    avg_history,
    CASE
        WHEN avg_spend >= 60 AND avg_history >= 25 THEN 'Premium Value'
        WHEN avg_spend >= 60 AND avg_history < 25 THEN 'Premium New'
        WHEN avg_spend < 60 AND avg_history >= 25 THEN 'Engaged Value'
        ELSE 'Developing'
    END AS value_segment
FROM category_metrics
ORDER BY avg_spend DESC;

-- ============================================================================
-- 12. Category Channel Preference
-- ============================================================================
SELECT
    [Category],
    [Preferred Login Device],
    COUNT(*) AS customer_count,
    COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(PARTITION BY [Category]) AS pct_within_category
FROM customer_cleaned
GROUP BY [Category], [Preferred Login Device]
ORDER BY [Category], COUNT(*) DESC;

-- ============================================================================
-- 13. Category Frequency Distribution
-- ============================================================================
SELECT
    [Category],
    [Purchase Frequency],
    COUNT(*) AS customer_count,
    COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(PARTITION BY [Category]) AS pct_within_category
FROM customer_cleaned
GROUP BY [Category], [Purchase Frequency]
ORDER BY [Category], COUNT(*) DESC;

-- ============================================================================
-- End of Category Analysis SQL
-- ============================================================================

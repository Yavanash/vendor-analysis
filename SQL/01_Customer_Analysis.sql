-- ============================================================================
-- Customer Analysis SQL
-- Purpose: Core customer-level profiling and value assessment
-- Author: Analytics Engineering Team
-- Date: 2026-08-27
-- ============================================================================

-- ============================================================================
-- 1. Customer Overview Statistics
-- ============================================================================
SELECT
    COUNT(DISTINCT [Customer ID]) AS total_customers,
    COUNT(*) AS total_transactions,
    SUM([Purchase Amount (USD)]) AS total_revenue,
    AVG([Purchase Amount (USD)]) AS avg_transaction_value,
    MIN([Purchase Amount (USD)]) AS min_transaction,
    MAX([Purchase Amount (USD)]) AS max_transaction
FROM customer_cleaned;

-- ============================================================================
-- 2. Customer Distribution by Purchase History
-- ============================================================================
SELECT
    CASE
        WHEN [Previous Purchases] = 0 THEN 'New (0 purchases)'
        WHEN [Previous Purchases] BETWEEN 1 AND 10 THEN '1-10 purchases'
        WHEN [Previous Purchases] BETWEEN 11 AND 25 THEN '11-25 purchases'
        WHEN [Previous Purchases] BETWEEN 26 AND 50 THEN '26-50 purchases'
        ELSE '51+ purchases'
    END AS purchase_history_band,
    COUNT(*) AS customer_count,
    COUNT(*) * 100.0 / SUM(COUNT(*)) OVER() AS pct_of_customers,
    AVG([Purchase Amount (USD)]) AS avg_spend,
    SUM([Purchase Amount (USD)]) AS total_revenue
FROM customer_cleaned
GROUP BY
    CASE
        WHEN [Previous Purchases] = 0 THEN 'New (0 purchases)'
        WHEN [Previous Purchases] BETWEEN 1 AND 10 THEN '1-10 purchases'
        WHEN [Previous Purchases] BETWEEN 11 AND 25 THEN '11-25 purchases'
        WHEN [Previous Purchases] BETWEEN 26 AND 50 THEN '26-50 purchases'
        ELSE '51+ purchases'
    END
ORDER BY
    CASE purchase_history_band
        WHEN 'New (0 purchases)' THEN 1
        WHEN '1-10 purchases' THEN 2
        WHEN '11-25 purchases' THEN 3
        WHEN '26-50 purchases' THEN 4
        ELSE 5
    END;

-- ============================================================================
-- 3. Frequency Distribution Analysis
-- ============================================================================
SELECT
    [Purchase Frequency] AS frequency,
    COUNT(*) AS customer_count,
    COUNT(*) * 100.0 / SUM(COUNT(*)) OVER() AS pct_of_customers,
    AVG([Purchase Amount (USD)]) AS avg_spend,
    AVG([Previous Purchases]) AS avg_previous_purchases,
    SUM([Purchase Amount (USD)]) AS total_revenue
FROM customer_cleaned
GROUP BY [Purchase Frequency]
ORDER BY COUNT(*) DESC;

-- ============================================================================
-- 4. Gender Distribution and Value
-- ============================================================================
SELECT
    [Gender],
    COUNT(*) AS customer_count,
    COUNT(*) * 100.0 / SUM(COUNT(*)) OVER() AS pct_of_customers,
    AVG([Purchase Amount (USD)]) AS avg_spend,
    SUM([Purchase Amount (USD)]) AS total_revenue,
    AVG([Previous Purchases]) AS avg_previous_purchases,
    AVG([Review Rating]) AS avg_review_rating
FROM customer_cleaned
GROUP BY [Gender];

-- ============================================================================
-- 5. Age Band Distribution and Value
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
    COUNT(*) * 100.0 / SUM(COUNT(*)) OVER() AS pct_of_customers,
    AVG([Purchase Amount (USD)]) AS avg_spend,
    SUM([Purchase Amount (USD)]) AS total_revenue,
    AVG([Previous Purchases]) AS avg_previous_purchases
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
-- 6. Subscription Status Analysis
-- ============================================================================
SELECT
    [Subscription Status],
    COUNT(*) AS customer_count,
    COUNT(*) * 100.0 / SUM(COUNT(*)) OVER() AS pct_of_customers,
    AVG([Purchase Amount (USD)]) AS avg_spend,
    SUM([Purchase Amount (USD)]) AS total_revenue,
    AVG([Previous Purchases]) AS avg_previous_purchases,
    AVG([Review Rating]) AS avg_review_rating
FROM customer_cleaned
GROUP BY [Subscription Status];

-- ============================================================================
-- 7. High-Value Customer Identification (Top 10% by Spend)
-- ============================================================================
WITH customer_values AS (
    SELECT
        [Customer ID],
        [Purchase Amount (USD)] AS current_spend,
        [Previous Purchases],
        NTILE(10) OVER (ORDER BY [Purchase Amount (USD)] DESC) AS spend_decile
    FROM customer_cleaned
)
SELECT
    spend_decile,
    COUNT(*) AS customer_count,
    MIN([Purchase Amount (USD)]) AS min_spend,
    MAX([Purchase Amount (USD)]) AS max_spend,
    AVG([Purchase Amount (USD)]) AS avg_spend,
    AVG([Previous Purchases]) AS avg_previous_purchases
FROM customer_values
GROUP BY spend_decile
ORDER BY spend_decile;

-- ============================================================================
-- 8. Location Summary (Top 10 by Customer Count)
-- ============================================================================
SELECT TOP 10
    [Location],
    COUNT(*) AS customer_count,
    COUNT(*) * 100.0 / SUM(COUNT(*)) OVER() AS pct_of_customers,
    AVG([Purchase Amount (USD)]) AS avg_spend,
    SUM([Purchase Amount (USD)]) AS total_revenue,
    AVG([Previous Purchases]) AS avg_previous_purchases
FROM customer_cleaned
GROUP BY [Location]
ORDER BY COUNT(*) DESC;

-- ============================================================================
-- End of Customer Analysis SQL
-- ============================================================================

-- ============================================================================
-- Retention Indicators SQL
-- Purpose: Proxy analysis for customer retention and engagement patterns
-- Author: Analytics Engineering Team
-- Date: 2026-08-27
-- ============================================================================

-- NOTE: This dataset contains cross-sectional data only. True retention,
-- churn, and CLV cannot be calculated. These queries identify behavioral
-- indicators associated with customer engagement.

-- ============================================================================
-- 1. Repeat Purchase Behavior Distribution
-- ============================================================================
SELECT
    CASE
        WHEN [Previous Purchases] = 0 THEN 'First-Time (0)'
        WHEN [Previous Purchases] BETWEEN 1 AND 5 THEN 'Occasional (1-5)'
        WHEN [Previous Purchases] BETWEEN 6 AND 15 THEN 'Regular (6-15)'
        WHEN [Previous Purchases] BETWEEN 16 AND 30 THEN 'Frequent (16-30)'
        WHEN [Previous Purchases] BETWEEN 31 AND 50 THEN 'Loyal (31-50)'
        ELSE 'Core (51+)'
    END AS engagement_tier,
    COUNT(*) AS customer_count,
    COUNT(*) * 100.0 / SUM(COUNT(*)) OVER() AS pct_of_customers,
    AVG([Purchase Amount (USD)]) AS avg_spend
FROM customer_cleaned
GROUP BY
    CASE
        WHEN [Previous Purchases] = 0 THEN 'First-Time (0)'
        WHEN [Previous Purchases] BETWEEN 1 AND 5 THEN 'Occasional (1-5)'
        WHEN [Previous Purchases] BETWEEN 6 AND 15 THEN 'Regular (6-15)'
        WHEN [Previous Purchases] BETWEEN 16 AND 30 THEN 'Frequent (16-30)'
        WHEN [Previous Purchases] BETWEEN 31 AND 50 THEN 'Loyal (31-50)'
        ELSE 'Core (51+)'
    END
ORDER BY MIN([Previous Purchases]);

-- ============================================================================
-- 2. Frequency Preference Analysis
-- ============================================================================
SELECT
    [Purchase Frequency],
    COUNT(*) AS customer_count,
    AVG([Previous Purchases]) AS avg_previous_purchases,
    SUM(CASE WHEN [Previous Purchases] >= 38 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS high_history_pct
FROM customer_cleaned
GROUP BY [Purchase Frequency]
ORDER BY AVG([Previous Purchases]) DESC;

-- ============================================================================
-- 3. Engagement Score (Combined Metric)
-- ============================================================================
SELECT
    CASE
        WHEN [Previous Purchases] >= 38 AND [Subscription Status] = 'Yes' THEN 'High Engagement'
        WHEN [Previous Purchases] >= 38 AND [Subscription Status] = 'No' THEN 'Repeat Buyer'
        WHEN [Previous Purchases] >= 20 AND [Subscription Status] = 'Yes' THEN 'Growing Engagement'
        WHEN [Previous Purchases] < 20 AND [Subscription Status] = 'Yes' THEN 'Early Subscriber'
        ELSE 'Casual Customer'
    END AS engagement_segment,
    COUNT(*) AS customer_count,
    COUNT(*) * 100.0 / SUM(COUNT(*)) OVER() AS pct_of_customers,
    AVG([Purchase Amount (USD)]) AS avg_spend,
    AVG([Review Rating]) AS avg_satisfaction
FROM customer_cleaned
GROUP BY
    CASE
        WHEN [Previous Purchases] >= 38 AND [Subscription Status] = 'Yes' THEN 'High Engagement'
        WHEN [Previous Purchases] >= 38 AND [Subscription Status] = 'No' THEN 'Repeat Buyer'
        WHEN [Previous Purchases] >= 20 AND [Subscription Status] = 'Yes' THEN 'Growing Engagement'
        WHEN [Previous Purchases] < 20 AND [Subscription Status] = 'Yes' THEN 'Early Subscriber'
        ELSE 'Casual Customer'
    END
ORDER BY COUNT(*) DESC;

-- ============================================================================
-- 4. Sticky Customer Indicators
-- ============================================================================
SELECT
    CASE
        WHEN [Previous Purchases] >= 38 AND [Subscription Status] = 'Yes' AND [Purchase Frequency] IN ('Weekly', 'Bi-Weekly', 'Monthly') THEN 'Very Sticky'
        WHEN [Previous Purchases] >= 25 AND [Subscription Status] = 'Yes' THEN 'Sticky'
        WHEN [Previous Purchases] >= 38 AND [Purchase Frequency] IN ('Weekly', 'Bi-Weekly', 'Monthly') THEN 'Frequent'
        WHEN [Previous Purchases] >= 25 THEN 'Engaged'
        ELSE 'Transactional'
    END AS stickiness_tier,
    COUNT(*) AS customer_count,
    AVG([Purchase Amount (USD)]) AS avg_spend,
    AVG([Review Rating]) AS avg_satisfaction
FROM customer_cleaned
GROUP BY
    CASE
        WHEN [Previous Purchases] >= 38 AND [Subscription Status] = 'Yes' AND [Purchase Frequency] IN ('Weekly', 'Bi-Weekly', 'Monthly') THEN 'Very Sticky'
        WHEN [Previous Purchases] >= 25 AND [Subscription Status] = 'Yes' THEN 'Sticky'
        WHEN [Previous Purchases] >= 38 AND [Purchase Frequency] IN ('Weekly', 'Bi-Weekly', 'Monthly') THEN 'Frequent'
        WHEN [Previous Purchases] >= 25 THEN 'Engaged'
        ELSE 'Transactional'
    END
ORDER BY COUNT(*) DESC;

-- ============================================================================
-- 5. Promotional Dependency Analysis
-- ============================================================================
SELECT
    CASE
        WHEN [Previous Purchases] >= 38 AND [Promo Code Used] = 'No' THEN 'Organic Loyalist'
        WHEN [Previous Purchases] >= 38 AND [Promo Code Used] = 'Yes' THEN 'Promo-Responsive Loyalist'
        WHEN [Previous Purchases] < 38 AND [Promo Code Used] = 'No' THEN 'Organic Explorer'
        WHEN [Previous Purchases] < 38 AND [Promo Code Used] = 'Yes' THEN 'Promo-Driven'
        ELSE 'Unknown'
    END AS promo_dependency,
    COUNT(*) AS customer_count,
    COUNT(*) * 100.0 / SUM(COUNT(*)) OVER() AS pct_of_customers,
    AVG([Review Rating]) AS avg_satisfaction
FROM customer_cleaned
GROUP BY
    CASE
        WHEN [Previous Purchases] >= 38 AND [Promo Code Used] = 'No' THEN 'Organic Loyalist'
        WHEN [Previous Purchases] >= 38 AND [Promo Code Used] = 'Yes' THEN 'Promo-Responsive Loyalist'
        WHEN [Previous Purchases] < 38 AND [Promo Code Used] = 'No' THEN 'Organic Explorer'
        WHEN [Previous Purchases] < 38 AND [Promo Code Used] = 'Yes' THEN 'Promo-Driven'
        ELSE 'Unknown'
    END
ORDER BY COUNT(*) DESC;

-- ============================================================================
-- 6. Customer Lifetime Value Proxy (Spend × History)
-- ============================================================================
SELECT
    CASE
        WHEN [Purchase Amount (USD)] * ([Previous Purchases] + 1) >= 3000 THEN 'Premium'
        WHEN [Purchase Amount (USD)] * ([Previous Purchases] + 1) >= 1500 THEN 'High'
        WHEN [Purchase Amount (USD)] * ([Previous Purchases] + 1) >= 750 THEN 'Medium'
        ELSE 'Low'
    END AS value_proxy,
    COUNT(*) AS customer_count,
    COUNT(*) * 100.0 / SUM(COUNT(*)) OVER() AS pct_of_customers,
    AVG([Purchase Amount (USD)]) AS avg_spend,
    AVG([Previous Purchases]) AS avg_history
FROM customer_cleaned
GROUP BY
    CASE
        WHEN [Purchase Amount (USD)] * ([Previous Purchases] + 1) >= 3000 THEN 'Premium'
        WHEN [Purchase Amount (USD)] * ([Previous Purchases] + 1) >= 1500 THEN 'High'
        WHEN [Purchase Amount (USD)] * ([Previous Purchases] + 1) >= 750 THEN 'Medium'
        ELSE 'Low'
    END
ORDER BY AVG([Purchase Amount (USD)] * ([Previous Purchases] + 1)) DESC;

-- ============================================================================
-- 7. Churn Risk Indicators (Proxy Only)
-- ============================================================================
SELECT
    CASE
        WHEN [Previous Purchases] >= 38 THEN 'Low Risk'
        WHEN [Previous Purchases] BETWEEN 20 AND 37 THEN 'Medium Risk'
        WHEN [Previous Purchases] BETWEEN 5 AND 19 THEN 'Elevated Risk'
        ELSE 'High Risk'
    END AS risk_segment,
    COUNT(*) AS customer_count,
    COUNT(*) * 100.0 / SUM(COUNT(*)) OVER() AS pct_of_customers,
    AVG([Review Rating]) AS avg_satisfaction,
    SUM(CASE WHEN [Subscription Status] = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS subscription_rate
FROM customer_cleaned
GROUP BY
    CASE
        WHEN [Previous Purchases] >= 38 THEN 'Low Risk'
        WHEN [Previous Purchases] BETWEEN 20 AND 37 THEN 'Medium Risk'
        WHEN [Previous Purchases] BETWEEN 5 AND 19 THEN 'Elevated Risk'
        ELSE 'High Risk'
    END
ORDER BY COUNT(*) DESC;

-- ============================================================================
-- 8. Engagement by Demographic Segment
-- ============================================================================
SELECT
    CASE
        WHEN Age < 30 THEN 'Young Adult (18-29)'
        WHEN Age BETWEEN 30 AND 44 THEN 'Adult (30-44)'
        WHEN Age BETWEEN 45 AND 59 THEN 'Middle Age (45-59)'
        ELSE 'Senior (60+)'
    END AS age_group,
    [Gender],
    COUNT(*) AS customer_count,
    AVG([Previous Purchases]) AS avg_previous_purchases,
    SUM(CASE WHEN [Subscription Status] = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS subscription_rate
FROM customer_cleaned
GROUP BY
    CASE
        WHEN Age < 30 THEN 'Young Adult (18-29)'
        WHEN Age BETWEEN 30 AND 44 THEN 'Adult (30-44)'
        WHEN Age BETWEEN 45 AND 59 THEN 'Middle Age (45-59)'
        ELSE 'Senior (60+)'
    END, [Gender]
ORDER BY COUNT(*) DESC;

-- ============================================================================
-- 9. Cross-Sell Opportunity Analysis
-- ============================================================================
SELECT
    [Category],
    [Purchase Frequency],
    COUNT(*) AS customer_count,
    AVG([Previous Purchases]) AS avg_previous_purchases,
    AVG([Purchase Amount (USD)]) AS avg_spend
FROM customer_cleaned
WHERE [Previous Purchases] >= 20
GROUP BY [Category], [Purchase Frequency]
ORDER BY COUNT(*) DESC;

-- ============================================================================
-- 10. At-Risk Customer Identification (Proxy)
-- ============================================================================
SELECT
    CASE
        WHEN [Previous Purchases] < 5 AND [Subscription Status] = 'No' AND [Review Rating] < 3 THEN 'High Risk'
        WHEN [Previous Purchases] < 10 AND [Subscription Status] = 'No' THEN 'Moderate Risk'
        WHEN [Review Rating] < 3 THEN 'Satisfaction Risk'
        ELSE 'Monitor'
    END AS risk_category,
    COUNT(*) AS customer_count,
    COUNT(*) * 100.0 / SUM(COUNT(*)) OVER() AS pct_of_customers,
    AVG([Purchase Amount (USD)]) AS avg_spend
FROM customer_cleaned
GROUP BY
    CASE
        WHEN [Previous Purchases] < 5 AND [Subscription Status] = 'No' AND [Review Rating] < 3 THEN 'High Risk'
        WHEN [Previous Purchases] < 10 AND [Subscription Status] = 'No' THEN 'Moderate Risk'
        WHEN [Review Rating] < 3 THEN 'Satisfaction Risk'
        ELSE 'Monitor'
    END
ORDER BY COUNT(*) DESC;

-- ============================================================================
-- 11. Subscription as Retention Indicator
-- ============================================================================
SELECT
    [Purchase Frequency],
    SUM(CASE WHEN [Subscription Status] = 'Yes' THEN 1 ELSE 0 END) AS subscribers,
    SUM(CASE WHEN [Subscription Status] = 'No' THEN 1 ELSE 0 END) AS non_subscribers,
    SUM(CASE WHEN [Subscription Status] = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS subscription_rate,
    AVG([Previous Purchases]) AS avg_previous_purchases
FROM customer_cleaned
GROUP BY [Purchase Frequency]
ORDER BY subscription_rate DESC;

-- ============================================================================
-- 12. Multi-Indicator Customer Score
-- ============================================================================
SELECT
    CASE
        WHEN [Previous Purchases] >= 38 AND [Subscription Status] = 'Yes' AND [Purchase Frequency] IN ('Weekly', 'Bi-Weekly', 'Monthly') AND [Review Rating] >= 4 THEN 'Champion'
        WHEN [Previous Purchases] >= 25 AND [Subscription Status] = 'Yes' AND [Purchase Frequency] IN ('Weekly', 'Bi-Weekly', 'Monthly') THEN 'Loyal'
        WHEN [Previous Purchases] >= 20 AND [Subscription Status] = 'Yes' THEN 'Engaged'
        WHEN [Previous Purchases] >= 15 THEN 'Regular'
        WHEN [Previous Purchases] >= 5 THEN 'Occasional'
        ELSE 'New/Infrequent'
    END AS customer_tier,
    COUNT(*) AS customer_count,
    COUNT(*) * 100.0 / SUM(COUNT(*)) OVER() AS pct_of_customers,
    AVG([Purchase Amount (USD)]) AS avg_spend,
    AVG([Review Rating]) AS avg_satisfaction
FROM customer_cleaned
GROUP BY
    CASE
        WHEN [Previous Purchases] >= 38 AND [Subscription Status] = 'Yes' AND [Purchase Frequency] IN ('Weekly', 'Bi-Weekly', 'Monthly') AND [Review Rating] >= 4 THEN 'Champion'
        WHEN [Previous Purchases] >= 25 AND [Subscription Status] = 'Yes' AND [Purchase Frequency] IN ('Weekly', 'Bi-Weekly', 'Monthly') THEN 'Loyal'
        WHEN [Previous Purchases] >= 20 AND [Subscription Status] = 'Yes' THEN 'Engaged'
        WHEN [Previous Purchases] >= 15 THEN 'Regular'
        WHEN [Previous Purchases] >= 5 THEN 'Occasional'
        ELSE 'New/Infrequent'
    END
ORDER BY COUNT(*) DESC;

-- ============================================================================
-- End of Retention Indicators SQL
-- ============================================================================

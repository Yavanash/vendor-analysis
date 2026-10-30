# Behavioral Ideal Customer Profile

## Purpose

This Behavioral ICP prioritizes signals of repeat engagement found in the current customer-level snapshot. It is a targeting hypothesis for validation, not a prediction of future behavior. The Behavioral Loyalty Proxy and Commercial Value Proxy are analytical rankings, not longitudinal measurements.

## Core behavioral signals

| Signal | Data-backed profile | Role in the ICP |
|---|---|---|
| Repeat-Purchase History | High previous-purchase count; the existing high-history flag begins at 38 purchases, the dataset's 75th-percentile threshold | Primary signal of demonstrated repeat depth, while recognizing that purchase timing is unknown |
| Purchase frequency | Weekly or bi-weekly stated frequency, represented by the existing high-frequency flag | Primary Engagement Proxy; use cautiously because frequency is stated, not transaction-derived |
| Satisfaction | Rating of 4.0 or higher where available | Quality/experience signal; retain a separate missing-rating treatment rather than assuming satisfaction |
| Behavioral Loyalty Proxy | Higher relative tier when behavioral prioritization is required | Composite prioritization aid; promo exposure is an input, so it is not independent proof of customer quality |

## Secondary commercial signals

| Signal | Data-backed use | Constraint |
|---|---|---|
| Current Observed Spend | Use to prioritize commercially relevant customers within otherwise similar behavioral groups | Single observed purchase amount, not future or cumulative value |
| Commercial Value Proxy | Use alongside, not in place of, the behavioral signals | Incorporates Current Observed Spend and remains an analytical proxy |
| Observed Promo Exposure | Use to choose treatment and testing strategy, not to exclude customers from the ICP | A single current indicator cannot show a customer's promotional pattern over time; current promo users are heterogeneous |
| Subscription status | Use as context for offer design and stratification | Not mandatory: every subscriber in the current source is also promo-exposed, so subscription and promo status are structurally confounded |

## Contextual demographic and geographic signals

| Signal | Recommended use | Evidence boundary |
|---|---|---|
| Category | Balance test cells and tailor merchandising or message relevance | Category differences are modest: average Repeat-Purchase History ranges from 25.0 to 25.7, and only one observed purchase category is available per customer |
| Geography | Create matched test/control cells and investigate operational differences | State variation suggests test opportunities, not established growth potential; market size, acquisition cost, and time trends are absent |
| Age | Reporting, accessibility, and creative relevance only | Satisfaction is broadly similar across age bands; age should not be a core qualification |
| Gender | Monitor representation and treatment balance | The available analysis does not support gender as a core behavioral-value criterion |
| Payment method | Operational convenience, checkout optimization, and balance checks where useful | Average Repeat-Purchase History and Current Observed Spend are similar across methods; do not use as a core value criterion |

## Practical qualification hierarchy

1. Start with Repeat-Purchase History.
2. Add stated purchase frequency and satisfaction as supporting Engagement Proxy signals.
3. Use Current Observed Spend or the Commercial Value Proxy to prioritize within behaviorally similar customers.
4. Use Observed Promo Exposure and subscription status to assign an appropriate test or communication treatment, never as mandatory ICP gates.
5. Use category, geography, age, gender, and payment method for context, creative relevance, operational planning, and experimental balance.

**One-sentence ICP:** The Behavioral ICP is a customer with deep Repeat-Purchase History, frequent stated purchasing and strong satisfaction, prioritized with Current Observed Spend where useful and treated according to current promo and subscription context rather than defined by demographics or a mandatory promo/subscriber status.

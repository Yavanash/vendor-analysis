# Project QA Summary: D2C Fashion Customer Intelligence

## Project Overview

| Attribute | Value |
|---|---|
| Dataset grain | Customer-level snapshot |
| Dataset size | 3,900 customers |
| Analysis scope | Current observed spend, loyalty proxies, segmentation, geography, category behavior, and observed promo exposure |
| Canonical analytical outputs | 8 CSV files |
| Active dashboard extracts | 5 CSV files |
| SQL scripts | 8 final scripts |

## Final Deliverables Inventory

### Canonical analytical outputs

All authoritative analytical tables are stored in `Outputs/analytical/`:

- `customer_features.csv`
- `loyalty_definition_a.csv`
- `loyalty_definition_b.csv`
- `loyalty_comparison.csv`
- `customer_segments.csv`
- `segment_summary.csv`
- `geographic_analysis.csv`
- `category_analysis.csv`

The cleaned customer-level intermediate remains at `Raw_Data/cleaned/customer_cleaned.csv`. The original source remains at `Raw_Data/Dataset.csv` and must not be modified.

### Active dashboard extracts

The five active Power BI-ready files in `Outputs/dashboards/` are:

- `02_segment_performance.csv` — behavioral value pyramid and segment-level promo/history context.
- `02a_segment_by_location.csv` — geographic segment composition.
- `03_all_locations.csv` — complete location-level opportunity table.
- `03_geographic_tier_summary.csv` — geographic tier rollup.
- `04_category_performance.csv` — Category × Purchase History analysis.

Legacy subsets and supporting cross-tabs are preserved in `Archive/`; they are not canonical outputs.

### Documentation and SQL

`Documentation/` contains the business questions, data audit, metric map, cleaning report, feature dictionary, loyalty comparison, segmentation methodology, geographic and category analyses, QA report, and consolidated findings. The corrected filename is `Business_Questions.md`.

The eight final scripts in `SQL/` cover customer, segment, geographic, category, observed promotion, subscription, satisfaction, and engagement/retention-proxy analysis.

## Constraint Compliance

- Raw source data is isolated from cleaned and derived data.
- The project uses proxy terminology for behavioral loyalty and engagement.
- Current Observed Spend is not presented as true lifetime value.
- Observed Promo Exposure is not presented as historical promo dependency.
- Actual retention, churn, and causal effects are not claimed.
- Customer assignments, loyalty scores, segment logic, metrics, and analytical findings were not changed during final structural cleanup.

## Validation

`Python/11_validation.py` checks file presence, customer-count integrity, Customer ID preservation, feature ranges, loyalty tiers, segment coverage, geographic and category coverage, missing-value handling, canonical outputs, and the five active dashboard extracts.

`Documentation/10_QA_Validation.md` is the report produced by the most recent analytical pipeline run. The final submission cleanup did not rerun or regenerate the analytical workflow; its dashboard-count failure reflects the former dashboard expectation. The validation script now recognizes the approved set of five active extracts.

## Final Structure Status

- `Outputs/analytical/` contains exactly the eight canonical analytical outputs.
- `Outputs/dashboards/` contains five retained Power BI-ready extracts.
- `Archive/` contains noncanonical legacy compositions and dashboard subsets.
- `PowerBI/` contains the final PBIX file, PBIP project, and dashboard preview image.
- `Presentation/` contains the final PPTX and PDF.
- `Strategy/` contains the executive summary, promotional sunset plan, Behavioral ICP, and 30/60/90-day plan.

## Known Limitations

1. The dataset has no time dimension or longitudinal transaction history.
2. True retention, churn, and CLV cannot be calculated.
3. Observed promo exposure is a snapshot indicator, not historical promotional dependency.
4. Associations in this project do not establish causation.
5. No cost or margin fields are available for profitability analysis.

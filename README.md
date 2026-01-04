# Cookie Bakery - simple data pipeline

**Simple data pipeline for a theoretical small cookie baking business.**

The following assumptions will be in place for this project:

    Hayes Baked Goods is a small, home-based bakery run by one full-time owner/manager, supported by a part-time baker and a contract bookkeeper. The business specializes in freshly baked cookies offered for local pickup and limited delivery.

    Customers can place orders by the dozen. The types of cookies offered are: Chocolate Chip Cookies, Emmy's Sugar Cookies, and Nutella Swirl Cookies (all the same price - $28 per dozen). Add-ons are available: Nutella Stuffing ($4), Crunchy Peanut Butter Stuffing ($4), and Sea Salt (free).

    Hayes Baked Goods wants to move from intuition-based decision-making to data-backed insights around pricing, product performance, profitability, and ingredient planning. We will do this with a simple data pipeline that organizes their data and turns it into meaningful, accessible insights.

### Project Components

This project includes the following components:

- **Source data**: CSV generation, organization, and inspection
- **Data audit report**
- **Business requirements & KPI definitions**
- **Schema documentation & ER diagram**
- **ETL pipeline & transformation documentation**
- **Data validation checks**
- **Data storage**: MySQL Workbench
- **Visualization dashboard**: Tableau
- **Insights & business recommendations**
- **README & future enhancements**

## Generate data

I don't like paying for a ChatGPT subscription, and you can't export CSV files in the free version, so I had it generate pre-formatted dummy data I could easily copy, paste, and plug into a Python script (createcsv.py) that loaded it all into CSVs that were immediately usable for the project. I know in real life the source data might not be quite this neat and ready to use, but there are still some imperfections that I'll be able to clean up in the transform stage to demonstrate my capability there. CSVs are stored in /source-data.

For the sake of this project, the source data will be shopify_orders.csv, shopify_products.csv, recipes.csv, and ingredients.csv. The first two are meant to simulate Shopify exports for a small business, while the second two are meant to simulate recipe and ingredients manual documentation. The Orders data will update on a regular cadence, while the other three will not and will only be updated as needed when business changes are made.

## Inspect data

To ensure the source data is clean and consistent, I created a single, consolidated Python script, `initial_inspectdata.py`, which performs both structural inspection and data validation across all CSV files in `/source-data`.

The script includes the following features:

1. **Structural & Quality Inspection**
   - Detects file encoding and delimiter automatically.
   - Prints column names, data types, row counts, and sample rows for a quick overview.
   - Computes basic statistics for numeric columns (mean, min, max, etc.).
   - Identifies missing, zero, or placeholder values, as well as duplicate rows.

2. **Data Validation Checks**
   - **Referential Integrity**: Ensures that order SKUs exist in the products table, recipe SKUs exist in products, and recipe ingredients exist in the ingredients table.
   - **Domain Validity**: Confirms numeric values make sense (e.g., `quantity > 0`, `price ≥ 0`, `cost_per_gram` calculation matches expected values within tolerance).
   - **Completeness**: Checks for null or missing keys such as `order_id`, `cookie_sku`, and `ingredient`.
   - **Consistency**: Validates categories and logical constraints (e.g., container sizes vs. unit sizes for ingredients).

3. **Automated Reporting**
   - Generates a consolidated inspection report at `/source-data/consolidated_inspection_report.txt`.
   - Summarizes any detected issues and flags validation failures, allowing early detection of potential problems before ETL.

This improved script combines initial inspection and detailed validation in a single workflow, streamlining data auditing and ensuring the dataset is ready for transformation and analysis.

Using this knowledge, I constructed the analytical model. The ERD and star schema diagrams can be found embedded in the audit as well as within this project under /documentation.

## Execute ETL

Using the logic laid out in the analytical model, I created an ran the etl.py script that handles the ETL process for this project.

The script follows these steps:

1. **Data Inspection**
   - Runs the consolidated `initial_inspectdata.py` script before any transformations.
   - Halts the ETL process if any data quality issues are detected, ensuring only clean data is processed.

2. **Extract**
   - Reads CSV files from `/source-data` including `shopify_orders.csv`, `shopify_products.csv`, `recipes.csv`, and `ingredients.csv`.

3. **Transform**
Since this data was fabricated, there weren't a lot of transformations needed, but I executed the following:
   - **Product Dimension (`dim_product`)**: Deduplicates products, creates a numeric key, and standardizes column names.
   - **Date Dimension (`dim_date`)**: Extracts unique dates from orders and creates attributes such as day of week, month, year, and a numeric date key.
   - **Ingredient Dimension (`dim_ingredient`)**: Deduplicates ingredients, creates a numeric key, and calculates `cost_per_gram`.
   - **Bridge Table (`bridge_product_ingredient`)**: Links products to ingredients with quantities, enabling cost calculations.
   - **Ingredient Cost per Product**: Aggregates ingredient costs to determine total cost per product.
   - **Fact Table (`fact_orders`)**: Combines orders with product, date, and cost data to calculate gross margin for each order.

4. **Load**
   - Saves all transformed tables (`dim_product`, `dim_date`, `dim_ingredient`, `bridge_product_ingredient`, `fact_orders`) as CSV files in `/staging-data` for downstream analysis.

This ETL script demonstrates a full end-to-end pipeline, including data validation, transformation into dimensional models, and preparation of fact and dimension tables suitable for business intelligence tools like Tableau.
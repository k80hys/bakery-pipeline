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

## Source Data Generation and Ingestion Preparation

I don't like paying for a ChatGPT subscription, and you can't export CSV files in the free version, so I had it generate pre-formatted dummy data I could easily copy, paste, and plug into a Python script (`createcsv.py`) that loaded it all into CSVs that were immediately usable for the project. I know in real life the source data might not be quite this neat and ready to use, but there are still some imperfections that I'll be able to clean up in the transform stage to demonstrate my capability there. CSVs are stored in `/source-data`.

For the sake of this project, the source data will be `shopify_orders.csv`, `shopify_products.csv`, `recipes.csv`, and `ingredients.csv`. The first two are meant to simulate Shopify exports for a small business, while the second two are meant to simulate recipe and ingredients manual documentation. The Orders data will update on a regular cadence, while the other three will not and will only be updated as needed when business changes are made.

## Data Inspection, Validation, and Modeling

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

Using this knowledge, I constructed the analytical model. The ERD and star schema diagrams can be found embedded in the audit as well as within this project under /documentation.

## ETL Pipeline

Using the validated source data, I created and ran the etl.py script that handles the ETL process for this project.

The script follows these steps:

1. **Data Inspection (Pre-ETL)**
   - Runs the consolidated `initial_inspectdata.py` script before any transformations
   - Halts the ETL process if any data quality issues are detected

2. **Extract**
   - Reads CSV files from `/source-data` including `shopify_orders.csv`, `shopify_products.csv`, `recipes.csv`, and `ingredients.csv`.

3. **Transform**
Since this data was fabricated, there weren't many transformations needed, but I executed the following:
   - **Product Dimension (`dim_product`)**: Deduplicates products, creates a numeric key, and standardizes column names.
   - **Date Dimension (`dim_date`)**: Extracts unique dates from orders and creates attributes such as day of week, month, year, and a numeric date key.
   - **Ingredient Dimension (`dim_ingredient`)**: Deduplicates ingredients, creates a numeric key, and calculates `cost_per_gram`.
   - **Bridge Table (`bridge_product_ingredient`)**: Links products to ingredients with quantities for cost calculations.
   - **Ingredient Cost per Product**: Aggregates ingredient costs to determine total cost per product.
   - **Fact Table (`fact_orders`)**: Combines orders with product, date, and cost data to calculate gross margin.

   Transformation-level validation ensures that surrogate keys, referential integrity, and derived metrics are correct.

4. **Load - Staging**
   - Saves all transformed tables (`dim_product`, `dim_date`, `dim_ingredient`, `bridge_product_ingredient`, `fact_orders`) as CSV files in `/staging-data` for backup, debugging, and downstream analysis.

5. **Load - MySQL Workbench**
   - Uses Python (`sqlalchemy` and `pymysql`) to connect to the `cookie_bakery_dw` database.
   - Loads tables in the following order:
      1. Dimensions → `dim_product`, `dim_date`, `dim_ingredient`
      2. Bridge → `bridge_product_ingredient`
      3. Fact → `fact_orders`
   - Prints row counts and terminates the load if counts or key constraints do not meet expectations.

This ETL script demonstrates a full end-to-end pipeline, including data validation, dimensional modeling, and preparation of fact and dimension tables suitable for BI tools like Tableau and MySQL.

## Post-Load Warehouse Validation (MySQL)

After loading all tables into the `cookie_bakery_dw` warehouse, a comprehensive set of validation checks ensures the data is trustworthy for analytics and BI consumption. These checks are executed via a consolidated SQL script (`validation_checks.sql`) and cover table integrity, referential correctness, and business logic.

Key validations include:

1. **Table Existence & Row Counts**: Confirms that all dimension, bridge, and fact tables exist and have expected rows.
2. **Foreign Key Integrity**: Ensures all fact table keys (`product_key`, `date_key`) exist in the corresponding dimension tables.
3. **Null & Completeness Checks**: Confirms no critical columns in fact or dimension tables are null (`order_id`, `cookie_sku`, `ingredient`, etc.).
4. **Negative or Impossible Values**: Verifies that `quantity > 0`, `total_price ≥ 0`, and `ingredient_cost ≥ 0`.
5. **Derived Metric Validation**: Checks that `gross_margin` equals `total_price - ingredient_cost` within a small tolerance.
6. **Ingredient Cost vs Revenue**: Ensures ingredient costs do not exceed the total order price.
7. **Profitability / Margin Sanity Checks**: Reviews min, max, and average gross margin and average margin percentage.
8. **Quantity vs Price Sanity**: Confirms price per unit is within reasonable bounds.
9. **High-Level KPI Summary**: Aggregates totals and averages for revenue, ingredient cost, gross margin, and margin percentage to spot outliers or anomalies.

These validations provide confidence that downstream analyses and Tableau dashboards are accurate, consistent, and aligned with business rules.

## Analytics and Visualization

### Google Sheets Integration for Tableau Dashboard

For the sake of this project, I decided to set up MySQL Workbench loading compatibility to showcase skills, while also relying on a simple automation to actually store the data for the practical Tableau usage purposes of this project, since my version of Tableau offers limited connection options. 

To automate updates of Tableau dashboards from the staging CSVs, the project uses a Google Sheet as a live data source.

- A Google Sheet named **`Cookie_Bakery`** is created to receive the staging data.
- A **service account** is generated in Google Cloud, with its email shared on the sheet.
- The service account JSON credentials are stored in `/staging-data/credentials.json`.
- Both **Google Sheets API** and **Google Drive API** are enabled for the project; it may take a few minutes (~1–5 minutes) for changes to propagate before the Python script can access the sheet.
- A Python script (`googlesheets.py`) reads all CSVs from `/staging-data` and uploads them to the sheet, creating or overwriting tabs as needed.
- Tableau Public connects to this Google Sheet to pull data dynamically, ensuring dashboards reflect the latest ETL output.

This approach provides a lightweight, cloud-accessible data source for visualization.

## Insights & Business Recommendations

## Future Enhancements

# Reproducible Steps

1. Clone the repository
```
git clone https://github.com/k80hys/bakery-pipeline.git
cd bakery-pipeline
```

2. Install dependencies
```
pip install -r requirements.txt
```

3. Generate source CSVs
```
python scripts/createcsv.py
```

4. Run data inspection and validation
```
python scripts/initial_inspectdata.py
```

5. Generate MySQL schema
```
python scripts/generate_schema_sql.py
```

6. In MySQL Workbench or equivalent:
```
CREATE DATABASE IF NOT EXISTS cookie_bakery_dw;
USE cookie_bakery_dw;
SOURCE sql/auto_generated_schema.sql;
```

7. Run ETL to load tables
```
python scripts/etl.py
```

8. Verify data in MySQL Workbench
```
SELECT COUNT(*) FROM dim_product;
SELECT COUNT(*) FROM fact_orders;
SELECT * FROM bridge_product_ingredient LIMIT 5;

NEXT: diagram in ASCII or markdown that visually shows staging CSV --> ETL --> MySQL --> Tableau
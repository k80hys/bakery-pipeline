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

I created scripts to generate dummy data and load it into CSVs, which constitutes the source data for the pipeline.

As is, the data sources are: `shopify_orders.csv`, `shopify_products.csv`, `recipes.csv`, and `ingredients.csv`. The first two are meant to simulate Shopify exports for a small business, while the second two are meant to simulate recipe and ingredients manual documentation.

In a real-world scenario, I'd use the Shopify Admin API to pull data, and set up a simple Zapier automation for any as-needed updates to the recipe and ingredients Sheets.

## Data Inspection, Validation, and Modeling

To ensure the source data is clean and consistent, I created `initial_inspectdata.py`, which performs both structural inspection and data validation across all CSV files in `/source-data`.

Using the findings (generated in an inspection report txt file), I constructed the analytical model. The ERD and star schema diagrams can be found embedded in the audit as well as within this project under /documentation.

## ETL Pipeline

Using the validated source data, I created and ran the `etl.py` script to handle the ETL process for this project. The script demonstrates a full end-to-end pipeline, including data validation, dimensional modeling, and creation of fact and dimension tables suitable for BI tools like Tableau and MySQL.

The pipeline loads to both a `/staging-data` folder (for backup, debugging, and downstream analysis) and to a MySQL database for local storage, as I wanted to demonstrate both approaches.

## Post-Load Warehouse Validation (MySQL)

After loading all tables into the `cookie_bakery_dw` warehouse, the SQL script (`validation_checks.sql`) runs validations that cover table integrity, referential correctness, and business logic.

## Analytics and Visualization

### Google Sheets Integration for Tableau Dashboard

Since my version of Tableau offers very limited connection options, not including MySQL, so I set up a Google Sheet as my Tableau source, and created the `googlesheets.py` automation (which operates off the Google Sheets API and Google Drive API) to load data to the Sheet.

### Insights

In the `/tableau-screenshots` folder I included screenshots of a few dashboards I put together to show basic product sales and revenue trends.

## Future Enhancements

- **Real Shopify integration**
- **Incremental ETL** - update the pipeline to pull only new or changed data
- **Event-driven automation** - automatically trigger ETL on new orders
- **Incorporate Instagram marketing data**
- **Enhanced forecasting**
- **Unit tests/CI/CD on ETL**

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
```
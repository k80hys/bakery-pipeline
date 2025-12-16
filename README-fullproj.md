# Cookie Bakery - simple data pipeline
Simple data pipeline for a theoretical small cookie baking business.

The following assumptions will be in place for this project:

    Hayes Baked Goods is a small, home-based bakery run by one full-time owner/manager, supported by a part-time baker and a contract bookkeeper. The business specializes in freshly baked cookies offered for local pickup and limited delivery.

    Customers can place orders by the dozen. The types of cookies offered are: Chocolate Chip Cookies, Emmy's Sugar Cookies, and Nutella Swirl Cookies (all the same price - $28 per dozen). Add-ons are available: Nutella Stuffing ($4), Crunchy Peanut Butter Stuffing ($4), and Sea Salt (free).

    Hayes Baked Goods wants to move from intuition-based decision-making to data-backed insights around pricing, product performance, profitability, and ingredient planning. We will do this with a simple data pipeline that organizes their data and turns it into meaningful, accessible insights.

This project will have the following components:
-Source data (CSV) generation, organization, and inspection
-Data audit report
-Business requirements & KPI definitions
-Schema documentation & ER diagram
-ETL pipeline & transformation documentation
-Data validation checks
-Data storage in MySQL Workbench
-Visualization dashboard in Tableau
-Insights & business recommendations
-README & future enhancements

## Generate data
I don't like paying for a ChatGPT subscription, and you can't export CSV files in the free version, so I had it generate pre-formatted dummy data I could easily copy, paste, and plug into a Python script (createcsv.py) that loaded it all into CSVs that were immediately usable for the project. I know in real life the source data might not be quite this neat and ready to use, but there are still some imperfections that I'll be able to clean up in the transform stage to demonstrate my capability there. CSVs are stored in /source-data.

For the sake of this project, the source data will be shopify_orders.csv, shopify_products.csv, recipes.csv, and ingredients.csv. The first two are meant to simulate Shopify exports for a small business, while the second two are meant to simulate recipe and ingredients manual documentation. The Orders data will update on a regular cadence, while the other three will not and will only be updated as needed when business changes are made.

## Inspect data
I created the initial-inspectdata.py file to show basic stats about the CSV data created - column names, row counts, missing values, etc. The results are printed in the /source-data/consolidated_inspection_report.txt file.

// Next steps: Create data audit and business requirements/KPI definitions, upload files to GitHub project
-- Auto-generated schema from staging CSVs
-- Includes dimension, fact, and bridge tables
-- Review keys and constraints before production use

-- BRIDGE TABLE
CREATE TABLE bridge_product_ingredient (
    product_key INT,
    ingredient_key INT,
    quantity DECIMAL(10,2),
    quantity_unit VARCHAR(255),
    PRIMARY KEY (product_key, ingredient_key)
);

-- DIMENSION TABLE
CREATE TABLE dim_date (
    date_key INT,
    date_only VARCHAR(255),
    day_of_week VARCHAR(255),
    month INT,
    year INT,
    PRIMARY KEY (date_key)
);

-- DIMENSION TABLE
CREATE TABLE dim_ingredient (
    ingredient VARCHAR(255),
    unit VARCHAR(255),
    grams_per_unit DECIMAL(10,2),
    supplier VARCHAR(255),
    container_description VARCHAR(255),
    container_grams INT,
    cost_per_unit DECIMAL(10,2),
    cost_per_gram DECIMAL(10,2),
    ingredient_key INT,
    PRIMARY KEY (ingredient_key)
);

-- DIMENSION TABLE
CREATE TABLE dim_product (
    product_sku VARCHAR(255),
    product_name VARCHAR(255),
    category VARCHAR(255),
    price DECIMAL(10,2),
    product_key INT,
    PRIMARY KEY (product_key)
);

-- FACT TABLE
CREATE TABLE fact_orders (
    order_id INT,
    product_key INT,
    date_key INT,
    quantity INT,
    total_price DECIMAL(10,2),
    ingredient_cost DECIMAL(10,2),
    gross_margin DECIMAL(10,2)
);
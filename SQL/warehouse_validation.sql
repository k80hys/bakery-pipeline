-- ============================================
-- Cookie Bakery Data Warehouse Full Validation
-- File: warehouse_validation.sql
-- Purpose: Post-load validation of all tables and fact_orders metrics
-- ============================================

-- 1. Confirm tables exist and row counts
SELECT table_name, table_rows
FROM information_schema.tables
WHERE table_schema = 'cookie_bakery_dw'
  AND table_name IN ('dim_product', 'dim_date', 'dim_ingredient', 'bridge_product_ingredient', 'fact_orders');

-- 2. Foreign Key Integrity: fact_orders -> dimensions
SELECT COUNT(*) AS orphan_product_keys
FROM fact_orders f
LEFT JOIN dim_product p ON f.product_key = p.product_key
WHERE p.product_key IS NULL;

SELECT COUNT(*) AS orphan_date_keys
FROM fact_orders f
LEFT JOIN dim_date d ON f.date_key = d.date_key
WHERE d.date_key IS NULL;

-- 3. Null & Completeness Checks
SELECT COUNT(*) AS null_order_id
FROM fact_orders
WHERE order_id IS NULL;

SELECT COUNT(*) AS null_product_key
FROM fact_orders
WHERE product_key IS NULL;

SELECT COUNT(*) AS null_date_key
FROM fact_orders
WHERE date_key IS NULL;

-- 4. Negative or impossible values
SELECT COUNT(*) AS invalid_rows
FROM fact_orders
WHERE total_price < 0
   OR ingredient_cost < 0
   OR quantity <= 0;

-- 5. Derived metric validation (gross margin)
SELECT COUNT(*) AS margin_mismatch_rows
FROM fact_orders
WHERE ABS(gross_margin - (total_price - ingredient_cost)) > 0.01;

-- 6. Ingredient cost should not exceed revenue
SELECT COUNT(*) AS cost_exceeds_revenue
FROM fact_orders
WHERE ingredient_cost > total_price;

-- 7. Profitability / margin sanity checks
SELECT
    MIN(gross_margin) AS min_gross_margin,
    MAX(gross_margin) AS max_gross_margin,
    AVG(gross_margin) AS avg_gross_margin,
    AVG(gross_margin / NULLIF(total_price,0)) AS avg_margin_pct
FROM fact_orders;

-- 8. Quantity vs price sanity
SELECT
    MIN(total_price / NULLIF(quantity,0)) AS min_price_per_unit,
    MAX(total_price / NULLIF(quantity,0)) AS max_price_per_unit
FROM fact_orders;

-- 9. High-level KPI summary
SELECT
    COUNT(*) AS total_orders,
    SUM(total_price) AS total_revenue,
    SUM(ingredient_cost) AS total_ingredient_cost,
    SUM(gross_margin) AS total_gross_margin,
    AVG(gross_margin / NULLIF(total_price,0)) AS avg_margin_pct
FROM fact_orders;

-- ============================================
-- End of Full Validation Checks
-- ============================================
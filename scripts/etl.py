import sys
from pathlib import Path
import pandas as pd

# -----------------------------
# ENSURE SCRIPT FOLDER IS ON PYTHON PATH
# -----------------------------
# This allows importing other scripts in the same folder
SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.append(str(SCRIPT_DIR))

# Try normal import (works when module is on PYTHONPATH), otherwise load by file path
try:
    from initial_inspectdata import run_data_inspection
except Exception:
    import importlib.util
    module_path = SCRIPT_DIR / "initial_inspectdata.py"
    if not module_path.exists():
        raise ImportError(f"Could not import 'initial_inspectdata' and file not found at {module_path}")
    spec = importlib.util.spec_from_file_location("initial_inspectdata", str(module_path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    run_data_inspection = module.run_data_inspection

# -----------------------------
# PATH CONFIGURATION
# -----------------------------
BASE_DIR = SCRIPT_DIR.parent
SOURCE_DIR = BASE_DIR / "source-data"
STAGING_DIR = BASE_DIR / "staging-data"

STAGING_DIR.mkdir(exist_ok=True)

# -----------------------------
# PIPELINE CONTROL: DATA INSPECTION
# -----------------------------
try:
    run_data_inspection(
        source_folder=SOURCE_DIR,
        output_file=SOURCE_DIR / "consolidated_inspection_report.txt",
        fail_on_issues=True  # Stops ETL if issues are found
    )
except RuntimeError as e:
    print("ETL aborted due to data quality issues.")
    raise e

# -----------------------------
# EXTRACT
# -----------------------------
orders = pd.read_csv(SOURCE_DIR / "shopify_orders.csv")
products = pd.read_csv(SOURCE_DIR / "shopify_products.csv")
ingredients = pd.read_csv(SOURCE_DIR / "ingredients.csv")
recipes = pd.read_csv(SOURCE_DIR / "recipes.csv")

# -----------------------------
# TRANSFORM: DIM_PRODUCT
# -----------------------------
dim_product = (
    products
    .loc[:, ["cookie_sku", "product_name", "category", "price"]]
    .drop_duplicates()
    .reset_index(drop=True)
)
dim_product["product_key"] = dim_product.index + 1
dim_product = dim_product.rename(columns={"cookie_sku": "product_sku"})

# -----------------------------
# TRANSFORM: DIM_DATE
# -----------------------------
orders["date"] = pd.to_datetime(orders["date"])

dim_date = (
    orders[["date"]]
    .drop_duplicates()
    .assign(
        date_only=lambda df: df["date"].dt.date,
        date_key=lambda df: df["date"].dt.strftime("%Y%m%d").astype(int),
        day_of_week=lambda df: df["date"].dt.day_name(),
        month=lambda df: df["date"].dt.month,
        year=lambda df: df["date"].dt.year,
    )
    .loc[:, ["date_key", "date_only", "day_of_week", "month", "year"]]
    .reset_index(drop=True)
)

# -----------------------------
# TRANSFORM: DIM_INGREDIENT
# -----------------------------
dim_ingredient = (
    ingredients
    .drop_duplicates()
    .reset_index(drop=True)
)
dim_ingredient["ingredient_key"] = dim_ingredient.index + 1
dim_ingredient["cost_per_gram"] = (
    dim_ingredient["cost_per_unit"] / dim_ingredient["grams_per_unit"]
)

# -----------------------------
# TRANSFORM: BRIDGE_PRODUCT_INGREDIENT
# -----------------------------
bridge_product_ingredient = (
    recipes
    .merge(dim_product, left_on="sku", right_on="product_sku", how="left")
    .merge(dim_ingredient, on="ingredient", how="left")
    .loc[:, [
        "product_key",
        "ingredient_key",
        "quantity",
        "quantity_unit"
    ]]
)

# -----------------------------
# TRANSFORM: INGREDIENT COST PER PRODUCT
# -----------------------------
ingredient_costs = (
    bridge_product_ingredient
    .merge(
        dim_ingredient[["ingredient_key", "cost_per_gram"]],
        on="ingredient_key"
    )
    .assign(ingredient_cost=lambda df: df["quantity"] * df["cost_per_gram"])
    .groupby("product_key", as_index=False)
    .agg(ingredient_cost=("ingredient_cost", "sum"))
)

# -----------------------------
# TRANSFORM: FACT_ORDERS
# -----------------------------
fact_orders = (
    orders
    .merge(dim_product, left_on="sku", right_on="product_sku")
    .merge(
        dim_date,
        left_on=orders["date"].dt.strftime("%Y%m%d").astype(int),
        right_on="date_key"
    )
    .merge(ingredient_costs, on="product_key", how="left")
)

fact_orders = fact_orders.assign(
    gross_margin=lambda df: df["total_price"] - df["ingredient_cost"]
)

fact_orders = fact_orders.loc[:, [
    "order_id",
    "product_key",
    "date_key",
    "quantity",
    "total_price",
    "ingredient_cost",
    "gross_margin"
]]

# -----------------------------
# LOAD
# -----------------------------
dim_product.to_csv(STAGING_DIR / "dim_product.csv", index=False)
dim_date.to_csv(STAGING_DIR / "dim_date.csv", index=False)
dim_ingredient.to_csv(STAGING_DIR / "dim_ingredient.csv", index=False)
bridge_product_ingredient.to_csv(
    STAGING_DIR / "bridge_product_ingredient.csv", index=False
)
fact_orders.to_csv(STAGING_DIR / "fact_orders.csv", index=False)

print("ETL pipeline completed successfully.")
import os
import sys
import pandas as pd
import chardet

ROUNDING_TOLERANCE = 1e-6


# --------------------------------------------------
# PHASE 1: STRUCTURAL & QUALITY INSPECTION
# --------------------------------------------------

def inspect_csv(file_path):
    print(f"INSPECTING FILE: {os.path.basename(file_path)}")
    print("-" * 60)

    # Detect encoding
    with open(file_path, "rb") as f:
        rawdata = f.read(10000)
    encoding = chardet.detect(rawdata)["encoding"]

    # Detect delimiter
    with open(file_path, "r", encoding=encoding) as f:
        sample = f.read(1024)
        delimiter = "," if sample.count(",") > sample.count("\t") else "\t"

    df = pd.read_csv(file_path, encoding=encoding, delimiter=delimiter)

    print(f"Encoding: {encoding}")
    print(f"Delimiter: {repr(delimiter)}")
    print(f"Row Count: {len(df)}\n")

    print("Column Names & Data Types:")
    print(df.dtypes, "\n")

    print("Sample Rows:")
    print(df.head(), "\n")

    print("Basic Statistics (Numeric Columns):")
    print(df.describe(), "\n")

    print("Missing / Invalid Values Per Column:")
    missing = (
        df.isnull().sum()
        + (df == "-").sum(numeric_only=False)
        + (df == 0).sum(numeric_only=False)
    )
    missing = missing[missing > 0]
    print(missing if not missing.empty else "No missing or invalid values detected.", "\n")

    print(f"Duplicate Rows: {df.duplicated().sum()}")
    print("-" * 60 + "\n")

    return df


# --------------------------------------------------
# PHASE 2: VALIDATION CHECKS
# --------------------------------------------------

def run_validations(data):
    issues = []

    orders = data.get("shopify_orders")
    products = data.get("shopify_products")
    recipes = data.get("recipes")
    ingredients = data.get("ingredients")

    # Referential Integrity
    if orders is not None and products is not None:
        if not orders["sku"].isin(products["cookie_sku"]).all():
            issues.append("Orders.sku contains values not found in Products.cookie_sku")

        if "add_on_sku" in orders.columns:
            invalid_addons = orders["add_on_sku"].dropna()
            if not invalid_addons.isin(products["cookie_sku"]).all():
                issues.append("Orders.add_on_sku contains invalid product references")

    if recipes is not None and products is not None:
        if not recipes["sku"].isin(products["cookie_sku"]).all():
            issues.append("Recipes.sku contains values not found in Products.cookie_sku")

    if recipes is not None and ingredients is not None:
        if not recipes["ingredient"].isin(ingredients["ingredient"]).all():
            issues.append("Recipes.ingredient contains values not found in Ingredients")

    # Domain & Validity
    if orders is not None:
        if (orders["quantity"] <= 0).any():
            issues.append("Orders.quantity must be > 0")
        if (orders["total_price"] < 0).any():
            issues.append("Orders.total_price must be ≥ 0")

    if recipes is not None and (recipes["quantity"] <= 0).any():
        issues.append("Recipes.quantity must be > 0")

    if products is not None:
        if (products["price"] < 0).any():
            issues.append("Products.price must be ≥ 0")

        valid_categories = {"Dozen Cookies", "Add-on"}
        if not products["category"].isin(valid_categories).all():
            issues.append("Products.category contains invalid values")

    if ingredients is not None:
        if (ingredients["cost_per_unit"] < 0).any():
            issues.append("Ingredients.cost_per_unit must be ≥ 0")
        if (ingredients["cost_per_gram"] < 0).any():
            issues.append("Ingredients.cost_per_gram must be ≥ 0")

        diff = (
            ingredients["cost_per_unit"] / ingredients["grams_per_unit"]
            - ingredients["cost_per_gram"]
        ).abs()

        if (diff > ROUNDING_TOLERANCE).any():
            issues.append("Ingredients.cost_per_gram calculation mismatch")

        if (ingredients["container_grams"] < ingredients["grams_per_unit"]).any():
            issues.append("Ingredients.container_grams < grams_per_unit")

    # Completeness
    if orders is not None and orders["order_id"].isna().any():
        issues.append("Null Orders.order_id detected")

    if products is not None and products["cookie_sku"].isna().any():
        issues.append("Null Products.cookie_sku detected")

    if ingredients is not None and ingredients["ingredient"].isna().any():
        issues.append("Null Ingredients.ingredient detected")

    return issues


# --------------------------------------------------
# PIPELINE ENTRY POINT
# --------------------------------------------------

def run_data_inspection(
    source_folder="./source-data",
    output_file="./source-data/consolidated_inspection_report.txt",
    fail_on_issues=True
):
    original_stdout = sys.stdout
    dataframes = {}

    with open(output_file, "w", encoding="utf-8") as report:
        sys.stdout = report

        for filename in os.listdir(source_folder):
            if filename.endswith(".csv"):
                path = os.path.join(source_folder, filename)
                df = inspect_csv(path)
                dataframes[filename.replace(".csv", "").lower()] = df

        print("\nVALIDATION SUMMARY")
        print("=" * 60)

        issues = run_validations(dataframes)

        if not issues:
            print("✅ All validation checks passed.")
        else:
            for i, issue in enumerate(issues, 1):
                print(f"{i}. ❌ {issue}")

    sys.stdout = original_stdout

    if issues and fail_on_issues:
        raise RuntimeError("Data inspection failed — see inspection report.")

    return issues


# --------------------------------------------------
# SCRIPT EXECUTION
# --------------------------------------------------

if __name__ == "__main__":
    run_data_inspection()
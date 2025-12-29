import os
import pandas as pd

SOURCE_DATA_FOLDER = "./source-data"
OUTPUT_FILE = os.path.join(SOURCE_DATA_FOLDER, "second_inspection.txt")
ROUNDING_TOLERANCE = 1e-6


def load_csvs(folder):
    """Load all CSVs into a dict keyed by filename (without .csv)."""
    data = {}
    for file in os.listdir(folder):
        if file.lower().endswith(".csv"):
            key = file.replace(".csv", "")
            data[key] = pd.read_csv(os.path.join(folder, file))
    return data


def audit(data):
    issues = []

    orders = data.get("shopify_orders")
    products = data.get("shopify_products")
    recipes = data.get("Recipes")
    ingredients = data.get("Ingredients")

    # --------------------------------------------------
    # 1. REFERENTIAL INTEGRITY CHECKS
    # --------------------------------------------------

    if orders is not None and products is not None:
        bad_skus = orders.loc[
            ~orders["sku"].isin(products["cookie_sku"]),
            "sku"
        ].unique()
        if len(bad_skus) > 0:
            issues.append(f"Orders.sku not found in Products.cookie_sku: {bad_skus}")

        if "add_on_sku" in orders.columns:
            bad_addons = orders.loc[
                orders["add_on_sku"].notna() &
                ~orders["add_on_sku"].isin(products["cookie_sku"]),
                "add_on_sku"
            ].unique()
            if len(bad_addons) > 0:
                issues.append(f"Orders.add_on_sku not found in Products.cookie_sku: {bad_addons}")

    if recipes is not None and products is not None:
        bad_recipe_skus = recipes.loc[
            ~recipes["sku"].isin(products["cookie_sku"]),
            "sku"
        ].unique()
        if len(bad_recipe_skus) > 0:
            issues.append(f"Recipes.sku not found in Products.cookie_sku: {bad_recipe_skus}")

    if recipes is not None and ingredients is not None:
        bad_ingredients = recipes.loc[
            ~recipes["ingredient"].isin(ingredients["ingredient"]),
            "ingredient"
        ].unique()
        if len(bad_ingredients) > 0:
            issues.append(f"Recipes.ingredient not found in Ingredients.ingredient: {bad_ingredients}")

    # --------------------------------------------------
    # 2. DOMAIN & VALIDITY CHECKS
    # --------------------------------------------------

    if orders is not None:
        bad_qty = orders.loc[orders["quantity"] <= 0, "order_id"]
        if not bad_qty.empty:
            issues.append(f"Orders.quantity <= 0 for order_id(s): {bad_qty.tolist()}")

        bad_price = orders.loc[orders["total_price"] < 0, "order_id"]
        if not bad_price.empty:
            issues.append(f"Orders.total_price < 0 for order_id(s): {bad_price.tolist()}")

    if recipes is not None:
        if not recipes.loc[recipes["quantity"] <= 0].empty:
            issues.append("Recipes.quantity <= 0 detected")

    if products is not None:
        bad_price = products.loc[products["price"] < 0, "cookie_sku"]
        if not bad_price.empty:
            issues.append(f"Products.price < 0 for sku(s): {bad_price.tolist()}")

        valid_categories = {"Dozen Cookies", "Add-on"}
        bad_categories = products.loc[
            ~products["category"].isin(valid_categories),
            "category"
        ].unique()
        if len(bad_categories) > 0:
            issues.append(f"Invalid Products.category values: {bad_categories}")

    if ingredients is not None:
        for field in ["cost_per_unit", "cost_per_gram"]:
            bad_costs = ingredients.loc[ingredients[field] < 0, "ingredient"]
            if not bad_costs.empty:
                issues.append(f"Ingredients.{field} < 0 for: {bad_costs.tolist()}")

    if recipes is not None and ingredients is not None:
        bad_units = recipes.loc[
            ~recipes["quantity_unit"].isin(ingredients["unit"]),
            "quantity_unit"
        ].unique()
        if len(bad_units) > 0:
            issues.append(f"Recipes.quantity_unit not found in Ingredients.unit: {bad_units}")

    # --------------------------------------------------
    # 3. CONSISTENCY & DERIVATION CHECKS
    # --------------------------------------------------

    if ingredients is not None:
        diff = (
            ingredients["cost_per_unit"] / ingredients["grams_per_unit"]
            - ingredients["cost_per_gram"]
        ).abs()

        bad_calc = ingredients.loc[diff > ROUNDING_TOLERANCE, "ingredient"]
        if not bad_calc.empty:
            issues.append(
                f"Cost per gram mismatch beyond tolerance for: {bad_calc.tolist()}"
            )

        bad_packaging = ingredients.loc[
            ingredients["container_grams"] < ingredients["grams_per_unit"],
            "ingredient"
        ]
        if not bad_packaging.empty:
            issues.append(
                f"container_grams < grams_per_unit for: {bad_packaging.tolist()}"
            )

    # --------------------------------------------------
    # 4. COMPLETENESS CHECKS
    # --------------------------------------------------

    if orders is not None and orders["order_id"].isna().any():
        issues.append("Null Orders.order_id detected")

    if products is not None and products["cookie_sku"].isna().any():
        issues.append("Null Products.cookie_sku detected")

    if ingredients is not None and ingredients["ingredient"].isna().any():
        issues.append("Null Ingredients.ingredient detected")

    return issues


if __name__ == "__main__":
    data = load_csvs(SOURCE_DATA_FOLDER)
    issues = audit(data)

    lines = []
    lines.append("SECOND DATA INSPECTION REPORT")
    lines.append("=" * 40)

    if not issues:
        lines.append("✅ No issues found.")
    else:
        for i, issue in enumerate(issues, 1):
            lines.append(f"{i}. ❌ {issue}")

    report_text = "\n".join(lines)

    # Print to console
    print(report_text)

    # Write to file
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(report_text)

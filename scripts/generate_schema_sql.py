import os
import pandas as pd

STAGING_DIR = "staging-data"
SQL_DIR = "sql"
OUTPUT_FILE = "auto_generated_schema.sql"

os.makedirs(SQL_DIR, exist_ok=True)

def pandas_dtype_to_mysql(dtype):
    if pd.api.types.is_integer_dtype(dtype):
        return "INT"
    elif pd.api.types.is_float_dtype(dtype):
        return "DECIMAL(10,2)"
    elif pd.api.types.is_bool_dtype(dtype):
        return "BOOLEAN"
    elif pd.api.types.is_datetime64_any_dtype(dtype):
        return "DATETIME"
    else:
        return "VARCHAR(255)"

sql_statements = []

for filename in sorted(os.listdir(STAGING_DIR)):
    if not filename.endswith(".csv"):
        continue

    table_name = filename.replace(".csv", "")
    file_path = os.path.join(STAGING_DIR, filename)
    df = pd.read_csv(file_path)

    # Detect table type
    if table_name.startswith("dim_"):
        table_type = "DIMENSION"
    elif table_name.startswith("fact_"):
        table_type = "FACT"
    elif table_name.startswith("bridge_"):
        table_type = "BRIDGE"
    else:
        table_type = "UNKNOWN"

    columns_sql = []
    key_columns = []

    for col in df.columns:
        mysql_type = pandas_dtype_to_mysql(df[col].dtype)
        columns_sql.append(f"    {col} {mysql_type}")

        if col.endswith("_key"):
            key_columns.append(col)

    # Primary key logic
    if table_type == "DIMENSION" and key_columns:
        columns_sql.append(f"    PRIMARY KEY ({key_columns[0]})")

    elif table_type == "BRIDGE" and len(key_columns) >= 2:
        columns_sql.append(f"    PRIMARY KEY ({', '.join(key_columns)})")

    # Fact tables: no automatic PK

    create_table_sql = f"""
-- {table_type} TABLE
CREATE TABLE {table_name} (
{",\n".join(columns_sql)}
);
""".strip()

    sql_statements.append(create_table_sql)

output_path = os.path.join(SQL_DIR, OUTPUT_FILE)
with open(output_path, "w") as f:
    f.write("-- Auto-generated schema from staging CSVs\n")
    f.write("-- Includes dimension, fact, and bridge tables\n")
    f.write("-- Review keys and constraints before production use\n\n")
    f.write("\n\n".join(sql_statements))

print(f"Schema written to {output_path}")

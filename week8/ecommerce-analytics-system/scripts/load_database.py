import sqlite3
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASE_PATH = BASE_DIR / "database" / "ecommerce.db"
SCHEMA_PATH = BASE_DIR / "sql" / "schema.sql"
CLEANED_DATA = BASE_DIR / "data" / "cleaned"

DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
SCHEMA_PATH = Path("sql/schema.sql")
CLEANED_DATA = Path("data/cleaned")


def create_database():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    with open(SCHEMA_PATH, "r") as file:
        cursor.executescript(file.read())

    customers = pd.read_csv(CLEANED_DATA / "customers_clean.csv")
    products = pd.read_csv(CLEANED_DATA / "products_clean.csv")
    orders = pd.read_csv(CLEANED_DATA / "orders_clean.csv")
    order_items = pd.read_csv(CLEANED_DATA / "order_items_clean.csv")

    customers.to_sql(
        "customers",
        conn,
        if_exists="append",
        index=False
    )

    products.to_sql(
        "products",
        conn,
        if_exists="append",
        index=False
    )

    orders.to_sql(
        "orders",
        conn,
        if_exists="append",
        index=False
    )

    order_items.to_sql(
        "order_items",
        conn,
        if_exists="append",
        index=False
    )

    tables = [
        "customers",
        "products",
        "orders",
        "order_items"
    ]

    print("\nDatabase Loaded Successfully\n")

    for table in tables:
        count = cursor.execute(
            f"SELECT COUNT(*) FROM {table}"
        ).fetchone()[0]

        print(f"{table}: {count} rows")

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_database()
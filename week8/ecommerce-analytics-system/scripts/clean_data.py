import pandas as pd
import re
from pathlib import Path

RAW_DATA_DIR = Path("data/raw")
CLEANED_DATA_DIR = Path("data/cleaned")
CLEANED_DATA_DIR.mkdir(parents=True, exist_ok=True)

EMAIL_PATTERN = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"


def clean_orders(df):
    issue_count = 0

    def fix_date(date):
        nonlocal issue_count

        if pd.isna(date):
            return None

        try:
            return pd.to_datetime(date, format="%Y-%m-%d %H:%M:%S")
        except:
            try:
                issue_count += 1
                return pd.to_datetime(date, format="%d-%m-%Y")
            except:
                issue_count += 1
                return pd.NaT

    df["order_date"] = df["order_date"].apply(fix_date)
    df["customer_id"] = df["customer_id"].fillna("UNKNOWN")

    return df, issue_count


def clean_products(df):
    df["product_name"] = (
        df["product_name"]
        .astype(str)
        .str.strip()
        .str.title()
    )

    return df


def validate_emails(df):
    invalid = df[
        ~df["email"].astype(str).str.match(EMAIL_PATTERN, na=False)
    ]

    return invalid["customer_id"].tolist()


def check_referential_integrity(order_items_df, orders_df):
    invalid = order_items_df[
        ~order_items_df["order_id"].isin(
            orders_df["order_id"]
        )
    ]

    return invalid


def main():

    customers = pd.read_csv(RAW_DATA_DIR / "customers.csv")
    products = pd.read_csv(RAW_DATA_DIR / "products.csv")
    orders = pd.read_csv(RAW_DATA_DIR / "orders.csv")
    order_items = pd.read_csv(RAW_DATA_DIR / "order_items.csv")

    orders, fixed_dates = clean_orders(orders)

    products = clean_products(products)

    invalid_emails = validate_emails(customers)

    invalid_order_items = check_referential_integrity(
        order_items,
        orders
    )

    customers.to_csv(
        CLEANED_DATA_DIR / "customers_clean.csv",
        index=False
    )

    products.to_csv(
        CLEANED_DATA_DIR / "products_clean.csv",
        index=False
    )

    orders.to_csv(
        CLEANED_DATA_DIR / "orders_clean.csv",
        index=False
    )

    order_items.to_csv(
        CLEANED_DATA_DIR / "order_items_clean.csv",
        index=False
    )

    with open(
        CLEANED_DATA_DIR / "issues_report.txt",
        "w"
    ) as f:

        f.write("DATA CLEANING REPORT\n")
        f.write("====================\n\n")

        f.write(f"Wrong date formats fixed : {fixed_dates}\n")
        f.write(f"Invalid emails found     : {len(invalid_emails)}\n")
        f.write(f"Broken order references  : {len(invalid_order_items)}\n")

        if invalid_emails:
            f.write("\nCustomer IDs with invalid emails:\n")
            for cid in invalid_emails:
                f.write(f"{cid}\n")

    print("Data cleaned successfully.")
    print("Cleaned files saved in data/cleaned/")
    print("Issue report generated.")


if __name__ == "__main__":
    main()
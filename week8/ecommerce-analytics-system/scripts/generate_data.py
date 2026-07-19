import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta
from pathlib import Path

fake = Faker()
random.seed(42)
Faker.seed(42)

NUM_CUSTOMERS = 500
NUM_PRODUCTS = 500
NUM_ORDERS = 500
NUM_ORDER_ITEMS = 1200

RAW_DATA_DIR = Path("data/raw")
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

categories = {
    "Electronics": ["Mobile", "Laptop", "Camera", "Headphones"],
    "Clothing": ["Shirt", "Jeans", "Jacket", "Shoes"],
    "Home": ["Furniture", "Kitchen", "Decor", "Appliances"],
    "Books": ["Fiction", "Education", "Biography", "Comics"]
}

customer_types = ["REGULAR", "PREMIUM", "VIP"]

order_status = [
    "PLACED",
    "SHIPPED",
    "DELIVERED",
    "CANCELLED",
    "RETURNED"
]


def generate_customers():
    customers = []

    for i in range(1, NUM_CUSTOMERS + 1):
        email = fake.email()

        if random.random() < 0.02:
            if random.random() < 0.5:
                email = email.replace("@", "")
            else:
                email = email.split("@")[0] + "@"

        customers.append({
            "customer_id": f"CUST{i:04}",
            "customer_name": fake.name(),
            "email": email,
            "registration_date": fake.date_between(start_date="-3y", end_date="today"),
            "customer_type": random.choice(customer_types)
        })

    return pd.DataFrame(customers)


def generate_products():
    products = []

    for i in range(1, NUM_PRODUCTS + 1):
        category = random.choice(list(categories.keys()))
        subcategory = random.choice(categories[category])

        name = fake.word().title() + " " + subcategory

        if random.random() < 0.20:
            if random.random() < 0.5:
                name = "  " + name.upper() + "  "
            else:
                name = "  " + name.lower() + "  "

        products.append({
            "product_id": f"PROD{i:04}",
            "product_name": name,
            "category": category,
            "subcategory": subcategory,
            "cost_price": round(random.uniform(100, 5000), 2)
        })

    return pd.DataFrame(products)


def generate_orders():
    orders = []
    start_date = datetime(2024, 1, 1)

    for i in range(1, NUM_ORDERS + 1):
        order_date = start_date + timedelta(
            days=random.randint(0, 700),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59)
        )

        if random.random() < 0.05:
            customer_id = None
        else:
            customer_id = f"CUST{random.randint(1, NUM_CUSTOMERS):04}"

        if random.random() < 0.05:
            date = order_date.strftime("%d-%m-%Y")
        else:
            date = order_date.strftime("%Y-%m-%d %H:%M:%S")

        orders.append({
            "order_id": f"ORD{i:05}",
            "customer_id": customer_id,
            "order_date": date,
            "status": random.choice(order_status)
        })

    return pd.DataFrame(orders)


def generate_order_items(products_df):
    items = []

    for i in range(1, NUM_ORDER_ITEMS + 1):
        product = products_df.sample(1).iloc[0]

        quantity = random.randint(1, 5)

        if random.random() < 0.03:
            quantity *= -1

        items.append({
            "item_id": f"ITEM{i:05}",
            "order_id": f"ORD{random.randint(1, NUM_ORDERS):05}",
            "product_id": product["product_id"],
            "quantity": quantity,
            "unit_price": round(product["cost_price"] * random.uniform(1.2, 2.5), 2),
            "discount_percent": random.randint(0, 100)
        })

    return pd.DataFrame(items)


def main():
    customers = generate_customers()
    products = generate_products()
    orders = generate_orders()
    order_items = generate_order_items(products)

    customers.to_csv(RAW_DATA_DIR / "customers.csv", index=False)
    products.to_csv(RAW_DATA_DIR / "products.csv", index=False)
    orders.to_csv(RAW_DATA_DIR / "orders.csv", index=False)
    order_items.to_csv(RAW_DATA_DIR / "order_items.csv", index=False)

    print("CSV files generated successfully.")


if __name__ == "__main__":
    main()
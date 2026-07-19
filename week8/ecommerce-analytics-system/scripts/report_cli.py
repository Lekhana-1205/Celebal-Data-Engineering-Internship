import sqlite3
import argparse
from datetime import datetime, timedelta


DATABASE_PATH = "database/ecommerce.db"


def connect_db():
    return sqlite3.connect(DATABASE_PATH)


def get_summary(start_date, end_date):

    conn = connect_db()
    cursor = conn.cursor()

    query = """
    SELECT
        COUNT(DISTINCT o.order_id) AS total_orders,
        ROUND(
            SUM(
                oi.quantity *
                oi.unit_price *
                (1 - oi.discount_percent / 100.0)
            ),
            2
        ) AS revenue,
        COUNT(DISTINCT o.customer_id) AS customers

    FROM orders o

    JOIN order_items oi
    ON o.order_id = oi.order_id

    WHERE DATE(o.order_date)
    BETWEEN DATE(?) AND DATE(?)
    """

    cursor.execute(query, (start_date, end_date))

    result = cursor.fetchone()

    print("\nREPORT SUMMARY")
    print("---------------------")
    print("Total Orders     :", result[0] or 0)
    print("Revenue          :", result[1] or 0)
    print("Unique Customers :", result[2] or 0)

    conn.close()


def top_products(start_date, end_date):

    conn = connect_db()
    cursor = conn.cursor()

    query = """
    SELECT
        p.product_name,
        SUM(oi.quantity) AS quantity_sold

    FROM order_items oi

    JOIN products p
    ON oi.product_id=p.product_id

    JOIN orders o
    ON o.order_id=oi.order_id

    WHERE DATE(o.order_date)
    BETWEEN DATE(?) AND DATE(?)

    GROUP BY p.product_name

    ORDER BY quantity_sold DESC

    LIMIT 3
    """

    cursor.execute(query,(start_date,end_date))

    print("\nTOP 3 PRODUCTS")
    print("---------------------")

    rows = cursor.fetchall()

    if not rows:
        print("No products found")
    else:
        for row in rows:
            print(row[0], "-", row[1], "units")

    conn.close()


def compare_previous_period(start_date,end_date):

    start = datetime.strptime(
        start_date,
        "%Y-%m-%d"
    )

    end = datetime.strptime(
        end_date,
        "%Y-%m-%d"
    )

    days = (end-start).days + 1

    previous_end = start - timedelta(days=1)

    previous_start = previous_end - timedelta(days=days-1)


    conn = connect_db()
    cursor = conn.cursor()


    query = """
    SELECT
        ROUND(
            SUM(
                oi.quantity *
                oi.unit_price *
                (1 - oi.discount_percent /100.0)
            ),
            2
        )

    FROM orders o

    JOIN order_items oi
    ON o.order_id=oi.order_id

    WHERE DATE(o.order_date)
    BETWEEN DATE(?) AND DATE(?)
    """


    cursor.execute(
        query,
        (
            previous_start.strftime("%Y-%m-%d"),
            previous_end.strftime("%Y-%m-%d")
        )
    )


    previous = cursor.fetchone()[0] or 0


    cursor.execute(
        query,
        (
            start_date,
            end_date
        )
    )


    current = cursor.fetchone()[0] or 0


    if previous == 0:
        change = 0
    else:
        change = ((current-previous)/previous)*100


    print("\nPERIOD COMPARISON")
    print("---------------------")
    print("Previous Revenue :", round(previous,2))
    print("Current Revenue  :", round(current,2))
    print("Change %         :", round(change,2))


    conn.close()



def main():

    parser = argparse.ArgumentParser(
        description="E-Commerce Analytics Reporting Tool"
    )


    parser.add_argument(
        "--report",
        required=True,
        choices=[
            "daily",
            "weekly",
            "monthly"
        ]
    )


    parser.add_argument(
        "--start",
        required=True
    )


    parser.add_argument(
        "--end",
        required=True
    )


    args = parser.parse_args()


    get_summary(
        args.start,
        args.end
    )

    top_products(
        args.start,
        args.end
    )

    compare_previous_period(
        args.start,
        args.end
    )


if __name__=="__main__":
    main()
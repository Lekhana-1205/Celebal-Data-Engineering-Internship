import sqlite3
from datetime import datetime


DATABASE_PATH = "database/ecommerce.db"


def test_invalid_order_id():

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM order_items
    WHERE order_id NOT IN
    (
        SELECT order_id FROM orders
    )
    """)

    result = cursor.fetchall()

    assert len(result) == 0, "Invalid order_id found"

    print("Invalid order_id test passed")

    conn.close()



def test_invalid_discount():

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM order_items
    WHERE discount_percent > 100
    """)

    result = cursor.fetchall()

    assert len(result) == 0, "Discount greater than 100 found"

    print("Discount validation test passed")

    conn.close()



def test_zero_quantity():

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM order_items
    WHERE quantity = 0
    """)

    result = cursor.fetchall()

    print(
        "Zero quantity records:",
        len(result)
    )

    print("Zero quantity test completed")

    conn.close()



def test_future_dates():

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    today = datetime.now().strftime("%Y-%m-%d")

    cursor.execute("""
    SELECT *
    FROM orders
    WHERE DATE(order_date) > DATE(?)
    """,(today,))

    result = cursor.fetchall()

    assert len(result) == 0, "Future order dates found"

    print("Future date validation test passed")

    conn.close()



if __name__ == "__main__":

    test_invalid_order_id()
    test_invalid_discount()
    test_zero_quantity()
    test_future_dates()
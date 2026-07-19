import sqlite3
from pathlib import Path

DATABASE_PATH = "database/ecommerce.db"

SQL_FILES = [
    "sql/basic_queries.sql",
    "sql/intermediate_queries.sql",
    "sql/advanced_queries.sql"
]


conn = sqlite3.connect(DATABASE_PATH)
cursor = conn.cursor()


for file in SQL_FILES:

    print("\n==============================")
    print("Running:", file)
    print("==============================")

    sql_path = Path(file)

    queries = sql_path.read_text().split(";")

    count = 1

    for query in queries:

        query = query.strip()

        if query:

            try:
                cursor.execute(query)

                rows = cursor.fetchmany(5)

                print(f"\nQuery {count} executed successfully")

                if rows:
                    for row in rows:
                        print(row)

                count += 1

            except Exception as e:
                print(f"\nQuery {count} failed")
                print(e)

                count += 1


conn.close()

print("\nAll SQL files tested")
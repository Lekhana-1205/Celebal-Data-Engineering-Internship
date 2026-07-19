# E-Commerce Order Analytics System

## Project Overview

The E-Commerce Order Analytics System is an end-to-end data analytics project built using Python and SQL.

The project simulates a real-world e-commerce data pipeline where raw order data from multiple sources is generated, cleaned, validated, stored in a database, and analyzed to generate business insights.

## Technologies Used

* Python
* Pandas
* SQLite
* SQL
* Faker
* Command Line Interface (CLI)

## Project Workflow

```
Data Generation
        |
        ↓
Data Cleaning & Validation
        |
        ↓
SQLite Database
        |
        ↓
SQL Analytics
        |
        ↓
CLI Reporting Tool
```

## Project Structure

```
ecommerce-analytics-system/

│── data/
│   ├── raw/
│   │   ├── customers.csv
│   │   ├── products.csv
│   │   ├── orders.csv
│   │   └── order_items.csv
│   │
│   └── cleaned/
│       ├── customers_clean.csv
│       ├── products_clean.csv
│       ├── orders_clean.csv
│       └── order_items_clean.csv
│
│── database/
│   └── ecommerce.db
│
│── scripts/
│   ├── generate_data.py
│   ├── clean_data.py
│   ├── load_database.py
│   ├── report_cli.py
│   └── test_cases.py
│
│── sql/
│   ├── schema.sql
│   ├── basic_queries.sql
│   ├── intermediate_queries.sql
│   └── advanced_queries.sql
│
│── output/
│   └── sample_reports/
│
└── README.md
```

## Dataset Generation

The project generates four realistic datasets:

### Customers

Contains customer details such as:

* Customer ID
* Customer name
* Email
* Registration date
* Customer type

### Products

Contains:

* Product ID
* Product name
* Category
* Subcategory
* Cost price

### Orders

Contains:

* Order ID
* Customer ID
* Order date
* Order status
* Region code

### Order Items

Contains:

* Item ID
* Order ID
* Product ID
* Quantity
* Unit price
* Discount percentage

The generated data includes intentional inconsistencies such as:

* Missing customer IDs
* Invalid email formats
* Incorrect date formats
* Duplicate records
* Product formatting issues
* Invalid quantities

## Data Cleaning and Validation

The cleaning process is performed using Pandas.

Operations include:

* Handling missing values
* Removing duplicates
* Standardizing product names
* Fixing date formats
* Validating emails
* Checking referential integrity between tables

Cleaned datasets are stored in:

```
data/cleaned/
```

## Database Implementation

The cleaned data is loaded into a SQLite database.

Database:

```
database/ecommerce.db
```

Tables created:

* customers
* products
* orders
* order_items

The database uses primary and foreign key relationships to maintain data consistency.

## SQL Analytics

The project includes SQL queries for business analysis.

### Basic Analysis

* Total revenue by category
* Top customers by order value
* Monthly order trends

### Intermediate Analysis

* Customers without delivered orders
* Product return analysis
* Category-wise return rates

### Advanced Analysis

* Running revenue totals using window functions
* Product ranking using DENSE_RANK
* Customer order gap analysis using LAG
* Customer segmentation using CTEs
* Quartile-based customer classification using NTILE
* Year-over-year revenue comparison
* First and last purchased category analysis
* Cumulative revenue contribution
* Cohort retention analysis

## CLI Reporting Tool

A command-line reporting tool is developed to generate dynamic reports from the SQLite database.

Example:

```
python scripts/report_cli.py --report monthly --start 2025-01-01 --end 2025-12-31
```

The report provides:

* Total orders
* Total revenue
* Unique customers
* Top 3 products
* Comparison with previous period

## Edge Case Testing

The system handles and tests:

* Invalid order references
* Discount percentage greater than allowed range
* Zero quantity records
* Future order dates
* Empty query results

Run tests using:

```
python scripts/test_cases.py
```

## Setup and Execution

### Create Virtual Environment

```
python -m venv .venv
```

### Activate Environment

Windows:

```
.venv\Scripts\activate
```

### Install Dependencies

```
pip install pandas faker tabulate
```

### Generate Dataset

```
python scripts/generate_data.py
```

### Clean Data

```
python scripts/clean_data.py
```

### Load Database

```
python scripts/load_database.py
```

### Generate Reports

```
python scripts/report_cli.py --report monthly --start 2025-01-01 --end 2025-12-31
```

## Sample Outputs

Execution screenshots and sample reports are available in:

```
output/sample_reports/
```

## Conclusion

This project demonstrates an end-to-end analytics workflow by combining Python-based data processing and SQL-based analysis to transform raw e-commerce data into meaningful business insights.

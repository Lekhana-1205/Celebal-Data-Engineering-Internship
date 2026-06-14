# Superstore SQL Analysis Project

## Project Overview

This project focuses on analyzing retail sales data from the Superstore dataset using SQL. The main goal is to apply core SQL techniques such as subqueries, CTEs (Common Table Expressions), window functions, and joins to extract meaningful business insights from raw transactional data.

The dataset includes information related to customers, products, and orders, which is structured into separate relational tables to improve query efficiency and organization.

---

## Dataset Description

The dataset consists of the following components:

- Customer information (Customer ID, Name, Segment, etc.)
- Product information (Product ID, Category, Sub-Category, Product Name)
- Order transactions (Order ID, Date, Sales, Quantity, Discount, Profit)

All raw data was initially loaded into a single table named `superstore_raw`.

---

## Database Structure

To improve data modeling, the dataset was divided into three tables:

### Customers Table
Contains unique customer records including:
- Customer ID
- Customer Name
- Segment

### Products Table
Contains product-level details such as:
- Product ID
- Product Name
- Category
- Sub-Category

### Orders Table
Contains transactional sales data including:
- Order ID
- Order Date
- Customer ID
- Product ID
- Sales
- Quantity
- Discount
- Profit

---

## SQL Techniques Applied

The following SQL concepts were used throughout the project:

- Basic SELECT and filtering operations
- Aggregate functions (SUM, AVG, COUNT)
- Subqueries for conditional filtering
- Common Table Expressions (CTEs) for intermediate calculations
- Window functions such as ROW_NUMBER() and RANK()
- JOIN operations for combining multiple tables

---

## Business Analysis Tasks

The dataset was analyzed to answer several business questions:

### 1. Sales-Based Filtering
- Identify orders where sales exceed the average sales value
- Retrieve the highest sales transaction for each customer

### 2. Customer-Level Aggregation
- Compute total sales per customer using CTEs
- Identify customers performing above the average spending level

### 3. Ranking Analysis
- Rank customers based on total sales using window functions
- Assign row numbers to transactions for ordered analysis

### 4. Combined Analysis
- Merge customer details with aggregated sales using JOIN + CTE + ranking functions

### 5. Business Insights
- Identify top-performing customers
- Identify low-value customers
- Detect customers with single or minimal orders
- Analyze customers above average sales contribution

---

## Key Observations

- A small group of customers contributes significantly to overall revenue.
- Aggregation at the customer level provides clearer business insights than raw transaction data.
- Window functions help in structured ranking and comparison of customers.
- CTEs simplify complex SQL queries and improve readability.
- Data normalization improves analysis efficiency and query performance.

---

## Learning Outcomes

Through this project, the following skills were developed:

- Structuring raw data into relational tables
- Writing advanced SQL queries for real-world analysis
- Applying subqueries and CTEs effectively
- Using window functions for ranking and sequencing
- Deriving business insights from structured data

---

## Conclusion

This project demonstrates how SQL can be used to transform raw retail data into meaningful insights. By applying analytical SQL techniques, it becomes easier to understand customer behavior, sales trends, and business performance, which supports better decision-making.

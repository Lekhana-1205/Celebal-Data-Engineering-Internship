database superstore_db;
use superstore_db;
select * from superstore_raw limit 10;

-- create customer table
create table customers(customer_id varchar(50) primary key, customer_name varchar(100), segment varchar(50));

-- create products table
create table products(product_id varchar(50),product_name varchar(250),category varchar(100),sub_category varchar(100));

-- create orders table
create table orders (order_id varchar(50), order_date date, customer_id varchar(50), product_id varchar(50), sales decimal(10,2),
 quantity int, discount decimal(5,2), profit decimal(10,2));
 
-- insert data into customers table
insert into customers
select distinct `Customer ID`, `Customer Name`, Segment
from superstore_raw;

select * from customers limit 10;

-- insert data into products table
insert into products
select distinct `Product ID`, `Product Name`, Category, `Sub-Category`
from superstore_raw;

select * from products limit 10;

-- insert data into orders table
insert into orders 
select distinct `Order ID`, str_to_date(`Order Date`, '%c/%e/%Y'), `Customer ID`, `Product ID`, cast(`Sales` as decimal(10,2)), cast(`Quantity` as signed), cast(`Discount` as decimal(5,2)), cast(`Profit` as decimal(10,2)) 
from superstore_raw;

SELECT * FROM orders limit 10;

-- customers with above average sales
select * from orders where sales>(select avg(sales) from orders);

-- Highest order value per Customer
select * from (
select *,row_number() over(partition by customer_id order by sales desc) as rn from orders
) t where rn=1;

-- total sales per customer using cte
with customer_sales as (
select customer_id,sum(sales) as total_sales from orders group by customer_id
)
select * from customer_sales;

-- customers above average total sales using cte
with customer_sales as (
select customer_id,sum(sales) as total_sales from orders group by customer_id
)
select * from customer_sales where total_sales>(select avg(total_sales) from customer_sales);

-- row number ranking based on sales
select *,row_number() over(order by sales desc) as rn from orders;

-- rank orders based on sales
select *,rank() over(order by sales desc) as rnk from orders;

-- dense rank order by sales
select *,dense_rank() over(order by sales desc) as drnk from orders;

-- final customer ranking using cte join and window function
with customer_sales as (
select customer_id,sum(sales) as total_sales from orders group by customer_id
)
select c.`Customer ID`,c.`Customer Name`,s.total_sales,rank() over(order by s.total_sales desc) as rnk
from customer_sales s join customers c on c.`Customer ID`=s.customer_id;

-- top 10 customers by total sales
select customer_id,sum(sales) as total_sales from orders group by customer_id order by total_sales desc limit 10;

-- lowest 10 customers by total sales
select customer_id,sum(sales) as total_sales from orders group by customer_id order by total_sales asc limit 10;


-- customers with only one distinct order
select customer_id,count(distinct order_id) as order_count from orders group by customer_id having count(distinct order_id)=1;


-- customers whose total sales are above average
with customer_sales as (select customer_id,sum(sales) as total_sales from orders group by customer_id)
select * from customer_sales where total_sales>(select avg(total_sales) from customer_sales);
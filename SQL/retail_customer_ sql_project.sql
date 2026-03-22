create  database retail_db;

use retail_db;

 select * from retail_customer_dataset ;
 
  ----  # Check Total Number of Rows  ------
SELECT COUNT(*) AS total_rows
FROM retail_customer_dataset;

 ------ # Check Missing Customer IDs ------
SELECT COUNT(*)
FROM retail_customer_dataset
WHERE CustomerID IS NULL;
 
 
-------  # Check Negative Quantity -------
SELECT *
FROM retail_customer_dataset
WHERE Quantity <= 0;


 ------ # Check Invalid Prices --------
SELECT *
FROM retail_customer_dataset
WHERE UnitPrice <= 0;

 ------- # Remove Extra Spaces in Product Names ---------
 
update retail_customer_dataset 
set 
Description = trim(Description) ,
Quantity = trim(Quantity),
UnitPrice = trim(UnitPrice) 
where  
Description != trim(Description) 
or Quantity != trim(Quantity)
or UnitPrice != trim(UnitPrice) 
;

--------  # Cheching duplicate values  ----------

SELECT
InvoiceNo,StockCode,
Description,Quantity,
InvoiceDate,UnitPrice,
CustomerID,Country,
COUNT(*) AS duplicate_count
FROM retail_customer_dataset
GROUP BY
InvoiceNo,StockCode,
Description,Quantity,
InvoiceDate,UnitPrice,
CustomerID,Country
HAVING COUNT(*) > 1 ;

------ # Standardize Country Names ----------

update retail_customer_dataset
set 
Country = upper(Country) ;

select country
from retail_customer_dataset;

-------- # converting text in to date format --------

describe retail_customer_dataset;

alter table retail_customer_dataset
modify InvoiceDate date;

select month(InvoiceDate)
 from retail_customer_dataset ;
 

--------- # Create Clean View -----------

 create view cleaned_dataset as 
 select InvoiceNo,StockCode,
 Description,Quantity,
 InvoiceDate,UnitPrice,
 CustomerID,Country,
 TotalPrice
 from retail_customer_dataset;
 
 select * from cleaned_dataset;
 
------- # Total Revenue -------

 select round(sum(TotalPrice),2) 
 from cleaned_dataset;

---------- # Top products --------
 
 select Description ,sum(Quantity) as total_sales
 from cleaned_dataset
 group by Description
 order by total_sales desc
 limit 10;
 
 
 --------  # Revenue by Country -----------
 
 select Country , round(sum(TotalPrice),2) as Revenue
 from cleaned_dataset
 group by country
 order by Revenue desc
 limit 10 ;
 
 
 ------  # Top Customers --------
 
 select CustomerID,round(sum(TotalPrice),2) as Total_spent
 from cleaned_dataset
 group by CustomerID
 order by Total_spent desc
 limit 10 ;
 
 -------- # Customer Purchase Frequency --------

select CustomerID,count(InvoiceNo)as Total_orders
 from cleaned_dataset
 group by CustomerID
 order by Total_orders desc
 limit 10 ;
 
 
 # ---------------------------------------------------------------------------- #

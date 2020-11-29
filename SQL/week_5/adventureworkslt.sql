/* Write a query to prepare a report containing the following fields. Use lag/lead window functions: 
 * 		- year of order (due date);
 * 		- month of order (due date);
 * 		- product category name;
 * 		- number of orders in current product category;
 * 		- changes in number of orders from previous month or zero if there is no previous data;
 * Customize the results layout so that records are sorted by category and date in chronological order.
*/

select      
    extract(year from duedate), 
    extract(month from duedate), 
    pc."name", 
    count(distinct s.salesorderid), 
    count(distinct s.salesorderid) - coalesce(lag(count(distinct s.salesorderid), 1)  
    over (partition by extract(year from duedate), pc."name" order by extract(month from duedate)),count(distinct s.salesorderid)) 
from salesorderdetail s 
    join salesorderheader sh using (salesorderid) 
    join product p using (productid) 
    join productsubcategory using (productsubcategoryid) 
    join productcategory pc using (productcategoryid) 
group by extract(year from duedate), extract(month from duedate), 
    pc."name"

/* 
 * How much did the company earn selling Water Bottle - 30 oz. in 2013?
 * Use orderdate column to find appropriate orders. The linetotal field contains 
 * information on the amount paid for the product.
 */

select floor(sum(total)) from (
	select salesorderid, orderdate from salesorderheader
	where (
		orderdate >= '2013-01-01 00:00:00'::timestamp 
		and orderdate <  '2014-01-01 00:00:00'::timestamp)
	) as order_id
	join (
		select salesorderid, sum(linetotal) as total from salesorderdetail 
		group by salesorderid 
	) as order_sum
	on order_id.salesorderid = order_sum.salesorderid

	
select floor(sum(d.linetotal))
from product p 
join salesorderdetail d on d.productid = p.productid
join salesorderheader h on h.salesorderid = d.salesorderid
where 
	p."name" = 'Water Bottle - 30 oz.' and 
	h.orderdate >= '2013-01-01 00:00:00'::timestamp and 
	h.orderdate <  '2014-01-01 00:00:00'::timestamp
	
	

	
	
/* 
 * Apply a join operator with derived tables to find a best-selling product by its 
 * amount (summarized linetotal) ordered in each month. Write the name of such a product 
 * that corresponds to the greatest amount sold in January 2012
 */

select mn_amt.year, mn_amt.month, p."name", p.productid 
from 
(select sd.productid,
	sum(sd.linetotal) total,
	extract('y' from sh.duedate) as year, 
	extract('mon' from sh.duedate) as month
from salesorderheader as sh 
	join salesorderdetail as sd on sh.salesorderid = sd.salesorderid 
group by 1, 3, 4) mn_amt 
join 
	product p on p.productid = mn_amt.productid
join
	(select max(total) mx_total, year, month from 
	(select sd.productid,
		sum(sd.linetotal) total,
		extract('y' from sh.duedate) as year, 
		extract('mon' from sh.duedate) as month
	from salesorderheader as sh 
		join salesorderdetail as sd on sh.salesorderid = sd.salesorderid 
	group by 1, 3, 4) as mn_max_from_sum group by 2, 3) mn_max 
		on mn_max.mx_total = mn_amt.total 
			and mn_max.year = mn_amt.year
			and mn_max.month = mn_amt.month
order by 1, 2





/* 
 * Find a company that was an active customer in 2013 and whose monthly ordered 
 * amount was at least 55 000 in 5 months out of 12.
 */

select companyname from 
(select customerid, count(*) from (
select 
	extract(year from s.orderdate) y, 
	extract(month from s.orderdate ) m, 
	s.customerid, 
	sum(s.subtotal) total
from salesorderheader s join customer c on c.customerid = s.customerid 
where extract(year from s.orderdate)=2012 and c.companyname is not null
group by 1, 2, 3
having sum(s.subtotal) >= 55000) as m
group by 1
having count(*)=5) as c1
join customer on c1.customerid = customer.customerid





/* The query should return total value for "totaldue" of orders 
 * shipped to country per day sorted by the date.
 */

select duedate::date, a.countryregioncode, sum(totaldue)
from salesorderheader s
	join address a
		on s.shiptoaddressid=a.addressid
group by duedate, a.countryregioncode
order by duedate




/* 
 * The query should find countries where at least 5 orders worth more than 10 000 
 * were shipped to. Correct errors in the following query to meet the requirements.
 */

select 
	a.countryregioncode country,
	count(distinct 
		case when totaldue < 10000 then s.salesorderid else 0 end) as orders_with_10k
from salesorderheader s
	join address a
		on a.addressid = s.shiptoaddressid
group by
	a.countryregioncode
having count(distinct 
	case when totaldue > 10000 then s.salesorderid else null end) >= 5;





/* 
 * Find monthly revenue compared to yearly income by calculating a share.
 */

select 
	''|| orderyear ||'.'|| to_char(ordermonth, '00') as month,
	data.subtotal / (select sum(subtotal) 
		from salesorderheader s2 
		where 
			extract(year from s2.duedate) = orderyear)
from 
(select 
	sum(s.subtotal) subtotal,
	extract(year from s.duedate) orderyear,
	extract(month from s.duedate) ordermonth
from salesorderheader s
group by 2, 3) data;





/*
 * Write a query to get a report with the following structure:
 * 		1) sales order id,
 * 		2) number of different products in the order,
 * 		3) comma-separated string of unique categories to which ordered products belong 
 * 			(calculate this string by using text aggregation function with distinct before a field).
 * 
 * The query should take into account only orders with multiple items completed in the first quarter 
 * of 2013 and in which all items costed 100 and cheaper (use boolean aggregation to check this condition.
 * Column - linetotal). 
 * 
 * Filter orders by "duedate" in the salesorderheader table.
 */

select 
	sd.salesorderid,
	count(distinct sd.productid) products,
	string_agg(distinct pc.name,', ' ) unique_categories
from salesorderdetail sd
join salesorderheader sh on sd.salesorderid = sh.salesorderid
join product p on p.productid = sd.productid 
join productsubcategory psc on psc.productsubcategoryid = p.productsubcategoryid 
join productcategory pc on pc.productcategoryid = psc.productcategoryid 
where sh.duedate between '2013-01-01' and '2013-03-31'
group by sd.salesorderid
having
	count(*) > 1 and
	bool_and(sd.linetotal <= 100) = true

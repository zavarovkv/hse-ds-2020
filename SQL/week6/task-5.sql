--select * from company_sales cs;
--select * from company_abc ca;
--select * from salesorderdetail sod;
--select * from salesorderheader s;
--truncate table company_sales;





/* Calculate quarterly sales amount before taxes in 2012 and 2013 individually. Fill the company_sales 
 * table using data about orders, companies, and classification results in the respective year. */

insert into company_sales (cid, salesamt, year, quarter_yr, categoryid, ccls, qr)
	select 
		dt.cid,
		dt.salesamt,
		dt.year,
		dt.quarter_yr,
		dt.categoryid,
		cabs.cls as ccls,
		dt.year || '.' || quarter_yr as qr
	from (
		select
			cmp.id as cid,
			sum(sod.linetotal) as salesamt,
			extract(year from soh.orderdate) as year,
			extract (quarter from soh.orderdate) quarter_yr,
			p2.pcid categoryid
		from salesorderdetail sod
		join salesorderheader soh on sod.salesorderid = soh.salesorderid
		join customer cmr on soh.customerid = cmr.customerid
		join company cmp on cmr.companyname = cmp.cname
		join product2 p2 on sod.productid = p2.productid
		where date_part('y', soh.orderdate) in (2012, 2013)
		group by cid, year, quarter_yr, categoryid
	) as dt
	join company_abc cabs on (cabs.cid  = dt.cid and cabs.year = dt.year);

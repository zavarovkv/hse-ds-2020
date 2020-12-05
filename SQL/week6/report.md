### Task No1. Access settings

```sql
grant usage on schema public to planadmin;
grant usage on schema public to planmanager;

grant select on all tables in schema public to planadmin;
grant select on all tables in schema public to planmanager;

grant select, insert, update, delete on plan_data to planadmin;
grant select, insert, update, delete on plan_data to planmanager;

grant select, insert, update, delete on plan_status to planadmin;
grant select, update on plan_status to planmanager;

grant select, insert, update, delete on country_managers to planadmin;
grant select on country_managers to planmanager;

grant select, update on v_plan_edit to planmanager;
grant select on v_plan to planmanager;

create user ivan;
grant planadmin to ivan;

create user sophie;
grant planmanager to sophie;

create user kirill;
grant planmanager to kirill;
```
```sql
insert into country_managers (username, country) values 
('sophie', 'US'), ('sophie', 'CA'), ('kirill', 'FR'), ('kirill', 'GB'), ('kirill', 'DE'), ('kirill', 'AU');
```

### Task No2. product2 & country2 materialized views

```sql
--drop materialized view if exists product2;

--select * from product p;
--select * from productcategory p;
--select * from productsubcategory p;
--select * from address a;


/* The ‘product2’ view should contain the product and its category. */

create materialized view product2 as
    select 
    	pc.productcategoryid	as pcid, 
    	p.productid 			as productid,
    	pc.name 				as pcname, 
    	p.name 					as pname 
    from product p
    join productsubcategory psc on p.productsubcategoryid = psc.productsubcategoryid
    join productcategory pc on psc.productcategoryid = pc.productcategoryid 
with no data;

refresh materialized view product2;





--drop materialized view if exists country2;

--select * from address a2;
--select * from customeraddress c;
--select * from customer c;

/* select distinct a.countryregioncode from customer c 
 * join customeraddress ca on c.customerid = ca.customerid 
 * join address a on ca.addressid = a.addressid
 * where ca.addresstype = 'Main Office';
 */


/* The ‘country2’ view should be filled with unique codes of the countries 
 * where the shops are located (the type of address is Main Office). */

create materialized view country2 as
	select distinct a.countryregioncode from customer c 
	join customeraddress ca on c.customerid = ca.customerid 
	join address a on ca.addressid = a.addressid
	where ca.addresstype = 'Main Office'
with no data;
		
refresh materialized view country2;





/* Allow managers and administrators to read from these views. */

grant select on product2 to planadmin;
grant select on product2 to planmanager;

grant select on country2 to planadmin;
grant select on country2 to planmanager;

```

### Task No3. Loading data into the company table

```sql
--select * from customer c;
--select * from company c;
--select * from customeraddress c;
--select * from address a;


/* In the current database the customer table contains information about two 
 * categories of buyers - individuals and companies. However, we consider only companies. 
 * For the convenience of further development, fill the company table with data.
 * Data from the companyname field should be included in the list of companies. 
 * The country and the city should be taken from the address table. Develop a query to 
 * load the country table. */
 
insert into company (cname, countrycode, city)
	select distinct
		c.companyname as cname, 
		a.countryregioncode as countrycode, 
		a.city as city
	from customer c
	join customeraddress ca on c.customerid = ca.customerid 
	join address a on ca.addressid = a.addressid 
	where ca.addresstype = 'Main Office';
```

### Task No4. Company classification by annual amount of orders

```sql
--select * from salesorderheader s;
--select * from customer c;
--select * from company_abc ca;


insert into company_abc (cid, salestotal, cls, year)
	select
		cid, 
		salestotal,
		case
			when (salestotal * 0.8) >= srt then 'A'
			when (salestotal * 0.95) >= srt then 'B'
			else 'C'
		end as cls,
		year
	from (
		select *, sum(salestotal) over(partition by year order by salestotal desc) as srt
		from (
			select 
				cmp.id as cid,
				sum(soh.subtotal) as salestotal,
				date_part('y', soh.orderdate) as year
			from salesorderheader soh
			join customer ctr on soh.customerid = ctr.customerid 
			join company cmp on cmp.cname = ctr.companyname
			where date_part('y', soh.orderdate) in (2012, 2013)
			group by cid, year
		) as all_data
	) as final_data
	order by cid;
```

### Task No5. Finding quarterly sales amount by company, and product category

```sql
--select * from company_sales cs;
--select * from company_abc ca;
--select * from salesorderdetail sod;
--select * from salesorderheader s;


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
```

### Task No6. Initial data preparation


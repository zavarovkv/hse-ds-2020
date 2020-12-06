--select * from plan_data;
--select * from plan_status;
--select * from country2 c;
--select * from company c;
--select * from productcategory p;
--select * from company_sales cs;





/* Create planning status records (plan_status table) for the selected quarter.
 * The number of records added equals the number of countries in which 
 * customer-companies (shops) are situated. */

insert into plan_status (quarterid, status, modifieddatetime, author, country)
	select 
	 	'2014.1'::text		as quarterid, 
	 	'R'::text 			as status, 
	 	now()				as modifieddatetime,
	 	user 				as author,
	  	countryregioncode 	as country
	from country2;





/* Generate version N of planning data in the plan_data table. Use the calculation 
 * algorithm is described in section 1.4. on the page. */

/*
select 
	countryregioncode 		as country,
	2012		 			as year,
	1						as quarter_yr,
	pc.productcategoryid 	as pcid
from country2
cross join productcategory pc;
*/

/*
select
	avg(cs.salesamt) 	as salesamt_year_early,
	cs.year 			as year,
	cs.quarter_yr 		as quarter_yr,
	cs.categoryid		as pcid,
	cmp.countrycode 	as country
from company_sales cs
join company cmp on cs.cid = cmp.id
where cs.ccls = 'C' and cs.year = 2012 and cs.quarter_yr = 1
group by year, quarter_yr, pcid, country;
*/

insert into plan_data (versionid, country, quarterid, pcid, salesamt)
	select 
		'N'::text 						as versionid,
		country						as country,
		year || '.' || quarter_yr 	as quarterid,
		pcid						as pcid,
		case 
			when (salesamt_year_early + salesamt_year_later) is not null 
				then (salesamt_year_early + salesamt_year_later) / 2 else 0 
			end as salesamt
	from (
		select 
			df.country 								 as country,
			df.year 								 as year,
			df.quarter_yr 							 as quarter_yr,
			df.pcid 								 as pcid,
			avg_sales_year_early.salesamt_year_early as salesamt_year_early,
			avg_sales_year_later.salesamt_year_later as salesamt_year_later
		from (
			select 
				countryregioncode 		as country,
				'2014'::dec  			as year,
				'1'::dec 				as quarter_yr,
				pc.productcategoryid 	as pcid
			from country2
			cross join productcategory pc) as df
		left join (
			select
				avg(cs.salesamt) 	as salesamt_year_early,
				cs.year + 2			as year,
				cs.quarter_yr 		as quarter_yr,
				cs.categoryid		as pcid,
				cmp.countrycode 	as country
			from company_sales cs
			join company cmp on cs.cid = cmp.id
			where cs.ccls != 'C'
			group by year, quarter_yr, pcid, country
		) as avg_sales_year_early
		on (
			avg_sales_year_early.country 	= df.country and 
			avg_sales_year_early.year	 	= df.year and
			avg_sales_year_early.quarter_yr = df.quarter_yr and
			avg_sales_year_early.pcid 		= df.pcid)
		left join (
			select
				avg(cs.salesamt) 	as salesamt_year_later,
				cs.year + 1			as year,
				cs.quarter_yr 		as quarter_yr,
				cs.categoryid		as pcid,
				cmp.countrycode 	as country
			from company_sales cs
			join company cmp on cs.cid = cmp.id
			where cs.ccls != 'C'
			group by year, quarter_yr, pcid, country
		) as avg_sales_year_later
		on (
			avg_sales_year_later.country = df.country and 
			avg_sales_year_later.year = df.year and
			avg_sales_year_later.quarter_yr = df.quarter_yr and
			avg_sales_year_later.pcid = df.pcid)
	) as dt;





/* Copy data from version N into version P in the plan_data table. */

insert into plan_data (versionid, country, quarterid, pcid, salesamt)
	select 
		'P'::text 	as versionid,
		country,
		quarterid,
		pcid,
		salesamt
	from plan_data pd
	where pd.quarterid = '2013.1' and versionid = 'N' and salesamt > 0;

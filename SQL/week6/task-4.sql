--select * from salesorderheader;
--select * from customer;
--select * from company_abc;
--select * from company;
--truncate table company_abc;





/* Split the companies into three groups according to algorithm in 
 * section 1.5 (on page 5) for 2012 and 2013. Fill in the ‘company_abc’ table using SQL query. 
 * All calculations should be done in one query. */

insert into company_abc (cid, salestotal, cls, year)
	select 
		cid, 
		salestotal,
		case 
			when srt <= (yeartotal * 0.80) then 'A'
	    	when srt <= (yeartotal * 0.95) then 'B'
	    	else 'C' end as cls,
	    year
	from (
		select
			cid, 
			salestotal,
			yeartotal,
			df.year,
			sum(salestotal) over (partition by df.year order by salestotal desc) as srt
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
		) as df
		join (
			select
				sum(soh.subtotal) as yeartotal, 
				date_part('y', soh.orderdate) as year 
			    from customer cmr
			    inner join company cmp on cmr.companyname = cmp.cname
			    join salesorderheader soh on cmr.customerid = soh.customerid
			    where date_part('y', soh.orderdate) in (2012, 2013)
			    group by year
		) as ys on df.year = ys.year
	) as df
	order by cid;

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


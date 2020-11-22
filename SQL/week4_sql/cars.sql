/* 
 * Query that calculate number of reservations in each car class.
 */

select count(clsid) nr, c.clsid 
from car c 
    join res ON res.cid = c.cid 
group by c.clsid    





/* 
 * How many different cars did each driver book?
 */

select count(distinct cid) nr, d.did , d."name"
from driver d 
    join res ON res.did = d.did
group by d.did , d."name" order by 2





/* 
 * Calculate the number of days each car was in use.
 */

select car.cid, car.make, sum(res.days) 
from res 
    join car on res.cid = car.cid 
group by car.make, car.cid

select car.cid, car.make, sum(res.days) 
from res, car 
where res.cid = car.cid 
group by car.make, car.cid;  





/* 
 * What is the average number of reservations per car make depending on 
 * month and year the reservation started?
 */
	
select yr, m, c.make,
	avg(res.cnt) as a
	from (
		select cid, count(*) as cnt, extract(year from res.start) yr, 
			extract(month from res."start" ) m 
		from res 
		group by cid, extract(year from res.start), extract(month from res."start") 
		) res , car c  
	group by yr, m, make
	order by yr, m, make




	
/* 
 * You need to prepare an operations report which includes dates and the number of 
 * pick-ups and drop-offs. Write the correct sequence in which these parts should be 
 * included in a single query
 */

select dt as date, count(rstart.*) as picked, count(rfinish.*) as dropped
from
((select start as dt from res)
union (select finish from res)) as dts
left join res as rstart on dts.dt = rstart."start"
left join res as rfinish on dts.dt = rfinish.finish
group by dt;

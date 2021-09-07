ADD JAR /opt/cloudera/parcels/CDH/lib/hive/lib/hive-contrib.jar;
use imansurov;


with 

delay as
(SELECT 1/avg(unix_timestamp(actual_departure) - unix_timestamp(scheduled_departure)) as avg_delay, flight_no
from flights f
join ticket_flights t
on f.flight_id = t.flight_id
where f.status = 'Arrived'
group by flight_no),
pricee as
(
select  min(t.amount) min_pr, f.flight_no
from flights f
left join ticket_flights t
on t.flight_id = f.flight_id
where t.amount is not null
and fare_conditions = 'Economy'
and f.status = 'Arrived'
group by f.flight_no),

priceb as
(
select  min(t.amount) min_pr, f.flight_no
from flights f
left join ticket_flights t
on t.flight_id = f.flight_id
where t.amount is not null
and fare_conditions = 'Business'
and f.status = 'Arrived'
group by f.flight_no),

b_seats as
(select count(*) cnt_b , t.flight_id
from ticket_flights t
join flights f
on f.flight_id = t.flight_id
where fare_conditions = 'Business'
and f.status = 'Arrived'
group by t.flight_id
),

b_seats2 as
(
select max(bs.cnt_b) b_seat, f.flight_no
from flights f
join b_seats bs
on bs.flight_id = f.flight_id
group by f.flight_no
)

select distinct
t1.flight_no, 
t1.avg_delay+(3/10000)*(t2.min_pr + t3.min_pr) + (7/100)*t4.b_seat metric
from delay t1
join pricee t2 
on t1.flight_no = t2.flight_no
join priceb t3
on t1.flight_no = t3.flight_no
join b_seats2 t4
on t1.flight_no = t4.flight_no
order by metric	desc

35622
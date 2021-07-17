-- Read dataset from the files 
-- /data/lsml/3-hive/ticket_flights/ticket_flights.csv 
-- and 
-- /data/lsml/3-hive/flights/flights.csv

ADD JAR /opt/cloudera/parcels/CDH/lib/hive/lib/hive-contrib.jar;
use zavarovkv;

select 
	new_fare_conditions,
	cast(sum(tt.amount) as int) as total_sum,
	count(*) as total_count
from (
	select
		case
    		when t.fare_conditions = 'Comfort' 
    		then 'Economy'
    		else t.fare_conditions
    	end as new_fare_conditions,
    	t.amount
    from flights f
    join ticket_flights t on t.flight_id = f.flight_id
    where 
    	f.flight_no = 'PG0013' and 
    	UNIX_TIMESTAMP(f.scheduled_departure) between UNIX_TIMESTAMP('2017-08-01 00:00:00') and UNIX_TIMESTAMP('2017-09-01 00:00:00')
) as tt 
group by new_fare_conditions;

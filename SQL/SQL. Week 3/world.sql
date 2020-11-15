/* Find out what 10 countries are closest to Argentina as per the following criterion:

C = ABS((GNP% + APC%) - (GNP_Argentina% + APC_Argentina%) )

GNP% - GNP of a country in percent out of to the biggest possible GNP in the world.

APC% - APC of a country in percent out of to the biggest possible APC in the world.

APC – SurfaceArea/Population. It is the area per one citizen.

Hint. Use JOIN operators to reach the desired result. Add condition on population to suppress the division by zero errors.

To apply cross join just write CROSS JOIN like you would write it with usual theta-join but do not add the ON keyword. */


select
	code,
	name,
	abs(gnp_part + apc_part - gnp_part_arg - apc_part_arg) as score
from (
	select 
		code, 
		name,
		nullif(gnp, 0) / (select max(gnp) from country) as gnp_part,
		(surfacearea / nullif(population, 0)) / (select max(surfacearea / nullif(population, 0)) from country) as apc_part
	from country) c1
	cross join (
		select
			nullif(gnp, 0) / (select max(gnp) from country) as gnp_part_arg,
			(surfacearea / nullif(population, 0)) / (select max(surfacearea / nullif(population, 0)) from country) as apc_part_arg
		from country
		where code = 'ARG') c2
where code != 'ARG'
order by score asc
fetch first 10 rows only




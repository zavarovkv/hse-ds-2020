/* 
 * Choose queries that calculate the number of official languages in each continent
 */

select count(distinct cl.language) nr, c.continent from country as c
	join countrylanguage as cl on cl.countrycode = c.code 
group by c.continent, isofficial 
having isofficial = True





/*
 * Write a query to find how many regions each continent has?
 */ 

select c.continent, count(distinct c.region) regions from country c group by c.continent





/* 
 * The following query finds cities with high population (>=8m) which are not capitals. 
 * Rewrite this query without a subquery.
 */

select * from city as ct 
	where not exists (select 1 from country as c where c.capital=ct.id)
and population >= 8000000;


select ct.id, ct.name, ct.countrycode, ct.district, ct.population from city ct
left join country c on ct.id = c.capital
where 	ct.population >= 8000000 and 
		c.code is null
order by ct.id;





/* 
 * You have a query to find cities that have population greater than average city population 
 * in the same country. Rewrite this query with a derived table in FROM. Replace this subquery 
 * with joining in from.
 */

select 
	c.name countryname,
	ct.name cityname,
	ct.population as city_population
from city as ct
	join country as c on c.code = ct.countrycode 
where 
	ct.population > (
		select avg(population) as avg_population  		
        from city  		
        where countrycode = ct.countrycode)
 order by c."name" , ct."name";


select 
	c."name" countryname,
	ct."name" cityname,
	ct.population as city_population
from city as ct 
join country as c on c.code = ct.countrycode 
join (
	select avg(population) avg_population, countrycode 
	from city
	group by countrycode) as avg_population 
on avg_population.countrycode = ct.countrycode 
where 
	ct.population > avg_population.avg_population 
order by c."name", ct."name";

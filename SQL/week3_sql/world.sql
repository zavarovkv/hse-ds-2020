/* Find out what 10 countries are closest to Argentina as per the following criterion:
 * C = ABS((GNP% + APC%) - (GNP_Argentina% + APC_Argentina%) )
 * GNP% - GNP of a country in percent out of to the biggest possible GNP in the world.
 * APC% - APC of a country in percent out of to the biggest possible APC in the world.
 * APC – SurfaceArea/Population. It is the area per one citizen.
 * Hint. Use JOIN operators to reach the desired result. Add condition on population to suppress the division by zero errors.
 * To apply cross join just write CROSS JOIN like you would write it with usual theta-join but do not add the ON keyword. 
 */

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
limit 10





/* Write a query that returns the following table showing data about two governmental
 * forms - 'Republic' and 'Federal republic. The last column shows the others.
 * 		GLE = greatest lifetime expectancy
 * 		LLE = least lifetime expectancy
 * 		X - corresponding calculated value of lifetime expectancy for a particular government form and indicator.
 * The "Others" column should contain results that relate to all government forms except 'Republic' and 'Federal republic'.
 * In this task you should use the following operations to prepare a query:
 * 		union
 * 		order by with limit
 * 		filtering in where
 * Aggregation or window functions should not be used.
 */

select
	'GLE' as Indicator,
	(select max(lifeexpectancy) from country where governmentform = 'Federal Republic') as "Federal Republic",
	(select max(lifeexpectancy) from country where governmentform = 'Republic') as "Republic",
	(select max(lifeexpectancy) from country where governmentform not in('Republic', 'Federal Republic')) as "Others"
union 
select 
	'LLE' as Indicator,
	(select min(lifeexpectancy) from country where governmentform = 'Federal Republic') as "Federal Republic",
	(select min(lifeexpectancy) from country where governmentform = 'Republic') as "Republic",
	(select min(lifeexpectancy) from country where governmentform not in('Republic', 'Federal Republic')) as "Others"

	

	
	
/* Write a query to "world" database to find a country with a gnp under 1% of the greatest GNP in the world. 
 * The records should be sorted by continent in alphabetical order and by gnp from greatest to lowest 
 */

select * from country 
where gnp / (select max(gnp) from country) < 0.01
order by continent asc, gnp desc





/* Write a SQL query to find out which non-capital city has the least population in North America? 
 * Type the city name into the text box like it was shown in the resultset.
 */

select * from (
	select * from city) c1
inner join (
	select code, capital from country
	where region = 'North America') c2
on c1.countrycode = c2.code
	and id != capital
order by population asc limit 1





/* Write a query to "world" database to find country with surface area under 200 000 wich has
 * the greatest number of people who speak English. Type the country's name into the text box.
 */

select 
	code,
	name,
	population * percentage / 100 as score
from (
	select code, name, population, surfacearea from country c where surfacearea < 200000) as c1
inner join (
	select * from countrylanguage where "language" = 'English') as c2
on c1.code = c2.countrycode
order by score desc limit 1





/* What country has more than 4 words in its local name and has area per capita > 0.02? 
 * Write the country code into the text prompt.
*/

select code, name from (
	select code, name, surfacearea / nullif(population, 0) as capita
	from country 
	where array_length(regexp_split_to_array(localname, '\s'),1) > 4) as c1
where capita > 0.02





/* Write a SQL query to find out which world’s capital has the least population? 
 * Type the city name into the text box.
 */

select name, population from (
	select capital from country) as c1
inner join (
	select * from city) as c2
on c1.capital = c2.id
order by population asc limit 1




/* What official languages do people speak in countries with the capital's population 
 * exceeding 80% of the most populated city in the world?
 * Write a SQL query to present the result in the following format:
 * 		continent - Continent name
 * 		country - Country name
 * 		lngname - Language name
 * 		lngcode - First three letters of language name in upper case (language code)
 * 		speakersnr - Number of speakers
 * The output should be sorted by continent and lngcode.
 * Write the value from lngcode column of the 3rd row into the text prompt.
 */

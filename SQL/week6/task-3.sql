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

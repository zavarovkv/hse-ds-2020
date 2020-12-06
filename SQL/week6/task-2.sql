--drop materialized view if exists product2;
--select * from product p;
--select * from productcategory p;
--select * from productsubcategory p;
--select * from address a;





/* The ‘product2’ view should contain the product and its category. */

create materialized view product2 as
    select 
    	pc.productcategoryid	as pcid, 
    	p.productid 			as productid,
    	pc.name 				as pcname, 
    	p.name 					as pname 
    from product p
    join productsubcategory psc on p.productsubcategoryid = psc.productsubcategoryid
    join productcategory pc on psc.productcategoryid = pc.productcategoryid 
with no data;

refresh materialized view product2;





--drop materialized view if exists country2;
--select * from address a2;
--select * from customeraddress c;
--select * from customer c;

/* select distinct a.countryregioncode from customer c 
 * join customeraddress ca on c.customerid = ca.customerid 
 * join address a on ca.addressid = a.addressid
 * where ca.addresstype = 'Main Office';
 */

/* The ‘country2’ view should be filled with unique codes of the countries 
 * where the shops are located (the type of address is Main Office). */

create materialized view country2 as
	select distinct a.countryregioncode from customer c 
	join customeraddress ca on c.customerid = ca.customerid 
	join address a on ca.addressid = a.addressid
	where ca.addresstype = 'Main Office'
with no data;
		
refresh materialized view country2;





/* Allow managers and administrators to read from these views. */

grant select on product2 to planadmin;
grant select on product2 to planmanager;

grant select on country2 to planadmin;
grant select on country2 to planmanager;

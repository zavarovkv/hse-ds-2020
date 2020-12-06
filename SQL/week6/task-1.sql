/* Set up permissions for roles
 * Create three users: Administrator (ivan), Managers: (sophie, kirill)
 * Manager sophie has access to data of US and CA countries. 
 * Manager kirill works with sales data in FR, GB, DE, AU countries. 
 * Put this information in the ‘country_managers’ table, which stores data about 
 * the anchoring of managers for certain countries.
 */

grant usage on schema public to planadmin;
grant usage on schema public to planmanager;

grant select on all tables in schema public to planadmin;
grant select on all tables in schema public to planmanager;

grant select, insert, update, delete on plan_data to planadmin;
grant select, insert, update, delete on plan_data to planmanager;

grant select, insert, update, delete on plan_status to planadmin;
grant select, update on plan_status to planmanager;

grant select, insert, update, delete on country_managers to planadmin;
grant select on country_managers to planmanager;

grant select, update on v_plan_edit to planmanager;
grant select on v_plan to planmanager;

drop user ivan;
create user ivan with password 'ivan_pwd';
grant planadmin to ivan;

create user sophie;
grant planmanager to sophie;


create user kirill;
grant planmanager to kirill;

insert into country_managers (username, country) values 
('sophie', 'US'), ('sophie', 'CA'), ('kirill', 'FR'), ('kirill', 'GB'), ('kirill', 'DE'), ('kirill', 'AU');

--select * from plan_status ps;
--select * from plan_data;
--select * from country_managers cm;
--select * from v_plan vp;
--select * from v_plan_edit vpe;
--select * from planadmin;
--select current_user; 


/* update plan_status 
set status = 'R', author = 'ivan'; */

/* set_lock(year, quarter, user, pwd), which will change status from R to L 
 * for data slices, that are associated with the target quarter and year, 
 * and connected to the current user in the country_managers configuration table.
 * To obtain the name of the current user, use current_user. Also write 
 * a timestamp of modification to the modifieddatetime field. */

update plan_status 
set 
	status = 'L',
	modifieddatetime = current_timestamp,
	author = current_user
where
	quarterid = '2014' || '.' || '1' and 
	country in (
		select country from country_managers 
		where username = current_user 
	) and 
	status = 'R';





/* remove_lock(year, quarter, user, pwd) function, that will change the planning 
 * data status from L to R. associated with the current user through the 
 * country_managers table. Write a change time stamp in the modifieddatetime field. */

update plan_status 
set 
	status = 'R',
	modifieddatetime = current_timestamp,
	author =current_user
where
	quarterid = '2014' || '.' || '1' and 
	country in (
		select country from country_managers 
		where username = current_user 
	) and 
	status = 'L';

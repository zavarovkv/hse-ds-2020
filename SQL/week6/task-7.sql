select * from plan_status ps;
select * from country_managers cm;
select * from v_plan vp;
select * from v_plan_edit vpe;


/* set_lock(year, quarter, user, pwd), which will change status from R to L 
 * for data slices, that are associated with the target quarter and year, 
 * and connected to the current user in the country_managers configuration table.
 * To obtain the name of the current user, use current_user. Also write 
 * a timestamp of modification to the modifieddatetime field. */


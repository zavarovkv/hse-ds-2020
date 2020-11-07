drop table if exists employeezones;
drop table if exists participant;
drop table if exists employee;
drop table if exists zone;
drop sequence if exists seq2;



create sequence seq2
	increment	1
	minvalue 	1
  	maxvalue	9223372036854775807
  	start		1
  	cache 		1;
  
  
  
create table if not exists zone(
	id				int not null default nextval('seq2') primary key,
	
	name				varchar(50) not null,
	designation			varchar(50) not null check (designation in ('food', 'concert', 'music', 'info')),
	opening_date			date not null,
	closing_date			date not null
);



create table if not exists employee(
	id				int not null default nextval('seq2') primary key,
	
	name				varchar(50) not null,
	surname				varchar(50) not null,
	date_of_birth			date not null,
	gender				varchar(1) 	not null check (gender in ('M', 'F')),
	status				varchar(50) not null check (status in ('working', 'vacation', 'quit')),
	salary				int not null,
	description			varchar(128)
);



create table if not exists participant(
	id				int not null default nextval('seq2') primary key,
	zone_id				int not null,
	
	name				varchar(50) not null,
	surname				varchar(50) not null,
	date_of_birth			date not null,
	gender				varchar(1) 	not null check (gender in ('M', 'F')),
	
	constraint fk_zone
		foreign key(zone_id) 
			references zone(id)
);



create table if not exists employeezones(
	emp_id				int not null,
	zone_id				int not null,
	
	employee_started		date not null,
	employee_ended			date,
	
	constraint pk_ez primary key(emp_id, zone_id)
);

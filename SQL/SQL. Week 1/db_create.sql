drop table if exists reservation;
drop table if exists room;
drop table if exists guest;
drop table if exists building;

drop sequence if exists seq;



create sequence seq
	increment	1
	minvalue 	1
  	maxvalue	9223372036854775807
  	start		1
  	cache 		1;
 
 
 
create table if not exists guest(
	id 				int not null DEFAULT nextval('seq') primary key,
	
	first_name			varchar(50) not null,
	last_name			varchar(50) not null,
	document_type		varchar(50) not null,
	document_number		varchar(50) not null,
	gender				varchar(1) 	not null check (gender in ('M', 'F'))
);

insert into guest(first_name, last_name, document_type, document_number, gender) 
	values('Konstantin', 'Zavarov', 'passport', '67123123', 'M');

insert into guest(first_name, last_name, document_type, document_number, gender) 
	values('Babicheva', 'Elizaveta', 'passport', '67546354', 'F');

insert into guest(first_name, last_name, document_type, document_number, gender) 
	values('Leonid', 'Volkob', 'passport', '67765443', 'M');

insert into guest(first_name, last_name, document_type, document_number, gender) 
	values('Nastya', 'Cvecinitskyya', 'passport', '67654433', 'F');



create table if not exists building(
	id 				int not null DEFAULT nextval('seq') primary key,
	
	building_name 		varchar(50) not null unique,
	latitude 			varchar(50) not null,
	longitude 			varchar(50) not null,
	number_of_rooms 	int not null check(number_of_rooms > 0),
	number_of_floors 	int not null check(number_of_floors > 0),
	description 		varchar(128)
);

insert into building(building_name, latitude, longitude, number_of_rooms, number_of_floors, description) 
	values('1A', '111', '222', 2, 1, 'best building');

insert into building(building_name, latitude, longitude, number_of_rooms, number_of_floors) 
	values('5A', '112', '223', 1, 1);



create table if not exists room(
	id 					int not null DEFAULT nextval('seq') primary key,
	building_id 		int not null,
		
	square 				int not null check(square > 0),
	number_of_beds 		int not null check(number_of_beds > 0),
	number_of_bath 		int not null check(number_of_bath > 0),
	max_peron 			int not null check(max_peron > 0),
	number_of_floor 	int not null check (number_of_floor > 0),
	
	constraint fk_building
		foreign key(building_id) 
			references building(id)
);

insert into room(building_id, square, number_of_beds, number_of_bath, max_peron, number_of_floor)
	values(5, 20, 2, 1, 2, 1);
	
insert into room(building_id, square, number_of_beds, number_of_bath, max_peron, number_of_floor)
	values(5, 25, 2, 1, 2, 2);

insert into room(building_id, square, number_of_beds, number_of_bath, max_peron, number_of_floor)
	values(5, 40, 4, 2, 4, 2);

insert into room(building_id, square, number_of_beds, number_of_bath, max_peron, number_of_floor)
	values(6, 15, 2, 1, 2, 1);

insert into room(building_id, square, number_of_beds, number_of_bath, max_peron, number_of_floor)
	values(6, 17, 2, 1, 2, 1);



create table if not exists reservation(
	id 					int not null DEFAULT nextval('seq') primary key,
	guest_id 			int not null,
	room_id 			int not null,
	
	start_period 		date not null,
	end_period 			date not null,
	duration_in_days 	int null check(duration_in_days > 0),
	board_type 			varchar(2),
	
	constraint fk_guest
		foreign key(guest_id) 
			references guest(id),
			
	constraint fk_room
		foreign key(room_id)
			references room(id),
	
	constraint cn_period 
		check (end_period >= start_period) 
);

insert into reservation(guest_id, room_id, start_period, end_period, duration_in_days, board_type)
	values(1, 7, '01-01-2020', '02-01-2020', 1, 'no');

insert into reservation(guest_id, room_id, start_period, end_period, duration_in_days, board_type)
	values(2, 8, '03-01-2020', '05-01-2020', 2, 'BB');

insert into reservation(guest_id, room_id, start_period, end_period, duration_in_days, board_type)
	values(3, 9, '04-01-2020', '05-01-2020', 1, 'HB');

insert into reservation(guest_id, room_id, start_period, end_period, duration_in_days, board_type)
	values(3, 7, '10-01-2020', '11-01-2020', 1, 'no');

insert into reservation(guest_id, room_id, start_period, end_period, duration_in_days, board_type)
	values(4, 8, '11-02-2020', '12-02-2020', 1, 'HB');
	
insert into reservation(guest_id, room_id, start_period, end_period, duration_in_days, board_type)
	values(4, 8, '01-03-2020', '03-03-2020', 2, 'no');


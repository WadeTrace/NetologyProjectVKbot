create table if not exists users
(
	user_id serial primary key, 
	vk_id VARCHAR(60),
	count_of_req integer,
	stage_of_req integer,
	last_req VARCHAR(60)
); 


create table if not exists people
(
	people_id serial primary key, 
	vk_id VARCHAR(60) unique
); 

create table if not exists user_people
(
	user_id integer references users(user_id),
	people_id integer references people(people_id),
	constraint p primary key (user_id, people_id)
);

create table if not exists favorite
(
	user_id integer references users(user_id),
	people_id integer references people(people_id),
	constraint pk primary key (user_id, people_id)
);


create table if not exists params
(
	id serial primary key,
	user_id integer references users(user_id),
	city VARCHAR(60),
	sex VARCHAR(60),
	min_age integer,
	max_age integer
)
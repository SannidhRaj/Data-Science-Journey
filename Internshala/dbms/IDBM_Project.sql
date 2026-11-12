-- Active: 1779098120208@@127.0.0.1@3306
-- creating and using the database
create database INDB;
use INDB;

create table movie 
(
id varchar(10) not null,
title varchar(100) default null,
year int default null,
date_published date default null,
duration int,
country varchar(250),
world_wide_gross_income varchar(30),
language varchar(200),
production_company varchar(200),
primary key(id)
);
describe movie;
alter table movie
modify date_published varchar(20);
truncate table movie;

create table genre
(
movie_id varchar(20),
genre varchar(200),
primary key(movie_id)
);
describe genre;

create table director_mapping
(
movie_id varchar(20),
name_id varchar(50),
primary key(movie_id,name_id)
);
describe director_mapping;

create table role_mapping
(
movie_id varchar(50) not null,
name_id varchar(50) not null,
category varchar(20),
primary key(movie_id,name_id)
);
describe role_mapping;

create table names
(
id varchar(50) not null,
name varchar(50) not null,
date_of_birth date not null,
known_for_movies varchar(100) not null,
primary key(id)
);
describe names;

create table ratings
(
movie_id varchar(50) not null,
avg_rating float not null,
total_votes int not null,
median_rating int not null,
primary key(movie_id)
);
describe ratings;

show tables;

-- inserting data
insert into movie
values('tt0111161','The Shawshank Redemption','1994','14/10/1994','142','USA','$ 16,000,000','English','Castle Rock Entertainment');

insert into genre
values('tt0111161','Drama');

insert into names
values('nm0000151'	,'Richard Gere	','1949-08-31',	'Indiana Jones and the Last Crusade');

insert into director_mapping
values('tt0111161'	,'nm0001104');

insert into ratings
values('tt0111161',	'9.3','2700000','9');

insert into role_mapping
values('tt0111161','nm0000102','actor');

show tables;
select*from names;
desc movie;

-- fetch the data from table
use indb;
select id,name from names;

-- joing the table so get the names hows rating excatly 8
select name,avg_rating
from ratings
join role_mapping on ratings.movie_id=role_mapping.movie_id
join names on role_mapping.name_id=names.id
where ratings.avg_rating>=8
and role_mapping.category='actor';


-- find out no. of rows 
select count(known_for_movies) from names;

SELECT *
FROM names
WHERE known_for_movies IS NOT NULL
AND TRIM(known_for_movies) <> ''; 

SELECT count(*)
FROM names
WHERE known_for_movies IS NOT NULL
AND TRIM(known_for_movies) <> '';



USE INDB
SHOW TABLES
SELECT * FROM movie

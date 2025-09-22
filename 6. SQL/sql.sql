select name from country where name like "G%";
select name from country where name like "%fa%";
select name from country where name like "i%a";

select*from country;
select name from country order by name desc;

select name from country where population>10000000;
select name from country where population>1000000 and population<5000000;

select name from country where name like "A%" and population>1000000;
select name from country where 'city'="bhopal" or 'city'="goa" or 'city'="russia";

select name from country order by surfacearea desc;
select name from country order by surfacearea desc limit 3,8;

select continent from country;
select distinct continent from country;   -- only one time it is use  
select distinct continet from country where 'city'="bhopal" and population<1000000 and name like"G%";

select avg(population) from country;
select count(name) from country where Continent="ASIA";
select min(population) from country;
select max(population) from country;

select continent, sum(population) from country group by continent;
select continent, count(*) from country group by continent;
select region, sum(surfacearea) from country group by region;
select region, avg(surfacearea) from country group by region;
select region, sum(surfacearea) from country group by region;
select continent, count(*) from country  where name like "A%" group by continent;
select continent, count(*) from country  where name like "A%" group by continent having count(*)>=2;
select continent, count(*) from country  where population=10000000 group by continent having count(*)>=2 order by count(*) desc;

select continent,count(*) from country group by continent;

select name from country where indepyear=1947;
select name from country where name like"ind%";








drop table if exists student;

create table students(
id int,
name varchar(32),
branch char(5),
age int,
city varchar(20),
primary key (id));

insert into students values (1, "shalu", "cs", 19, "bhopal");
insert into students values (2, "angel", "cse", 18, "indore");
insert into students values (3, "shalini", "it", 20, "bhopal");
insert into students values (4, "saloni", "ai", 19, "indore");
insert into students values (5, "junnu", "cse", 17, "goa");

 delete from students where id=5; -- delete only one row from table
 drop table students;  -- delete table from databse
--  truncate --  complete data delete but table remain same
 
select * from students;





create table family(
id int primary key,
name varchar(20),
relation varchar(25),
city varchar(15),
rating int
);

insert into family values
(1,"vicky","brother", "spj",8),
(2,"shalu","sister", "spj",6),
(3,"mahesh","father", "spj",10),
(4,"kanchan","mother", "spj",10),
(5,"deepa","cousin", "spj",7);

select *from family;

insert into family values
(6,"alok","brother", "spj",5),
(7,"saloni","sister", "spj",5),
(8,"ram","uncle", "spj",10),
(9,"junnu","aunty", "spj",10),
(10,"rita","cousin", "spj",8);

select name from family where rating=(select max(rating) from family);

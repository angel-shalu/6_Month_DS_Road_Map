CREATE DATABASE customer;
use customer;
CREATE TABLE customer (
    customer_id INT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    phone_number VARCHAR(15),
    address TEXT,
    created_at DATE
);

select*from customer;
describe customer;

INSERT INTO customer (customer_id, first_name, last_name, email, phone_number, address, created_at)
VALUES (1, 'Shalini', 'Kumari', 'shalini@example.com', '9876543210', 'Bhopal, MP', '2025-08-01');
select*from customer;

INSERT INTO customer (customer_id, first_name, last_name, email, phone_number, address, created_at)
VALUES
  (22, 'Suman', 'Raj', 'suman@gmail.com', '9876745626', 'Bihar', '2004-10-22'),
  (25, 'Amit', 'Verma', 'amitv@example.com', '9876123456', 'Delhi', '1999-05-14'),
  (96, 'Saloni', 'Sharma', 'saloni@example.com', '9812345678', 'Mumbai', '2001-12-01'),
  (11, 'Angel', 'Raj', 'angel@example.com', '981234758528', 'Bengaluru', '2003-12-01');

SELECT * FROM customer;
DELETE FROM customer WHERE customer_id IN (7, 8, 9);

select*from customer;
update customer set email='shalini7@gmail.com' where customer_id=1;

select*from customer;
update customer set last_name='Raj' where customer_id=1;

select*from customer;
ALTER TABLE customer ADD salary INT;

select*from customer;
select customer_id, first_name from customer;

select*from customer;
UPDATE customer SET salary = 50000 WHERE customer_id = 1;

SELECT*FROM customer;
UPDATE customer SET salary = 8000 WHERE customer_id = 11;

select*from customer;
UPDATE customer
SET salary = CASE customer_id
    WHEN 22 THEN 8000
    WHEN 25 THEN 9000
    WHEN 96 THEN 7500
    ELSE salary
END
WHERE customer_id IN (22, 25, 96);

select*from customer;
UPDATE customer SET address = 'Chennai' WHERE customer_id = 96;

SELECT*FROM customer;
ALTER TABLE customer RENAME COLUMN created_at TO date;

select*from customer;
update customer set address ="Bhopal" where customer_id=1;

select*from customer;
use customer;
INSERT INTO customer (customer_id, first_name, last_name, email, phone_number, address, date)
VALUES
  (20, 'Shalu', 'Raj', 'shalu@gmail.com', '9876945626', 'Bihar', '2004-10-12'),
  (21, 'Aman', 'Singh', 'amanv@example.com', '97806123456', 'Delhi', '1997-05-14'),
  (91, 'Soni', 'Sharma', 'soni8@example.com', '9812340078', 'Mumbai', '2005-12-01'),
  (17, 'Annu', 'Raj', 'annu77@example.com', '981234765428', 'Bengaluru', '2006-12-01');
  
select*from customer;
alter table customer add salary int;

select*from customer;
UPDATE customer
SET salary = CASE customer_id
    WHEN 21 THEN 45000
    WHEN 17 THEN 6000
    WHEN 20 THEN 7800
    WHEN 25 THEN 3500
    WHEN 91 THEN 4500
    ELSE salary
END
WHERE customer_id IN (21, 20, 91, 25,17);

select*from customer;
update customer set address='Mumbai' where customer_id=21;

select*from customer;
SELECT email, COUNT(*) AS count FROM customer GROUP BY email HAVING COUNT(*) > 1;

select*from customer;
SELECT salary, COUNT(*) AS count FROM customer GROUP BY salary HAVING COUNT(*) > 8000;

select*from customer;
SELECT *, COUNT(*) AS count FROM customer GROUP BY customer_id, first_name, last_name, email, phone_number, address, date HAVING COUNT(*) > 1;

select*from customer;
select date, last_name, count(*) as count from customer group by date, last_name having count(*)<8000;

select*from customer;
select max(salary) as SecondHighestSalary from customer where salary < (select max(salary) from customer);

select*from customer;
select max(salary) as HighestSalary from customer where salary < (select max(salary) from customer);












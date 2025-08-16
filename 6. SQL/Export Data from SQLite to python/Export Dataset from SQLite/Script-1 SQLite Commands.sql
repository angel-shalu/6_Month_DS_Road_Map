select*from dataset_1;

--Retrieves the first 10 rows from the table dataset_1, including all columns.
select*from dataset_1 limit 10;

--Retrieves all unique passenger names or IDs from the column passanger in the table dataset_1.
select distinct passanger from dataset_1;

--Retrieves only the weather and temperature columns for all rows in the table dataset_1.
SELECT weather, temperature From dataset_1;

--Returns all columns for only those rows where the destination is "Home"
select*from dataset_1 where destination ="Home";

-- Selects all rows from dataset_1 and sorts them in ascending order based on the coupon column.
select*from dataset_1 order by coupon;

--Selects the destination column from dataset_1 and renames it as Destination in the output.
select destination as Destination from dataset_1;

-- Groups the data by weather and returns the average temperature for each weather type
select weather, avg(temperature) as avg_tem from dataset_1 group by weather;

-- Groups the data by weather and returns the count of non-null temperature values for each weather type.
select weather, count(temperature) as count_temp from dataset_1 group by weather;

--Returns the number of unique temperatures recorded for each weather type.
SELECT weather , COUNT(DISTINCT temperature) AS count_distinct_temp FROM dataset_1 GROUP BY weather;

--Returns the total sum of temperature for each weather type.
select weather, sum(temperature) as sum_temp from dataset_1 group by weather;

--Returns the minimum (lowest) temperature for each weather type.
select weather, min(temperature) as min_temp from dataset_1 group by weather;

--Returns the maximum (highest) temperature for each weather type.
select weather, max(temperature) as max_temp from dataset_1 group by weather;

-- Groups the rows by occupation and only returns the group where occupation is "Student".
--📝 NOTE: Normally, HAVING is used with aggregate functions (like COUNT, AVG). This can be replaced with a WHERE clause in this case.
select occupation from dataset_1 group by occupation having occupation="Student";

--Combines all rows from dataset_1 and table_to_union without duplicates (UNION), then returns unique destination values from the merged result.
select distinct destination from(select*from dataset_1 union select*from table_to_union);

--Performs an inner join between dataset_1 and table_to_join based on matching time values.
-- Returns destination, time from a (dataset_1), and part_of_day from b
select a.destination, a.time, b.part_of_day from dataset_1 a inner join table_to_join b on a.time=b.time;

-- Filters rows where passanger = 'Alone', then returns only the destination and passanger columns.
select destination, passanger from (select*from dataset_1 where passanger='Alone');

--Selects all rows where the weather starts with "Sun", e.g., "Sunny", "Sunlight", etc.
select*from dataset_1 where weather like'Sun%';

--Returns unique temperatures between 29 and 75 inclusive from the dataset.
select distinct temperature from dataset_1 where temperature between 29 and 75;

--Returns rows where the occupation is either "Sale & Related" or "Management".
select occupation from dataset_1 where occupation in('Sale & Related','Management');
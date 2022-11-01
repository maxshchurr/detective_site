-- some of the queries


-- to get an income for orders of a specific type
select distinct (tor.type), sum(tor.price * o.rate) over (partition by tor.type)
from orders o left join type_of_order tor on o.type_of_order_id = tor.id
group by tor.type, tor.price, o.rate
having tor.type = 'Сбор информации' and o.status in ('Closed', 'Payed', 'In work')


-- get quantity of orders which were handle by managers this month
select distinct (e.id), e.first_name , ' ' || e.surname as "Managers name", count(o.id) over (partition by o.manager_id)
from orders o left join agency_employees e on o.manager_id = e.id 
where date_part('year', o.created_at) = date_part('year', CURRENT_DATE)
and date_part('month', o.created_at) = date_part('month', (select current_date))


-- get quantity of orders which were handle by managers this month and are already finished (have o.status = 'Closed')
select distinct (e.id), e.first_name , ' ' || e.surname as "Managers name", count(o.id) over (partition by o.manager_id)
from orders o left join agency_employees e on o.manager_id = e.id
where o.status = 'Closed' and date_part('year', o.created_at) = date_part('year', CURRENT_DATE)
and date_part('month', o.created_at) = date_part('month', (select current_date))


-- count quantity of orders which were handle by detectives within a certain range of time
SELECT COUNT(o.id), e.first_name || ' ' || e.surname AS "Name"
FROM orders o right JOIN agency_employees e ON o.detective_id = e.id
WHERE o.created_at BETWEEN CURRENT_DATE::date-interval '14 days' AND CURRENT_DATE and e.position = ‘Detective’
GROUP BY e.first_name, e.surname


-- get information about order
SELECT o.created_at, o.status, tor.type, sum(o.rate * tor.price), 
CASE WHEN o.manager_id is not null THEN concat(man.surname, ' ', man.first_name) ELSE '-'
END
AS manager,
CASE WHEN o.detective_id is not null THEN concat(det.surname, ' ', det.first_name) ELSE '-'
END
AS detective
	FROM orders o
	LEFT JOIN agency_employees man ON man.id=o.manager_id
	LEFT JOIN type_of_order tor ON tor.id=o.type_of_order_id
	LEFT JOIN agency_employees det ON det.id=o.detective_id
	WHERE o.manager_id =1 
	group by o.created_at, tor.type, o.status, o.manager_id,
	o.detective_id, man.surname, man.first_name, det.surname, det.first_name
	
	
-- reject clients order
UPDATE orders SET status='Rejected by manager', manager_id=1
WHERE id = 100 and status=’In process’


-- create task for detectives assistant
INSERT INTO tasks (id, task_date, task_description, employees_id, orders_id) 
values (15, 'new task', (select e.id from agency_employees e 
						 where e.id=your_id and chief_id=your_id), (select o.id from orders o where o.id=100))
						 
						 
-- view assistants comment on the task 
select  a_c.assistant_comments as "assistant comment", a_c.created_at as "Date", e.first_name || ' ' 
|| e.surname as "employees name" 
from assistant_comments a_c JOIN agency_employees e ON a_c.employees_id=e.id
WHERE task_id=1 and e.chief_id = your_id


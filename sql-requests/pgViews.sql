-- Views


create or replace view all_client_info 
as
select  cl.full_name as "Имя клиента", cl.tel_number as "Номер телефона", u.email as "Почта"
from clients cl JOIN auth_user u ON cl.user_id=u.id



create or replace view all_employees_info 
as
select  e1.first_name || ' ' ||  e1.surname as "Имя сотурдника", e1.position as "Должнолсть" , e1.status as "Статус", 
e1.tel_number as "Номер телефона", u.email as "Почта", e.first_name || ' ' ||  e.surname as "Имя chief"
from agency_employees e JOIN auth_user u ON e.user_id=u.id
RIGHT JOIN agency_employees e1 ON e.id=e1.chief_id
where e.id = e1.chief_id



CREATE OR REPLACE VIEW "accumulative_sum" AS 
SELECT  DISTINCT ON(date_part('month', o.created_at)) 
	   date_part('YEAR', o.created_at) AS "YEAR",
       date_part('month', o.created_at) AS "MONTH",
	   SUM(o.rate * otype.price) over (partition by date_part('month', o.created_at)) SumForMonth,
	   SUM(o.rate * otype.price) OVER (ORDER BY o.created_at ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) SUMMARY
		
FROM orders o JOIN type_of_order otype ON o.type_of_order_id = otype.id 			  
WHERE date_part('year', o.created_at) = date_part('year', CURRENT_DATE) and o.status in ('Closed', 'In work')
GROUP BY  date_part('month', o.created_at),
o.id,otype.price
ORDER BY  date_part('month', o.created_at),SUMMARY DESC;

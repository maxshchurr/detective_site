-- Functions


CREATE OR REPLACE FUNCTION count_quantity_of_rejected_orders(start_date date, end_date date)
RETURNS TABLE
(	
"quantity of rejected orders" bigint
)
AS 
$$
BEGIN
RETURN QUERY
	SELECT count(o.id)
	FROM orders o
	where o.status='Rejected by client' and o.created_at between start_date and end_date;
END
$$  language plpgsql;



CREATE FUNCTION count_quantity_of_new_orders(start_date date, end_date date)
RETURNS TABLE
(	
"quantity of orders" bigint
)
AS 
$$
BEGIN
RETURN QUERY
	SELECT count(o.id)
	FROM orders o
	where o.created_at between start_date and end_date;

END
$$  language plpgsql;


-- potential income, to count income use o.status in ('Payed', 'In work', 'Closed')
CREATE OR REPLACE FUNCTION count_income(start_date date, end_date date)
RETURNS TABLE
(	
"income" int
)
AS 
$$
BEGIN
RETURN QUERY
	SELECT sum(o.rate * type_of_order.price)
	FROM orders o LEFT JOIN type_of_order ON o.type_of_order_id=type_of_order.id
	where o.created_at between start_date and end_date;
END
$$  language plpgsql;

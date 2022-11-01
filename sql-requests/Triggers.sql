-- Triggers


CREATE TRIGGER change_order_status_to_closed_before_insert_report_trg
BEFORE INSERT ON report
FOR EACH ROW
EXECUTE PROCEDURE change_order_status_to_closed_before_insert_report_func();

CREATE FUNCTION change_order_status_to_closed_before_insert_report_func()
RETURNS TRIGGER AS 
$$
BEGIN
	UPDATE orders
	SET status = 'Closed'
	WHERE orders.id = NEW.orders_id and orders.status='Payed';
    RETURN NEW;
END
$$ language plpgsql




CREATE TRIGGER check_assistant_status_after_new_task_trg
AFTER INSERT ON tasks  
FOR EACH ROW 
EXECUTE PROCEDURE check_assistant_status_after_new_task();

CREATE OR REPLACE FUNCTION check_assistant_status_after_new_task() 
RETURNS TRIGGER 
AS $$
BEGIN
	update agency_employees
	set status =
	case status when 'Available' then 'Busy'
		  		when 'Busy' then 'Busy'
	end
	where agency_employees.id=new.employees_id;	
RETURN NEW;
END
$$ LANGUAGE plpgsql;



CREATE TRIGGER check_assistant_status_before_delete_task_trg
BEFORE DELETE ON tasks  
FOR EACH ROW 
EXECUTE PROCEDURE check_assistant_status_before_delete_task_func();

CREATE OR REPLACE FUNCTION check_assistant_status_before_delete_task_func() 
RETURNS TRIGGER 
AS $$
declare
 quantity_of_tasks smallint;
BEGIN

  	select count(ta.id)
  	into quantity_of_tasks
  	from tasks ta
  	where ta.employees_id=old.employees_id;
   
	update agency_employees
    set status=
	case  when quantity_of_tasks = 1 then 'Available'
				   else 'Busy'
	end
	
  where id=old.employees_id;	
  RETURN OLD;
END
$$ LANGUAGE plpgsql;



CREATE TRIGGER check_det_and_man_status_after_insert_report_trg
AFTER INSERT ON report  
FOR EACH ROW 
EXECUTE PROCEDURE check_det_and_man_status_after_insert_report_func();
CREATE OR REPLACE FUNCTION check_det_and_man_status_after_insert_report_func() 
RETURNS TRIGGER 
AS $$
declare
 quantity_of_active_orders int;
 temp_detective_id bigint;
 temp_manager_id bigint;

BEGIN
  select o.detective_id, o.manager_id
  into temp_detective_id, temp_manager_id
  from orders o
  where o.id=new.orders_id
  group by o.detective_id, o.manager_id;
   
   	select count(o.id)
   	into quantity_of_active_orders
   	from orders o
   	where o.detective_id = temp_detective_id 
   	and o.manager_id = temp_manager_id and o.status!='Closed';
   
	
   	update agency_employees
   	set status=case  when quantity_of_active_orders = 0 then 'Available'
				    								   else 'Busy'
   	end
	where id = temp_manager_id;
	
	update agency_employees
    set status=case  when quantity_of_active_orders = 0 then 'Available'
				   else 'Busy'
 	end
	where id = temp_detective_id;


RETURN NEW;
END
$$ LANGUAGE plpgsql;







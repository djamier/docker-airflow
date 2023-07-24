select
    order_source
    , sum(price) as total_sales
from fact_orders
where
    order_date between {start_date_str}::timestamp and {end_date_str}::timestamp
    and order_status = 'Completed'
group by 1 

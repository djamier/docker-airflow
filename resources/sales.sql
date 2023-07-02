select
    order_source
    , sum(price) as total_sales
from fact_orders
where
    order_date between '2023-02-01'::timestamp and '2023-02-28'::timestamp
    and order_status = 'Completed'
group by 1

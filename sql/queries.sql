-- As tabelas que utilizarei são:
-- "customers", para as informações dos clientes
-- "order_items", para informações dos itens dos pedidos
-- "products", informações dos produtos
-- "orders", para informações dos pedidos

WITH items_pedidos AS (
    SELECT order_id,
        product_id,
        SUM(price + freight_value) AS valor_final
    FROM order_items
    GROUP BY order_id, product_id
),

pedidos_validos as (
    SELECT order_id,
        customer_id,
        order_purchase_timestamp,
        order_estimated_delivery_date,
        order_delivered_customer_date
    FROM orders
    WHERE order_status = 'delivered'
)

SELECT t1.*,
    t3.product_category_name AS categoria,
    t2.customer_id,
    t4.customer_state,
    t2.order_purchase_timestamp,
    t2.order_estimated_delivery_date,
    t2.order_delivered_customer_date    

FROM items_pedidos aS t1

LEFT JOIN pedidos_validos AS t2
    ON t1.order_id = t2.order_id

LEFT JOIN products AS t3
    ON t1.product_id = t3.product_id

LEFT JOIN customers AS t4
    ON t2.customer_id = t4.customer_id
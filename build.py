# Builds demo.duckdb: fictional customers, orders and order lines (October 2026).
# Run with a pinned DuckDB so the MCP server can open the file:
#   uv run --python 3.12 --with duckdb==1.5.6 python build.py
import duckdb, random
random.seed(7)
con = duckdb.connect('demo.duckdb')
con.execute("""
create or replace table customers as
select i as customer_id, 'cliente'||i||'@ejemplo.test' as email, 'ES' as country
from range(1,201) t(i);
create or replace table orders(order_id int, customer_id int, status varchar, created_at date, amount decimal(10,2));
create or replace table order_items(order_id int, sku varchar, qty int, price decimal(10,2));
""")
oid=0
for _ in range(1000):
    oid+=1
    st=random.choices(['completed','refunded','cancelled'],[80,10,10])[0]
    d=f"2026-10-{random.randint(1,31):02d}"
    items=[(f"SKU{random.randint(1,30)}",random.randint(1,3),round(random.uniform(5,60),2)) for _ in range(random.randint(1,4))]
    amt=round(sum(q*p for _,q,p in items),2)
    con.execute("insert into orders values (?,?,?,?,?)",[oid,random.randint(1,200),st,d,amt])
    for s,q,p in items: con.execute("insert into order_items values (?,?,?,?)",[oid,s,q,p])
con.close()

# Second file for the controls test (controls/README.md): same data, but the
# customers table has no email column, so the agent cannot read what is not there.
masked = duckdb.connect('demo_masked.duckdb')
masked.execute("attach 'demo.duckdb' as src (read_only)")
masked.execute("create or replace table customers as select customer_id, country from src.customers")
masked.execute("create or replace table orders as select * from src.orders")
masked.execute("create or replace table order_items as select * from src.order_items")
masked.close()

# Third file for the definitions test (definitions/README.md): same data plus a
# view that carries the revenue definition. The raw orders table stays available.
view = duckdb.connect('demo_view.duckdb')
view.execute("attach 'demo.duckdb' as src (read_only)")
view.execute("create or replace table customers as select * from src.customers")
view.execute("create or replace table orders as select * from src.orders")
view.execute("create or replace table order_items as select * from src.order_items")
view.execute("create or replace view revenue_orders as select order_id, customer_id, created_at, amount from orders where status = 'completed'")
view.execute("comment on view revenue_orders is 'Revenue: completed orders only. Refunded and cancelled orders are excluded.'")
view.close()

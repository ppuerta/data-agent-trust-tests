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

from sqlalchemy import (Column, MetaData, Table, BigInteger, String, DECIMAL, Integer, DateTime, ForeignKey)

metadata = MetaData()

t_products = Table(
    "products",
    metadata,
    Column("id", BigInteger, primary_key=True, autoincrement=True, nullable=False),
    Column("name", String(100), nullable=False, unique=True),
    Column("description", String(255), nullable=False, unique=True),
    Column("value", DECIMAL, nullable=False),
    Column("quantity", Integer, nullable=False),
)

t_orders = Table(
    "orders",
    metadata,
    Column("id", BigInteger, primary_key=True, autoincrement=True, nullable=False),
    Column("customer_id",ForeignKey("users.id", ondelete="SET NULL", onupdate="CASCADE"), index=True),
    Column("order_data", DateTime, nullable=False)
)

t_order_itens = Table(
    "order_itens",
    metadata,
    Column("id", BigInteger, primary_key=True, autoincrement=True, nullable=False),
    Column("order_id", ForeignKey("orders.id", ondelete="SET NULL", onupdate="CASCADE"), index=True),
    Column("product_id", ForeignKey("products.id", ondelete="SET NULL", onupdate="CASCADE"), index=True),
    Column("quantity", BigInteger, nullable=False),
)

t_users = Table(
    "users",
    metadata,
    Column("id", BigInteger, primary_key=True, autoincrement=True, nullable=False),
    Column("customer_name", String(100), nullable=False),
    Column("CPF/CNPJ", String(15), nullable=False, unique=True)
)

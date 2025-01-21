from sqlalchemy import (Column, MetaData, Table, String, DECIMAL, Integer, DateTime, ForeignKey)

metadata = MetaData()

# Tabela de Produtos
t_products = Table(
    "products",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("nome", String(100), nullable=False, unique=True),
    Column("descricao", String(66), nullable=False),
    Column("quantidade", Integer, nullable=False),
    Column("preco", DECIMAL, nullable=False),
    Column("reposicao", DECIMAL, nullable=True),
)

# Tabela de Clientes
t_customers = Table(
    "customers",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("nome", String(100), nullable=False),
    Column("cpf_cnpj", String(255), nullable=False, unique=True),
    Column("telefone", String(255), nullable=False),
    Column("email", String(255), nullable=True),
)

# Tabela de Pedidos
t_orders: Table = Table(
    "orders",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("cliente_id", Integer, ForeignKey("customers.id", ondelete='CASCADE'), nullable=False),
    Column("data", DateTime, nullable=False),
    Column("status", String(25), nullable=False),
    Column("status_pagamento", String(25), nullable=False),
    Column("status_entrega", String(25), nullable=False),
    Column("end_entrega", String(62), nullable=False),
    Column("data_entrega", DateTime, nullable=False),
    Column("data_retirada", DateTime, nullable=False),
)

# Tabela de Itens do Pedido
t_order_items = Table(
    "order_items",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("pedido_id", Integer, ForeignKey("orders.id", ondelete='CASCADE'), nullable=False),
    Column("produto_id", Integer, ForeignKey("products.id", ondelete='CASCADE'), nullable=False),
    Column("quantidade", Integer, nullable=False),
    Column("preco_unitario", DECIMAL, nullable=False),
    Column("preco_total", DECIMAL, nullable=False),
)

from datetime import datetime
from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy import select, delete, update

from CRUD.customers import get_cliente
from CRUD.products import total_products_on_request, get_product
from models.ProductsModels import Produtos, ItensPedidos, Produto, Budget, Pedidos
from persistence.data_definition import t_orders, t_order_items, t_products


def cadastrar_pedido(order, db):
    data_atual = datetime.now()

    for item in order.items:
        total = total_products_on_request(item.product_id, db)
        product = get_product(item.product_id, db)

        if product.quantidade - total - item.amount < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Não a produtos o suficente para o produto {product.nome}",
            )

    input_ = {
        "cliente_id": order.client_id,
        "data": data_atual,
        "status": order.status,
        "status_pagamento": "AGUARDANDO",
        "status_entrega": "AGUARDANDO",
        "data_entrega": order.data_entrega,
        "data_retirada": order.data_retirada,
        "end_entrega": order.end_entrega,
    }

    a = db.execute(t_orders.insert().values(input_).returning(t_orders.c.id))
    id_pedido = a.scalar()

    # Salvando os itens dos pedidos

    for item in order.items:
        query = select(t_products).where(t_products.c.id == item.product_id)

        result = db.execute(query)

        product = result.fetchone()
        product_dict = dict(product._mapping)

        produto = Produtos(**product_dict)

        input_ = {
            "pedido_id": id_pedido,
            "produto_id": produto.id,
            "quantidade": item.amount,
            "preco_unitario": produto.preco,
            "preco_total": produto.preco * item.amount,
        }

        items_pedidos = ItensPedidos(**input_)

        db.execute(t_order_items.insert().values(items_pedidos.dict(exclude={"id"})))

    db.commit()

    return order.__dict__


def listar_order(db):
    query = select(t_products)

    # Executa o SELECT para listar os produtos
    result = db.execute(query).fetchall()

    # Cria a lista com os produtos e suas quantidades
    nomes_produtos = [
        {
            "id": row.id,
            "name": row.nome,
            "price": row.preco,
            "description": row.descricao,
            "quantity": row.quantidade,
        }
        for row in result
    ]
    return nomes_produtos


def listar_orcamento(db):
    query = select(t_orders.c.id).where(t_orders.c.status == "ORCAMENTO")

    return get_pedidos(db, query)


def listar_pedido(db):
    query = select(t_orders.c.id).where(t_orders.c.status != "ORCAMENTO")

    return get_pedidos(db, query)


def apagar_orcamento(id, db):
    db.execute(delete(t_orders).where(t_orders.c.id == id))

    db.execute(delete(t_order_items).where(t_order_items.c.pedido_id == id))

    db.commit()


def update_orcamento(id, order_input, db):
    # Exclui os pedidos relacionados
    db.execute(
        update(t_orders)
        .where(t_orders.c.id == id)
        .values(
            status=order_input.status,
            client_id=order_input.client_id,
        )
    )

    db.commit()


def change_budget_in_order_status(id, status, db):
    # Exclui os pedidos relacionados
    db.execute(
        update(t_orders)
        .where(t_orders.c.id == id)
        .values(
            status=status,
        )
    )

    db.commit()


def update_orcamento_status(id, update_pedido, db):
    # Exclui os pedidos relacionados
    if update_pedido.statusPagamento:
        db.execute(
            update(t_orders)
            .where(t_orders.c.id == id)
            .values(status_pagamento=update_pedido.statusPagamento)
        )
    if update_pedido.statusEntrega:
        db.execute(
            update(t_orders)
            .where(t_orders.c.id == id)
            .values(status_entrega=update_pedido.statusEntrega)
        )

    db.commit()


def get_pedidos(db, query):
    result = db.execute(query).scalars().all()
    pedidos = []
    for id_ in result:
        valor_total = Decimal(0)

        products = []

        query = select(t_order_items).where(t_order_items.c.pedido_id == id_)

        result_ = db.execute(query).fetchall()
        result_ = [ItensPedidos(**dict(item._mapping)) for item in result_]
        for i in result_:
            valor_total += i.preco_total

            products.append(Produto(product_id=i.produto_id, amount=i.quantidade))

        query = db.execute(select(t_orders.c).where(t_orders.c.id == id_)).first()

        pedido = Pedidos(**dict(query._mapping))

        cliente = get_cliente(pedido.cliente_id, db)

        response = {
            "pedido": Budget(items=products, clientName=cliente.nome, id=id_),
            "valor": valor_total,
            "statusEntrega": pedido.status_entrega,
            "statusPagamento": pedido.status_pagamento,
        }

        pedidos.append(response)

    return pedidos

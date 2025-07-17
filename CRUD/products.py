from sqlalchemy import select, delete, func

from models.ProductsModels import Produtos
from persistence.data_definition import t_products, t_order_items, t_orders


def cadastrar_produtos(product, db):
    produto = {
        "nome": product.nome.strip(),
        "descricao": product.descricao.strip(),
        "preco": product.preco,
        "quantidade": product.quantidade,
        "reposicao": product.reposicao,
    }

    # Executa o INSERT para cadastrar o produto
    db.execute(t_products.insert().values(**produto))
    db.commit()

    return {
        "name": product.nome.strip(),
        "description": product.descricao.strip(),
        "price": product.preco,
    }


def editar_produto(id, produto, db):
    produto_dict = produto.dict(exclude={"id"})

    query = t_products.update().where(t_products.c.id == id).values(produto_dict)

    # Executa a atualização do produto
    db.execute(query)
    db.commit()


def listar_produto(db):
    query = select(t_products).order_by(t_products.c.nome)

    # Executa o SELECT para listar os produtos
    result = db.execute(query).fetchall()

    # Cria a lista com os produtos e suas quantidades
    produtos = []

    for row in result:
        produto = {
            "id": row.id,
            "name": row.nome,
            "price": row.preco,
            "description": row.descricao,
            "quantity": row.quantidade,
            "replacement": row.reposicao,
        }

        produtos.append(produto)

    return produtos


def total_products_on_request(id_, db):
    orcamentos_ids = (
        db.execute(
            select(t_orders.c.id).where(
                t_orders.c.status == "ORCAMENTO"
                or t_orders.c.status_entrega == "RETIRADO"
            )
        )
        .scalars()
        .all()
    )

    query = select(func.sum(t_order_items.c.quantidade)).where(
        t_order_items.c.produto_id == id_
    )

    if orcamentos_ids:
        query = query.where(t_order_items.c.pedido_id.not_in(orcamentos_ids))

    total = db.execute(query).scalar() or 0

    total = total or 0

    return total


def listar_produto_estoque(db):
    query = select(t_products)

    result = db.execute(query).fetchall()

    produtos = []

    for row in result:
        total = total_products_on_request(row.id, db)

        produto = {
            "id": row.id,
            "name": row.nome,
            "price": row.preco,
            "description": row.descricao,
            "quantity": row.quantidade - total,
        }

        produtos.append(produto)

    return produtos


def apagar_produtos(id, db):
    pedidos_ids = (
        db.execute(
            select(t_order_items.c.pedido_id).where(t_order_items.c.produto_id == id)
        )
        .scalars()
        .all()
    )

    # Exclui os pedidos relacionados
    db.execute(delete(t_orders).where(t_orders.c.id.in_(pedidos_ids)))

    # Exclui os itens dos pedidos
    db.execute(delete(t_order_items).where(t_order_items.c.pedido_id.in_(pedidos_ids)))

    # Prepara a query DELETE para apagar o produto
    db.execute(delete(t_products).where(t_products.c.id == id))

    # Executa o DELETE no banco de dados
    db.commit()

    # Verifica se o produto foi apagado
    return {"message": "Produto apagado com sucesso!"}


def get_product(id_, db):
    query = select(t_products).where(t_products.c.id == id_)
    result = db.execute(query).first()
    produto = Produtos(**dict(result._mapping))

    return produto

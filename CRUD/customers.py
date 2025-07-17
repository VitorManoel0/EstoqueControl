from sqlalchemy import select, delete

from models.ProductsModels import Clientes
from persistence.data_definition import t_customers


def cadastrar_cliente(cliente, db):
    db.execute(t_customers.insert().values(**cliente.model_dump(exclude='id')))
    db.commit()

    return cliente.__dict__


def editar_cliente(id, client, db):
    cliente_dict = client.dict(exclude={"id"})

    query = t_customers.update().where(t_customers.c.id == id).values(cliente_dict)

    # Executa a atualização do produto
    db.execute(query)
    db.commit()


def listar_cliente(db):
    query = select(t_customers)

    # Executa o SELECT para listar os produtos
    result = db.execute(query).fetchall()

    # Cria a lista com os produtos e suas quantidades
    nomes_produtos = [
        Clientes(
            **{
                "id": row[0],
                "nome": row[1],
                "cpf_cnpj": row[2],
                "email": row[4],
                "telefone": row[3],
            }
        )
        for row in result
    ]
    return nomes_produtos


def apagar_cliente(id, db):
    # Prepara a query DELETE para apagar o produto
    query = delete(t_customers).where(t_customers.c.id == id)

    # Executa o DELETE no banco de dados
    result = db.execute(query)
    db.commit()

    # Verifica se o produto foi apagado
    if result.rowcount > 0:
        return {"message": "Produto apagado com sucesso!"}
    else:
        return {"message": "Produto não encontrado."}


def get_cliente(id, db):
    query = select(t_customers).where(t_customers.c.id == id)

    result = db.execute(query).first()
    db.commit()

    return result

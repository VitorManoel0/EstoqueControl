from fastapi import Depends, APIRouter
from sqlmodel import Session

from CRUD.orders import (
    cadastrar_pedido,
    listar_pedido,
    update_orcamento_status,
)
from db import get_db
from models.ProductsModels import OrderInput, UpdateOrder

router = APIRouter(tags=["Pedidos"])


@router.post("/create_orders")
def cadastrar_pedidos(order_input: OrderInput, db: Session = Depends(get_db)):
    try:
        cadastrar_pedido(order_input, db)
        return {"message": "Pedido cadastrado com sucesso!"}

    except Exception as e:
        raise e


@router.get("/listar_pedidos")
def listar_pedidos(db: Session = Depends(get_db)):
    a = listar_pedido(db)
    return a


@router.put("/atualizar_pedido/{id}")
def listar_pedidos(id, update_pedido: UpdateOrder, db: Session = Depends(get_db)):
    a = update_orcamento_status(id, update_pedido, db)
    return a

from fastapi import Depends, APIRouter
from sqlmodel import Session

from CRUD.customers import (
    cadastrar_cliente,
    listar_cliente,
    apagar_cliente,
    editar_cliente,
)
from db import get_db
from models.ProductsModels import Clientes

router = APIRouter(tags=["Clientes"])


@router.post("/cadastrar_clientes")
def cadastrar_clientes(cliente: Clientes, db: Session = Depends(get_db)):
    cadastrar_cliente(cliente, db)
    return {"message": f"Produto '{cliente.nome}' cadastrado com sucesso!"}


@router.get("/listar_clientes")
def listar_clientes(db: Session = Depends(get_db)):
    try:
        nomes_clientes = listar_cliente(db)
        return nomes_clientes
    except Exception:
        return {"Nome de produto ja existente"}


@router.delete("/apagar_clientes")
def apagar_clientes(id: int, db: Session = Depends(get_db)):
    try:
        apagar_cliente(id, db)
    except Exception as e:
        return {"error": str(e)}


@router.put("/editar_cliente/{id}")
def atualizar_quantidade(cliente: Clientes, id: int, db: Session = Depends(get_db)):
    try:
        editar_cliente(id, cliente, db)
        return {"message": f"Cliente '{cliente.nome}' atualizado"}
    except Exception:
        return {"Nome de produto ja existente"}

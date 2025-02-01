from fastapi import Depends, APIRouter
from sqlmodel import Session

from CRUD.products import (
    cadastrar_produtos,
    listar_produto,
    apagar_produtos,
    editar_produto,
    listar_produto_estoque,
)
from db import get_db
from models.ProductsModels import Produtos

router = APIRouter(tags=["Produtos"])


@router.post("/cadastrar_produto")
def cadastrar_produto(produto: Produtos, db: Session = Depends(get_db)):
    produto = cadastrar_produtos(produto, db)
    return produto


@router.put("/editar_produto/{id}")
def editar_produtos(produto: Produtos, id: int, db: Session = Depends(get_db)):
    try:
        editar_produto(id, produto, db)
        return {"message": f"Produto '{produto.nome}' atualizado"}
    except Exception:
        return {"Nome de produto ja existente"}


@router.get("/listar_produtos")
def listar_produtos(db: Session = Depends(get_db)):
    try:
        nomes_produtos = listar_produto(db)
        return nomes_produtos
    except Exception:
        return {"Nome de produto ja existente"}


@router.get("/listar_produtos_estoque")
def listar_produtos_estoque(db: Session = Depends(get_db)):
    try:
        nomes_produtos = listar_produto_estoque(db)
        return nomes_produtos
    except Exception:
        return {"Nome de produto ja existente"}


@router.delete("/apagar_produto")
def apagar_produto(id: str, db: Session = Depends(get_db)):
    try:
        apagar_produtos(id, db)
    except Exception as e:
        return {"error": str(e)}

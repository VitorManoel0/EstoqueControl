from fastapi import Depends, APIRouter
from fastapi.responses import FileResponse
from sqlmodel import Session

from CRUD.orders import (
    cadastrar_pedido,
    apagar_orcamento,
    listar_orcamento,
    update_orcamento,
    change_budget_in_order_status,
)
from CRUD.pdf import generate_pdf
from db import get_db
from models.ProductsModels import OrderInput

router = APIRouter(tags=["Orçamento"])


@router.post("/create_budget")
def cadastrar_orcamentos(order_input: OrderInput, db: Session = Depends(get_db)):
    order_input.status = "ORCAMENTO"

    cadastrar_pedido(order_input, db)
    return {"message": "Pedido cadastrado com sucesso!"}


@router.get("/listar_budgets")
def listar_orders(db: Session = Depends(get_db)):
    a = listar_orcamento(db)
    return a


@router.delete("/delete_budget/{id_}")
def delete_budget(id_, db: Session = Depends(get_db)):
    apagar_orcamento(id_, db)


@router.put("/update_budget/{id_}")
def update_budget(id_, order_input: OrderInput, db: Session = Depends(get_db)):
    update_orcamento(id_, order_input, db)


@router.put("/change_budget_in_order/{id_}")
def change_budget_in_order(id_, status: str, db: Session = Depends(get_db)):
    change_budget_in_order_status(id_, status, db)


@router.post("/export_pdf/{id_}")
def export_pdf(id_, db: Session = Depends(get_db)):
    logo_path = "logo_meire.png"

    generate_pdf("orcamento_meire_pinho.pdf", logo_path, id_, db)

    return FileResponse(
        "orcamento_meire_pinho.pdf",
        media_type="application/pdf",
        filename="ORÇAMENTO.pdf",
    )

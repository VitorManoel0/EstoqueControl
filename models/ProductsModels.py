import datetime
from typing import List

from pydantic import BaseModel

from decimal import Decimal


class Produtos(BaseModel):
    id: int = None
    nome: str
    descricao: str
    preco: Decimal
    quantidade: int
    reposicao: Decimal


class Clientes(BaseModel):
    id: int = None
    nome: str
    cpf_cnpj: str
    email: str
    telefone: str


class Pedidos(BaseModel):
    id: int = None
    cliente_id: int
    status: str
    data: datetime.datetime
    status_pagamento: str
    status_entrega: str
    end_entrega: str
    data_entrega: datetime.datetime
    data_retirada: datetime.datetime


class ItensPedidos(BaseModel):
    id: int = None
    pedido_id: int
    produto_id: int
    quantidade: int
    preco_unitario: Decimal
    preco_total: Decimal


class Produto(BaseModel):
    product_id: int
    amount: int


class OrderInput(BaseModel):
    items: List[Produto]
    status: str = "Aguardando"
    client_id: str
    end_entrega: str = ""
    data_entrega: datetime.datetime = datetime.datetime.now()
    data_retirada: datetime.datetime = datetime.datetime.now()


class Budget(BaseModel):
    clientName: str
    items: List[Produto]
    id: int = None


class UpdateOrder(BaseModel):
    statusPagamento: str = None
    statusEntrega: str = None

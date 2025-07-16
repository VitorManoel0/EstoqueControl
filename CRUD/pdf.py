from decimal import Decimal
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle, Paragraph, Frame
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from sqlalchemy import select
from CRUD.customers import get_cliente
from CRUD.products import get_product
from models.ProductsModels import Clientes, Pedidos, ItensPedidos
from persistence.data_definition import t_orders, t_order_items
from utils import formatar_telefone


def get_data(id_, db):
    dict_ = dict(
        db.execute(select(t_orders).where(t_orders.c.id == id_)).first()._mapping
    )
    pedido = Pedidos(**dict_)
    valor_total = Decimal(0)
    products = []
    items = db.execute(
        select(t_order_items).where(t_order_items.c.pedido_id == id_)
    ).fetchall()
    result_ = [ItensPedidos(**dict(item._mapping)) for item in items]
    cliente = Clientes(**dict(get_cliente(pedido.cliente_id, db)._mapping))

    for item in result_:
        valor_total += item.preco_total
        product = get_product(item.produto_id, db)
        products.append(
            [
                item.quantidade,
                product.descricao,
                f"R$ {round(item.preco_unitario, 2)}",
                f"R$ {round(product.reposicao, 2)}",
                f"R$ {round(item.preco_unitario * item.quantidade, 2)}",
            ]
        )
    products.append(["", "", "", "", f"R$: {round(valor_total, 2)}"])
    return products, cliente, pedido


def generate_pdf(file_name, logo_path, id_, db):
    products, cliente, pedido = get_data(id_, db)
    pdf = canvas.Canvas(file_name, pagesize=letter)
    print(letter)
    width, height = letter

    # Logo (começo, fim, proporção da imagem)
    pdf.drawImage(logo_path, 231, height - 100, width=150, height=50)
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(200, height - 150, "ORÇAMENTO DE LOCAÇÃO")
    pdf.setFont("Helvetica", 12)

    # Criando o estilo para o parágrafo
    styles = getSampleStyleSheet()
    custom_style = ParagraphStyle(
        "CustomStyle",
        parent=styles["Normal"],
        fontSize=12,
        fontName="Helvetica",
        alignment=4,
        spaceAfter=12,
        leftIndent=9,
        rightIndent=9,
        leading=14,
        spaceBefore=10,
    )

    # String com marcação HTML para negrito
    string_formatted = """A CONTRATADA, <b>MEIRE E PINHO BUFFET E LOCADORA</b>, razão social
<b>R.R.BATISTA LOCADORA LTDA.</b>, CNPJ n.º <b>12.106.567/0001-26</b>, ora representada
por <b>ROSIMEIRE RODRIGUES BATISTA</b>, brasileira, casada, autônoma, portadora
da Cédula de Identidade – RG n.º 989255 SSP MT, e inscrita no CPF n.º
652.222.881-53 MF, residente a Rua Lucinópolis, n.º 16, Bairro Coophema, Cuiabá/MT,
receberá o pagamento via PIX para a conta bancária do Beneficiário, que possui os
seguintes detalhes: R.R.BATISTA LOCADORA LTDA., CNPJ: 12.106.567/0001-26,
Conta PIX: 12.106.567/0001-26, na instituição financeira NUBANK PAGAMENTOS
SA., agência 0001."""

    # Criando o parágrafo
    paragraph = Paragraph(string_formatted, custom_style)
    # Criando um frame para o parágrafo
    frame = Frame(
        0,
        0,
        width,
        height,
        leftPadding=0,
        bottomPadding=0,
        rightPadding=0,
        topPadding=0,
    )
    # Posicionando o parágrafo
    paragraph.wrapOn(pdf, width - 170, height)  # width - margens
    paragraph.drawOn(pdf, 85, 485)  # x, y position

    # CONTRATANTE com nome em negrito
    pdf.setFont("Helvetica", 12)
    pdf.drawString(100, height - 330, "CONTRATANTE: ")
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(200, height - 330, cliente.nome)

    # TELEFONE com número em negrito
    pdf.setFont("Helvetica", 12)
    pdf.drawString(390, height - 330, "TELEFONE: ")
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(460, height - 330, formatar_telefone(cliente.telefone))

    # END. ENTREGA com endereço em negrito
    pdf.setFont("Helvetica", 12)
    pdf.drawString(100, height - 365, "END. ENTREGA: ")
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(200, height - 365, pedido.end_entrega)

    # DATA ENTREGA com data em negrito
    pdf.setFont("Helvetica", 12)
    pdf.drawString(100, height - 400, "DATA ENTREGA: ")
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(200, height - 400, pedido.data_entrega.strftime("%d/%m/%Y"))

    # DATA RETIRADA com data em negrito
    pdf.setFont("Helvetica", 12)
    pdf.drawString(390, height - 400, "DATA RETIRADA: ")
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(490, height - 400, pedido.data_retirada.strftime("%d/%m/%Y"))

    # Volta para fonte normal
    pdf.setFont("Helvetica", 12)
    pdf.drawString(260, height - 735, "ATENÇÃO")
    pdf.drawString(
        80,
        height - 750,
        "1. AS ENTREGAS E RETIRADAS SÃO FEITAS APENAS EM HORÁRIO COMERCIAL",
    )

    cabecalho = ["QTD.", "DESCRIÇÃO", "PREÇO UN.", "REP. UN.", "TOTAL"]
    data = [cabecalho] + products

    # TAMANHO
    col_widths = [30, 300, 60, 50, 70]
    table = Table(data, colWidths=col_widths)
    style = TableStyle(
        [
            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.white,
            ),  # Fundo cinza no cabeçalho
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),  # Texto branco no cabeçalho
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),  # Alinhamento centralizado
            (
                "FONTNAME",
                (0, 0),
                (-1, 0),
                "Helvetica-Bold",
            ),  # Fonte negrito no cabeçalho
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),  # Espaçamento inferior no cabeçalho
            ("BACKGROUND", (0, 1), (-1, -1), colors.white),  # Fundo bege nas linhas
            ("GRID", (0, 0), (-1, -1), 1, colors.black),  # Grade com linhas pretas
            # Estilo específico para a última linha
            (
                "SPAN",
                (0, -1),
                (-2, -1),
            ),  # Mesclar células da última linha (exceto a última coluna)
            (
                "ALIGN",
                (-1, -1),
                (-1, -1),
                "RIGHT",
            ),  # Alinhar à direita o valor da última coluna
            (
                "FONTNAME",
                (-1, -1),
                (-1, -1),
                "Helvetica-Bold",
            ),  # Fonte negrito na última coluna
            (
                "TEXTCOLOR",
                (-1, -1),
                (-1, -1),
                colors.black,
            ),  # Texto preto na última coluna
            (
                "BACKGROUND",
                (0, -1),
                (-1, -1),
                colors.white,
            ),  # Fundo branco na última linha
            (
                "LINEBELOW",
                (0, -2),
                (-1, -2),
                1,
                colors.black,
            ),  # Linha inferior antes do total
        ]
    )

    table.setStyle(style)
    x, y = 50, height - (460 + (18 * (len(data) - 2)))
    table.wrapOn(pdf, x, y)
    table.drawOn(pdf, x, y)
    pdf.showPage()

    # Página 2
    # pdf.setFont("Helvetica-Bold", 16)
    # pdf.drawString(200, height - 100, "SEGUNDA PÁGINA DO DOCUMENTO")
    # pdf.setFont("Helvetica", 12)
    # pdf.drawString(100, height - 150, "Aqui está o conteúdo adicional.")

    pdf.save()
    print(f"PDF '{file_name}' criado com sucesso!")


# Exemplo de uso alternativo - função helper para criar parágrafos com negrito
def create_formatted_paragraph(text, style, x, y, pdf, width):
    """
    Função helper para criar parágrafos formatados com negrito
    """
    paragraph = Paragraph(text, style)
    paragraph.wrapOn(pdf, width, 200)  # ajuste a altura conforme necessário
    paragraph.drawOn(pdf, x, y)
    return paragraph

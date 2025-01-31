from decimal import Decimal

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from sqlalchemy import select

from CRUD.customers import get_cliente
from CRUD.products import get_product
from models.ProductsModels import Clientes, Pedidos, ItensPedidos
from persistence.data_definition import t_orders, t_order_items
from utils import formatar_telefone


def get_data(id_, db):
    dict_ = dict(db.execute(select(t_orders).where(t_orders.c.id == id_)).first()._mapping)

    pedido = Pedidos(**dict_)

    valor_total = Decimal(0)

    products = []

    items = db.execute(select(t_order_items).where(t_order_items.c.pedido_id == id_)).fetchall()

    result_ = [ItensPedidos(**dict(item._mapping)) for item in items]

    cliente = Clientes(**dict(get_cliente(pedido.cliente_id, db)._mapping))

    for item in result_:
        valor_total += item.preco_total

        product = get_product(item.produto_id, db)

        products.append([item.quantidade, product.descricao, f"R$ {round(item.preco_unitario, 2)}",
                         f"R$ {round(product.reposicao, 2)}",
                         f"R$ {round(item.preco_unitario * item.quantidade, 2)}"
                         ])

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

    text_object = pdf.beginText(85, 610)
    text_object.setFont("Helvetica", 12)

    words = string_.split()
    line = ""
    for word in words:
        if pdf.stringWidth(line + word, "Helvetica", 12) < 450:
            line += word + " "
        else:
            text_object.textLine(line)
            line = word + " "
    text_object.textLine(line)  # Adiciona a última linha

    pdf.drawText(text_object)

    pdf.drawString(100, height - 330, f"CONTRATANTE: {cliente.nome}")
    pdf.drawString(390, height - 330, f"TELEFONE: {formatar_telefone(cliente.telefone)}")

    pdf.drawString(100, height - 365, f"END. ENTREGA: {pedido.end_entrega}")

    pdf.drawString(100, height - 400, f"DATA ENTREGA: {pedido.data_entrega.strftime('%d/%m/%Y')}")
    pdf.drawString(390, height - 400, f"DATA RETIRADA: {pedido.data_retirada.strftime('%d/%m/%Y')}")

    pdf.drawString(260, height - 735, f"ATENÇÃO")
    pdf.drawString(80, height - 750, f"1. AS ENTREGAS E RETIRADAS SÃO FEITAS APENAS EM HORÁRIO COMERCIAL")

    cabecalho = ["QTD.", "DESCRIÇÃO", "PREÇO UN.", "REP. UN.", "TOTAL"]

    data = [cabecalho] + products

    # TAMANHO
    col_widths = [30, 300, 60, 50, 70]

    table = Table(data, colWidths=col_widths)

    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgoldenrodyellow),  # Fundo cinza no cabeçalho
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),  # Texto branco no cabeçalho
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Alinhamento centralizado
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Fonte negrito no cabeçalho
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Espaçamento inferior no cabeçalho
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),  # Fundo bege nas linhas
        ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Grade com linhas pretas

        # Estilo específico para a última linha
        ('SPAN', (0, -1), (-2, -1)),  # Mesclar células da última linha (exceto a última coluna)
        ('ALIGN', (-1, -1), (-1, -1), 'RIGHT'),  # Alinhar à direita o valor da última coluna
        ('FONTNAME', (-1, -1), (-1, -1), 'Helvetica-Bold'),  # Fonte negrito na última coluna
        ('TEXTCOLOR', (-1, -1), (-1, -1), colors.black),  # Texto preto na última coluna
        ('BACKGROUND', (0, -1), (-1, -1), colors.beige),  # Fundo branco na última linha
        ('LINEBELOW', (0, -2), (-1, -2), 1, colors.black),  # Linha inferior antes do total
    ])

    table.setStyle(style)

    x, y = 50, height - (460 + (18 * (len(data) - 2)))

    table.wrapOn(pdf, x, y)
    table.drawOn(pdf, x, y)

    pdf.showPage()

    # Página 2
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(200, height - 100, "SEGUNDA PÁGINA DO DOCUMENTO")

    pdf.setFont("Helvetica", 12)
    pdf.drawString(100, height - 150, "Aqui está o conteúdo adicional.")

    pdf.save()
    print(f"PDF '{file_name}' criado com sucesso!")


string_ = f"""A CONTRATADA, MEIRE E PINHO BUFFET E LOCADORA, razão social R.R.BATISTA LOCADORA LTDA., 
    CNPJ nº 12.106.567/0001-26, ora representada por ROSIMEIRE RODRIGUES BATISTA, brasileira, casada, autônoma, portadora da 
    Cédula de Identidade – RG nº 989255 SSP MT, e inscrita no CPF nº 652.222.881-53 MF, residente à Rua Lucinópolis, nº 16, 
    Bairro Coophema, Cuiabá/MT, receberá o pagamento via PIX para a conta bancária do Beneficiário, que possui os seguintes 
    detalhes: R.R.BATISTA LOCADORA LTDA., CNPJ: 12.106.567/0001-26, Conta PIX: 12.106.567/0001-26, na instituição financeira 
    NUBANK PAGAMENTOS SA., agência 0001.
    """

def formatar_telefone(numero: str) -> str:
    """Formata um número de telefone no padrão (XX) XXXXX-XXXX."""
    if len(numero) == 11:
        ddd = numero[:2]
        primeira_parte = numero[2:7]
        segunda_parte = numero[7:]
        return f"({ddd}) {primeira_parte}-{segunda_parte}"
    if len(numero) == 10:
        ddd = numero[:2]
        primeira_parte = numero[2:6]
        segunda_parte = numero[6:]
        return f"({ddd}) 9{primeira_parte}-{segunda_parte}"
    else:
        raise ValueError("O número deve conter 11 dígitos.")

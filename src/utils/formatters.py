def format_currency(value: float, symbol: str = "R$") -> str:
    """
    Formata um número como valor monetário.
    """
    return f"{symbol} {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def format_percentage(value: float, decimals: int = 2) -> str:
    """
    Formata um número como porcentagem.
    """
    return f"{value:.{decimals}%}"

"""Funciones de formato de texto."""


def money(value: float) -> str:
    """Devuelve un monto formateado, por ejemplo 1234.5 -> '$1,234.50'."""
    return f"${value:,.2f}"

from django import template

register = template.Library()


@register.filter
def clp(valor):
    """Formatea un monto en pesos chilenos: 25000 → "$25.000"."""
    if valor in (None, ""):
        return ""
    try:
        return "$" + f"{int(valor):,}".replace(",", ".")
    except (TypeError, ValueError):
        return valor

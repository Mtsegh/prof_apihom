from django import template

register = template.Library()

# Extend as needed — anything not listed falls back to showing the
# raw code followed by a space (e.g. "AUD 25.00"), so it never
# silently breaks on an unmapped currency.
CURRENCY_SYMBOLS = {
    'NGN': '₦',
    'USD': '$',
    'GBP': '£',
    'EUR': '€',
    'INR': '₹',
}


@register.filter
def currency_symbol(code):
    """Maps an ISO 4217 currency code to its display symbol."""
    return CURRENCY_SYMBOLS.get(code, f'{code} ')
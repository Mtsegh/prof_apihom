from django.shortcuts import render

from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .models import Book


def book_list(request):
    """
    Books page: dynamic list of all books.

    Assumed Book model fields:
      title            — CharField
      subtitle         — CharField, blank=True
      slug             — SlugField, unique=True (drives book_detail's URL)
      cover            — ImageField, blank=True (card/detail both handle missing cover)
      price            — DecimalField, null=True, blank=True (hidden on card if unset)
      description      — TextField (truncated on the card, shown in full on detail —
                          one field for both, not a separate short/long pair)
      isbn             — CharField, blank=True
      category         — CharField, blank=True (plain text for now — see note below)
      publisher        — CharField, blank=True
      availability     — CharField, choices=[
                              ('in_stock', 'In Stock'),
                              ('preorder', 'Pre-order'),
                              ('out_of_stock', 'Out of Stock'),
                          ], default='in_stock'
      purchase_url     — URLField, blank=True (Buy Now button hides if empty)
      featured_order   — PositiveSmallIntegerField, null=True, blank=True, unique=True
      published_date   — DateField, null=True, blank=True
      currency — CharField, max_length=3, default='NGN'
           (ISO 4217 code — 'NGN', 'USD', etc. Symbol resolved
           via the currency_symbol template filter, not stored directly)

    No filtering/search/pagination here — the brief only asked for that
    on Publications. Add pagination first if the catalog grows large.
    """
    context = {
        'books': Book.objects.all().order_by('-published_date', 'title'),
    }
    return render(request, 'books/books.html', context)


def book_detail(request, slug):
    """Single book page, looked up by slug — not pk (see urls.py from Phase 1)."""
    book = get_object_or_404(Book, slug=slug)
    context = {
        'book': book,
        'breadcrumbs': [
            {'label': 'Books', 'url': reverse('books:book_list')},
            {'label': book.title, 'url': None},
        ],
    }
    return render(request, 'books/book_detail.html', context)
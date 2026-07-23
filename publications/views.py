from django.shortcuts import render

from django.core.paginator import Paginator
from django.db.models import Q, Min, Max
from django.shortcuts import render

from .models import Publication


def publication_list(request):
    """
    Publications page: search + filter + paginate.

    Assumed Publication model fields:
      title              — CharField
      authors            — CharField, e.g. "Ihom, A.P., Offiong, A."
      journal            — CharField, blank=True
                            (also holds "Proceedings of..." for conference entries)
      publication_type   — CharField, choices=[
                                ('journal', 'Journal Article'),
                                ('conference', 'Conference Proceedings'),
                                ('review', 'Review Article'),
                            ], default='journal'
      year               — PositiveSmallIntegerField
      doi                — CharField, blank=True (no "https://doi.org/" prefix stored)
      abstract           — TextField, blank=True
      pdf_file           — FileField, blank=True, null=True
      external_url       — URLField, blank=True
                            (fallback link — journal page, ResearchGate, etc. —
                             shown only if pdf_file is empty)

    Filters combine with AND: ?q= (title/authors/journal), ?type=,
    ?year_from= / ?year_to= (inclusive range).
    """
    publications = Publication.objects.all()

    query = request.GET.get('q', '').strip()
    pub_type = request.GET.get('type', '').strip()
    year_from = request.GET.get('year_from', '').strip()
    year_to = request.GET.get('year_to', '').strip()

    if query:
        publications = publications.filter(
            Q(title__icontains=query) |
            Q(authors__icontains=query) |
            Q(journal__icontains=query)
        )

    if pub_type:
        publications = publications.filter(publication_type=pub_type)

    # Swap silently if entered backwards, rather than returning an
    # empty, confusing result set for something like "2020 to 2005"
    if year_from.isdigit() and year_to.isdigit() and int(year_from) > int(year_to):
        year_from, year_to = year_to, year_from

    if year_from.isdigit():
        publications = publications.filter(year__gte=year_from)
    if year_to.isdigit():
        publications = publications.filter(year__lte=year_to)

    publications = publications.order_by('-year', 'title')

    # Bounds for the input placeholders/min/max attrs — built off the
    # unfiltered queryset so the range doesn't shrink once a filter is applied
    year_bounds = Publication.objects.aggregate(min_year=Min('year'), max_year=Max('year'))

    paginator = Paginator(publications, 9)
    page_obj = paginator.get_page(request.GET.get('page'))

    # Strip `page` so filters survive pagination links (see partials/pagination.html)
    querystring = request.GET.copy()
    querystring.pop('page', None)
    querystring = querystring.urlencode()

    context = {
        'page_obj': page_obj,
        'query': query,
        'selected_type': pub_type,
        'selected_year_from': year_from,
        'selected_year_to': year_to,
        'min_year': year_bounds['min_year'],
        'max_year': year_bounds['max_year'],
        'publication_types': [
            ('journal', 'Journal Article'),
            ('conference', 'Conference Proceedings'),
            ('review', 'Review Article'),
        ],
        'querystring': querystring,
        'has_active_filters': bool(query or pub_type or year_from or year_to),
    }
    return render(request, 'publications/publications.html', context)

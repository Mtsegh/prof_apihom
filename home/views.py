from urllib.parse import quote_plus

from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse

from books.models import Book
from publications.models import Publication
from research.models import ResearchInterest, ResearchProject, TeachingResource
from achievements.models import Achievement
from .models import Statistic

MIN_QUERY_LENGTH = 3
LIVE_RESULTS_PER_CATEGORY = 4


def home(request):
    """
    Landing page: hero, stats, featured books, recent publications,
    research interests, and an achievements preview.

    `profile` is no longer fetched here — it comes from the
    home.context_processors.profile context processor and is
    available in every template project-wide.

    Assumed model fields — adjust here if your models end up different:
      Statistic         — label, value, order
      Book              — title, subtitle, cover, slug,
                           featured_order (PositiveSmallIntegerField,
                           null=True, blank=True, unique=True)
      Publication       — title, journal, authors, year, doi
      ResearchInterest  — title, short_description
      Achievement       — title, date, category
    """
    
    context = {
        'statistics': Statistic.objects.all().order_by('order'),
        'featured_books': Book.objects.filter(
            featured_order__isnull=False
        ).order_by('featured_order')[:3],
        'recent_publications': Publication.objects.order_by('-year')[:4],
        'research_interests': ResearchInterest.objects.all()[:6],
        'achievements_preview': Achievement.objects.order_by('-date')[:4],
    }
    return render(request, 'home/home.html', context)


# ---------- Search ----------
# Achievements deliberately excluded — matches the scope confirmed earlier
# (Books, Publications, Teaching Resources, Research Projects only).

def _search_books(query):
    return Book.objects.filter(
        Q(title__icontains=query) |
        Q(subtitle__icontains=query) |
        Q(description__icontains=query) |
        Q(isbn__icontains=query)
    ).order_by('title')


def _search_publications(query):
    return Publication.objects.filter(
        Q(title__icontains=query) |
        Q(authors__icontains=query) |
        Q(journal__icontains=query) |
        Q(abstract__icontains=query)
    ).order_by('-year')


def _search_research_projects(query):
    return ResearchProject.objects.filter(
        Q(title__icontains=query) | Q(description__icontains=query)
    ).order_by('title')


def _search_teaching_resources(query):
    return TeachingResource.objects.filter(
        Q(title__icontains=query) |
        Q(course__icontains=query) |
        Q(description__icontains=query)
    ).order_by('course', 'title')


def search_results(request):
    """
    Full search results page. Deliberately reuses the real card
    partials (book_card, publication_card, research_card,
    resource_card) grouped by type, rather than a separate
    lightweight rendering — results look and behave identically
    to browsing each section directly, no second design language
    invented just for search.
    """
    query = request.GET.get('q', '').strip()
    query_too_short = bool(query) and len(query) < MIN_QUERY_LENGTH

    books = publications = research_projects = teaching_resources = []

    if query and not query_too_short:
        books = list(_search_books(query))
        publications = list(_search_publications(query))
        research_projects = list(_search_research_projects(query))
        teaching_resources = list(_search_teaching_resources(query))

    total_results = len(books) + len(publications) + len(research_projects) + len(teaching_resources)

    context = {
        'query': query,
        'query_too_short': query_too_short,
        'books': books,
        'publications': publications,
        'research_projects': research_projects,
        'teaching_resources': teaching_resources,
        'total_results': total_results,
    }
    return render(request, 'home/search_results.html', context)


def search_live(request):
    """
    AJAX endpoint powering the navbar dropdown. Returns a rendered
    HTML fragment (not JSON) — Alpine drops it straight into the
    dropdown via x-html, no client-side templating needed.

    Deliberately lightweight (title + one line of meta, no images) —
    a card built for a 3-column grid is the wrong shape for a
    384px popover. Full cards are what search_results() is for.
    """
    query = request.GET.get('q', '').strip()
    query_too_short = bool(query) and len(query) < MIN_QUERY_LENGTH
    groups = []

    if query and not query_too_short:
        books = _search_books(query)
        publications = _search_publications(query)
        projects = _search_research_projects(query)
        resources = _search_teaching_resources(query)

        pub_search_url = f"{reverse('publications:publication_list')}?q={quote_plus(query)}"

        groups = [
            {
                'label': 'Books',
                'count': books.count(),
                'items': [
                    {
                        'title': b.title,
                        'url': reverse('books:book_detail', args=[b.slug]),
                        'meta': b.subtitle or b.category,
                    }
                    for b in books[:LIVE_RESULTS_PER_CATEGORY]
                ],
            },
            {
                'label': 'Publications',
                'count': publications.count(),
                'items': [
                    {
                        'title': p.title,
                        'url': pub_search_url,
                        'meta': f"{p.journal} · {p.year}" if p.journal else str(p.year),
                    }
                    for p in publications[:LIVE_RESULTS_PER_CATEGORY]
                ],
            },
            {
                'label': 'Research Projects',
                'count': projects.count(),
                'items': [
                    {
                        'title': proj.title,
                        'url': f"{reverse('research:research_list')}#project-{proj.pk}",
                        'meta': proj.get_status_display(),
                    }
                    for proj in projects[:LIVE_RESULTS_PER_CATEGORY]
                ],
            },
            {
                'label': 'Teaching Resources',
                'count': resources.count(),
                'items': [
                    {
                        'title': r.title,
                        'url': f"{reverse('research:teaching_list')}#resource-{r.pk}",
                        'meta': r.course,
                    }
                    for r in resources[:LIVE_RESULTS_PER_CATEGORY]
                ],
            },
        ]

    total_results = sum(g['count'] for g in groups)

    context = {
        'query': query,
        'query_too_short': query_too_short,
        'groups': groups,
        'total_results': total_results,
        'search_results_url': f"{reverse('home:search_results')}?q={quote_plus(query)}",
    }
    return render(request, 'partials/search_dropdown.html', context)
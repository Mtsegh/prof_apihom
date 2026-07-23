from django.shortcuts import render

from django.shortcuts import render

from .models import Achievement


def achievement_list(request):
    """
    Achievements page: awards, recognitions, invited talks, conferences,
    certifications, and professional honors — timeline layout with
    client-side category filtering (Alpine.js, no page reload needed
    since this dataset is small enough to filter in the browser).

    Assumed Achievement model fields (unchanged from Phase 2, where
    this model was first referenced):
      title                 — CharField
      date                  — DateField (kept as DateField, not a bare
                               year int, to stay consistent with the
                               home.views.home query from Phase 2:
                               Achievement.objects.order_by('-date'))
      category              — CharField, choices=CATEGORY_CHOICES (below)
      issuing_organization  — CharField, blank=True
      description           — TextField, blank=True
    """
    context = {
        'achievements': Achievement.objects.all().order_by('-date'),
        'categories': [
            ('award', 'Awards'),
            ('recognition', 'Recognitions'),
            ('invited_talk', 'Invited Talks'),
            ('conference', 'Conferences'),
            ('certification', 'Certifications'),
            ('honor', 'Professional Honors'),
        ],
    }
    return render(request, 'achievements/achievements.html', context)

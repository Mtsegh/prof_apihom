from django.shortcuts import render

from django.shortcuts import render

from .models import (
    ResearchInterest,
    ResearchProject,
    Collaborator,
    Grant,
    Dataset,
    TeachingResource,
)


def research_list(request):
    """
    Research page: interests, current/past projects, collaborators,
    grants, and datasets/downloads — all pulled dynamically.

    Assumed model fields:
      ResearchInterest  — title, short_description, order
                          (already referenced by home.views.home in Phase 2 —
                           same model, no changes needed there)
      ResearchProject   — title, description, status (choices:
                            [('ongoing', 'Ongoing'), ('completed', 'Completed')]),
                            start_date, end_date (null=True, blank=True — ongoing
                            projects won't have one yet), funding_source (blank=True)
      Collaborator      — name, affiliation (blank=True), photo (blank=True),
                            url (blank=True — link to their own page/profile)
      Grant             — title, funding_body, amount (CharField, blank=True —
                            see note below on why this isn't a DecimalField),
                            year
      Dataset           — title, description (blank=True),
                            file (FileField, blank=True, null=True),
                            external_url (blank=True — for datasets hosted
                            elsewhere, e.g. a repository), published_date
    """
    context = {
        'research_interests': ResearchInterest.objects.all().order_by('order'),
        'current_projects': ResearchProject.objects.filter(status='ongoing').order_by('-start_date'),
        'past_projects': ResearchProject.objects.filter(status='completed').order_by('-end_date'),
        'collaborators': Collaborator.objects.all().order_by('name'),
        'grants': Grant.objects.all().order_by('-year'),
        'datasets': Dataset.objects.all().order_by('-published_date'),
    }
    return render(request, 'research/research.html', context)


def teaching_list(request):
    """
    Teaching Resources page: downloadable materials grouped by course.

    Assumed TeachingResource model fields:
      title        — CharField
      course       — CharField (e.g. "MEE 212: Engineering Materials")
      semester     — CharField, blank=True (e.g. "First Semester 2025/2026")
      description  — TextField, blank=True
      file         — FileField, blank=True, null=True
                      (file size is rendered via Django's built-in
                      `filesizeformat` filter on file.size — no separate
                      stored field needed for that)
      order        — PositiveSmallIntegerField, default=0

    Ordered by course first so {% regroup %} in the template can
    cluster resources under a per-course heading — this only works
    correctly if items sharing a course are adjacent in the queryset,
    which is what this ordering guarantees.
    """
    resources = TeachingResource.objects.all().order_by('course', 'order')
    context = {'resources': resources}
    return render(request, 'research/teaching.html', context)

from django.shortcuts import render

from django.shortcuts import render

from research.models import ResearchInterest  # reused, not duplicated — see note below

from .models import AboutContent, Education, CareerMilestone, Membership, Skill


def about(request):
    """
    About page: biography, education, academic journey, teaching philosophy,
    research interests, memberships, career timeline, and skills.

    Assumed models (new — all live in the `about` app):

      AboutContent (singleton, like home.Profile — fetched via .first())
        full_bio             — TextField (the long-form version;
                                 Profile.short_bio from Phase 2 remains
                                 the homepage teaser, this is the full text)
        academic_journey      — TextField, blank=True (short narrative,
                                 shown above the career timeline)
        teaching_philosophy   — TextField, blank=True

      Education
        institution   — CharField
        degree        — CharField (e.g. "PhD, Materials and Metallurgical Engineering")
        start_year    — PositiveSmallIntegerField, null=True, blank=True
        end_year      — PositiveSmallIntegerField
        order         — PositiveSmallIntegerField, default=0
        Ordered by -end_year: most advanced/recent qualification shown
        first, which is the convention on academic profile pages —
        not the same as the CV's own chronological listing order.

      CareerMilestone (the "Timeline of career")
        title         — CharField (role/position)
        organization  — CharField
        start_year    — PositiveSmallIntegerField
        end_year      — PositiveSmallIntegerField, null=True, blank=True
                         (blank = current position)
        description   — TextField, blank=True
        Ordered ascending by start_year — this one tells a chronological
        "rise" story, opposite direction from Education above.

      Membership
        organization  — CharField
        role          — CharField, blank=True
        year_joined   — PositiveSmallIntegerField, null=True, blank=True

      Skill
        name      — CharField
        category  — CharField, blank=True (e.g. "Technical", "Software")
    """
    context = {
        'about_content': AboutContent.objects.first(),
        'education': Education.objects.all().order_by('-end_year'),
        'career_milestones': CareerMilestone.objects.all().order_by('start_year'),
        'memberships': Membership.objects.all().order_by('year_joined'),
        'skills': Skill.objects.all().order_by('category', 'name'),
        'research_interests': ResearchInterest.objects.all().order_by('order'),
    }
    return render(request, 'about/about.html', context)

"""
Seed data — core app
=====================
Source: prof. IhomCURRICULUM VITAE.doc 2023.docx
Models seeded: Profile, SocialLink, Statistic  (core/models.py)

Place this file at:
    core/management/commands/seed_core.py

(core/management/__init__.py and core/management/commands/__init__.py
must also exist — both included alongside this file.)

Run with:
    python manage.py seed_core
"""

from django.core.management.base import BaseCommand
from django.db import transaction

from core.models import Profile, SocialLink, Statistic


class Command(BaseCommand):
    help = "Seed the core app: Profile, SocialLink, and Statistic records for Prof. A.P. Ihom."

    @transaction.atomic
    def handle(self, *args, **options):
        profile = self.seed_profile()
        self.seed_social_links(profile)
        self.seed_statistics()
        self.stdout.write(self.style.SUCCESS("core: seeding complete."))

    def seed_profile(self):
        profile = Profile.load()
        profile.full_name = "Aondona Paul Ihom"
        profile.short_name = "Prof. A. P. Ihom"

        # Headline title: the CV's own self-description / stated Area of
        # Specialization, used on its own. Per instruction, this is NOT
        # combined with department — department is applied separately,
        # wherever the affiliation itself needs to be shown (e.g.
        # "Professor, {{ profile.department }}").
        profile.title = "Professor of Materials, Production and Industrial Engineering"
        profile.department = "Mechanical and Aerospace Engineering"
        profile.university = "University of Uyo"

        profile.short_bio = (
            "Professor Aondona Paul Ihom is a researcher and academician in "
            "Materials, Production and Industrial Engineering at the "
            "University of Uyo. His more than 22 years of industrial "
            "experience have shaped a research career spanning foundry "
            "technology, corrosion science, and advanced materials "
            "development."
        )

        # TODO: no personal/academic quote found in the CV — left blank
        # until supplied.
        profile.quote = ""

        # TODO: no portrait image available in the source document —
        # profile.portrait intentionally left unset.

        profile.save()
        return profile

    def seed_social_links(self, profile):
        # NOTE: the CV names these three scholarly platforms by name only,
        # with no profile URLs given. Each is seeded with the platform's
        # bare homepage as an explicit, flagged placeholder — replace with
        # the real profile URL. "Website" is the one real, CV-sourced
        # link (not a placeholder).
        social_links = [
            {
                "label": "Google Scholar",
                "icon": "google-scholar",
                "url": "https://scholar.google.com/",  # TODO: replace with real profile URL
                "order": 0,
            },
            {
                "label": "ResearchGate",
                "icon": "researchgate",
                "url": "https://www.researchgate.net/",  # TODO: replace with real profile URL
                "order": 1,
            },
            {
                "label": "Academia.edu",
                "icon": "academia",
                "url": "https://www.academia.edu/",  # TODO: replace with real profile URL
                "order": 2,
            },
            {
                "label": "Website",
                "icon": "globe",
                "url": "https://www.profapihom.com",
                "order": 3,
            },
        ]
        for link in social_links:
            label = link.pop("label")
            SocialLink.objects.update_or_create(
                profile=profile,
                label=label,
                defaults=link,
            )

    def seed_statistics(self):
        # Hybrid design: Publications, Books, and Research Projects are
        # deliberately NOT stored here. Once the books/publications/research
        # apps are seeded, the home view should compute these live —
        # Publication.objects.count(), Book.objects.count(),
        # ResearchProject.objects.count() — so the homepage can never
        # drift out of sync with the actual records.
        #
        # Years of Experience uses the CV's own stated figure verbatim
        # ("sound industrial experience of over 22 years") rather than a
        # computed span, since the CV's own career dates don't reconcile
        # to a single clean start year.
        #
        # Citations is intentionally left unseeded — not stated anywhere
        # in the CV. Add once a real figure is available from Google
        # Scholar / ResearchGate.
        Statistic.objects.update_or_create(
            label="Years of Experience",
            defaults={
                "value": 22,
                "suffix": "+",
                "order": 0,
            },
        )

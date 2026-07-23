from django.db import models
from django.core.exceptions import ValidationError
from home.models import SingletonModel, TimeStampedModel


class AboutContent(SingletonModel, TimeStampedModel):
    """One row — the long-form content blocks on the About page."""
    full_bio = models.TextField(
        blank=True,
        help_text="Full biography — this is the long-form version. "
                   "Profile.short_bio remains the homepage teaser."
    )
    academic_journey = models.TextField(
        blank=True, help_text="Short narrative shown above the career timeline."
    )
    teaching_philosophy = models.TextField(blank=True)

    class Meta:
        verbose_name = "About Page Content"
        verbose_name_plural = "About Page Content"

    def __str__(self):
        return "About Page Content"


class Education(TimeStampedModel):
    """
    Ordered -end_year by default (most advanced degree first — PhD,
    then Masters, then Bachelor's) — the academic-site convention, not
    necessarily the order a CV lists them in.
    """
    institution = models.CharField(max_length=200)
    degree = models.CharField(
        max_length=200,
        help_text="e.g. 'PhD, Materials and Metallurgical Engineering'"
    )
    start_year = models.PositiveSmallIntegerField(null=True, blank=True)
    end_year = models.PositiveSmallIntegerField()
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['-end_year']

    def __str__(self):
        return f"{self.degree} — {self.institution}"

    def clean(self):
        if self.start_year and self.end_year and self.start_year > self.end_year:
            raise ValidationError("Start year can't be after end year.")


class CareerMilestone(TimeStampedModel):
    """
    The "Timeline of career" section — ordered ascending (oldest first),
    the opposite direction from Education, since a career timeline reads
    better as a chronological rise.
    """
    title = models.CharField(max_length=150)  # role/position
    organization = models.CharField(max_length=200)
    start_year = models.PositiveSmallIntegerField()
    end_year = models.PositiveSmallIntegerField(
        null=True, blank=True, help_text="Leave blank for a current position."
    )
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['start_year']

    def __str__(self):
        return f"{self.title}, {self.organization} ({self.start_year})"

    def clean(self):
        if self.end_year and self.start_year > self.end_year:
            raise ValidationError("Start year can't be after end year.")


class Membership(TimeStampedModel):
    organization = models.CharField(max_length=200)
    role = models.CharField(max_length=150, blank=True)
    year_joined = models.PositiveSmallIntegerField(null=True, blank=True)

    class Meta:
        ordering = ['year_joined']

    def __str__(self):
        return self.organization


class Skill(TimeStampedModel):
    name = models.CharField(max_length=100)
    category = models.CharField(
        max_length=100, blank=True, help_text="e.g. 'Technical', 'Software'"
    )

    class Meta:
        ordering = ['category', 'name']

    def __str__(self):
        return self.name


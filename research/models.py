from django.db import models
from cloudinary.models import CloudinaryField
from django.urls import reverse
from django.core.exceptions import ValidationError
from home.models import TimeStampedModel
from cloudinary.models import CloudinaryField


class ResearchInterest(TimeStampedModel):
    title = models.CharField(max_length=150)
    short_description = models.TextField(blank=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class ResearchProject(TimeStampedModel):

    class ProjectStatus(models.TextChoices):
        ONGOING = 'ongoing', 'Ongoing'
        COMPLETED = 'completed', 'Completed'

    title = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=20, choices=ProjectStatus.choices, default=ProjectStatus.ONGOING
    )
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(
        null=True, blank=True,
        help_text="Leave blank for ongoing projects."
    )
    funding_source = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ['-start_date']
        indexes = [models.Index(fields=['status'])]

    def __str__(self):
        return self.title

    def clean(self):
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValidationError("Start date can't be after end date.")

    def get_absolute_url(self):
        """
        No dedicated detail page for research projects — this resolves
        to an anchor on the research list page, matching the #project-N
        IDs already rendered by research_card.html. Lets core.views'
        search functions call proj.get_absolute_url() instead of
        rebuilding the anchor string by hand.
        """
        return f"{reverse('research:research_list')}#project-{self.pk}"


class Collaborator(TimeStampedModel):
    name = models.CharField(max_length=150)
    affiliation = models.CharField(max_length=200, blank=True)
    photo = CloudinaryField(folder='research/collaborators/', blank=True)
    url = models.URLField(blank=True, help_text="Link to their own page or profile.")

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Grant(TimeStampedModel):
    """
    `amount` is a CharField, not a DecimalField — most grants on record
    are identified by sponsor only ("TETFUND Sponsored"), without a
    disclosed figure. A required numeric field would force fake data
    into records that genuinely don't have a number to report.
    """
    title = models.CharField(max_length=250)
    funding_body = models.CharField(max_length=200)
    amount = models.CharField(
        max_length=100, blank=True,
        help_text="Free text — e.g. '₦2,000,000' or 'Undisclosed'."
    )
    year = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ['-year']

    def __str__(self):
        return f"{self.title} ({self.year})"


class Dataset(TimeStampedModel):
    title = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    file = CloudinaryField(resource_type="raw", folder='research/datasets/', blank=True, null=True)
    external_url = models.URLField(
        blank=True, help_text="For datasets hosted elsewhere, e.g. a repository."
    )
    published_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['-published_date']

    def __str__(self):
        return self.title


class TeachingResource(TimeStampedModel):
    title = models.CharField(max_length=250)
    course = models.CharField(
        max_length=150, help_text="e.g. 'MEE 212: Engineering Materials'"
    )
    semester = models.CharField(
        max_length=100, blank=True, help_text="e.g. 'First Semester 2025/2026'"
    )
    description = models.TextField(blank=True)
    file = CloudinaryField(resource_type="raw",folder='research/teaching/', blank=True, null=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['course', 'order']

    def __str__(self):
        return f"{self.title} ({self.course})"

    def get_absolute_url(self):
        """Anchor on the teaching list page — see ResearchProject.get_absolute_url."""
        return f"{reverse('research:teaching_list')}#resource-{self.pk}"

from django.db import models
from django.core.validators import MinValueValidator, FileExtensionValidator
from home.models import TimeStampedModel
from cloudinary.models import CloudinaryField


class Publication(TimeStampedModel):

    class PublicationType(models.TextChoices):
        JOURNAL = 'journal', 'Journal Article'
        CONFERENCE = 'conference', 'Conference Proceedings'
        REVIEW = 'review', 'Review Article'

    title = models.CharField(max_length=400)
    authors = models.CharField(
        max_length=500, help_text="e.g. 'Ihom, A.P., Offiong, A.'"
    )
    journal = models.CharField(
        max_length=300, blank=True,
        help_text="Also holds 'Proceedings of...' for conference entries."
    )
    publication_type = models.CharField(
        max_length=20, choices=PublicationType.choices,
        default=PublicationType.JOURNAL
    )
    year = models.PositiveSmallIntegerField(validators=[MinValueValidator(1900)])
    doi = models.CharField(
        max_length=100, blank=True,
        help_text="Bare DOI only, e.g. '10.53294/ijfetr.2023.4.2.0015' — "
                   "no 'https://doi.org/' prefix. Templates prepend it."
    )
    abstract = models.TextField(blank=True)
    pdf_file = CloudinaryField(
        folder='publications/pdfs/', blank=True, null=True,
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])]
    )
    external_url = models.URLField(
        blank=True,
        help_text="Fallback link (journal page, ResearchGate, etc.) — "
                   "shown only when pdf_file is empty."
    )

    class Meta:
        ordering = ['-year', 'title']
        indexes = [
            models.Index(fields=['year']),
            models.Index(fields=['publication_type']),
        ]

    def __str__(self):
        return f"{self.title} ({self.year})"

    @property
    def doi_url(self):
        return f"https://doi.org/{self.doi}" if self.doi else None



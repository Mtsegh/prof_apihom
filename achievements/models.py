from django.db import models
from home.models import TimeStampedModel


class Achievement(TimeStampedModel):

    class AchievementCategory(models.TextChoices):
        AWARD = 'award', 'Award'
        RECOGNITION = 'recognition', 'Recognition'
        INVITED_TALK = 'invited_talk', 'Invited Talk'
        CONFERENCE = 'conference', 'Conference'
        CERTIFICATION = 'certification', 'Certification'
        HONOR = 'honor', 'Professional Honor'

    title = models.CharField(max_length=250)
    date = models.DateField(
        help_text="Full date required — for year-only facts, use the "
                   "1st of January (e.g. 2011-01-01). Templates display "
                   "just the year via |date:\"Y\"."
    )
    category = models.CharField(max_length=20, choices=AchievementCategory.choices)
    issuing_organization = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['-date']
        indexes = [
            models.Index(fields=['category']),
            models.Index(fields=['date']),
        ]

    def __str__(self):
        return f"{self.title} ({self.date.year})"

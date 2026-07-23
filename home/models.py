from django.db import models
from cloudinary.models import CloudinaryField


class TimeStampedModel(models.Model):
    """
    Abstract base adding created/updated timestamps to any model that
    inherits it. Every concrete model in this project uses this instead
    of redeclaring the same two fields — free audit trail, no repetition.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SingletonModel(models.Model):
    """
    Abstract base for "exactly one row" models — Profile, AboutContent,
    ContactInfo. Every subclass gets save()/delete()/load() for free
    instead of each one reimplementing the same pk=1 trick independently.

    save() always overwrites the same row (pk=1), so accidentally saving
    a "new" instance in code or in a bad migration can't create a second
    row. delete() is a no-op — the only row is never removable through
    the ORM. load() is the one method callers actually use.
    """
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass  # block accidental deletion of the only row

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj




class Profile(SingletonModel, TimeStampedModel):
    """
        One row holds the professor's identity — pulled into every template
        via core.context_processors.profile, not fetched per-view.
        """
    full_name = models.CharField(max_length=150, default="Prof. A. P. Ihom")
    short_name = models.CharField(
        max_length=60, blank=True,
        help_text="Compact form for the navbar logo, e.g. 'Prof. A. P. Ihom'. "
                   "Falls back to full_name in templates if left blank."
    )
    title = models.CharField(
        max_length=150, blank=True,
        help_text="e.g. 'Professor of Materials and Metallurgical Engineering'"
    )
    department = models.CharField(max_length=150, blank=True)
    university = models.CharField(max_length=150, blank=True)

    short_bio = models.TextField(
        blank=True,
        help_text="Homepage hero teaser and meta-description fallback — "
                   "a few sentences, not the full biography (that's "
                   "about.AboutContent.full_bio)."
    )
    portrait = CloudinaryField('Portrait', folder='profile/', blank=True)

    quote = models.CharField(
        max_length=300, blank=True,
        help_text="Shown in the footer — an academic motto or favorite quote."
    )

    class Meta:
            verbose_name = "Profile"
            verbose_name_plural = "Profile"  # singular on purpose — there's only one
    

    def __str__(self):
        return self.full_name or "Site Profile"


class SocialLink(models.Model):
    """
    One row per social/profile link (Google Scholar, ResearchGate,
    Academia.edu). A separate model rather than a JSONField, so it can
    be added/reordered/removed from a normal admin inline instead of
    hand-editing a JSON blob.
    """
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='social_links')
    label = models.CharField(max_length=60)   # e.g. "Google Scholar"
    url = models.URLField()
    icon = models.CharField(default='user')
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.label


class Statistic(models.Model):
    """
    Homepage stat cards. `value` is numeric (not a display string like
    "200+") so it can drive the count-up animation directly —
    `suffix` holds the "+" or "%" the template appends after counting.
    """
    label = models.CharField(max_length=60)          # e.g. "Publications"
    value = models.PositiveIntegerField()            # e.g. 200
    suffix = models.CharField(max_length=10, blank=True)  # e.g. "+"
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.value}{self.suffix} {self.label}"
    
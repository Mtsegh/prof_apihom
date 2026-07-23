from django.db import models
from django.utils import timezone


# ── ContactInfo ──────────────────────────────────────────────────────────────

class ContactInfo(models.Model):
    # Office address
    department      = models.CharField(max_length=255, default="Department of Engineering")
    university      = models.CharField(max_length=255, default="University of Cambridge")
    street          = models.CharField(max_length=255, default="Trumpington Street")
    postcode        = models.CharField(max_length=20,  default="CB2 1PZ")
    city            = models.CharField(max_length=100, default="Cambridge")
    country         = models.CharField(max_length=100, default="United Kingdom")

    # Direct contact
    email           = models.EmailField(default="paulaihiom@uniuyo.edu.ng")
    email_note      = models.CharField(max_length=255, blank=True, default="Response within 3–5 working days")
    phone           = models.CharField(max_length=50, blank=True, default="+234 803 333 444")
    phone_note      = models.CharField(max_length=255, blank=True, default="Mon – Fri, 09:00 – 17:00 GMT")

    # Office hours
    office_hours_days  = models.CharField(max_length=100, blank=True, default="Tuesday & Thursday")
    office_hours_times = models.CharField(max_length=100, blank=True, default="14:00 – 16:00 (term time only)")
    office_hours_note  = models.CharField(max_length=255, blank=True, default="Book via email in advance")

    # Google Maps link shown on the map placeholder
    map_embed_url = models.URLField(
            blank=True, help_text="A Google Maps embed src URL."
        )

    class Meta:
        verbose_name        = "Contact Info"
        verbose_name_plural = "Contact Info"

    def __str__(self):
        return f"{self.department} — {self.email}"


# ── SocialLink ────────────────────────────────────────────────────────────────



# ── ContactCategory ───────────────────────────────────────────────────────────

class ContactCategory(models.Model):
    value   = models.SlugField(max_length=50, unique=True)
    label   = models.CharField(max_length=150)
    order   = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering    = ["order", "id"]
        verbose_name        = "Contact Category"
        verbose_name_plural = "Contact Categories"

    def __str__(self):
        return self.label


# ── FAQ ───────────────────────────────────────────────────────────────────────

class FAQ(models.Model):
    """
    A single FAQ item. The 'category' field maps to the faqTabs keys:
    all | phd | research | books | general
    """
    CATEGORY_CHOICES = [
        ("phd",      "PhD & Study"),
        ("research", "Research"),
        ("books",    "Books"),
        ("general",  "General"),
    ]

    category    = models.CharField(max_length=20, choices=CATEGORY_CHOICES, db_index=True)
    question    = models.CharField(max_length=500)
    answer      = models.TextField()
    order       = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["category", "order", "id"]

    def __str__(self):
        return f"[{self.get_category_display()}] {self.question[:80]}"


# ── ContactMessage ────────────────────────────────────────────────────────────

class ContactMessage(models.Model):
    """
    Stores every submitted contact form entry.
    The view saves to this model and then sends an email notification.
    """
    STATUS_CHOICES = [
        ("new",      "New"),
        ("read",     "Read"),
        ("replied",  "Replied"),
        ("archived", "Archived"),
    ]

    name            = models.CharField(max_length=255)
    email           = models.EmailField()
    affiliation     = models.CharField(max_length=255, blank=True)
    category        = models.CharField(max_length=50, blank=True)   # ContactCategory.value
    subject         = models.CharField(max_length=500)
    message         = models.TextField()
    consent         = models.BooleanField(default=False)

    submitted_at    = models.DateTimeField(default=timezone.now)
    ip_address      = models.GenericIPAddressField(blank=True, null=True)
    status          = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")

    class Meta:
        ordering = ["-submitted_at"]

    def __str__(self):
        return f"{self.name} <{self.email}> — {self.subject[:60]}"
    
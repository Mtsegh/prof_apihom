from django.db import models
from cloudinary.models import CloudinaryField
from django.urls import reverse
from django.utils.text import slugify
from django.core.validators import MinValueValidator
from home.models import TimeStampedModel
from cloudinary.models import CloudinaryField

class Book(TimeStampedModel):

    class AvailabilityChoices(models.TextChoices):
        IN_STOCK = 'in_stock', 'In Stock'
        PREORDER = 'preorder', 'Pre-order'
        OUT_OF_STOCK = 'out_of_stock', 'Out of Stock'

    class CurrencyChoices(models.TextChoices):
        """
        Kept in sync with books/templatetags/currency_extras.py's
        CURRENCY_SYMBOLS dict — same five codes on both sides.
        """
        NGN = 'NGN', 'Nigerian Naira (₦)'
        USD = 'USD', 'US Dollar ($)'
        GBP = 'GBP', 'British Pound (£)'
        EUR = 'EUR', 'Euro (€)'
        INR = 'INR', 'Indian Rupee (₹)'

    title = models.CharField(max_length=250)
    subtitle = models.CharField(max_length=250, blank=True)
    slug = models.SlugField(unique=True, blank=True, max_length=270)
    cover = CloudinaryField(folder='books/covers/', blank=True, null=True)

    price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True,
        validators=[MinValueValidator(0)]
    )
    currency = models.CharField(
        max_length=3, choices=CurrencyChoices.choices, default=CurrencyChoices.NGN
    )

    description = models.TextField(blank=True)
    isbn = models.CharField(max_length=20, blank=True)
    category = models.CharField(max_length=100, blank=True)
    publisher = models.CharField(max_length=200, blank=True)
    availability = models.CharField(
        max_length=20, choices=AvailabilityChoices.choices,
        default=AvailabilityChoices.IN_STOCK
    )
    purchase_url = models.URLField(blank=True)

    featured_order = models.PositiveSmallIntegerField(
        null=True, blank=True, unique=True,
        help_text="Set a number to feature this book on the homepage — "
                   "the number controls display order. Leave blank to "
                   "keep it off the homepage."
    )
    published_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['-published_date', 'title']
        indexes = [
            models.Index(fields=['featured_order']),
            models.Index(fields=['category']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Book.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                counter += 1
                slug = f"{base_slug}-{counter}"
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('books:book_detail', kwargs={'slug': self.slug})




    
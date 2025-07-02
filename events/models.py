# Updating the Event model to use the admin CKEditor configuration for the description field.
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField
from core.models import District, Category
import uuid

class Event(models.Model):
    title = models.CharField(max_length=200, verbose_name="कार्यक्रम नाम")
    slug = models.SlugField(unique=True, blank=True)
    description = RichTextUploadingField(verbose_name="विवरण")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="श्रेणी")
    district = models.ForeignKey(District, on_delete=models.CASCADE, verbose_name="जिला")
    venue = models.CharField(max_length=200, verbose_name="स्थान")
    event_date = models.DateTimeField(verbose_name="कार्यक्रम तिथि")
    registration_deadline = models.DateTimeField(verbose_name="पंजीकरण अंतिम तिथि")
    registration_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="पंजीकरण शुल्क")
    max_participants = models.PositiveIntegerField(default=100, verbose_name="अधिकतम प्रतिभागी")
    is_published = models.BooleanField(default=True, verbose_name="प्रकाशित")
    is_featured = models.BooleanField(default=False, verbose_name="मुख्य कार्यक्रम")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "कार्यक्रम"
        verbose_name_plural = "कार्यक्रम"
        ordering = ['event_date']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('events:detail', kwargs={'pk': self.pk})

    @property
    def registered_count(self):
        return self.registrations.filter(is_confirmed=True).count()

    @property
    def available_spots(self):
        return self.max_participants - self.registered_count

    @property
    def registration_percentage(self):
        if self.max_participants > 0:
            return round((self.registered_count / self.max_participants) * 100, 1)
        return 0

class EventRegistration(models.Model):
    GENDER_CHOICES = [
        ('M', 'पुरुष'),
        ('F', 'महिला'),
        ('O', 'अन्य'),
    ]

    event = models.ForeignKey(Event, related_name='registrations', on_delete=models.CASCADE)
    registration_number = models.CharField(max_length=20, unique=True, blank=True)
    full_name = models.CharField(max_length=100, verbose_name="पूरा नाम")
    email = models.EmailField(verbose_name="ईमेल")
    phone = models.CharField(max_length=15, verbose_name="फोन नंबर")
    age = models.PositiveIntegerField(verbose_name="आयु")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="लिंग")
    address = models.TextField(verbose_name="पता")
    occupation = models.CharField(max_length=100, verbose_name="व्यवसाय")
    district = models.ForeignKey(District, on_delete=models.CASCADE, verbose_name="जिला")
    is_confirmed = models.BooleanField(default=True, verbose_name="पुष्ट")
    registration_date = models.DateTimeField(auto_now_add=True)
    payment_status = models.BooleanField(default=False, verbose_name="भुगतान स्थिति")

    class Meta:
        verbose_name = "पंजीकरण"
        verbose_name_plural = "पंजीकरण"
        ordering = ['-registration_date']

    def __str__(self):
        return f"{self.full_name} - {self.event.title}"

    def save(self, *args, **kwargs):
        if not self.registration_number:
            self.registration_number = f"REG{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

class EventImage(models.Model):
    event = models.ForeignKey(Event, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='event_images/', verbose_name="छवि")
    caption = models.CharField(max_length=200, blank=True, verbose_name="कैप्शन")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "कार्यक्रम छवि"
        verbose_name_plural = "कार्यक्रम छवियां"

    def __str__(self):
        return f"{self.event.title} - Image"
```

```python
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from core.models import District, Category
import uuid

class Event(models.Model):
    title = models.CharField(max_length=200, verbose_name="कार्यक्रम नाम")
    slug = models.SlugField(unique=True, blank=True)
    description = RichTextField(verbose_name="विवरण", config_name='admin')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="श्रेणी")
    district = models.ForeignKey(District, on_delete=models.CASCADE, verbose_name="जिला")
    venue = models.CharField(max_length=200, verbose_name="स्थान")
    event_date = models.DateTimeField(verbose_name="कार्यक्रम तिथि")
    registration_deadline = models.DateTimeField(verbose_name="पंजीकरण अंतिम तिथि")
    registration_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="पंजीकरण शुल्क")
    max_participants = models.PositiveIntegerField(default=100, verbose_name="अधिकतम प्रतिभागी")
    is_published = models.BooleanField(default=True, verbose_name="प्रकाशित")
    is_featured = models.BooleanField(default=False, verbose_name="मुख्य कार्यक्रम")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "कार्यक्रम"
        verbose_name_plural = "कार्यक्रम"
        ordering = ['event_date']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('events:detail', kwargs={'pk': self.pk})

    @property
    def registered_count(self):
        return self.registrations.filter(is_confirmed=True).count()

    @property
    def available_spots(self):
        return self.max_participants - self.registered_count

    @property
    def registration_percentage(self):
        if self.max_participants > 0:
            return round((self.registered_count / self.max_participants) * 100, 1)
        return 0

class EventRegistration(models.Model):
    GENDER_CHOICES = [
        ('M', 'पुरुष'),
        ('F', 'महिला'),
        ('O', 'अन्य'),
    ]

    event = models.ForeignKey(Event, related_name='registrations', on_delete=models.CASCADE)
    registration_number = models.CharField(max_length=20, unique=True, blank=True)
    full_name = models.CharField(max_length=100, verbose_name="पूरा नाम")
    email = models.EmailField(verbose_name="ईमेल")
    phone = models.CharField(max_length=15, verbose_name="फोन नंबर")
    age = models.PositiveIntegerField(verbose_name="आयु")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="लिंग")
    address = models.TextField(verbose_name="पता")
    occupation = models.CharField(max_length=100, verbose_name="व्यवसाय")
    district = models.ForeignKey(District, on_delete=models.CASCADE, verbose_name="जिला")
    is_confirmed = models.BooleanField(default=True, verbose_name="पुष्ट")
    registration_date = models.DateTimeField(auto_now_add=True)
    payment_status = models.BooleanField(default=False, verbose_name="भुगतान स्थिति")

    class Meta:
        verbose_name = "पंजीकरण"
        verbose_name_plural = "पंजीकरण"
        ordering = ['-registration_date']

    def __str__(self):
        return f"{self.full_name} - {self.event.title}"

    def save(self, *args, **kwargs):
        if not self.registration_number:
            self.registration_number = f"REG{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

class EventImage(models.Model):
    event = models.ForeignKey(Event, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='event_images/', verbose_name="छवि")
    caption = models.CharField(max_length=200, blank=True, verbose_name="कैप्शन")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "कार्यक्रम छवि"
        verbose_name_plural = "कार्यक्रम छवियां"

    def __str__(self):
        return f"{self.event.title} - Image"
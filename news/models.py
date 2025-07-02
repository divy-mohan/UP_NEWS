from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField
from core.models import District, Category

class News(models.Model):
    title = models.CharField(max_length=200, verbose_name="शीर्षक")
    slug = models.SlugField(unique=True, blank=True)
    summary = models.TextField(max_length=500, verbose_name="सारांश")
    content = RichTextUploadingField(verbose_name="मुख्य सामग्री", config_name='admin')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="श्रेणी")
    district = models.ForeignKey(District, on_delete=models.CASCADE, verbose_name="जिला")
    author = models.CharField(max_length=100, default="Admin", verbose_name="लेखक")
    date_posted = models.DateTimeField(auto_now_add=True, verbose_name="प्रकाशन तिथि")
    last_updated = models.DateTimeField(auto_now=True, verbose_name="अपडेट तिथि")
    is_published = models.BooleanField(default=True, verbose_name="प्रकाशित")
    is_featured = models.BooleanField(default=False, verbose_name="मुख्य समाचार")
    views_count = models.PositiveIntegerField(default=0, verbose_name="देखे गए")
    likes_count = models.PositiveIntegerField(default=0, verbose_name="पसंद")

    class Meta:
        verbose_name = "समाचार"
        verbose_name_plural = "समाचार"
        ordering = ['-date_posted']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('news:detail', kwargs={'pk': self.pk})

    def increment_views(self):
        self.views_count += 1
        self.save(update_fields=['views_count'])

class NewsImage(models.Model):
    news = models.ForeignKey(News, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='news_images/', verbose_name="छवि")
    caption = models.CharField(max_length=200, blank=True, verbose_name="कैप्शन")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "समाचार छवि"
        verbose_name_plural = "समाचार छवियां"

    def __str__(self):
        return f"{self.news.title} - Image"

class Comment(models.Model):
    news = models.ForeignKey(News, related_name='comments', on_delete=models.CASCADE)
    author_name = models.CharField(max_length=100, verbose_name="नाम")
    author_email = models.EmailField(verbose_name="ईमेल")
    content = models.TextField(verbose_name="टिप्पणी")
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=True, verbose_name="स्वीकृत")

    class Meta:
        verbose_name = "टिप्पणी"
        verbose_name_plural = "टिप्पणियां"
        ordering = ['-created_at']

    def __str__(self):
        return f"Comment by {self.author_name} on {self.news.title}"
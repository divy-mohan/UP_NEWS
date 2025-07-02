from django.db import models

class District(models.Model):
    name = models.CharField(max_length=100, verbose_name="जिला नाम")
    slug = models.SlugField(unique=True)
    is_active = models.BooleanField(default=True, verbose_name="सक्रिय")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "जिला"
        verbose_name_plural = "जिले"
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="श्रेणी नाम")
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, verbose_name="विवरण")
    is_active = models.BooleanField(default=True, verbose_name="सक्रिय")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "श्रेणी"
        verbose_name_plural = "श्रेणियां"
        ordering = ['name']
    
    def __str__(self):
        return self.name

class SiteSettings(models.Model):
    site_name = models.CharField(max_length=200, default="प्रांतीय युवा प्रकोष्ठ-उत्तर प्रदेश")
    site_description = models.TextField(default="युवाओं के सशक्तिकरण और राष्ट्र निर्माण में योगदान")
    contact_email = models.EmailField(default="info@pranteeyyuva.org")
    contact_phone = models.CharField(max_length=20, default="+91 9415156122")
    contact_address = models.TextField(default="सुल्तानपुर - उत्तर प्रदेश")
    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    whatsapp_number = models.CharField(max_length=20, default="+91 9415156122")
    
    class Meta:
        verbose_name = "साइट सेटिंग्स"
        verbose_name_plural = "साइट सेटिंग्स"
    
    def __str__(self):
        return self.site_name

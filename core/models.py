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

class Banner(models.Model):
    title = models.CharField(max_length=200, verbose_name="बैनर शीर्षक")
    image = models.ImageField(upload_to='banners/', verbose_name="बैनर छवि")
    link = models.URLField(blank=True, verbose_name="लिंक (वैकल्पिक)")
    is_active = models.BooleanField(default=True, verbose_name="सक्रिय")
    order = models.PositiveIntegerField(default=0, verbose_name="क्रम")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "बैनर"
        verbose_name_plural = "बैनर"
        ordering = ['order', '-created_at']
    
    def __str__(self):
        return self.title

class HomepageStats(models.Model):
    active_members = models.PositiveIntegerField(default=0, verbose_name="सक्रिय सदस्य")
    events_held = models.PositiveIntegerField(default=0, verbose_name="आयोजित कार्यक्रम")
    districts_covered = models.PositiveIntegerField(default=0, verbose_name="जिले कवर")
    social_projects = models.PositiveIntegerField(default=0, verbose_name="समाजसेवा परियोजनाएं")

    class Meta:
        verbose_name = "Homepage आकड़े"
        verbose_name_plural = "Homepage आकड़े"

    def __str__(self):
        return "Homepage आकड़े"

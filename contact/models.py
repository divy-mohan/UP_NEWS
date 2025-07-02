from django.db import models

class ContactMessage(models.Model):
    SUBJECT_CHOICES = [
        ('general', 'सामान्य पूछताछ'),
        ('membership', 'सदस्यता'),
        ('event', 'कार्यक्रम संबंधी'),
        ('complaint', 'शिकायत'),
        ('suggestion', 'सुझाव'),
    ]
    
    name = models.CharField(max_length=100, verbose_name="नाम")
    email = models.EmailField(verbose_name="ईमेल")
    phone = models.CharField(max_length=15, blank=True, verbose_name="फोन नंबर")
    subject = models.CharField(max_length=20, choices=SUBJECT_CHOICES, verbose_name="विषय")
    message = models.TextField(verbose_name="संदेश")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="भेजा गया")
    is_read = models.BooleanField(default=False, verbose_name="पढ़ा गया")
    is_replied = models.BooleanField(default=False, verbose_name="जवाब दिया गया")
    reply_message = models.TextField(blank=True, verbose_name="जवाब")
    replied_at = models.DateTimeField(null=True, blank=True, verbose_name="जवाब तिथि")
    
    class Meta:
        verbose_name = "संपर्क संदेश"
        verbose_name_plural = "संपर्क संदेश"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.get_subject_display()}"

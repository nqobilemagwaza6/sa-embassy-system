from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Application(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('UNDER_REVIEW', 'Under Review'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    passport_number = models.CharField(max_length=100)
    nationality = models.CharField(max_length=100)
    destination_country = models.CharField(max_length=100)
    travel_date = models.DateField()

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    admin_comment = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} ({self.passport_number})"


class Document(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    DOC_TYPE_CHOICES = [
        ('PASSPORT', 'Passport'),
        ('ID', 'ID'),
        ('OTHER', 'Other'),
    ]

    doc_type = models.CharField(max_length=20, choices=DOC_TYPE_CHOICES, default='OTHER')
    file = models.FileField(upload_to='documents/%Y/%m/%d/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


class ApplicationStatusEvent(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='status_events')
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    from_status = models.CharField(max_length=20, choices=Application.STATUS_CHOICES)
    to_status = models.CharField(max_length=20, choices=Application.STATUS_CHOICES)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']

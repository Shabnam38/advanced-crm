from django.db import models
from django.core.exceptions import ValidationError


class Lead(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('qualified', 'Qualified'),
        ('lost', 'Lost'),
    ]

    SOURCE_CHOICES = [
        ('website', 'Website'),
        ('referral', 'Referral'),
        ('cold_call', 'Cold Call'),
        ('social_media', 'Social Media'),
        ('other', 'Other'),
    ]

    STATUS_SCORE = {
        'new': 20,
        'contacted': 50,
        'qualified': 80,
        'lost': 0,
    }

    full_name = models.CharField(max_length=150)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    company_name = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES, default='other')
    score = models.PositiveIntegerField(default=20, help_text="Auto-calculated lead score (0-100)")
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Leads"

    def clean(self):
        if self.phone and not self.phone.replace('+', '').replace('-', '').replace(' ', '').isdigit():
            raise ValidationError({'phone': 'Phone number should only contain digits, spaces, "+" or "-".'})

        if not self.email and not self.phone:
            raise ValidationError('A lead must have at least an email or a phone number.')

    def save(self, *args, **kwargs):
        self.score = self.STATUS_SCORE.get(self.status, self.score)
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name
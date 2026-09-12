from django.db import models
from django.core.exceptions import ValidationError
from companies.models import Company
from customers.models import Customer

class Deal(models.Model):
    STAGE_CHOICES = [
        ('prospecting', 'Prospecting'),
        ('proposal', 'Proposal Sent'),
        ('negotiation', 'Negotiation'),
        ('won', 'Won'),
        ('lost', 'Lost'),
    ]

    STAGE_PROBABILITY = {
        'prospecting': 10,
        'proposal': 40,
        'negotiation': 60,
        'won': 100,
        'lost': 0,
    }

    title = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='deals')
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, related_name='deals')
    value = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    stage = models.CharField(max_length=20, choices=STAGE_CHOICES, default='prospecting')
    probability = models.PositiveIntegerField(default=10, help_text="Auto-set based on stage")
    expected_close_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Deals"

    def clean(self):
        if self.value < 0:
            raise ValidationError({'value': 'Deal value cannot be negative.'})

    def save(self, *args, **kwargs):
        self.probability = self.STAGE_PROBABILITY.get(self.stage, self.probability)
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
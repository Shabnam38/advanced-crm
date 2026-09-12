from django.db import models
from leads.models import Lead
from customers.models import Customer

class Interaction(models.Model):
    TYPE_CHOICES = [
        ('call', 'Call'),
        ('email', 'Email'),
        ('meeting', 'Meeting'),
        ('note', 'Note'),
    ]

    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, null=True, blank=True, related_name='interactions')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True, related_name='interactions')
    interaction_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='note')
    summary = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Interactions"
        ordering = ['-date']

    def __str__(self):
        return f"{self.get_interaction_type_display()} - {self.date.strftime('%Y-%m-%d')}"
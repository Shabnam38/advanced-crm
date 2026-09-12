from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import Lead


class LeadModelTests(TestCase):

    def test_score_auto_set_for_qualified(self):
        lead = Lead.objects.create(full_name="Test Lead", status='qualified', email="test@example.com")
        self.assertEqual(lead.score, 80)

    def test_score_auto_set_for_new(self):
        lead = Lead.objects.create(full_name="Test Lead 2", status='new', email="test2@example.com")
        self.assertEqual(lead.score, 20)

    def test_invalid_phone_raises_error(self):
        lead = Lead(full_name="Bad Phone Lead", phone="abc123")
        with self.assertRaises(ValidationError):
            lead.save()

    def test_valid_phone_saves_successfully(self):
        lead = Lead(full_name="Good Phone Lead", phone="+92 300-1234567")
        lead.save()
        self.assertEqual(Lead.objects.count(), 1)

    def test_lead_without_email_or_phone_raises_error(self):
        lead = Lead(full_name="No Contact Lead")
        with self.assertRaises(ValidationError):
            lead.save()
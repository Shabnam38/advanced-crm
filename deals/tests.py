from django.test import TestCase
from django.core.exceptions import ValidationError
from companies.models import Company
from .models import Deal


class DealModelTests(TestCase):

    def setUp(self):
        self.company = Company.objects.create(name="Test Company")

    def test_probability_auto_set_for_won(self):
        deal = Deal.objects.create(
            title="Test Deal",
            company=self.company,
            stage='won',
        )
        self.assertEqual(deal.probability, 100)

    def test_probability_auto_set_for_prospecting(self):
        deal = Deal.objects.create(
            title="Test Deal 2",
            company=self.company,
            stage='prospecting',
        )
        self.assertEqual(deal.probability, 10)

    def test_negative_value_raises_error(self):
        deal = Deal(
            title="Bad Deal",
            company=self.company,
            value=-500,
        )
        with self.assertRaises(ValidationError):
            deal.save()
from django.test import TestCase
from .models import Company

class CompanyModelTests(TestCase):
    def test_create_company(self):
        company = Company.objects.create(name="Test Co", industry="Tech")
        self.assertEqual(str(company), "Test Co")
        self.assertEqual(company.industry, "Tech")
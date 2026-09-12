from django.test import TestCase
from companies.models import Company
from .models import Customer

class CustomerModelTests(TestCase):
    def setUp(self):
        self.company = Company.objects.create(name="Test Co")

    def test_create_customer(self):
        customer = Customer.objects.create(
            company=self.company,
            first_name="John",
            last_name="Doe",
        )
        self.assertEqual(str(customer), "John Doe")

    def test_customer_deleted_when_company_deleted(self):
        Customer.objects.create(company=self.company, first_name="Jane", last_name="Smith")
        self.company.delete()
        self.assertEqual(Customer.objects.count(), 0)
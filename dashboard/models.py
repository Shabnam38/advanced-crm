from django.http import JsonResponse
from companies.models import Company
from customers.models import Customer
from leads.models import Lead
from deals.models import Deal
from tasks.models import Task
from interactions.models import Interaction

def dashboard_summary(request):
    data = {
        'companies': Company.objects.count(),
        'customers': Customer.objects.count(),
        'leads': Lead.objects.count(),
        'deals': Deal.objects.count(),
        'tasks': Task.objects.count(),
        'interactions': Interaction.objects.count(),
    }
    return JsonResponse(data)
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.db.models import Sum, Count, Avg
from django.core.paginator import Paginator
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


def paginate(request, queryset):
    page_number = request.GET.get('page', 1)
    paginator = Paginator(queryset, 10)
    page = paginator.get_page(page_number)
    return {
        'count': paginator.count,
        'num_pages': paginator.num_pages,
        'current_page': page.number,
        'results': list(page),
    }


def company_list(request):
    companies = Company.objects.all().values('id', 'name', 'industry', 'phone')
    return JsonResponse(paginate(request, companies))


def company_detail(request, pk):
    company = get_object_or_404(Company, pk=pk)
    data = {
        'id': company.id,
        'name': company.name,
        'industry': company.industry,
        'website': company.website,
        'phone': company.phone,
        'address': company.address,
    }
    return JsonResponse(data)


def customer_list(request):
    customers = Customer.objects.all()
    company_id = request.GET.get('company_id')
    if company_id:
        customers = customers.filter(company_id=company_id)
    customers = customers.values('id', 'first_name', 'last_name', 'email', 'company_id')
    return JsonResponse(paginate(request, customers))


def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    data = {
        'id': customer.id,
        'first_name': customer.first_name,
        'last_name': customer.last_name,
        'email': customer.email,
        'phone': customer.phone,
        'job_title': customer.job_title,
        'company': customer.company.name,
    }
    return JsonResponse(data)


def lead_list(request):
    leads = Lead.objects.all()
    status = request.GET.get('status')
    if status:
        leads = leads.filter(status=status)
    source = request.GET.get('source')
    if source:
        leads = leads.filter(source=source)
    leads = leads.values('id', 'full_name', 'status', 'score', 'source')
    return JsonResponse(paginate(request, leads))


def lead_detail(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    data = {
        'id': lead.id,
        'full_name': lead.full_name,
        'email': lead.email,
        'phone': lead.phone,
        'company_name': lead.company_name,
        'status': lead.status,
        'score': lead.score,
        'source': lead.source,
        'notes': lead.notes,
    }
    return JsonResponse(data)


def deal_list(request):
    deals = Deal.objects.all()
    stage = request.GET.get('stage')
    if stage:
        deals = deals.filter(stage=stage)
    deals = deals.values('id', 'title', 'value', 'stage', 'probability')
    return JsonResponse(paginate(request, deals))


def deal_detail(request, pk):
    deal = get_object_or_404(Deal, pk=pk)
    data = {
        'id': deal.id,
        'title': deal.title,
        'company': deal.company.name,
        'customer': str(deal.customer) if deal.customer else None,
        'value': str(deal.value),
        'stage': deal.stage,
        'probability': deal.probability,
        'expected_close_date': deal.expected_close_date,
    }
    return JsonResponse(data)


def task_list(request):
    tasks = Task.objects.all()
    priority = request.GET.get('priority')
    if priority:
        tasks = tasks.filter(priority=priority)
    is_completed = request.GET.get('is_completed')
    if is_completed is not None:
        tasks = tasks.filter(is_completed=is_completed.lower() == 'true')
    tasks = tasks.values('id', 'title', 'due_date', 'priority', 'is_completed')
    return JsonResponse(paginate(request, tasks))


def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    data = {
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'due_date': task.due_date,
        'priority': task.priority,
        'is_completed': task.is_completed,
    }
    return JsonResponse(data)


def interaction_list(request):
    interactions = Interaction.objects.all()
    interaction_type = request.GET.get('type')
    if interaction_type:
        interactions = interactions.filter(interaction_type=interaction_type)
    interactions = interactions.values('id', 'interaction_type', 'date')
    return JsonResponse(paginate(request, interactions))


def interaction_detail(request, pk):
    interaction = get_object_or_404(Interaction, pk=pk)
    data = {
        'id': interaction.id,
        'type': interaction.interaction_type,
        'summary': interaction.summary,
        'date': interaction.date,
        'lead': str(interaction.lead) if interaction.lead else None,
        'customer': str(interaction.customer) if interaction.customer else None,
    }
    return JsonResponse(data)


def company_stats(request, pk):
    company = get_object_or_404(Company, pk=pk)
    deal_stats = company.deals.aggregate(
        total_value=Sum('value'),
        deal_count=Count('id'),
        avg_probability=Avg('probability'),
    )
    data = {
        'company': company.name,
        'total_deal_value': str(deal_stats['total_value'] or 0),
        'deal_count': deal_stats['deal_count'],
        'average_probability': deal_stats['avg_probability'],
        'customer_count': company.customers.count(),
    }
    return JsonResponse(data)


def pipeline_summary(request):
    stages = Deal.objects.values('stage').annotate(
        count=Count('id'),
        total_value=Sum('value'),
    )
    return JsonResponse(list(stages), safe=False)
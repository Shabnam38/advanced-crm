from django.urls import path
from . import views

urlpatterns = [
    path('summary/', views.dashboard_summary, name='dashboard_summary'),

    path('companies/', views.company_list, name='company_list'),
    path('companies/<int:pk>/', views.company_detail, name='company_detail'),
    path('companies/<int:pk>/stats/', views.company_stats, name='company_stats'),

    path('customers/', views.customer_list, name='customer_list'),
    path('customers/<int:pk>/', views.customer_detail, name='customer_detail'),

    path('leads/', views.lead_list, name='lead_list'),
    path('leads/<int:pk>/', views.lead_detail, name='lead_detail'),

    path('deals/', views.deal_list, name='deal_list'),
    path('deals/<int:pk>/', views.deal_detail, name='deal_detail'),

    path('tasks/', views.task_list, name='task_list'),
    path('tasks/<int:pk>/', views.task_detail, name='task_detail'),

    path('interactions/', views.interaction_list, name='interaction_list'),
    path('interactions/<int:pk>/', views.interaction_detail, name='interaction_detail'),

    path('pipeline/', views.pipeline_summary, name='pipeline_summary'),
]
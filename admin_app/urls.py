"""
URL configuration for housecrew project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin_dashboard/',views.admin_dashboard,name='admin_dashboard'),
    path('category/',views.category, name='category'),
    path('service_categories/',views.service_categories,name="service_categories"),
    path('add_category/', views.add_category, name='add_category'),
    path('delete_category/<int:s_id>/', views.delete_category, name='delete_category'),
    path('add_service/',views.add_service,name='add_service'),
    path('services/',views.view_services,name='services'),
    path('update_services/<int:pk>/', views.update_services,name='update_services'),
    path('delete_service/<int:pk>/',views.delete_service,name='delete_service'),
    path('company/',views.company,name='company'),
    path('location/',views.location,name='location'),
    path('add_location/',views.add_location,name='add_location'),
    path('delete_location/<int:pk>/', views.delete_location, name='delete_location'),
    path('company_requests/',views.company_requests,name='company_requests'),
    path('verify_company/<int:company_id>/',views.verify_company,name='verify_company'),
    path('sub_services/',views.sub_services,name='sub_services'),
    path('add_sub_services/',views.add_sub_services,name='add_sub_services'),
    path('update_subservices/<int:pk>/',views.update_sub_services,name='update_subservices'),
    path('delete_subservices/<int:pk>/',views.delete_subservices,name='delete_subservices'),
    path('monitor_services/',views.monitor_services,name='monitor_services'),
    
    
    
]

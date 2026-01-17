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
    path('company_home/',views.company_home,name='company_home'),
    path('register_company/',views.register_company,name='register_company'),
    path('company_profile/',views.company_profile,name='company_profile'),
    path('authorized_person/',views.authorized_person,name='authorized_person'),
    path('legal_info/',views.legalInfo,name='legal_info'),
    path('work_profile/',views.work_profile,name='work_profile'),
    path('company_declaration/',views.c_declaration,name='company_declaration'),
    path('insurance_details/',views.insurance_details,name='insurance_details'),
    path('chief_details/',views.chief_details,name='chief_details'),
    path('login_credentials/',views.show_temp_login,name='login_credentials'),
    path('company_login/',views.company_login,name='company_login'),
    path('company_dashboard/',views.company_dashboard,name='company_dashboard'),
    path('update_credentials/',views.update_login_credentials,name='update_credentials'),
    path('service_booking_requests/',views.service_booking_requests,name='service_booking_requests'),
    path('service_booking_update/<user>/',views.service_booking_update,name='service_booking_update'),
    path('service_allocated/',views.service_allocated,name='service_allocated'),
    path('service_done/<user>/',views.service_done,name='service_done'),
    
    
]

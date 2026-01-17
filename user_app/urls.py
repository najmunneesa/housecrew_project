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
    
    path('',views.home,name='home'),
    path('base/',views.base,name='base'),
    path('search/',views.search,name='search'),
    path('about/',views.about,name='about'),
    #user
    path('user_registration/',views.user_registration,name='user_registration'),
    path('user_login/',views.user_login,name='user_login'),
    path('logout/',views.user_logout,name='logout'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('update_user_credentials/',views.update_user_credentials,name='update_user_credentials'),
    path('get_quote/',views.get_quote,name='get_quote'),
    #services
    path('category_services/<slug:slug>/',views.category_services,name='category_services'),
    path('user_sub_services/',views.sub_services_list, name='user_sub_services'),
    path('cleaning/',views.cleaning,name='cleaning'),
    path('plumbing/',views.plumbing,name='plumbing'),
    path('bookservices/<int:service_id>/',views.bookservices,name='bookservices'),
    path('emergency_services/',views.emergency_services,name='emergency_services'),
    path('book_emergency_services/<int:service_id>/',views.book_emergency_services,name='book_emergency_services'),
    path('appliance_repair/',views.appliance_repair,name='appliance repair'),
    path('maintenance_repair/',views.maintenance_repair,name='maintenance and repair'),
    path('electrical/',views.electrical,name='electrical'),
    path('installation/',views.installation_services,name='installation'),
    path('relocation/',views.relocation,name='relocation'),
    path('additional/',views.additional,name='additional'),
    #house crew
    path('house_crew/',views.house_crew,name='house crew'),
     #companies
    path('companies/',views.companies,name='companies'),
    path('service/<int:service_id>/',views.service_detail,name='service_detail'),
    path('company_list/',views.company_list,name='company_list'),
  
]

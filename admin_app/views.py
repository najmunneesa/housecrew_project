from django.shortcuts import render,redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib import messages
from django.db import transaction
from company_app.models import S_Company
from user_app.models import Booking


def admin_dashboard(request):
    company_requests= S_Company.objects.filter(approval_status = 'PENDING')
    c_requests=company_requests.count()
    return render(request, 'admin_app/admin_dashboard.html', {'c_requests' : c_requests})

def service_categories(request):
    return render(request, 'admin_app/service_categories.html')

#location
def location(request):
    location=Location.objects.all()
    return render(request, 'admin_app/location.html', {'location':location})

def add_location(request):    
    if request.method=='POST':
        form=LocationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'location added successfully')
            return redirect ('location')
    else:
        form=LocationForm(label_suffix='')
    return render(request, 'admin_app/add_location.html', {'form':form})

def delete_location(request, pk):
    if request.method== 'POST':
        location=Location.objects.get(pk=pk)
        location.delete()
        messages.success(request, "Location deleted successfully")
    return redirect('location')

#category
def category(request):
    categories=S_Category.objects.all()
    for c in categories:
        if not c.slug:
            c.slug = unique_slug(c)
            c.sace()
        
    return render(request, 'admin_app/category.html', {'categories':categories})

def add_category(request):
    if request.method== 'POST':
        form=S_categoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "successfully added")
            return redirect('category')
    else:
        form=S_categoryForm(label_suffix='')
    return render(request, 'admin_app/add_category.html', {'form' :form })

def delete_category(request, s_id):
    if request.method== 'POST':
        category=S_Category.objects.get(id=s_id)
        category.delete()
        messages.success(request, "category deleted successfully")
    return redirect('category')
    
#services-main
def add_service(request):
    if request.method=='POST':
        form=HouseCrewForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "service added successfully")
            return redirect('services')
    else:
        form=HouseCrewForm(label_suffix='')
    return render(request, 'admin_app/add_service.html', {'form':form})

def view_services(request):
    services=HouseCrew.objects.all()
    return render(request, 'admin_app/services.html',{'services':services})

def update_services(request, pk):
    service= HouseCrew.objects.get(pk=pk)
    
    if request.method== 'POST':
        form = HouseCrewForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            return redirect('services')
    else:
        form= HouseCrewForm(instance=service, label_suffix='')
        return render(request, 'admin_app/update_services.html', {'form' : form})
    
def delete_service(request , pk):
    if request.method== 'POST':
        service= HouseCrew.objects.get(pk=pk)
        service.delete()
        messages.info(request,"service removed")
    return redirect('services')

#sub-services
def sub_services(request):
    sub_services=AddServices.objects.all()
    return render(request, 'admin_app/sub_services.html', {'services' : sub_services})

def add_sub_services(request):
    if request.method== 'POST':
        form = AddServiceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Added successfully")
            return redirect('sub_services')
    else:
        form = AddServiceForm(label_suffix='')
    return render(request, 'admin_app/add_subservices.html', {'form' :form})

def update_sub_services(request,pk):
    service= AddServices.objects.get(pk=pk)
    
    if request.method== 'POST':
        form=AddServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            return redirect('sub_services')
    else:
        form = AddServiceForm(instance=service, label_suffix='')
    return render(request, 'admin_app/update_subservices.html', {'form': form, 'service':service})

def delete_subservices(request, pk):
    service= AddServices.objects.get(pk=pk)
    service.delete()
    messages.info(request, "Deleted")
    return redirect('sub_services')
            
#company details
def company(request):
    return render(request,'admin_app/company.html')

def company_requests(request):
    company_requests= S_Company.objects.filter(approval_status = 'Pending')
    companies=S_Company.objects.all()
    return render(request,'admin_app/company.html', {'requests' : company_requests, 'companies' : companies})

def verify_company(request, company_id):
    company = get_object_or_404(S_Company, id=company_id)
    user = company.user

    if request.method == 'POST':
        action = request.POST.get('action', '').lower()
        reason = request.POST.get('rejection_reason', '')

        with transaction.atomic():
            if action == 'approved':
                company.approval_status = 'Approved'
                company.is_active = True
                company.save()

                if user:
                    if hasattr(user, 'profile'):
                        user.profile.role = 'COMPANY'
                        user.profile.save()
                    user.is_staff=True
                    user.is_active = True
                    user.save()

                messages.success(request, 'Company approved successfully!')

            elif action == 'rejected':
                if not reason:
                    messages.error(request, "Please provide a rejection reason.")
                    return redirect('verify_company', company_id=company.id)

                company.approval_status = 'Rejected'
                company.is_active = False
                company.rejection_reason = reason
                company.can_resubmit = True
                company.save()

                messages.warning(request, "Company rejected.")

            else:
                messages.error(request, "Invalid action.")
                return redirect('verify_company', company_id=company.id)

        return redirect('company_requests')

    return render(request, 'admin_app/verify_company.html', {'company': company})

    
    context= {
        'company' : company,
        'auth' : getattr(company, 'authorized_person', None),
        'legal': getattr(company, 'legal_registration', None),
        'work_profiles': company.work_profiles.all(),
        'declaration': getattr(company, 'declaration', None),
        'insurance': company.insurances.all(),
        'chief_technician': getattr(company, 'chief_technician', None),
    }
    return render(request, 'admin_app/verify_company.html', context)


def monitor_services(request):
    bookings = Booking.objects.all().order_by('-booked_at')

    context = {
        'total_bookings': bookings.count(),
        'pending_count': bookings.filter(status ='pending').count(),
        'allocated_count': bookings.filter(status='allocated').count(),
        'completed_count': bookings.filter(status='completed').count(),
        'emergency_count': bookings.filter(is_emergency=True).count(),
        'bookings': bookings,
    }

    return render(request, 'admin_app/monitor_services.html', context)
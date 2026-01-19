from django.shortcuts import render,redirect, get_object_or_404
from .models import UserProfile , CallBackRequest,Booking
from admin_app.models import *
from company_app.models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from company_app.forms import UpdateCredentialsForm

def base(request):
    
    return render(request, 'user_app/base.html')

def search(request):
    query = request.GET.get('q')
    results = []
    
    if query:
        results =HouseCrew.objects.filter(h_services__icontains=query)
    
    return render(request, 'user_app/search_results.html',{'query' : query, 'results' : results})


def home(request):
    
    carousel_images = [
        'user_app/images/home3.png',
        'user_app/images/home4.png',
        'user_app/images/home5.png',
        'user_app/images/home6.png',
        'user_app/images/home8.png',
        'user_app/images/recostruction1.png'
    ]

    locations = Location.objects.all()
    services = AddServices.objects.all()
    
    categories = S_Category.objects.all()
    services = HouseCrew.objects.all()
    
    category_services= {}
    for cat in categories:
        sub_services = AddServices.objects.filter(category=cat)
        category_services[cat]= services
        
    #callback
    if request.method== 'POST':
        name=request.POST.get('name')
        contact=request.POST.get('contact')
        
        CallBackRequest.objects.create(name=name, contact=contact)
        messages.info(request,"Thank you. Our crew will reach you soon.")
        return redirect('home')
    
        
    return render(request, 'user_app/home.html', {'carousel_images': carousel_images,
        'locations': locations,
        'services': services,
        'sub_services' : sub_services,
        'category_services': category_services,})
 
#registration

def user_registration(request):
    if request.method== 'POST':
        username= request.POST['username']
        email=request.POST['email']
        password= request.POST['password']
        confirm_password= request.POST['confirm_password']
        if password!= confirm_password:
            return render(request, 'user_app/user_registration.html',{'error' : 'Password doesnt match!'})
        if User.objects.filter(username=username).exists():
            return render(request, 'user_app/user_registration.html', {'erroe' : 'Username already exists'})
        user= User.objects.create_user(username=username, password=password, email=email)
        user.save()
        return redirect('user_login')
    return render(request, 'user_app/user_registration.html')

#login session
def user_login(request):
    if request.method== 'POST':
        username= request.POST.get('username')
        password= request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user:
            login(request, user)

            if user.is_superuser:
                return redirect('/admin/')
            elif user.is_staff:
                return redirect('admin_dashboard')

            profile, created = UserProfile.objects.get_or_create(user=user)

            if profile:
                if profile.role == 'company':
                    return redirect('company_dashboard')
                else:
                    return redirect('home')
        else:
            messages.error(request, "Invalid Username or Password")
                
    return render(request, 'user_app/user_login.html')

@login_required
def user_logout(request):
    logout(request)
    messages.info(request,"You are Logged out")
    return redirect('user_login')

@login_required
def update_user_credentials(request):
    user=request.user
    
    if request.method== 'POST':
        form = UpdateCredentialsForm(request.POST, user=user)
        
        if form.is_valid():
            
            if form.cleaned_data['username_changed']:
                user.username= form.cleaned_data['username']
            if form.cleaned_data['password_changed']:
                user.set_password(form.cleaned_data['password'])
            
            user.save()
            #kepps user logged in
            update_session_auth_hash(request, user)
            
            messages.success(request, "Login cedentials updated successfully")
            return redirect('house crew')
    else:
        form = UpdateCredentialsForm(user=request.user , label_suffix='')
        
    return render(request, 'user_app/user_login_credentials.html', {'form' : form})

@login_required
def dashboard(request):
    role = request.user.profile.role

    if role == 'ADMIN':
        return redirect('admin_dashboard')

    elif role == 'COMPANY':
        return redirect('company_dashboard')

    else:
        if role == 'USER':
            #bookings
            bookings= Booking.objects.filter(user=request.user).order_by('-booked_at')
            return render(request, 'user_app/dashboard.html',{'bookings' : bookings})
    
    return render(request, 'user_app/dashboard.html')
    


def cleaning(request):
    
    return render(request, 'user_app/cleaning_services.html')

def plumbing(request):
    return render(request,'user_app/plumbing_services.html')

def electrical(request):
    return render(request, 'user_app/electrical_services.html')

def appliance_repair(request):
    return render(request, 'user_app/appliance_repair_services.html')

def maintenance_repair(request):
    return render(request, 'user_app/maintenance&repair_services.html')

def installation_services(request):
    return render(request, 'user_app/installation_services.html')

def relocation(request):
    return render(request, 'user_app/relocation_services.html')

def additional(request):
    return render(request, 'user_app/additional_services.html')

def about(request):
    return render(request, 'user_app/about_house crew.html')

def house_crew(request):
    categories= S_Category.objects.all()
    
    # category images
    for category in categories:
        if category.category.lower() == "cleaning":
            category.image_url = "user_app/images/cleaning.png"
        elif category.category.lower() == "plumbing":
            category.image_url = "user_app/images/plumbing.png"
        elif category.category.lower() == "electrical":
            category.image_url = "user_app/images/electrical.png"
        elif category.category.lower() == "relocation":
            category.image_url = "user_app/images/relocate.png"
        elif category.category.lower() == "additional":
            category.image_url = "user_app/images/additional.png"
        elif category.category.lower() == "installation":
            category.image_url = "user_app/images/installation.png"
        elif category.category.lower() == "repair & maintenance":
            category.image_url = "user_app/images/appliance_repair.png"
        else:
            category.image_url = "user_app/images/default.png"
            
    #service list
    sub_services = AddServices.objects.select_related('crew', 'crew__s_category').all()
    return render(request, 'user_app/house_crew.html', {'categories' : categories, 'sub_services' :sub_services})


def companies(request):
    return render(request, 'user_app/companies.html')


def category_services(request, slug):
    
    category=get_object_or_404(S_Category, slug=slug)
    services=HouseCrew.objects.filter(s_category=category)
    
    return render(request, 'user_app/category_services.html', {'services' : services, 'category' : category})


def service_detail(request, sub_id):
    service= get_object_or_404(HouseCrew, id=sub_id)
    sub_services= AddServices.objects.filter(category=service.s_category).exclude(id=service.id)
    
    return render(request,'user_app/service_detail.html', {'service' :service, 'sub_services' :sub_services})

def sub_services_list(request):
    sub_services = AddServices.objects.select_related('crew', 'crew__s_category').all()
        
    return render(request, 'user_app/house_crew.html', {'sub_services' :sub_services})


def company_list(request):
    companies = S_Company.objects.all()
    
    return render(request, 'user_app/companies.html', {'companies' : companies})

@login_required(login_url='user_login')
def bookservices(request, service_id):
    service= AddServices.objects.get(id=service_id)
    user = request.user
    
    if request.method== 'POST':
        work_profile= C_profile_work.objects.filter(c_nature_service=service.category).first()
        
        if not work_profile:
            messages.info(request, "No Service is available.")
            return redirect('dashboard')
        
        crew =HouseCrew.objects.filter(s_category=service.category).first()
        
        if not crew:
            messages.info(request,"No Company available")
            return redirect('dashboard')
        
        Booking.objects.create(user=user, service=service,crew= crew, company=work_profile.company, status='pending')
        return redirect('dashboard')
    
    return render(request, 'user_app/book_services.html', {'service' : service})

@login_required
def emergency_services(request):
    services= AddServices.objects.filter(is_emergency=True)
    
    return render(request, 'user_app/emergency_services.html', {'services' : services})

def book_emergency_services(request, service_id):
    service = AddServices.objects.get(id=service_id ,is_emergency=True)
    user = request.user
    
    is_emergency = True
    if request.method== 'POST':
        work_profile= C_profile_work.objects.filter(c_nature_service=service.category).first()
        
        if not work_profile:
            messages.info(request, "No service is available.")
            return redirect('dashboard')
    
        crew =HouseCrew.objects.filter(s_category=service.category).first()
        
        if not crew:
            messages.info(request,"No Company available")
            return redirect('dashboard')
        
        Booking.objects.create(user=user, service=service,crew= crew, company=work_profile.company, status='pending', is_emergency=is_emergency)
        return redirect('dashboard')
    
    return render(request, 'user_app/book_emergency_service.html', {'service' : service, 'is_emergency':is_emergency})


def get_quote(request):
    services = AddServices.objects.all()
    locations = Location.objects.all()
    quote = None
    selected_service = None
    selected_location = None
    is_emergency = False

    if request.method == "POST":
        service_id = request.POST.get("service")
        location_id = request.POST.get("location")
        is_emergency = bool(request.POST.get("is_emergency"))

        if service_id and location_id:
            service = get_object_or_404(AddServices, id=service_id)
            location = get_object_or_404(Location, id=location_id)
            selected_service = service.id
            selected_location = location.id
            quote = service.base_charge + location.extra_charge
            if is_emergency:
                quote *= 1.5

    context = {
        "services": services,
        "locations": locations,
        "quote": quote,
        "selected_service": selected_service,
        "selected_location": selected_location,
        "is_emergency": is_emergency,
    }
    return render(request, "quote_form.html", context)

def cancel_service(request, id):
    booking = get_object_or_404(Booking, id=id)

    if booking.status != 'cancelled':
        booking.status = 'cancelled'
        booking.delete()
        messages.info(request, "The service has been cancelled from your request list.")
        
    else:
        messages.info(request, "This service is already cancelled.")

    return redirect('dashboard')


from django.shortcuts import render, redirect,get_object_or_404
from .forms import *
from .models import *
from django.contrib import messages
from django.db import transaction
from django.core.files import File
from django.core.files.storage import default_storage
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.db.models import Model, QuerySet
from django.contrib.auth import authenticate , login, logout ,update_session_auth_hash
from django.contrib.auth.decorators import login_required
from user_app.models import UserProfile, Booking


#cleaned data to jason-serializable dictionary
def serialized_cleaned_data(cleaned_data):
    data= {}
    for key , value in cleaned_data.items():
        #foreignkey/model instance
        if isinstance(value, Model):
            data[key] =value.pk
            #manytomany queryset
        elif isinstance(value, QuerySet):
            data[key]= list(value.values_list('id', flat=True))
            #normal field
        else:
            data[key]= value
            
    return data

def create_company(data):
    company= S_Company.objects.create(
        **{k: v for k, v in data.items() if not isinstance(v, list)}
    )
    
    for fields, ids in data.items():
        if isinstance(ids, list) and hasattr(company, fields):
            getattr(company, fields).set(ids)
        
    return company

def session_duration(request):
    request.session.set_expiry(20 * 60)
            
def company_home(request):
    return render(request, 'company_app/company_home.html')

def register_company(request):
    if request.user.is_authenticated:
        try:
            company = request.user.company_profile
            if company.approval_status == 'Rejected':
                company.approval_status = 'Pending'
                company.rejection_reason = ''
                company.save()
        except:
            pass
    return render(request,'company_app/company_registration.html')


def company_profile(request):
    saved_data = request.session.get('company')
    
    if saved_data:
        initial_data = saved_data.copy()
        if 'c_service_location' in saved_data:
            initial_data['c_service_location'] = Location.objects.filter(id__in=saved_data['c_service_location'])
        else:
            initial_data = None
    
    if request.method== 'POST':
        form= Company_form(request.POST)
        
        if form.is_valid():
            service_location= form.cleaned_data.get('c_service_location')
            #company = form.save()
            request.session['company']={
                'c_name': form.cleaned_data['c_name'],
                'c_registration': form.cleaned_data['c_registration'],
                'c_email_id': form.cleaned_data['c_email_id'],
                'c_mobile_no': form.cleaned_data['c_mobile_no'],
                'c_service_location': list(service_location.values_list('id', flat=True)) if service_location else [],
            }
            session_duration(request)
            return redirect('authorized_person')
        else:
            messages.error(request,"Please correct the errors below.")
            
    else:
         form= Company_form(initial=saved_data if saved_data else None ,label_suffix='')   
    
    return render(request, 'company_app/company_profile.html', {'form': form})

def authorized_person(request):
    if 'company' not in request.session:
        messages.error(request, "Session expired")
        return redirect('company_profile')
    
    saved_data= request.session.get('authorized_person', {})
    initial_file_path = saved_data.get('auth_id_path', None)
    
    if request.method== 'POST':
        form= Authorized_person_form(request.POST, request.FILES)
        
        if form.is_valid():
            auth_id= form.cleaned_data.get('auth_id')
            temp_path = initial_file_path
            
            if auth_id:
                if initial_file_path and default_storage.exists(initial_file_path):
                    default_storage.delete(initial_file_path)
                    temp_path= default_storage.save(f'temp/{auth_id.name}', auth_id)     
            
            request.session['authorized_person'] = {
                'auth_p_name': form.cleaned_data['auth_p_name'],
                'auth_p_designation': form.cleaned_data['auth_p_designation'],
                'auth_p_mobile_no': form.cleaned_data['auth_p_mobile_no'],
                'auth_p_email_id' :form.cleaned_data['auth_p_email_id'],
                'auth_id_path': temp_path,
            }
            session_duration(request)
            return redirect('legal_info')
    else:
        form=Authorized_person_form(
            initial=saved_data if saved_data else None ,
            initial_file_path=initial_file_path,
            label_suffix='')
        
    
    return render(request, 'company_app/authorized_person.html', {'form' : form})
        
#legal info
def legalInfo(request):
    if 'company' not in request.session:
        messages.error(request, "session expired")
        return redirect('company_profile')
    
    saved_data= request.session.get('legal_info', {})
    
    if request.method== 'POST':
        form =C_legal_registration_form(request.POST)
        if form.is_valid():
            request.session['legal_info'] = {
                'c_pan' : form.cleaned_data['c_pan'],
                'c_gst' : form.cleaned_data['c_gst'],
                                            }
            session_duration(request)
            return redirect('work_profile')
    else:
        form=C_legal_registration_form(initial=saved_data if saved_data else None ,label_suffix='')
    return render(request, 'company_app/company_legalInfo.html', {'form' : form})

#work profile
def work_profile(request):
    if 'company' not in request.session:
        messages.error(request, "session expired")
        return redirect('company_profile')
    
    saved_data= request.session.get('work_profile')
    
    if request.method== 'POST':
        form= C_profile_form(request.POST, request.FILES)
    
        if form.is_valid():        
            c_wportfolio=request.FILES.get('c_wportfolio')
            temp_path= saved_data.get('c_wportfolio_path') if saved_data else None
            
            if c_wportfolio:
                if temp_path and default_storage.exists(temp_path):
                    default_storage.delete(temp_path)
                temp_path= default_storage.save(f'temp/{c_wportfolio.name}', c_wportfolio)
            
            nature_services= form.cleaned_data.get('c_nature_service')
            
            request.session['work_profile']= {
                'c_year' : form.cleaned_data['c_year'],
                'c_nature_service' :list(nature_services.values_list('id', flat=True)),
                'c_wportfolio_path' :temp_path
                    
            }
            session_duration(request)
            return redirect('company_declaration')
    else:
        initial = {}
        if saved_data:
            initial['c_year'] = saved_data.get('c_year')
            initial['c_nature_service']= saved_data.get('c_nature_service')
        form=C_profile_form(initial= initial,
                            label_suffix='')
        
    return render(request, 'company_app/company_workProfile.html', {'form' :form})

#company dclaration
def c_declaration(request):
    if 'company' not in request.session:
        messages.error(request, "session expired")
        return redirect('company_profile')
    
    saved_data= request.session.get('c_declaration')
    
    if request.method== 'POST':
        form= C_declaration_form(request.POST, request.FILES)
        
        if form.is_valid():
            c_noc= request.FILES.get('c_noc')
            temp_path= saved_data.get('c_noc_path') if saved_data else None
            
            if c_noc:
                if temp_path and default_storage.exists(temp_path):
                    default_storage.delete(temp_path)
                
                temp_path= default_storage.save(f'temp/{c_noc.name}', c_noc)
                
            request.session['c_declaration']= {
                    'c_p_verification': form.cleaned_data['c_p_verification'],
                    'c_noc_path': temp_path
            }
            session_duration(request)
            return redirect('insurance_details')
    else:
        initial = {}
        if saved_data:
            initial['c_p_verification'] = saved_data.get('c_p_verification')
        form=C_declaration_form(initial=initial, label_suffix='')
    return render(request, 'company_app/company_declaration.html', {'form' : form})

#insurance
def insurance_details(request):
    if 'company' not in request.session:
        messages.error(request, "session expired")
        return redirect('company_profile')
    
    saved_data = request.session.get('insurance_details')
    
    if request.method== 'POST':
        form= C_insurance_form(request.POST)
        if form.is_valid():
            ins_type = form.cleaned_data.get('c_ins_type')
            request.session['insurance_detail'] ={
                'c_ins_type' : ins_type,
                'c_ins_provider' : form.cleaned_data['c_ins_provider'],
                'c_ins_number' : form.cleaned_data['c_ins_number']
                }
            session_duration(request)
            return redirect('chief_details')
    else:
        form= C_insurance_form(initial=saved_data if saved_data else None,
                               label_suffix='')
        
    return render(request, 'company_app/company_insurance.html', {'form' : form})


#chief tech
def chief_details(request):
    if 'company' not in request.session:
        messages.error(request, "session expired")
        return redirect('company_profile')

    saved_data = request.session.get('chief_technician')
    if saved_data:
        form = C_Chieftechnician_form(initial=saved_data)
    else:
        form = C_Chieftechnician_form(label_suffix='')

    if request.method == 'POST':
        form = C_Chieftechnician_form(request.POST, request.FILES)

        if form.is_valid():
            action = request.POST.get('action')
            request.session['chief_technician'] = serialized_cleaned_data(form.cleaned_data)

            if action == 'submit':
                try:
                    with transaction.atomic():
                        company = create_company(request.session['company'])

                        # authorized person
                        auth_data = request.session.get('authorized_person')
                        if not auth_data:
                            raise ValueError("authorized person data is missing")

                        authorized_p = Auth_personal_details(
                            company=company,
                            auth_p_name=auth_data['auth_p_name'],
                            auth_p_designation=auth_data['auth_p_designation'],
                            auth_p_mobile_no=auth_data['auth_p_mobile_no'],
                        )

                        auth_path = auth_data.get('auth_id_path')
                        if auth_path and default_storage.exists(auth_path):
                            with default_storage.open(auth_path, 'rb') as f:
                                authorized_p.auth_id.save(
                                    auth_path.split('/')[-1], File(f), save=False
                                )
                        authorized_p.save()

                        if auth_path and default_storage.exists(auth_path):
                            default_storage.delete(auth_path)

                        # legal
                        C_legal_registration.objects.create(
                            company=company,
                            **request.session['legal_info']
                        )

                        # work profile
                        workprofile_data = request.session.get('work_profile')
                        if not workprofile_data:
                            raise ValueError("work profile data is missing")

                        work_profile = C_profile_work(
                            company=company,
                            c_year=workprofile_data['c_year'],
                        )

                        portfolio_path = workprofile_data.get('c_wportfolio_path')
                        nature_service = workprofile_data.get('c_nature_service')

                        if portfolio_path and default_storage.exists(portfolio_path):
                            with default_storage.open(portfolio_path, 'rb') as f:
                                work_profile.c_wportfolio.save(
                                    portfolio_path.split('/')[-1], File(f), save=False
                                )

                        work_profile.save()

                        if nature_service:
                            work_profile.c_nature_service.set(nature_service)

                        if portfolio_path and default_storage.exists(portfolio_path):
                            default_storage.delete(portfolio_path)

                        # declaration
                        declaration_data = request.session.get('c_declaration')
                        if declaration_data:
                            declaration = C_declaration(
                                company=company,
                                c_p_verification=declaration_data['c_p_verification']
                            )

                            noc_path = declaration_data.get('c_noc_path')
                            if noc_path and default_storage.exists(noc_path):
                                with default_storage.open(noc_path, 'rb') as f:
                                    declaration.c_noc.save(
                                        noc_path.split('/')[-1], File(f), save=False
                                    )
                            declaration.save()

                            if noc_path and default_storage.exists(noc_path):
                                default_storage.delete(noc_path)

                        # insurance
                        C_insurance.objects.create(
                                company=company,
                                **request.session['insurance_detail']
                            )

                        # chief technician
                        C_chief_technician.objects.create(
                                company=company,
                                **request.session['chief_technician']
                            )

                    request.session['company_id'] = company.id

                    for key in [
                        'company',
                        'authorized_person',
                        'legal_info',
                        'work_profile',
                        'c_declaration',
                        'insurance_details',
                        'chief_technician',
                    ]:
                        request.session.pop(key, None)

                    '''messages.info(
                        request,
                        "Your form has been submitted. Please wait until admin approval."
                    )'''

                    username = company.c_email_id.split('@')[0]
                    temp_password = get_random_string(8)

                    user = User.objects.create_user(
                        username=username,
                        password=temp_password,
                        is_active=False
                    )

                    company.user = user
                    UserProfile.objects.create(user=user, role='company')
                    company.save()

                    request.session['temp_login'] = {
                        'username': username,
                        'password': temp_password
                    }

                    return redirect('login_credentials')

                except Exception as e:
                    import traceback
                    messages.error(
                        request,
                        f"Registration failed: {e}\n{traceback.format_exc()}"
                    )

    return render(request, 'company_app/chief_technician.html', {'form': form})


#company login credential
def show_temp_login(request):
    credentials= request.session.get('temp_login')
    if not credentials:
        messages.warning(request, "temporary credentials expired")
        return redirect('home')
    #del request.sesson['temp_login']
    
    return render(request, 'company_app/temp_login.html', {'credentials':credentials})
    
    
def company_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if not user:
            messages.error(request, "Invalid username or password")
            return redirect('company_login')
        
        login(request, user)
        try:
            company = S_Company.objects.get(user=user)
        except S_Company.DoesNotExist:
            messages.error(request, "Company profile not found")
            return redirect('company_login')
        
        #pending
        if company.approval_status == 'Pending':
            messages.warning(request, "Your request is under review. Please wait for the approval")
            return redirect('register_company')
        
        #rejected
        if company.approval_status == 'Rejected':
            messages.warning(request, "Your registration rejected. please submit with sufficient data")
            return redirect('register_company')
        
        #approved
        if company.approval_status == 'Approved':
            return redirect('company_dashboard')
    
    return render(request, 'company_app/company_login.html')


@login_required
def company_dashboard(request):
    company = request.user.company_profile
    
    work_profiles= company.work_profiles.all()
    s_categories = S_Category.objects.filter(nature_of_services__company=company).distinct()
    
    return render(request, 'company_app/company_dashboard.html' , {
        'company' : company,
        'work_Profiles' : work_profiles,
        's_categories' : s_categories,
    })

@login_required
def update_login_credentials(request):
    company = S_Company.objects.get(user=request.user)
    
    if company.approval_status != 'APPROVED':
        messages.warning(request, "You are not allowed to update credentials")
        return redirect('company_login')
    
    if request.method== 'POST':
        form = UpdateCredentialsForm(request.POST, user=request.user)
        
        if form.is_valid():
            user=request.user
            
            if form.cleaned_data['username_changed']:
                user.username= form.cleaned_data['username']
            if form.cleaned_data['password_changed']:
                user.set_password(form.cleaned_data['password'])
            
            user.save()
            #kepps user logged in
            update_session_auth_hash(request, user)
            
            messages.success(request, "Login cedentials updated successfully")
            return redirect('company_dashboard')
    else:
        form = UpdateCredentialsForm(user=request.user , label_suffix='')
        
    return render(request, 'company_app/update_credentials.html',{'form' : form})


#service
def service_booking_requests(request):
    company = get_object_or_404(S_Company, user=request.user)
    
    
    bookings = Booking.objects.filter(company=company, status='pending' ,).order_by('-booked_at')
    
    return render(request, 'company_app/service_booking_requests.html', {'bookings' : bookings})

def service_booking_update(request, user):
    company = get_object_or_404(S_Company, user=request.user)
    
    booking= Booking.objects.get(user=user, company=company)
    
    if request.method== 'POST':
        action = request.POST.get('action')
        if action == 'accept':
            booking.status = 'allocated'
        elif action == 'rejected':
            booking.status = 'rejected'
            
        booking.save()
        return redirect('service_booking_requests')
    
    return redirect('service_booking_requests')

def service_allocated(request):
    company = get_object_or_404(S_Company, user=request.user)
    
    bookings= Booking.objects.filter(company=company, status='allocated').order_by('-booked_at')
    
    return render(request, 'company_app/allocated_sevices.html', {'bookings' : bookings})

def service_done(request, user):
    company = get_object_or_404(S_Company, user=request.user)
    
    booking= Booking.objects.get(user=user, company=company, status='allocated')
    
    if request.method== 'POST':
        booking.status = 'completed'
        booking.save()
        
    return redirect('service_allocated')

def emergency_service_requests(request):
    company =get_object_or_404(S_Company, user=request.user)
    
    bookings = Booking.objects.filter(company=company, is_emergency=True).order_by('-booked_at')
    
    return render(request, 'company_app/emergency_services.html',{'bookings' : bookings})
    
    
    
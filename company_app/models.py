from django.db import models
from django.contrib.auth.models import User
from admin_app.models import Location, S_Category
from django.contrib.auth.hashers import make_password, check_password
from django.core.validators import RegexValidator, EmailValidator

registration_validator=RegexValidator(
    regex=r'^[LU]\d{5}(KL)\d{4}(PVT|PLC|LLP|OPC)\d{6}$',
    message="Enter CIN registration. (eg: L12345KL2023PLC123456)"

)
mobile_validator= RegexValidator(
    regex=r'^[6-9]\d{9}$',
    message="Enter a valid 10-digit mobile number"
)
email_validator= EmailValidator(
    message="Enter a valid email"
)
pan_validator= RegexValidator(
    regex=r'^[A-Z]{5}[0-9]{4}[A-Z]$',
    message="Enter a valid PAN number (eg: ABCDE1234S)"
)
gst_validator= RegexValidator(
    regex=r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$',
    message="Enter a valid GST number (eg: 22ABCDE1234F1Z5)"
)
adhaar_validator= RegexValidator(
    regex=r'^\d{4}\s\d{4}\s\d{4}$',
    message="Enter valid Adhaar number"
)
class S_Company(models.Model):
    APPROVAL_STATUS = [
        ('Pending' , 'Pending'),
        ('Approved' , 'Approved'),
        ('Rejected', 'Rejected')
    ]
    c_name=models.CharField(max_length=100, unique=True, 
                            verbose_name="Company Name",
                            error_messages={"unique" : "This company already exists"})
    c_registration=models.CharField(max_length=30, unique=True, validators=[registration_validator])
    c_mobile_no=models.CharField(max_length=15, validators=[mobile_validator])
    c_email_id=models.EmailField(unique=True, validators=[email_validator])
    c_service_location=models.ManyToManyField(Location, related_name='companies')
    
    approval_status = models.CharField(max_length=15, choices=APPROVAL_STATUS, default='Pending')
    
    is_active = models.BooleanField(default=False)
    
    rejection_reason= models.TextField(blank=True, null=True)
    
    can_resubmit= models.BooleanField(default=False)
    #user model
    user= models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='company_profile')
    
    def __str__(self):
        return self.c_name
    
class Auth_personal_details(models.Model):
    company=models.OneToOneField(S_Company, on_delete=models.CASCADE, related_name='authorized_person')
    
    Designation_choices = [
        ('OWNER', 'Owner'),
        ('MANAGER', 'Manager'),
        ('ADMIN', 'Admin'),
    ]
    auth_p_name=models.CharField(max_length=50)
    auth_p_designation=models.CharField(max_length=20, choices=Designation_choices)
    auth_p_mobile_no=models.CharField(max_length=15, validators=[mobile_validator])
    auth_p_email_id=models.EmailField(validators=[email_validator])
    auth_id=models.FileField(upload_to='auth_ids/', null=True, blank=True)
    
    def __str__(self):
        return self.auth_p_name
    
class C_legal_registration(models.Model):
    company=models.OneToOneField(S_Company, on_delete=models.CASCADE, related_name='legal_registration')
    
    c_pan=models.CharField(max_length=10, unique=True, validators=[pan_validator])
    c_gst=models.CharField(max_length=15, unique=True, null=True, blank=True, validators=[gst_validator])
    
    def __str__(self):
        return f"{self.company.c_name} - legal"
    
'''class Service(models.Model):
    service=models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.service'''
    
class C_profile_work(models.Model):
    company=models.ForeignKey(S_Company, on_delete=models.CASCADE, related_name='work_profiles')
    
    year_of_company=[
        ('1','1 years'),
        ('2','2 years'),
        ('3','3 years'),
        ('4','4 years'),
        ('5','5 years'),
        ('5+','More than 5 years'),
    ]
    
    c_year=models.CharField(max_length=20, choices=year_of_company)
    c_nature_service=models.ManyToManyField(S_Category, related_name='nature_of_services')
    c_wportfolio=models.FileField(upload_to='wrok_portfolios/',null=True, blank=True)
    
    def __str__(self):
        return f"{self.company.c_name} - work profile"
    
class C_declaration(models.Model):
    company=models.OneToOneField(S_Company, on_delete=models.CASCADE, related_name='declaration')
    
    declaration=[
        ('YES', 'Yes'),
        ('NO', 'No'),
    ]
    c_p_verification=models.CharField(max_length=3, choices=declaration)
    c_noc=models.FileField(upload_to='company_noc/', null=True, blank=True)
    
    def __str__(self):
        return f"{self.company.c_name} - declaration"
    
class C_insurance(models.Model):
    company=models.ForeignKey(S_Company, on_delete=models.CASCADE, related_name='insurances')
    
    INSURANCE_TYPE=[
        ('LIABILITY', 'Liability'),
        ('WORKMEN', 'Workmen Compensation'),
        ('EQUIPMENT', 'Equipment'),
    ]
    
    c_ins_type=models.CharField(max_length=20, choices=INSURANCE_TYPE)
    c_ins_provider=models.CharField(max_length=30)
    c_ins_number=models.CharField(max_length=20)
    
    def __str__(self):
        return f"{self.company.c_name} - {self.c_ins_type}"
    
class C_chief_technician(models.Model):
    CHIEF_ROLE_CHOICES=[
        ('SUPERVISOR','CHIEF SUPERVISOR'),
        ('TECH_LEAD', 'TECHNICAL LEAD'),
        ('OPS_HEAD', 'OPERATION HEAD'),
        ('SITE_HEAD','SITE HEAD'),
        ('SERVICE_MANAGER','SERVICE MANAGER')
        
    ]
    CHIEF_EXP_CHOICES=[
        ('2','2 years'),
        ('2+','More than 2 years')
    ]
    company=models.OneToOneField(S_Company, on_delete=models.CASCADE, related_name='chief_technician')
    
    c_chief_name=models.CharField(max_length=30)
    c_chief_role=models.CharField(max_length=20, choices=CHIEF_ROLE_CHOICES)
    c_chief_exp=models.CharField(max_length=10,choices=CHIEF_EXP_CHOICES)
    c_chief_contact=models.CharField(max_length=15, validators=[mobile_validator])
    
    def __str__(self):
        return self.c_chief_name
    
    
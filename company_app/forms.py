from django import forms
from .models import *
from django.contrib.auth.password_validation import validate_password

#company details
class Company_form(forms.ModelForm):
    c_service_location = forms.ModelMultipleChoiceField(
        queryset=Location.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label= 'Service locations',
        error_messages= {'required' : "Please select atleast one service Location"})
    
    c_registration= forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        error_messages={
            'required':'Enter CIN registration (eg:L12345KL2023PLC123456)',
            'invalid': 'Enter a valid CIN number'
            })
    
    c_mobile_no= forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        error_messages={
            'required' : "Enter a valid 10-digit mobile number",
            'invalid' : 'Enter a valid 10-digit mobile number'
        }
    )
    c_email_id= forms.EmailField(
        widget=forms.TextInput(attrs={'class' :'form-control'}),
        error_messages={
            'required' : 'Enter a valid email address',
            'invalid' : 'Enter a valid email address'
        }
    )
    class Meta:
        model= S_Company
        
        fields = ['c_name',
                  'c_registration',
                  'c_mobile_no',
                  'c_email_id',
                  'c_service_location']
        
        widgets = {
            'c_name' : forms.TextInput(attrs={'class' : 'form-control',}),
        }
        
        labels = {
            'c_name' :'Company name',
            'c_registration' : 'CIN Registration',
            'c_mobile_no' : 'Mobile Number',
            'c_email_id' : 'Email ID',
            'c_service_location' : 'Location of Services'
             
        }
        help_text = {
            
        }

#authorized person details  
class Authorized_person_form(forms.ModelForm):
    
    class Meta:
        model = Auth_personal_details
        fields = ['auth_p_name',
                  'auth_p_designation',
                  'auth_p_mobile_no',
                  'auth_p_email_id',
                  'auth_id']
        
        widgets = {
            'auth_p_name' : forms.TextInput(attrs={'class' : 'form-control'}),
            'auth_p_designation' : forms.Select(attrs={'class' : 'form-control'}),
            'auth_p_mobile_no' : forms.TextInput(attrs={'class' : 'form-control'}),
            'auth_p_email_id' : forms.EmailInput(attrs={'class' : 'form-control'}),
            'auth_id' : forms.ClearableFileInput(attrs={'class': 'form-control'})
        }
        
        labels = {
            'auth_p_name' : 'Authorized Person Name',
            'auth_p_designation' : 'Designation',
            'auth_p_mobile_no' : 'Mobile Number',
            'auth_p_email_id' :'Email ID',
            'auth_id' :'Company ID Proof'
    
        }
        help_text = {
            
        }
    def __init__(self, *args, **kwargs):
            self.initial_file_path = kwargs.pop('initial_file_path', None)
            super().__init__(*args, **kwargs)
            
    def clean_auth_id(self):
            auth_id= self.cleaned_data.get('auth_id')
            if not auth_id and not self.initial_file_path:
                raise forms.ValidationError("Authorized person ID is required.")
            return auth_id

#legal info
class C_legal_registration_form(forms.ModelForm):
    class Meta:
        model= C_legal_registration
        fields = ['c_pan', 'c_gst']
        
        widgets = {
            'c_pan' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : ''}),
            'c_gst' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : ''}),
            }
        
        labels = {
            'c_pan' : 'PAN Card Number',
            'c_gst' : 'GST Registration Number',
        }
        help_text = {
            
        }
        
#company profile
class C_profile_form(forms.ModelForm):
    class Meta:
        model= C_profile_work
        fields = [
            'c_year',
            'c_nature_service',
            'c_wportfolio']
        
        widgets = {
            'c_year' : forms.Select(attrs={'class' : 'form-control'}),
            'c_nature_service' : forms.CheckboxSelectMultiple(),
            'c_wportfolio' : forms.ClearableFileInput(attrs={'class' : 'form-control'})
            }
        
        labels = {
            'c_year' : 'Year of Experience',
            'c_nature_service' : 'Company Service Categories',
            'c_wportfolio' : 'Upload Previous Work Portfolio'
            
        }
        help_text = {
            
        }
        
#company declaration 
class C_declaration_form(forms.ModelForm):
    class Meta:
        model = C_declaration
        
        fields = ['c_p_verification', 'c_noc']
        
        widgets = {
            'c_p_verification':forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'c_noc' : forms.ClearableFileInput(attrs={'class' : 'form-control'}),            
        }
        labels = {
            'c_p_verification' : 'Please confirm whether the company is verified.',
            'c_noc' : 'Upload Signed No Objection Certificate'
        }
        help_text = {
            'c_p_verification': 'please confirm whether the company is verified',
                'c_noc': 'upload signed no objection certificate'
            
        }
    
#insurance
class C_insurance_form(forms.ModelForm):
    class Meta:
        model= C_insurance
        fields = ['c_ins_type', 'c_ins_provider', 'c_ins_number']
        
        widgets = {
            'c_ins_type':forms.Select(attrs={'class':'form-control'}),
            'c_ins_provider':forms.TextInput(attrs={'class':'form-control',}),
            'c_ins_number':forms.TextInput(attrs={'class':'form-control'})
        }
        labels = {
            'c_ins_type' :'Insurance Type',
            'c_ins_provider' :'Insurance Provider',
            'c_ins_number' :'Insurance Number'
        }
        help_text = {

        }
        
#chief technician details
class C_Chieftechnician_form(forms.ModelForm):
    class Meta:
        model = C_chief_technician
        fields = ['c_chief_name',
                  'c_chief_role',
                  'c_chief_exp',
                  'c_chief_contact']
        
        widgets = {
            'c_chief_name' : forms.TextInput(attrs={'class':'form-control', 'placeholder':''}),
            'c_chief_role' :forms.Select(attrs={'class':'form-control', 'placeholder':''}),
            'c_chief_exp' :forms.Select(attrs={'class':'form-control', 'placeholder':''}),
            'c_chief_contact' :forms.TextInput(attrs={'class':'form-control', 'placeholder':''}),
        }
        labels = {
            'c_chief_name' : 'Name',
            'c_chief_role' : 'Role',
            'c_chief_exp' : 'Experience',
            'c_chief_contact' :'Mobile Number '
        }
        help_text = {}
  
#update credentials
class UpdateCredentialsForm(forms.Form):
    username = forms.CharField(
        max_length=50,
        required=False,
        label="New Username",
        widget=forms.TextInput(attrs={'class': 'form-control'})
        )

    password = forms.CharField(
        required=False,
        label="New Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
        )

    confirm_password = forms.CharField(
        required=False,
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
        )
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data['username']
        
        #
        if not username:
            return username
        #no change
        if username == self.user.username:
            return username
        # changes
        if User.objects.filter(username=username).exclude(id=self.user.id).exists():
            raise forms.ValidationError("This name is already taken")
        return username
    
            
    def clean(self):
        cleaned_data = super().clean()
        username= cleaned_data.get('username')
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        username_changed= False
        password_changed= False
        
        if username and username != self.user.username:
            username_changed =True
            
        if password:
            if not confirm_password:
                raise forms.ValidationError("Please confirm new password")
            
            if password != confirm_password:
                raise forms.ValidationError("Passwords do not match")
            
            if self.user.check_password(password):
                raise forms.ValidationError("New password cannot be same as old password")
            
            validate_password(password, self.user)
            password_changed = True
            
        if not username_changed and not password_changed:
            raise forms.ValidationError("No changes detected")
        
        self.cleaned_data['username_changed'] = username_changed
        self.cleaned_data['password_changed'] = password_changed
        
        return cleaned_data
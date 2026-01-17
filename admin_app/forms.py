from django import forms
from .models import *

class S_categoryForm(forms.ModelForm):
    def clean_category(self):
        category=self.cleaned_data['category'].strip()
        if S_Category.objects.filter(category=category).exists():
            raise forms.ValidationError("category already exists!")
        return category.title()
    
    label_suffix = ''
    
    class Meta:
        model=S_Category
        
        fields= ['category']
        
        labels = { 'category': 'Category Name',
                  }
        
        widgets= {'category':forms.TextInput(attrs={'class': 'form-control' , 'placeholder': 'enter service category name'}),
                  }
        
        help_texts={}
        
class HouseCrewForm(forms.ModelForm):
    
    class Meta:
        model=HouseCrew
        
        fields = ['h_services','s_category','is_emergency']
        
        widgets = {'h_services':forms.TextInput(attrs={'class':'form-control', 'placeholder':'enter the service'}),
                   's_category':forms.Select(attrs={'class':'form-control'}),
                   'is_emergency':forms.CheckboxInput(attrs={ 'class' : 'form-check-input', 'id' : 'emergencyCheckbox'})}
        
        labels= {
            'h_services' : 'Service',
            's_category' : 'Choose category',
            'is_emergency' : 'Emergency Yes/No'
            
        }
        
        help_texts = {}
    def clean_h_services(self):
        service= self.cleaned_data.get('h_services')
        if service:
            service = service.capitalize()
        return service

class LocationForm(forms.ModelForm):
    def clean_location(self):
        location=self.cleaned_data['location'].strip()
        if Location.objects.filter(location=location).exists():
            raise forms.ValidationError("location already exists!")
        return location.title()
    label_suffix=''
    class Meta:
        model=Location
        
        fields=['location']
        
        widgets= {'location' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'enter the location'})}
        
        
class AddServiceForm(forms.ModelForm):
    class Meta:
        model = AddServices
        
        fields = [
            'crew',
            'category',
            'name_of_service',
            'description',
            'base_charge',
            'is_emergency'
        ]
        
        widgets= {
            'crew' : forms.Select(attrs={'class': 'form-control'}),
            'category' : forms.Select(attrs={'class': 'form-control'}),
            'name_of_service' : forms.TextInput(attrs= { 'class': 'form-control', 'rows' : 3}),
            'description' :forms.Textarea(attrs={ 'class': 'form-control'}),
            'base_charge' : forms.NumberInput(attrs={'class' : 'form-control'}),
            'is_emergency':forms.CheckboxInput(attrs={ 'class' : 'form-check-input', 'id' : 'emergencyCheckbox'})    
              
        }
        labels= {
            'crew' : 'Choose service',
            'category' : 'Choose Category',
            'name_of_service' :'Enter the Service',
            'description' : 'Description',
            'base_charge' : 'Base charge',
            'is_emergency' : 'Emergency'
        }
    def clean_name_of_service(self):
        name=self.cleaned_data.get('name_of_service')
        if name:
            name=name.capitalize()
        return name
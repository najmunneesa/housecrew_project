from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError

def unique_slug(instance, new_slug=None):
    base_slug = new_slug or slugify(instance.category)
    slug = base_slug
    Klass = instance.__class__
    counter= 1
    while Klass.objects.filter(slug=slug).exists():
        slug = f"{base_slug}-{counter}"
        counter +=1
    return slug
    
#category
class S_Category(models.Model):
    category=models.CharField(max_length=60)
    slug = models.SlugField(unique=True, blank=True, db_index=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug(self)
        super().save(*args, **kwargs)
            
    
    def __str__(self):
        return self.category
   
#services
class HouseCrew(models.Model):
    h_services=models.CharField(max_length=100)
    s_category=models.ForeignKey(S_Category, on_delete=models.CASCADE, null=False, blank=False )
    is_emergency=models.BooleanField(default=False)
    
    class Meta:
        unique_together=('h_services', 's_category')
    
    def __str__(self):
        return f"{self.h_services} - {self.s_category}"
    
class Location(models.Model):
    location=models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.location
    

#sub_services
class AddServices(models.Model):
    
    crew=models.ForeignKey(HouseCrew, on_delete=models.CASCADE, null=False, blank=False, related_name='services')
    name_of_service=models.CharField(max_length=100)
    description=models.TextField()
    base_charge=models.DecimalField(max_digits=10, decimal_places=2)
    category=models.ForeignKey(S_Category, on_delete=models.CASCADE, null=True, blank=False, related_name='services')
    is_emergency=models.BooleanField(default=False)
    
    
    def __str__(self):
        return f"{self.name_of_service}({self.crew} - {self.category})"
    
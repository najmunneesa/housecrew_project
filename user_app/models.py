from django.db import models
from django.contrib.auth.models import User
from admin_app.models import S_Category, HouseCrew, AddServices
from company_app.models import S_Company

class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('ADMIN', 'ADMIN'),
        ('COMPANY', 'COMPANY'),
        ('USER', 'USER'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='USER')

    def __str__(self):
        return f"{self.user.username} - {self.role}"
    
class CallBackRequest(models.Model):
    name=models.CharField(max_length=50)
    contact=models.CharField(max_length=15)
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name}-{self.contact}"
    
    
class Booking(models.Model):
    STATUS_CHOICES=[
        ('pending' , 'pending'),
        ('allocated', 'allocated'),
        ('completed' , 'completed'),
        ('rejected' , 'rejected')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(AddServices, on_delete=models.CASCADE)
    company=models.ForeignKey(S_Company, on_delete=models.CASCADE, null=True, blank=True)
    booked_at = models.DateTimeField(auto_now_add=True)
    is_emergency=models.BooleanField(default=False)
    is_available= models.BooleanField(default=True)
    crew=models.ForeignKey(HouseCrew, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES ,default='PENDING')
    
    def __str__(self):
        return f"{self.user.username} - {self.crew.h_services} - {self.company}"
    

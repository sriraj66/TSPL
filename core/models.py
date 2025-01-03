from django.db import models
from django.contrib.auth.models import User
from .constants import *
import uuid

class Setting(models.Model):
    name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    
    amount = models.PositiveIntegerField(default=0,verbose_name="Registration Amount")
    accept_response = models.BooleanField(default=False,verbose_name="Accept Response")
    
    class Meta:
        ordering = ['-id']
    
    def __str__(self):
        return self.name
    

class PlayerRegistration(models.Model):
    
    id = models.UUIDField( 
         primary_key = True, 
         default = uuid.uuid4, 
         editable = False) 
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User')
    registration_category = models.CharField(max_length=20, choices=REGISTRATION_CATEGORIES, verbose_name='Registration Category')
    date_application = models.DateField(auto_now_add=True, verbose_name='Date of Application')
    player_name = models.CharField(max_length=100, verbose_name='Player Name')
    father_name = models.CharField(max_length=100, verbose_name='Father’s Name')
    mother_name = models.CharField(max_length=100, verbose_name='Mother’s Name')
    dob = models.DateField(verbose_name='Date of Birth')
    gender = models.CharField(max_length=10, choices=GENDERS, verbose_name='Gender')
    tshirt_size = models.CharField(max_length=1, choices=TSHIRT_SIZES, verbose_name='T-Shirt Size')
    mobile = models.CharField(max_length=15, verbose_name='Mobile Number')
    emergency_mobile = models.CharField(max_length=15, verbose_name='Emergency Mobile Number')
    email = models.EmailField(verbose_name='Email Address')
    adhar_card = models.CharField(max_length=12, unique=True, verbose_name='Aadhar Card Number')
    player_image = models.ImageField(upload_to='player_images/', verbose_name='Player Image')
    district = models.CharField(max_length=100,choices=DISTRICT_CHOICES, verbose_name='District')
    
    zone = models.CharField(max_length=10, editable=False, verbose_name="ZONE",default="ZONE A")
    
    pin_code = models.PositiveIntegerField(verbose_name='PIN Code')
    address = models.TextField(verbose_name='Address')
    level = models.CharField(max_length=20, choices=LEVELS, verbose_name='Player Level')
    bowling_arm = models.CharField(max_length=10, choices=BOWLING_ARMS, verbose_name='Bowling Arm')
    bowling_pace = models.CharField(max_length=10, choices=BOWLING_PACES, verbose_name='Bowling Pace')
    first_preference = models.CharField(max_length=10, choices=FIRST_PREFERENCES, verbose_name='First Preference')
    captain_exp = models.CharField(max_length=3, choices=CAPTAIN_EXPERIENCES, verbose_name='Captain Experience')


    is_paid = models.BooleanField(default=False,verbose_name="Is Player Paid")
    tx_id = models.CharField(blank=True,max_length=255,verbose_name="Transition ID#")
    
    created = models.DateTimeField(auto_now_add=True,verbose_name="Created At")

    class Meta:
        ordering = ['-created']

    def save(self, *args, **kwargs):
        self.zone = DISTRICT_ZONE_MAP.get(self.district, 'Unknown')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.player_name

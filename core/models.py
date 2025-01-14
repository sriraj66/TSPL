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
    
    reg_id = models.CharField(
        max_length=20,
        unique=True,
        editable=False,
        verbose_name="Register ID"
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User')
    player_name = models.CharField(max_length=100, verbose_name='Player Name')
    father_name = models.CharField(max_length=100, verbose_name='Father’s Name')
    
    category = models.CharField(max_length=25, choices=REGISTRATION_CATEGORIES, verbose_name='Category')
    age = models.PositiveIntegerField( verbose_name='Player Age')

    dob = models.DateField(verbose_name='Date of Birth')
    gender = models.CharField(max_length=10, choices=GENDERS, verbose_name='Gender')
    tshirt_size = models.CharField(max_length=4, choices=TSHIRT_SIZES, verbose_name='T-Shirt Size')
    occupation = models.CharField(max_length=14,choices=OCCUPATION,default=3,verbose_name="Player Occupation")
    mobile = models.CharField(max_length=10, verbose_name='Mobile Number')
    
    wathsapp_number = models.CharField(max_length=10, verbose_name='Wathsapp Number')
    
    email = models.EmailField(verbose_name='Email Address')
    adhar_card = models.CharField(max_length=12, unique=True, verbose_name='Aadhar Card Number')
    player_image = models.ImageField(upload_to='player_images/', verbose_name='Player Image')
    
    district = models.CharField(max_length=100,choices=DISTRICT_CHOICES, verbose_name='District')
    
    zone = models.CharField(max_length=10, editable=False, verbose_name="Zone",default="ZONE A")
    
    pin_code = models.PositiveIntegerField(verbose_name='PIN Code')
    address = models.TextField(verbose_name='Address')
    first_preference = models.CharField(max_length=10,default=0,choices=FIRST_PREFERENCES, verbose_name='First Preference')
    batting_arm = models.CharField(max_length=10, default=0 ,choices=BOWLING_ARMS, verbose_name='Batting Arm')
    role = models.CharField(max_length=100,choices=ROLE,verbose_name="Player Role",default=0)


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


# Signals
from django.db.models.signals import pre_save
from django.dispatch import receiver
import datetime



@receiver(pre_save, sender=PlayerRegistration)
def generate_user_id(sender, instance, **kwargs):
    if not instance.reg_id:  
        print("")
        current_date = datetime.datetime.now()
        month = current_date.strftime('%m') 
        year = current_date.strftime('%y')

        last_record = (
            sender.objects.filter(reg_id__startswith=f"TSPL{month}{year}")
            .order_by('-reg_id')
            .first()
        )

        if last_record:
            # last_number = int(last_record.reg_id.split(f"TSPL{month}{year}")[-1])
            last_number = len(sender.objects.all())
            new_number = last_number + 1
        else:
            new_number = 1

        instance.reg_id = f"TSPL{month}{year}{new_number}"
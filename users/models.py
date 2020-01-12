from django.db import models
from django.contrib.auth.models import User
from blog.models import State

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    bio = models.CharField(
        max_length=50, default='Not Specified', null=True)
    credits = models.IntegerField(default=10)

    def __str__(self):
        return f'{self.user.username} Profile'


class Authority(models.Model):
    AUTHORITYTYPES_CHOICES = (('Department of consumer affairs','Department of consumer affairs'),('Department of food and public distribution','Department of food and public distribution'),('Serious Fraud Investigation Office','Serious Fraud Investigation Office'),('Forest Reserve Conservation Authority','Forest Reserve Conservation Authority'),('Criminal Investigation Department','Criminal Investigation Department'),('Labour Beauro','Labour Beauro'),('National Commission for Minorities','National Commission for Minorities'),('National Commission for Women','National Commission for Women'),('Incometax Department','Incometax Department'))
    STATE_CHOICES = (("Select State","Select State"),("Andhra Pradesh","Andhra Pradesh"),("Arunachal Pradesh ","Arunachal Pradesh "),("Assam","Assam"),("Bihar","Bihar"),("Chhattisgarh","Chhattisgarh"),("Goa","Goa"),("Gujarat","Gujarat"),("Haryana","Haryana"),("Himachal Pradesh","Himachal Pradesh"),("Jammu and Kashmir ","Jammu and Kashmir "),("Jharkhand","Jharkhand"),("Karnataka","Karnataka"),("Kerala","Kerala"),("Madhya Pradesh","Madhya Pradesh"),("Maharashtra","Maharashtra"),("Manipur","Manipur"),("Meghalaya","Meghalaya"),("Mizoram","Mizoram"),("Nagaland","Nagaland"),("Odisha","Odisha"),("Punjab","Punjab"),("Rajasthan","Rajasthan"),("Sikkim","Sikkim"),("Tamil Nadu","Tamil Nadu"),("Telangana","Telangana"),("Tripura","Tripura"),("Uttar Pradesh","Uttar Pradesh"),("Uttarakhand","Uttarakhand"),("West Bengal","West Bengal"),("Andaman and Nicobar Islands","Andaman and Nicobar Islands"),("Chandigarh","Chandigarh"),("Dadra and Nagar Haveli","Dadra and Nagar Haveli"),("Daman and Diu","Daman and Diu"),("Lakshadweep","Lakshadweep"),("National Capital Territory of Delhi","National Capital Territory of Delhi"),("Puducherry","Puducherry"))
    
    state = models.CharField(max_length=100, default='not provided', choices = STATE_CHOICES)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Email_id = models.EmailField(default='shadow@gmail.com')
    Dept_id = models.CharField(max_length=50, default='123')
    Dept_name = models.CharField(max_length=50, default='Incometax Department',choices=AUTHORITYTYPES_CHOICES)
    profile_complete = models.BooleanField(default=False)
    credits = models.IntegerField(default=10)
    def __str__(self):
        return str(self.user)


class Anonymous(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Email_id = models.EmailField(default='shadow@gmail.com')
    Dept_id = models.CharField(max_length=10, default='Ano')
    Dept_name = models.CharField(max_length=10, default='ano')
    profile_complete = models.BooleanField(default=False)
    credits = models.IntegerField(default=10)

    def __str__(self):
        return str(self.user)

class Journalist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Email_id = models.EmailField(default='shadow@gmail.com')
    Dept_id = models.CharField(max_length=50, default='123')
    Dept_name = models.CharField(max_length=50, default='BBC')
    profile_complete = models.BooleanField(default=False)
    credits = models.IntegerField(default=10)
    def __str__(self):
        return str(self.user)
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import MinLengthValidator, MaxLengthValidator

# Create your models here.


class State(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class City(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Location(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE, null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True)

class Post(models.Model):
    CRIMETYPE_CHOICES = (('White-Collar Crime', 'White-Collar Crime'), ('Robbery', 'Robbery'), ('Rape', 'Rape'), ('Assualt', 'Assault'), ('Arson', 'Arson'), ('Homicide', 'Homicide'), ('Crimes Against Morality', 'Crimes Against Morality'), ('Illegal goods', 'Illegal goods'),
                         ('Poaching and Illegal Felling', 'Poaching and Illegal Felling'), ('Adultery in Food Sector', 'Adultery in Food Sector'), ('Ill-treatment of Workers', 'Ill-treatment of Workers'), ('Tax Evasion', 'Tax Evasion'), ('Sexual Harrassment', 'Sexual Harrassment'), ('Communal Crimes', 'Communal Crimes'))
    #STATE_CHOICES = (("Select State","Select State"),("Andhra Pradesh","Andhra Pradesh"),("Arunachal Pradesh ","Arunachal Pradesh "),("Assam","Assam"),("Bihar","Bihar"),("Chhattisgarh","Chhattisgarh"),("Goa","Goa"),("Gujarat","Gujarat"),("Haryana","Haryana"),("Himachal Pradesh","Himachal Pradesh"),("Jammu and Kashmir ","Jammu and Kashmir "),("Jharkhand","Jharkhand"),("Karnataka","Karnataka"),("Kerala","Kerala"),("Madhya Pradesh","Madhya Pradesh"),("Maharashtra","Maharashtra"),("Manipur","Manipur"),("Meghalaya","Meghalaya"),("Mizoram","Mizoram"),("Nagaland","Nagaland"),("Odisha","Odisha"),("Punjab","Punjab"),("Rajasthan","Rajasthan"),("Sikkim","Sikkim"),("Tamil Nadu","Tamil Nadu"),("Telangana","Telangana"),("Tripura","Tripura"),("Uttar Pradesh","Uttar Pradesh"),("Uttarakhand","Uttarakhand"),("West Bengal","West Bengal"),("Andaman and Nicobar Islands","Andaman and Nicobar Islands"),("Chandigarh","Chandigarh"),("Dadra and Nagar Haveli","Dadra and Nagar Haveli"),("Daman and Diu","Daman and Diu"),("Lakshadweep","Lakshadweep"),("National Capital Territory of Delhi","National Capital Territory of Delhi"),("Puducherry","Puducherry"))
    CRIMETYPE1_CHOICES = (('None', 'None'), ('White-Collar Crime', 'White-Collar Crime'), ('Robbery', 'Robbery'), ('Rape', 'Rape'), ('Assualt', 'Assault'), ('Arson', 'Arson'), ('Homicide', 'Homicide'), ('Crimes Against Morality', 'Crimes Against Morality'), ('Illegal goods', 'Illegal goods'),
                          ('Poaching and Illegal Felling', 'Poaching and Illegal Felling'), ('Adultery in Food Sector', 'Adultery in Food Sector'), ('Ill-treatment of Workers', 'Ill-treatment of Workers'), ('Tax Evasion', 'Tax Evasion'), ('Sexual Harrassment', 'Sexual Harrassment'), ('Communal Crimes', 'Communal Crimes'))

    AUTHORITYTYPES_CHOICES = (('Department of Consumer Affairs', 'Department of Consumer Affairs'), ('Department of Food and Public Distribution', 'Department of Food and Public Distribution'), ('Serious Fraud Investigation Office', 'Serious Fraud Investigation Office'), ('Forest Reserve Conservation Authority', 'Forest Reserve Conservation Authority'),
                              ('Criminal Investigation Department', 'Criminal Investigation Department'), ('Labour Bureau', 'Labour Bureau'), ('National Commission for Minorities', 'National Commission for Minorities'), ('National Commission for Women', 'National Commission for Women'), ('Income Tax Department', 'Income Tax Department'))

    title = models.CharField(max_length=100)
    crimetype1 = models.CharField(
        max_length=100, default='not provided', choices=CRIMETYPE_CHOICES, null=True)
    crimetype2 = models.CharField(
        max_length=100, default=None, choices=CRIMETYPE1_CHOICES, null=True)
    crimetype3 = models.CharField(
        max_length=100, default=None, choices=CRIMETYPE1_CHOICES, null=True)
    crimetype4 = models.CharField(
        max_length=100, default=None, choices=CRIMETYPE1_CHOICES, null=True)
    authority = models.CharField(
        max_length=10000, default='Incometax Department')
    location = models.TextField(max_length=60)
    content = models.TextField(max_length=300)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    country = models.CharField(max_length=20, default="India")
    upvotes = models.ManyToManyField(User, related_name='upvotes', blank=True)
    downvotes = models.ManyToManyField(
        User, related_name='downvotes', blank=True)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    tags = models.CharField(max_length=1000,default="None")

    #state = models.CharField(max_length=100, default='not provided', choices = STATE_CHOICES)
    #city = models.CharField(max_length=20, default='not provided')
    # city = models.ForeignKey(City, default='Delhi',
    #                          on_delete=models.CASCADE, null=False)
    pincode = models.CharField('Pincode', validators=[
                               MinLengthValidator(6)], max_length=6, default='000000')
    photo1 = models.ImageField(upload_to='post_pics',
                               blank='True')
    photo2 = models.ImageField(upload_to='post_pics',
                               blank='True')
    photo3 = models.ImageField(upload_to='post_pics',
                               blank='True')
    photo4 = models.ImageField(upload_to='post_pics',
                               blank='True')

    def __str__(self):
        return self.title

    def total_upvotes(self):
        return self.upvotes.count()

    def total_downvotes(self):
        return self.downvotes.count()

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={"pk": self.pk})

    def approve(self):
        self.approved_posts = True
        self.save()

    def approved_posts1(self):
        return self.post.filter(approved_posts=True)

class Comment(models.Model):
    post = models.ForeignKey(
        'blog.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)

    class Meta:
        ordering = ["-created_date"]


class registerCamera(models.Model):
    STATE_CHOICES = (("Select State","Select State"),("Andhra Pradesh","Andhra Pradesh"),("Arunachal Pradesh ","Arunachal Pradesh "),("Assam","Assam"),("Bihar","Bihar"),("Chhattisgarh","Chhattisgarh"),("Goa","Goa"),("Gujarat","Gujarat"),("Haryana","Haryana"),("Himachal Pradesh","Himachal Pradesh"),("Jammu and Kashmir ","Jammu and Kashmir "),("Jharkhand","Jharkhand"),("Karnataka","Karnataka"),("Kerala","Kerala"),("Madhya Pradesh","Madhya Pradesh"),("Maharashtra","Maharashtra"),("Manipur","Manipur"),("Meghalaya","Meghalaya"),("Mizoram","Mizoram"),("Nagaland","Nagaland"),("Odisha","Odisha"),("Punjab","Punjab"),("Rajasthan","Rajasthan"),("Sikkim","Sikkim"),("Tamil Nadu","Tamil Nadu"),("Telangana","Telangana"),("Tripura","Tripura"),("Uttar Pradesh","Uttar Pradesh"),("Uttarakhand","Uttarakhand"),("West Bengal","West Bengal"),("Andaman and Nicobar Islands","Andaman and Nicobar Islands"),("Chandigarh","Chandigarh"),("Dadra and Nagar Haveli","Dadra and Nagar Haveli"),("Daman and Diu","Daman and Diu"),("Lakshadweep","Lakshadweep"),("National Capital Territory of Delhi","National Capital Territory of Delhi"),("Puducherry","Puducherry"))

    
    address = models.CharField(max_length=60)
    pincode = models.CharField('Pincode', validators=[
                               MinLengthValidator(6)], max_length=6)
    state = models.CharField(max_length=100, default='not provided', choices = STATE_CHOICES)
    city = models.CharField(max_length=20)

    def __str__(self):
        return self.address

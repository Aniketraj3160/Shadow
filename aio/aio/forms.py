from django import forms
from .models import *
from django.utils import timezone

crimetypes=(('Personal Crimes', 'Personal Crimes'),
            ('Larceny', 'Larceny'),
            ('Forgery', 'Forgery'),
            ('False Pretenses', 'False Pretenses'),
            ('Solicitation', 'Solicitation'),
            ('Conspiracy', 'Conspiracy'),
) 

class Add_Forum(forms.Form):
    subject = forms.CharField(required=True, min_length=5, strip=True, label = "Subject")
    forumID = forms.CharField(required=True, min_length=6, label = "ForumID")
    
class Add_location(forms.Form):
    pincode = forms.IntegerField(required = True, label="Pincode")
    city = forms.CharField(required = True, min_length=3, label="City")
    state = forms.CharField(required = True, min_length=3, label="State")

class add_Authority(forms.Form):
    authid = forms.CharField(min_length=2, label="Authority ID")
    department = forms.CharField(min_length=5, label="Department Name")
    contact_person = forms.CharField(min_length=3, label="Person of Contact")
    email = forms.CharField(min_length=5, label="Email")

class add_post(forms.Form):
    title = forms.CharField(min_length = 3, label = "Title")
    content = forms.CharField(min_length = 10, label = "Complaint")
    crime_type = forms.ChoiceField(choices=crimetypes, label='Type of Crime')
    


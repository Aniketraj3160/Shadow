from django.db import models
#Import USer here from the user app
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.models import User
from PIL import Image
from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator


class Location(models.Model):
    pincode = models.CharField(max_length = 10, primary_key=True)
    city = models.CharField(max_length = 100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default="India")

    def __str__(self):
        return "Pincode : {0} City : {1} State : {2} Country : {3}".format(self.pincode, self.city, self.state, self.country)

class Authority(models.Model):
    authid = models.CharField(max_length = 10, primary_key=True)
    department = models.CharField(max_length = 10, primary_key=True)
    contact_person = models.CharField(max_length = 100)
    email = models.CharField(max_length=100, null=True)

    def __str__(self):
        return "AuthorityID : {0} Person of Contact : {1} Email : {2}".format(self.authid, self.contact_person, self.email)

class images(models.Model):
    evidenceid=models.CharField(max_length = 10, primary_key=True)
    photo1 = models.ImageField(null=True, blank=True, default='default.jpg', upload_to='pics')
    photo2 = models.ImageField(null=True, blank=True, default='default.jpg', upload_to='pics')
    photo3 = models.ImageField(null=True, blank=True, default='default.jpg', upload_to='pics')
    photo4 = models.ImageField(null=True, blank=True, default='default.jpg', upload_to='pics')
    photo5 = models.ImageField(null=True, blank=True, default='default.jpg', upload_to='pics')


class forums(models.Model):
    forumid = models.CharField(max_length = 10, primary_key=True)
    subject = models.CharField(max_length = 100, default=None)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    authority = models.ForeignKey(Authority, on_delete=models.CASCADE)

    def __str__(self):
        return "ForumID : {0} Authority : {2} ".format(self.tipid, self.authority.authid)

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    forum = models.ForeignKey(forums, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    content = models.TextField(max_length=5000, blank=True)
    ups = models.IntegerField(default=0)
    downs = models.IntegerField(default=0)
    score = models.IntegerField(default=0)
    timestamp = models.DateTimeField(default=timezone.now)
    comment_count = models.IntegerField(default=0)
    crimeType = models.CharField(max_length=100)
    images = models.ForeignKey(images, on_delete=models.DO_NOTHING)

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    submission = models.ForeignKey(Post, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    ups = models.IntegerField(default=0)
    downs = models.IntegerField(default=0)
    score = models.IntegerField(default=0)
    raw_comment = models.TextField(blank=True)
    

#


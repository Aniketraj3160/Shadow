from django.contrib import admin
from .models import Post, Comment, registerCamera, State, City
# Register your models here.

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(registerCamera)
admin.site.register(State)
admin.site.register(City)

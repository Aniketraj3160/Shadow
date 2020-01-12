from django.contrib import admin
from .models import *

admin.site.register(Profile)
admin.site.register(Journalist)
admin.site.register(Authority)
admin.site.register(Anonymous)

# Register your models here.

from django.contrib import admin
from .models import Location,Authority,images,forums,Post,Comment
# Register your models here.

@admin.register(Location,Authority,images,forums,Post,Comment)
class ViewAdmin(admin.ModelAdmin):
	pass
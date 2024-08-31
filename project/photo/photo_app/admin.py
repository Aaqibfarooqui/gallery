from django.contrib import admin
from .models import pro

# Register your models here.
class servicesAdmin(admin.ModelAdmin):
    list_display=['id','name','price','description','Categories','is_active']
    list_filter=['Categories','is_active']
admin.site.register(pro,servicesAdmin)
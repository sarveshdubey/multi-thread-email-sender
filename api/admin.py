from django.contrib import admin
from .models import Subscribe_model
# Register your models here.
@admin.register(Subscribe_model)
class Subscribe_model(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'email'
    ]

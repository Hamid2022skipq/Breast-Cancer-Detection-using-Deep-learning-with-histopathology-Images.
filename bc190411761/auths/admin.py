from django.contrib import admin
from .models import Predict

@admin.register(Predict)
class YourModelAdmin(admin.ModelAdmin):
    list_display = ('prediction_image',) 

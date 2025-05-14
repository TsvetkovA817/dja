from django.contrib import admin

# регистрация моделей

from .models import Client, Car
admin.site.register(Client)
admin.site.register(Car)

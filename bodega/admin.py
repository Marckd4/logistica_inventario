from django.contrib import admin
from .models import Producto
from django.contrib.auth.models import Group, Permission


admin.site.register(Producto)

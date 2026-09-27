from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_at")
    search_fields = ("name",)

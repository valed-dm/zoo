from django.contrib import admin

from .models import Animal, Card, Category, Food

# Register your models here.
admin.site.register(Animal)
admin.site.register(Card)
admin.site.register(Category)
admin.site.register(Food)

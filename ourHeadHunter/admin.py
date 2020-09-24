from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User,Person,Company,Vacancy,Category

# Register your models here.

admin.site.register(User)
admin.site.register(Person)
admin.site.register(Company)
admin.site.register(Vacancy)
admin.site.register(Category)


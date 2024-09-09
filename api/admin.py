from django.contrib import admin
from .models import User, Order


class UserAdmin(admin.ModelAdmin):
    pass

class SalesAdmin(admin.ModelAdmin):
    pass

class UserAdmin(admin.ModelAdmin):
    pass


admin.site.register(Order, SalesAdmin)
admin.site.register(User, UserAdmin)
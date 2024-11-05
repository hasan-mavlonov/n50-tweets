from django.contrib import admin
from tweets.models import UserModel
# Register your models here.
@admin.register(UserModel)
class UserModelAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'date_joined', 'last_login')
    search_fields = ('username', 'email')
    list_filter = ('date_joined', 'last_login')

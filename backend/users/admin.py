from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """настройка интерфейса админки для User"""

    list_display = (
        'pk',
        'username',
        'email',
        'first_name',
        'last_name',
    )
    list_filter = ('email', 'username',)
    search_fields = ('email', 'username',)
    list_editable = ('username', 'first_name', 'last_name',)

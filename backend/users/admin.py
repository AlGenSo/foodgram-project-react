from django.contrib import admin

from .models import Subscription, User


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


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):

    list_display = (
        'author',
        'user'
    )
    search_fields = ('author',)
    list_filter = ('author',)

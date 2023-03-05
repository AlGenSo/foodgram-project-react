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
        'count_recipes',
        'count_subscribers'
    )
    list_filter = ('email', 'username',)
    search_fields = ('email', 'username',)
    list_editable = ('username', 'email', 'first_name', 'last_name')

    def count_subscribers(self, obj):
        return obj.blogger.count()
    count_subscribers.short_description = 'Подписчиков'

    def count_recipes(self, obj):
        return obj.recipes.count()
    count_recipes.short_description = 'Рецептов'


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):

    list_display = (
        'author',
        'user'
    )
    search_fields = ('author',)
    list_filter = ('author',)

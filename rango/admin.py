from django.contrib import admin
from . models import Page, Category, UserProfile

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'id']


class PageAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'url', 'views']

admin.site.register(UserProfile)
admin.site.register(Page, PageAdmin)
admin.site.register(Category, CategoryAdmin)

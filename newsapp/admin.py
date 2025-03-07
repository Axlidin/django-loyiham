from django.contrib import admin
from .models import News, Category
# admin.site.register(Category)
# admin.site.register(News)

# @admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['id', 'name']
    list_filter = ['name']

# @admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'category', 'status', 'created_time', 'published_time')
    list_filter = ['status', 'created_time', 'published_time']
    search_fields = ['title', 'status', 'category__name', 'published_time', 'created_time']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_time'
    search_fields = ['title', 'body']
    ordering = ['status', 'published_time']

admin.site.register(News, NewsAdmin)
admin.site.register(Category, CategoryAdmin
                    )
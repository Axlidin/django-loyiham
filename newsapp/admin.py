from django.contrib import admin
from .models import News, Category, ContactModel, Comment, NewsLike


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
    list_filter = ['status', 'category', 'created_time', 'published_time']
    search_fields = ['title', 'status', 'category__name', 'published_time', 'created_time']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_time'
    search_fields = ['title', 'body']
    ordering = ['status', 'published_time']

class ContactAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email']

# @admin.register(Comment)
class AdminComment(admin.ModelAdmin):
    list_display = ['user', 'body', 'active', 'created_time']
    list_filter = ['active', 'created_time']
    search_fields = ['user', 'body']
    actions = ['disabled_actived', 'enabled_actived']

    def disabled_actived(self, request, queryset):
        queryset.update(active=False)

    def enabled_actived(self, request, queryset):
        queryset.update(active=True)

@admin.register(NewsLike)
class NewsLikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'news']


admin.site.register(Comment, AdminComment)
admin.site.register(News, NewsAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(ContactModel, ContactAdmin)
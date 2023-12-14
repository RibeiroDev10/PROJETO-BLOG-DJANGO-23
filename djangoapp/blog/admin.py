from django.contrib import admin
from blog.models import Tag, Category, Page
# Register your models here.
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = 'id', 'name', 'slug',
    list_display_links = 'name',
    search_fields = 'id', 'name', 'slug',
    list_per_page = 10
    ordering = '-id',
    prepopulated_fields = {
        "slug": ('name', ),   # Campo SLUG pega o valor do campo NAME
    }

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = 'id', 'name', 'slug',
    list_display_links = 'name',
    search_fields = 'id', 'name', 'slug',
    list_per_page = 10
    ordering = '-id',
    prepopulated_fields = {
        "slug": ("name", ),
    }

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = 'id', 'title', 'is_published'
    list_display_links = 'id', 'title',
    list_editable = 'is_published',
    search_fields = 'id', 'title',
    list_per_page = 10
    ordering = '-id',
    prepopulated_fields = {
        "slug": ("title", ),
    }
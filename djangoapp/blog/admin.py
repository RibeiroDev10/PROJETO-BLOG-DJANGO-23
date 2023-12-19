from django.contrib import admin
from blog.models import Tag, Category, Page, Post
from django_summernote.admin import SummernoteModelAdmin
from django.urls import reverse
from django.utils.safestring import mark_safe


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
class PageAdmin(SummernoteModelAdmin):
    summernote_fields = ('content', )
    list_display = 'id', 'title', 'is_published'
    list_display_links = 'id', 'title',
    list_editable = 'is_published',
    search_fields = 'id', 'title',
    list_per_page = 10
    ordering = '-id',
    prepopulated_fields = {
        "slug": ("title", ),
    }
            # Post -> obj
@admin.register(Post)  # Campos que aparecerão na tabela
class PostAdmin(SummernoteModelAdmin):  # PostAdmin -> self
    summernote_fields = ('content', )
    list_display = 'id', 'title', 'is_published', 'created_by'
    list_display_links = 'title',
    search_fields = 'id', 'slug', 'title', 'excerpt', 'content',
    list_per_page = 50
    list_filter = 'category', 'is_published'
    list_editable = 'is_published',
    ordering = '-id',
    readonly_fields = 'created_at', 'updated_at', 'created_by', 'updated_by', 'link'
    prepopulated_fields = {
        "slug": ("title", ),
    }
    autocomplete_fields = 'tags', 'category',

    # Este método se torna um campo, em: readonly_fields.
    # self -> classe, obj -> Post e seus atributos.
    def link(self, obj):
        if not obj.pk:  # Se o objeto no momento atual não tiver Primary Key... (Não foi criado)
            return '-'
        
        url_do_post = obj.get_absolute_url()  # Pegando a URL do post de modo reverso
        safe_link = mark_safe(f'<a target="_blank" href="{url_do_post}">Ver post</a>')
        return safe_link


    def save_model(self, request, obj, form, change):
        # Se estiver ALTERANDO ...
        if change:
            obj.updated_by = request.user  # obj é o model, no caso model POST
        else:  # Se estiver CRIANDO ...
            obj.created_by = request.user

        obj.save()
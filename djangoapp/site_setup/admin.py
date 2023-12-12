from django.contrib import admin
from django.http.request import HttpRequest
from site_setup.models import MenuLink, SiteSetup

"""
Essencialmente, o @admin.register() é uma maneira de
dizer ao Django que você deseja tornar um modelo gerenciável através da interface 
de administração e que você forneceu uma classe (como MenuLinkAdmin) para 
personalizar como esse modelo é apresentado e gerenciado na interface de administração.
"""
# @admin.register(MenuLink)
# class MenuLinkAdmin(admin.ModelAdmin):
#     list_display = 'id', 'text', 'url_or_path', 'new_tab',  # Exibição da lista/tabelas de dados
#     list_display_links = 'id', 'text', 'url_or_path',  # Colunas que são links
#     search_fields = 'id', 'text', 'url_or_path',  # Colunas que são buscáveis


class MenuLinkInline(admin.TabularInline):
    model = MenuLink
    extra = 1


@admin.register(SiteSetup)
class SiteSetupAdmin(admin.ModelAdmin):
    list_display = 'title', 'description',
    inlines = MenuLinkInline,  # Define campos do atribudo model da classe MenuLinkAdmin na classe SiteSetup do Django Admin

    # Tem permissão para 'Adicionar'? -> True or False
    def has_add_permission(self, request: HttpRequest) -> bool:
        return not SiteSetup.objects.exists()  # True or False
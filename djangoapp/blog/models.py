from django.db import models
from utils.rands import slugify_new

# Create your models here.
class Tag(models.Model):
    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    name = models.CharField(max_length=255)
    slug = models.SlugField(
        unique=True, default=None,
        null=True, blank=True, max_length=255,
    )

    def save(self, *args, **kwargs):
        # Se nao existe uma SLUG, vou criar uma...
        if not self.slug:
            self.slug = slugify_new(self.name, 5)  # Pegando o nome da TAG e gerando a partir disso.
        return super().save(*args, **kwargs)
    
    # Quando eu entro dentro de uma categoria, esse será o TÍTULO que aparecerá.
    def __str__(self) -> str:
        return self.name


class Category(models.Model):
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=255)
    slug = models.SlugField(
        unique=True, default=None,
        null=True, blank=True, max_length=255,
    )

    # Verifica se existe o SLUG
    # Insere um novo SLUG se não existe
    # Salva no banco de dados esse novo SLUG
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_new(self.name, 5)
        return super().save(*args, **kwargs)
    
    # Quando eu entro dentro de uma categoria, esse será o TÍTULO que aparecerá.
    def __str__(self) -> str:
        return self.name
    

class Page(models.Model):
    class Meta:
        verbose_name = 'Page'
        verbose_name_plural = 'Pages'

    title = models.CharField(max_length=65)
    slug = models.SlugField(
        unique=True, default=None,
        null=True, blank=True, max_length=255,
    )
    is_published = models.BooleanField(
        default=False, 
        help_text='Este campo precisará estar marcado para a página ser exibida publicamente'
    )
    content = models.TextField()

    def save(self, *args, **kwargs):
        if not self.title:
            self.title = slugify_new(self.title, 5)
        return super().save(*args, **kwargs)
    
    # Quando eu entro dentro de uma categoria, esse será o TÍTULO que aparecerá.
    def __str__(self) -> str:
        return self.title
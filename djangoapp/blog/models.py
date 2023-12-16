from django.db import models
from utils.rands import slugify_new
from utils.images import resize_image
from datetime import datetime
from django.contrib.auth.models import User
from django_summernote.models import AbstractAttachment

# Create your models here.
class PostAttachment(AbstractAttachment):
    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.file.name
        
        current_file_name = str(self.file.name)
        super_save = super().save(*args, **kwargs)
        image_changed = False

        if self.file:
            image_changed = current_file_name != self.file.name

        # Se o FILE foi enviado, redimensionamos este FILE dps que foi enviado e salva.
        if image_changed:
            resize_image(self.file, 900, True, 50)
        
        return super_save



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



class Post(models.Model):
    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    title = models.CharField(max_length=65,)
    slug = models.SlugField(
        unique=True, default="",
        null=False, blank=True, max_length=255
    )
    excerpt = models.CharField(max_length=150, default="")
    is_published = models.BooleanField(
        default=False,
        help_text=(
            'Este campo precisará estar marcado '
            'para o post ser exibido publicamente.'
        ),
    )
    content = models.TextField(default='')
    cover = models.ImageField(upload_to='posts/%Y/%m/', blank=True, default='')  # Esse atributo, tem outro atributo dentro dele que é uma URL da IMAGEM
    cover_in_post_content = models.BooleanField(
        default=True,
        help_text='Se marcado, exibirá a capa dentro do post.',
    )
    created_at = models.DateTimeField(default=datetime.now)
    created_by = models.ForeignKey(  # Relação inversa - Usando o USUÁRIO para buscar os posts dentro dele.
        User,
        on_delete=models.SET_NULL,  # Se eu deletar este usuário, não apagarei o POST dele.
        blank=True, null=True, 
        related_name='post_created_by'
    )
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(  # Relação inversa - Usando o USUÁRIO para buscar os posts dentro dele.
        User,
        on_delete=models.SET_NULL,  # Se eu deletar este usuário, não apagarei o POST dele.
        blank=True, null=True, 
        related_name='post_updated_by'
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True,
        default=None,
    )
    tags = models.ManyToManyField(Tag, blank=True, default='')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_new(self.title, 4)

        current_cover_name = str(self.cover.name)
        super_save = super().save(*args, **kwargs)
        cover_changed = False
        
        if self.cover: # Retorna TRUE se atual nome do cover for diferente que o nome do cover cadastrado no BD no momento
            cover_changed = current_cover_name != self.cover  # Isso retorna BOOLEAN TYPE

        if cover_changed:  # se a variavel for true executa o IF
            resize_image(self.cover, 900, True, 50)

        return super_save
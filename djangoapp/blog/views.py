from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.core.paginator import Paginator
from blog.models import Post, Page
from django.db.models import Q
from django.contrib.auth.models import User
from django.http import Http404
from django.views.generic import ListView
from pprint import pprint

PER_PAGE = 9

class PostListView(ListView):
    model = Post
    template_name = 'blog/pages/index.html'
    context_object_name = 'posts'  # Nome da variável que será acessível no template, lista de objetos
    ordering = '-pk',  # Primary Key do OBJETO POST
    paginate_by = PER_PAGE  # Quantos elementos por página
    queryset = Post.objManager.get_published()

    # def get_queryset(self):
    #     return self.queryset

    # **kwargs -> deixa explicito que ao CHAMAR esse metódo, PODE SER PASSADO argumentos, ou seja, este método ACEITA argumentos ao ser chamado. 
    #  Método para mexer no contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # super -> chama o método da classe ListView (que está sendo herdada) que obtém os dados do contexto
        
        #  Define variáveis (chave) que ficarão acessíveis no template com seus devidos valores (Home - )
        context.update({
            'page_title': 'Home - '
        })

        return context

def index(request):
    posts = Post.objManager.get_published()
    
    paginator = Paginator(posts, PER_PAGE)  # Cria uma paginação que divide a lista de OBJ (posts) em páginas, cada uma, contendo até 9 posts.
    page_number = request.GET.get("page")  # Obtém o número da página a ser exibida
    page_obj = paginator.get_page(page_number)  # Obtém a página atual

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
            'page_title': 'Home - '
        }
    )


def created_by(request, author_pk):
    user = User.objects.filter(pk=author_pk).first()

    if user is None:
        raise Http404()

    posts = Post.objManager.get_published() \
            .filter(created_by__pk=author_pk)
    user_full_name = user.username

    if user.first_name:
        user_full_name = f'{user.first_name}  {user.last_name}'
    page_title = ' posts de ' + user_full_name


    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
            'page_title': page_title
        }
    )


def category(request, slug):
    posts = Post.objManager.get_published() \
            .filter(category__slug=slug)
    
    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    if len(page_obj) == 0:
        raise Http404
    
    page_title = f'{page_obj[0].category.name} - Categoria - '
    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
            'page_title': page_title
        }
    )


def post(request, slug):  #  Imagine que slug seja -> /post/o-titulo-do-post/
    post_obj = (
        Post.objManager.get_published()
        .filter(slug=slug)
        .first()
    )

    if post_obj is None:
        raise Http404
    
    post_title = f'{post_obj.title} - Postagem - '

    return render(
        request,
        'blog/pages/post.html',
        context = {
            'post': post_obj,
            'page_title': post_title
        }
    )


def page(request, slug):
    page_obj = (
        Page.objects
        .filter(is_published=True)
        .filter(slug=slug)
        .first()
    ) 

    if page_obj is None:
        raise Http404
    
    page_title = f'{page_obj.title} - Página -'

    return render(
        request,
        'blog/pages/page.html',
        {
            'page': page_obj,
            'page_title': page_title
        }
    )


def tag(request, slug):
    posts = Post.objManager.get_published() \
            .filter(tags__slug=slug)
    
    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    # print()
    # print()
    # print("PAGE OBJ ::: ", page_obj[1].tags.first().name)

    if len(page_obj) == 0:
        raise Http404
    
                # page_obj, acesso aos posts(OBJETOS do BD), e também às páginas que contém os POSTS
                # os indices indicam os POSTS(objetos do BD)
    page_title = f'{page_obj[0].tags.first().name } - Tag -'

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
            'page_title': page_title
        }
    )


def search(request):                # search -> name do input do form
    search_value = request.GET.get("search", '').strip()  # strip -> remove os espaços do inicio e fim.
    posts = Post.objManager.get_published() \
            .filter(
                Q(title__icontains=search_value) |
                Q(excerpt__icontains=search_value) |
                Q(content__icontains=search_value)
            )[:PER_PAGE]

    if len(posts) == 0:
        raise Http404
    
    post_title = f'{search_value[:30]} - Search - '

    return render(
        request,
        'blog/pages/index.html',
        {
            'posts': posts,
            'search_value': search_value,
            'page_title': post_title
        }
    )
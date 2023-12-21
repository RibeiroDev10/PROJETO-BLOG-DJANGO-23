from django.shortcuts import render
from django.core.paginator import Paginator
from blog.models import Post, Page
from django.db.models import Q
from django.contrib.auth.models import User
from django.http import Http404

PER_PAGE = 9

# Create your views here.
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
    post = (
        Post.objManager.get_published()
        .filter(slug=slug)
        .first()
    )

    return render(
        request,
        'blog/pages/post.html',
        context = {
            'post': post,
            'page_title': 'Home - '
        }
    )


def page(request, slug):
    page = (
        Page.objects
        .filter(is_published=True)
        .filter(slug=slug)
        .first()
    ) 

    return render(
        request,
        'blog/pages/page.html',
        {
            'page': page,
            'page_title': 'Home - '
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
    
    post_title = f'{posts[0].title}'

    return render(
        request,
        'blog/pages/index.html',
        {
            'search_value': search_value,
            'page_title': 'Home - '
        }
    )
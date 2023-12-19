from django.shortcuts import render
from django.core.paginator import Paginator
from blog.models import Post

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
        }
    )



def post(request):
    return render(
        request,
        'blog/pages/post.html'
    )



def page(request):
    return render(
        request,
        'blog/pages/page.html'
    )
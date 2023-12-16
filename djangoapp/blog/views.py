from django.shortcuts import render
from django.core.paginator import Paginator
from blog.models import Post

posts = list(range(1000))

# Create your views here.
def index(request):
    posts = Post.objects.order_by('-pk')

    paginator = Paginator(posts, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

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
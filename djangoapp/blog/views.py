from django.shortcuts import render
from django.core.paginator import Paginator

posts = list(range(1000))

# Create your views here.
def index(request):
    paginator = Paginator(posts, 9)
    page_number = request.GET.get("page")
    print('PAGE NUMBER: ', page_number)
    print('PAGE NUMBER: ', page_number)
    page_obj = paginator.get_page(page_number)
    print('PAGE OBJ: ', page_obj)
    print('PAGE OBJ: ', page_obj)
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
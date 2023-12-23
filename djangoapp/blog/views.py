from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.core.paginator import Paginator
from blog.models import Post, Page
from django.db.models import Q
from django.contrib.auth.models import User
from django.http import Http404, HttpRequest, HttpResponse
from django.views.generic import ListView
from pprint import pprint

PER_PAGE = 9

# Essa classe é a nossa HOME do site
class PostListView(ListView):
    model = Post
    template_name = 'blog/pages/index.html'
    context_object_name = 'posts'  # Nome da variável que será acessível no template, lista de objetos
    ordering = '-pk',  # Primary Key do OBJETO POST
    paginate_by = PER_PAGE  # Quantos elementos por página
    queryset = Post.objManager.get_published()  # Traz somente os objetos do POST que estão marcados no is_published

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


class CreatedByListView(PostListView):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._temp_context: dict[str, Any] = {}

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data()  # ctx -> chama o método de contexto da superclass, no caso ListView da classe PostLisView

        # Como executamoso o DISPATCH e depois o GET(que faz as ações ali embaixo, pegando o usuario no BD com base na author_pk passada como parametro)
        # aqui então temos acesso à self_temp_context contexto que retorna esses dados do banco de dados(LÓGICA SENDO FEITA NO MÉTODO GET ABAIXO)
        user = self._temp_context['user']
        user_full_name = user.username

        if user.first_name:
            user_full_name = f'{user.first_name} {user.last_name}'
        page_title = 'Posts de ' + user_full_name

        # Estamos atualizando a variavel context_object_name da classe PostLisView,
        # Neste caso, estamos definindo um contexto para essa classe aqui. ( CreatedByListView ). Diferente da classe herdada.
        # Atualizando o Contexto: ctx.update({'page_title': page_title}) adiciona a variável 'page_title' ao contexto da classe. 
        # Isso significa que essa variável estará disponível para uso no template associado a CreatedByListView.
        ctx.update({
            'page_title': page_title
        })

        return ctx
    
    # Manipulando a QUERY
    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset()
        qs = qs.filter(created_by__pk=self._temp_context['user'].pk)

        # Retorna o conjunto de consultas filtrado. 
        # Isso afetará a renderização dos objetos na sua visualização, 
        # garantindo que apenas os objetos associados ao usuário atual sejam exibidos.
        return qs

    #  Nesta classe quando é executada, primeiro executa o método DISPATCH da classe PAI, e logo em seguida o GET
    #  então definimos este método get abaixo para o código ficar mais performático e escrito melhor.
    def get(self, request, *args, **kwargs):
        # self.kwargs -> vem de ListView. get -> pega o parametro da requisição, no caso: created_by/<int:author_pk>
        # Quando temos uma URL que envia um parametro na requisiçao dela, este parametro é recebido na classe ListView,
        # ListView temos acesso com self.kwargs pois estamos herdando ela de PostListView.
        # Com isso obtemos chave-valor do parametro da URL de requisição e temos acesso à esses valores em self.kwargs  
        author_pk = self.kwargs.get('author_pk')
        user = User.objects.filter(pk=author_pk).first()

        if user is None:
            raise Http404()
        self._temp_context.update({
            'author_pk': author_pk,  # Retornado pelo get(classe Atual) no kwargs(pegado na classe pai - ListView)
            'user': user
        })
        # print(self._temp_context)
        # retorno de self._temp_context ----> {'author_pk': 1, 'user': <User: rafael>}
        # User: É o modelo de usuário no Django, que geralmente representa um usuário no sistema. 
        # Cada instância desse modelo representa um usuário específico no banco de dados.
        # rafael: É o valor associado ao campo username desse objeto User. No contexto de um modelo de usuário, 
        # 'rafael' é o nome de usuário (ou login) desse usuário específico.
        
        return super().get(request, *args, **kwargs)


class CategoryListView(PostListView):
    # Permitir vazio? Não(False).
    # Esse atributo gera automaticamente o erro 404 not found
    # Quando allow_empty é configurado como False, 
    # isso significa que a visualização não mostrará uma página se o conjunto de consultas (QuerySet) resultar em uma lista vazia.
    allow_empty = False

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(category__slug=self.kwargs.get('slug'))  # kwargs --> da classe pai, que traz sempre os parametros de URL após a requisição.


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
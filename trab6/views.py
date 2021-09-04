from django.shortcuts import render
from categoria.models import Categoria
from produto.models import Produto
from produto.forms import ProdutoForm
from django.http.response import JsonResponse

def add_produto( request ):

    print( request.POST)
 

def base_dummy( request ):

    render_items = {}

    nomes = []
    for cat in Categoria.objects.all( ).order_by('nome'):
        nomes.append( cat.nome )
    render_items[ 'catg_list' ] = nomes

    prods = []
    for prod in Produto.objects.all( ).order_by('nome'):
        prods.append( prod.get_render_tup() )
    render_items[ 'prod_list' ] = enumerate( prods , start = 1 )
    
    foo = lambda x : x.preco
    render_items[ 'soma_preco' ]  = sum( map( foo , prods ) )

    return render(request, 'base.html' , render_items )


    

def base( request ):

    render_items = {}

    nomes = []
    for cat in Categoria.objects.all( ).order_by('nome'):
        nomes.append( cat.nome )
    render_items[ 'catg_list' ] = nomes

    prods = []
    for prod in Produto.objects.all( ).order_by('nome'):
        prods.append( prod.get_render_tup() )
    render_items[ 'prod_list' ] = prods

    return render(request, 'base.html' , render_items )
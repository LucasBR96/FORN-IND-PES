from django.shortcuts import render
from categoria.models import Categoria
from produto.models import Produto
from produto.forms import ProdutoForm , ProdutoRemoveForm, ProdutoQuantidadeForm 
from django.http.response import JsonResponse
from utils import format_br_currency as fbr

def get_preco_total():

    seq = Produto.objects.all()
    foo = lambda x : x.preco*x.quantidade
    return fbr( sum( map( foo , list( seq ) ) ) )

def add_produto( request ):

    form = ProdutoForm( request.POST )
    resp = { "valid" : False }
    if form.is_valid():
        resp[ "valid" ] = True 
        # print( form )

        nome = form.cleaned_data[ 'nome' ]
        slug = nome.lower()
        cater = form.cleaned_data[ 'cater' ]
        qtd = int( form.cleaned_data[ 'quantidade' ] )
        preco = float( form.cleaned_data[ 'preco' ] )

        prod = Produto(
            cater = Categoria.objects.get( nome = cater ),
            nome = nome,
            slug = slug,
            preco = preco,
            quantidade = qtd
        )

        prod.save()
        tup = prod.get_tabular_info()

        resp[   "nome"   ] = tup.nome,
        resp[   "cater"  ] = tup.cater,
        resp[   "preco"  ] = tup.preco,
        resp[   "qtd"    ] = tup.qtd,
        resp[   "idt"    ] = tup.idt,
        resp["novo_preco"] = get_preco_total()
        
    return JsonResponse( resp )
 
def remove_prod( request ):

    seq = ProdutoRemoveForm( request.POST )
    print( seq )

    resp = { "valid" : False }
    if seq.is_valid():
        
        resp[ 'valid' ] = True

        prod_id = seq.cleaned_data[ 'idt' ]
        item = Produto.objects.get( id = prod_id )
        item.delete()

        resp[ 'preco_final' ] = get_preco_total()
    return JsonResponse( resp )

def atualiza_quantidade( request ):

    seq = ProdutoQuantidadeForm( request.POST )
    # print( seq )

    resp = { "valid" : False }
    if seq.is_valid():
        
        resp[ 'valid' ] = True

        prod_id = seq.cleaned_data[ 'idt' ]
        item = Produto.objects.get( id = prod_id )
        item.quantidade = int( seq.cleaned_data[ 'quantidade' ])
        item.save()

        resp[ 'preco_final' ] = get_preco_total()
    return JsonResponse( resp )

def base_dummy( request ):

    render_items = {}
    render_items[ 'form' ] = ProdutoForm()
    
    prods = []
    for prod in Produto.objects.all( ).order_by('nome'):
        info = prod.get_tabular_info()
        prods.append( info )
        
    render_items[ 'prod_list' ] = prods
    render_items[ 'soma_preco' ]  = get_preco_total()

    return render( request, 'base.html' , render_items )

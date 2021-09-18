from django.shortcuts import render
from categoria.models import Categoria
from produto.models import Produto , ProdutoForm , ProdutoRemoveForm, ProdutoQuantidadeForm
from django.http.response import JsonResponse
from utils import format_br_currency as fbr

def get_preco_total():

    seq = Produto.objects.all()
    foo = lambda x : x.preco*x.quantidade
    return fbr( sum( map( foo , list( seq ) ) ) )

def add_produto( request ):

    form = ProdutoForm( request.POST )

    if form.is_valid():
        print( form )

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
        print( prod.get_tabular_info() )

        return JsonResponse( { 
            "prod":prod.get_tabular_info(), 
            "novo_preco": get_preco_total()
            # "prod_rm": ProdutoRemoveForm( initial = { "id_rmv":prod.id } )
            } )
    else:
        raise ValueError( "Ih, alguma coisa deu errado")
 
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

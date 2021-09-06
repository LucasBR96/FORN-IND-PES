from django.shortcuts import render
from categoria.models import Categoria
from produto.models import Produto , ProdutoForm , ProdutoRemoveForm, ProdutoQuantidadeForm
from django.http.response import JsonResponse

def get_preco_total():

    seq = Produto.objects.all()
    foo = lambda x : x.preco*x.quantidade
    return sum( map( foo , list( seq ) ) )

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
    seq.is_valid()
    prod_id = seq.cleaned_data[ 'id_rmv' ]
    item = Produto.objects.get( id = prod_id )
    item.delete()

    preco = get_preco_total()
    return JsonResponse({ "preco" : preco })

def atualiza_quantidade( request ):

    seq = ProdutoQuantidadeForm( request.POST )
    seq.is_valid()
    prod_id = seq.cleaned_data[ 'id' ]
    item = Produto.objects.get( id = prod_id )
    item.quantidade = int( seq.cleaned_data[ 'quantidade' ])
    item.save()

    preco = get_preco_total()
    return JsonResponse({ "preco" : preco })

def base_dummy( request ):

    render_items = {}
    render_items[ 'form' ] = ProdutoForm()
    
    prods = []
    for prod in Produto.objects.all( ).order_by('nome'):
        info = prod.get_tabular_info()
        rm   = ProdutoRemoveForm( initial = { "id_rmv":prod.id } )
        qtd  = ProdutoQuantidadeForm( initial = { "id":prod.id , "quantidade":prod.quantidade } )

        prods.append( ( info , rm , qtd ) )
        
    render_items[ 'prod_list' ] = prods
    render_items[ 'soma_preco' ]  = get_preco_total()

    return render( request, 'base.html' , render_items )

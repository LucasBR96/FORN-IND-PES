from django.shortcuts import render
from categoria.models import Categoria
from produto.models import Produto , ProdutoForm
from django.http.response import JsonResponse

def get_preco_total():

    seq = Produto.objects.all()
    foo = lambda x : x.preco*x.qtd
    return sum( map( foo , list( seq ) ) )

def add_produto( request ):

    form = ProdutoForm( request.POST )
    print( form )

    if form.is_valid():

        nome = form.cleaned_data[ 'nome' ]
        slug = nome.lower()
        cater = form.cleaned_data[ 'cater' ]
        qtd = form.cleaned_data[ 'quantidade' ]
        preco = float( form.cleaned_data[ 'preco' ] )

        prod = Produto(
            cater = Categoria.objects.get( nome = cater ),
            nome = nome,
            slug = slug,
            preco = preco,
            quantidade = qtd
        )
        prod.save()
        
        return JsonResponse( { 
            "prod":prod.get_tabular_info(), 
            "novo_preco": get_preco_total() } )
    else:
        raise ValueError( "Ih, alguma coisa deu errado")
 

def base_dummy( request ):

    render_items = {}

    nomes = []
    for cat in Categoria.objects.all( ).order_by('nome'):
        nomes.append( cat.nome )
    render_items[ 'catg_list' ] = nomes

    prods = []
    for prod in Produto.objects.all( ).order_by('nome'):
        prods.append( prod.get_tabular_info() )
    render_items[ 'prod_list' ] = enumerate( prods , start = 1 )
    
    render_items[ 'soma_preco' ]  = get_preco_total()

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
from categoria.models import Categoria
from produto.models import Produto

def run():

    Categoria.objects.all().delete()
    Produto.objects.all().delete()

    f = open('dummy_data.csv' , 'r')
    while True:

        try: args = f.readline().split( ',' )
        except EOFError: break

        print( args )
        nome = args[ 1 ]
        slug = nome.lower()
        if args[ 0 ] == 'Categoria':
            cat = Categoria( nome = nome , slug = slug )
            cat.save()
        else:

            cat        = Categoria.objects.get( nome = args[ 2 ] )
            preco      = float( args[ 3 ] )
            ratio      = float( args[ 4 ] )
            modo_venda = int( args[ 5 ] )

            prod = Produto( cater = cat , nome = nome , slug = slug, ratio = ratio, modo_venda = modo_venda , preco = preco)
            prod.save()
    f.close()
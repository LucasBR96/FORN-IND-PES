from typing import Text
from django.db import models
from categoria.models import Categoria

from collections import namedtuple
from utils import format_br_currency as fbr

render_tup = namedtuple( 'render_tup' , ['nome','cater','preco','ratio','modo_venda', 'desc' , 'img'] )
table_tup = namedtuple( 'table_tup' , ['nome','cater','preco', 'qtd', 'idt'] )
class Produto( models.Model ):

    nome = models.CharField( max_length = 50 ,blank = False )
    slug = models.SlugField( max_length = 50 )

    cater = models.ForeignKey( Categoria , on_delete = models.CASCADE )

    #----------------------------------------------------------------------
    # Cada produto pode ser vendido em volume, peso ou unidades
    #
    # Ratio siginfica o desconto marginal por centena e milhares de unidades.
    # Por exemplo, Ácido sulfúrico é vendido a R$ 5,48 por litro, com um ratio
    # de 0.05 ( 5% de desconto ). O custo de um lote de 1728 litros custaria
    #
    # 28 litros     ->  28*5,48       = R$ 153,44  ( sem desconto ) 
    # 7*100 litros  ->  700*0.95*5,48 = R$ 3644,20 ( 5% de desconto ) 
    # 1*1000 litros ->  1000*0.9*5,48 = R$ 4932,00 ( 10% de desconto )
    #  _____________________________________________________________   +
    # total = R$ 8729,64 
     
    preco      = models.FloatField( blank = False, default = 0 )
    quantidade = models.IntegerField( blank = False , default = 0)
    ratio      = models.FloatField( default = 0.1 )
    modo_venda = models.IntegerField( default = 0 )

    class __Meta__:
        db_table = 'produto'
        orderby  = 'nome'
    
    def __str__( self ):
        return self.nome
    
    def get_render_tup( self ):

        nome = self.nome
        cater = self.cater.nome
        preco = self.preco
        ratio = self.ratio

        modo_venda = "unidade"
        if self.modo_venda == 1:
            modo_venda = "peso"
        elif self.modo_venda == 2:
            modo_venda = "volume"
        
        img  = 'static/imgs/' + nome + '.png' 
        desc = 'static/desc/' + nome + '.txt'

        return render_tup( nome, cater, preco, ratio, modo_venda, desc, img )
    
    def get_tabular_info( self ):

        nome  = self.nome
        cater = self.cater.nome
        preco = fbr( self.preco )
        qtd   = self.quantidade
        idt   = self.id

        return table_tup( nome, cater, preco, qtd, idt )

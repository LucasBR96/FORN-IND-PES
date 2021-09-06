from typing import Text
from django.db import models
from django.forms.widgets import TextInput
from categoria.models import Categoria
from collections import namedtuple
from django import forms

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
        preco = self.preco
        qtd   = self.quantidade
        idt   = self.id

        return table_tup( nome, cater, preco, qtd, idt )


class ProdutoForm( forms.Form ):
    
        class Meta:
            model = Produto
            fields = ( 'nome' , 'preco' , 'cater', 'quantidade' )
        
        cater = forms.ModelChoiceField( 
            label = "inputCategoria",
            error_messages = { "required": "Campo Obrigatório" },
            queryset = Categoria.objects.all().order_by( 'nome' ),
            empty_label = "--- Selecione ---",
            widget = forms.Select( attrs = {"class" : "form-control" , "id":"inputCategoria" } )
        )

        nome = forms.CharField( 
            label = "inputNome", 
            max_length = 100,
            error_messages = { "required": "Campo Obrigatório" },
            widget = forms.TextInput( attrs = { "class" : "form-control" , "id":"inputNome"} ) )
        
        preco = forms.CharField( 
            label = "inputPreco", 
            max_length = 10,
            error_messages = { "required": "Campo Obrigatório" },
            widget = forms.TextInput( attrs = { "class" : "form-control" , "id":"inputPreco"} ) )
        
        quantidade = forms.CharField( label = "inputQuantidade",
            max_length = 5,
            error_messages = { "required": "Campo Obrigatório" },
            widget = forms.TextInput( attrs = { "class" : "form-control" , "id":"inputQuantidade"} ) )

class ProdutoRemoveForm( forms.Form ):

    class Meta:
        fields = ( 'id_rmv' )
    
    id_rmv = forms.CharField(
        required = True,
        widget = forms.HiddenInput()
    )

class ProdutoQuantidadeForm( forms.Form ):

    class Meta:
        fields = ( 'id' , 'quantidade' )
    
    id = forms.CharField(
        required = True,
        widget = forms.HiddenInput()
    )

    quantidade = forms.CharField(
        required = True,
        widget = forms.TextInput( attrs = {
            "class":"form-control",
        })
    )
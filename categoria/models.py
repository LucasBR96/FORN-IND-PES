from django.db import models

class Categoria( models.Model ):

    nome = models.CharField( max_length = 50 , unique = True , blank = False )
    slug = models.SlugField( max_length = 50 , unique = True )

    class __Meta__:
        db_table = 'categoria'
        orderby  = 'nome'
    
    def __str__( self ):
        return self.nome
    
from produto.models import Produto
from django import forms
import re

preco_regex = "\d+[\.,]?\d{0,2}"

class ProdutoForm( forms.ModelForm ):
    
    class Meta:
        model = Produto
        fields = ( )
    
    Nome = forms.CharField(
        error_messages = { 
            "required":"Campo obrigatório",
            "unique":"Nome duplicado"
        },
        widget = forms.TextInput( attrs = {'class':'form-control form-control-sm', 'max-lenght': '100'})
    )

    Endereco = forms.CharField(
        error_messages = { 
            "required":"Campo obrigatório",
            "unique":"Endereco duplicado"
        },
        widget = forms.TextInput( attrs = {'class':'form-control form-control-sm', 'max-lenght': '100'})
    )

    Telefone = forms.CharField(
        error_messages = { 
            "required":"Campo obrigatório",
            "unique":"Telefone duplicado"
        },
        widget = forms.TextInput( attrs = {'class':'form-control form-control-sm', 'max-lenght': '25'})
    )

    CNPJ = forms.CharField(
        error_messages = { 
            "required":"Campo obrigatório",
            "unique":"CNPJ duplicado"
        },
        widget = forms.TextInput( attrs = {'class':'form-control form-control-sm', 'max-lenght': '30'})
    )
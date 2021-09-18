
$("button#sub-btn").click( function( event ){
    
    event.preventDefault();
    // $.post(
    //     // -------------------------------------------
    //     //Ação 
    //     'add_produto/',

    //     // --------------------------------------------
    //     // O que será enviado para o servidor 
    //     $("#produtoForm").serializeArray(),

    //     function( resposta ){
    //         if( resposta.valid ){
    //             console.log( resposta );
    //             novaLinha( resposta );

    //             $("#inputCategoria").val("");
    //             $("#inputPreco").val("");
    //             $("#inputQuantidade").val("");
    //             $("#inputNome").val("");

    //             let val = resposta.novo_preco;
    //             $( "#final-price" ).text( val );

    //             addToken( resposta.idt );
    //         }
    //     }
    // )

    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            console.log( cookie );
        }
    }

} )

novaLinha = function( resposta ){
    let s = `                    
    <tr id = "linhaNum${ resposta.idt }">
        <th scope="row" style = "display: none;">${ resposta.idt }</th>
        <td>${ resposta.cater }</td>
        <td>${ resposta.nome }</td>

        <td>
            <form action = "modifica_prod/" method = "POST">
                <input type = "number" class = "d-none" name = "idt" value = "${ resposta.idt }" >
                <input type="text" name = "quantidade" placeholder="${ resposta.qtd }" class="form-control new-qtd" required="">
            </form>
        </td>

        <td>${ resposta.preco }</td>

        <td>
            <form class = "d-none" action = "remove_prod/" method = "POST">
                <input type = "number" name = "idt" value = "${ resposta.idt }" >
            </form>
                <button class="btn btn-danger mb-2 btn-rmv">Remover</button>
        </td>
    </tr>
        `
    $("tbody").append( s );
}

$(".btn-rmv").click( function( event ){

    event.preventDefault();

    let form = $( this ).prev()
    let url  = $( form ).attr( 'action' );
    let data = $( form ).serializeArray();

    let linha = $( this ).parent().parent();

    $.post(
        url, data,
        function( resposta ){

            if( resposta.valid ){
                $(linha).fadeTo( 'fast' , 0.3 , function(){ 
                    // $( linha ).hide();
                    $( linha ).remove(); 
                } );
                changeLineColors( linha );
                    
                let val = resposta.preco_final;
                $( "#final-price" ).text( val );
            }
    })

})

changeLineColors = function( linha ){
    console.log( linha )
}

$(".new-qtd").focusout( function( event ){
    event.preventDefault();

    let linha = $( this );
    let qtd   = $( linha ).val();
    // let ph    = $( linha ).attr("placeholder")
    if ( qtd == "" )
        return
    
    let form = $(this).parent();
    let url  = $( form ).attr( 'action' );
    let formData = form.serializeArray();
    
    $.post(
        url,
        formData,
        function( resposta ){

                console.log( resposta )

                if( !resposta.valid ){
                    $( linha ).val( "" );
                    return;
                }

                $( linha ).attr("placeholder", qtd );
                $( linha ).val( "" );
                let val = resposta.preco_final;
                $( "#final-price" ).text( val );
            }
        )
    }
)


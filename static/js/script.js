
$("button#sub-btn").click( function( event ){
    
    event.preventDefault();
    $.post(
        // -------------------------------------------
        //Ação 
        'add_produto/',

        // --------------------------------------------
        // O que será enviado para o servidor 
        $("#produtoForm").serializeArray(),

        function( resposta ){
            console.log( resposta );

            let prod = resposta.prod;
            let s = `                    
                <tr = "linhaNum${ prod[4] }}">
                    <th scope="row" style = "display: none;">${ prod[4] }</th>
                    <td>${ prod[1] }</td>
                    <td>${ prod[0] }</td>

                    <td>
                        <input class="form-control modif-inpt" id = "" placeholder="${ prod[ 3 ] }">
                    </td>

                    <td>R$ ${ prod[2] }</td>
                    <td>
                        <form action="remove_prod/" method="POST">
                            <input type="hidden" name="id_rmv" value="${ prod[4] }" id="id_id_rmv">
                            <button class="btn btn-danger mb-2 btn-rmv">Remover</button>
                        </form>
                    </td>
                </tr>
                `
            $("tbody").append( s );

            let val = resposta.novo_preco;
            $( "#final-price" ).text( "R$ " + val );
        }
    );

} )

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



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
            // let prod_rm = resposta.prod_rm
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
                        <button class="btn btn-danger mb-2 btn-rmv">Remover</button>
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

    let linha = $( this ).parent().parent().parent();
    let form = $( this ).parent();
    let url  = $( form ).attr( 'action' );

    let formData = form.serializeArray();
    $.post(
        url,
        formData,
        function( resposta ){
            $(linha).fadeTo( 'fast' , 0.3 , function(){
                $(linha).hide();

                let val = resposta.preco;
                $( "#final-price" ).text( "R$ " + val );
            })
        })

})

$(".new-qtd").focusout( function( event ){
    event.preventDefault();

    let form = $(this).parent();
    let url  = $( form ).attr( 'action' );
    let formData = form.serializeArray();
    
    $.post(
        url,
        formData,
        function( resposta ){
                let val = resposta.preco;
                $( "#final-price" ).text( "R$ " + val );
            }
        )
    }
)


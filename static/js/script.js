$( ".comprar" ).click( function(){

})

$(".add-prod-btn").click( function(){
    console.log( $( this ).parent().parent() )

} )

$("button#sub-btn").click( function( event ){
    
    event.preventDefault();
    $.post(
        'add_produto/',
        $("#produtoForm").serialize(),
        function( resposta ){}
    );

} )

$(".filtra_produto").click( function(){

    let cat_nome = this.id;
    console.log( cat_nome );

    $("option").each( function(){
        console.log( this.attributes.action )
    })
})
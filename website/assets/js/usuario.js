const tabela = document.getElementsByClassName("tabela-usuarios");
const linhas = tabela[0].getElementsByTagName("tbody");

function modal_cadastrar_usuarios(){
    $('#cadastrar_usuarios').modal("show");
}

function modal_editar_usuarios(id){
    $('#editar_usuarios').modal("show");
    form_right = document.getElementById("form-editar-usuarios-operacoes")
    form_left = document.getElementById("form-editar-usuarios")
    if($('#editar-usuarios-roles').val() === "OPERADOR"){
        form_left.classList.value = 'form-group col-7'
        form_right.style = "display:block;"
    }else{
        form_left.classList.value = 'form-group'
        form_right.style = "display:none;"
    }
}

function modal_excluir_usuarios(id){
    $('#excluir_usuarios').modal("show");
}

function cadastrar_usuarios(){
    $('#cadastrar_usuarios_form').on('submit',function(event){
        event.preventDefault();
        let formData = {
            'roles':$('#cadastrar-roles').val(),
            'user':$('#cadastrar-user').val(),
            'csrfmiddlewaretoken':$('[name=csrfmiddlewaretoken]').val()
        }
        const URL = "cadastrar";
        $.ajax({
            type: 'POST',
            url: URL,
            data:formData,
            success: function(response) {
                if(response){
                    $('.cadastrar-error-usuarios').text("");
                    $('#cadastrar-error-usuarios-generico')[0].style = "display:none;";
                    if(response.sucesso != false){
                        event.currentTarget.submit(); 
                    }
                    if(response.error){
                        $('#cadastrar-error-usuarios-generico')[0].style = "display:block;";
                        $('#cadastrar-error-usuarios-generico-text').text(response.error);
                    }
                    if(response.errors){
                        for (let campos in response.errors){
                            console.log(campos)
                            $('#cadastrar-error-usuarios-'+campos).text(response.errors[campos].join(', '));
                            console.log(response.errors[campos].join(', '))
                        }
                    }

                    console.log(response.error)
                    console.log(response.errors)
                }
            },
            error: function(error) {
                console.log(error)
            },
        });   
    });
}

function editar_usuarios(){
    $('#editar_usuarios_form').on('submit',function(event){
        event.preventDefault();
        console.log("editar")
    });
}

function excluir_usuarios(){
    $('#excluir_usuarios_form').on('submit',function(event){
        event.preventDefault();
        console.log("excluir")
    });
}

$('#cadastrar-usuarios-roles').change(function(){
    form_right = document.getElementById("form-cadastrar-usuarios-operacoes")
    form_left = document.getElementById("form-cadastrar-usuarios")
    if($(this).val() === "OPERADOR"){
        form_left.classList.value = 'form-group col-7'
        form_right.style = "display:block;"
    }else{
        form_left.classList.value = 'form-group'
        form_right.style = "display:none;"
    }
});

$('#editar-usuarios-roles').change(function(){
    form_right = document.getElementById("form-editar-usuarios-operacoes")
    form_left = document.getElementById("form-editar-usuarios")
    if($(this).val() === "OPERADOR"){
        form_left.classList.value = 'form-group col-7'
        form_right.style = "display:block;"
    }else{
        form_left.classList.value = 'form-group'
        form_right.style = "display:none;"
    }
});
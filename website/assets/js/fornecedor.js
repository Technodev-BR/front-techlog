const tabela = document.getElementsByClassName("tabela-fornecedores");
const linhas = tabela[0].getElementsByTagName("tbody");

function modal_cadastrar_fornecedores(){
    $('#cadastrar_fornecedores').modal("show");

    $('#cadastrar-fornecedores-nome').val('');
    $('#cadastrar-error-fornecedores-nome').text('');

    $('#cadastrar-fornecedores-email').val('');
    $('#cadastrar-error-fornecedores-email').text('');

    $('#cadastrar-fornecedores-telefone').val('');
    $('#cadastrar-error-fornecedores-telefone').text('');

    $('#cadastrar-error-fornecedores-generico')[0].style = "display:none;";
    $('#cadastrar-error-fornecedores-generico-text').text('');
    fechar_alerta("container_alerta_sucesso");
}

function modal_editar_fornecedores(id){
    $('#editar_fornecedores').modal("show");
    $.ajax({
        type: 'GET',
        url: `buscar_by_Id/${id}/`,
        success: function(response) {
            if(response.data.id){ 
                $('#editar-fornecedores-id').val(response.data.id);
                $('#editar-fornecedores-nome').val(response.data.nome);
                $('#editar-error-fornecedores-nome').text('');
                $('#editar-fornecedores-recebe_email')[0].checked = response.data.recebe_email;
                
                $('#editar-fornecedores-email').val(response.data.email);
                $('#editar-error-fornecedores-email').text('');
                
                $('#editar-fornecedores-telefone').val(response.data.telefone);
                $('#editar-error-fornecedores-telefone').text('');
            }
        },  
        error: function(error) {
            console.log(error)
        }
    });  
    fechar_alerta("container_alerta_sucesso");
}

function modal_excluir_fornecedores(id){
    $('#excluir_fornecedores').modal("show");
    $('#excluir-error-fornecedores-generico')[0].style = "display:none;";
    $('#excluir-error-fornecedores-generico-text').text('');
    
    $.ajax({
        type: 'GET',
        url: `buscar_by_Id/${id}/`,
        success: function(response) {
            if(response.data.id){ 
                const dataAtual = new Date(response.data.data_criado);
                const dataFormatada = dataAtual.toLocaleDateString('pt-BR');
                $('#excluir-fornecedores-informacao').val(`${response.data.nome} - ${dataFormatada}`);
                $('#excluir-fornecedores-id').val(`${response.data.id}`);
            } 
        },  
        error: function(error) {
            console.log(error)
        }
    });
    fechar_alerta("container_alerta_sucesso");  
}

function cadastrar_fornecedores(){
    let formData = {
        'nome': $('#cadastrar-fornecedores-nome').val(),
        'email':$('#cadastrar-fornecedores-email').val(),
        'recebe_email':$('#cadastrar-fornecedores-recebe_email')[0].checked,
        'telefone':$('#cadastrar-fornecedores-telefone').val(),
        'csrfmiddlewaretoken':$('[name=csrfmiddlewaretoken]').val()
    }
    $.ajax({
        type: 'POST',
        url: 'cadastrar',
        data:formData,
        success: function(response) {
            if(response){ 
                $('.cadastrar-error-fornecedores').text("");
                $('#cadastrar-error-fornecedores-generico')[0].style = "display:none;";
                
                if(response.sucesso != false){
                    var modal_buscado = document.getElementById('cadastrar_fornecedores');
                    var modal_cadastrar_fornecedores = bootstrap.Modal.getInstance(modal_buscado)
                    modal_cadastrar_fornecedores.hide();
                    $.ajax({
                        type: 'GET',
                        url: `buscar`,
                        success: function(response) {
                            recarrega_tabela(response.data,'ativo')
                        },
                        error: function(error) {
                            console.log(error)
                        }
                    });
                    $('#alerta_mensagem_sucesso').text(response.mensagem);
                    abrir_alerta("container_alerta_sucesso");
                }

                if(response.sucesso == false){
                    if(response.mensagem){
                        $('#cadastrar-error-fornecedores-generico')[0].style = "display:block;";
                        $('#cadastrar-error-fornecedores-generico-text').text(response.mensagem);
                    }
                    if(response.errors){
                        for (let campos in response.errors){
                            $('#cadastrar-error-fornecedores-'+campos).text(response.errors[campos].join(', '));
                        }
                    }
                }
            }
        },  
        error: function(error) {
            console.log(error)
        }
    });  
}

function editar_fornecedores(){
    let formData = {
        'nome': $('#editar-fornecedores-nome').val(),
        'email':$('#editar-fornecedores-email').val(),
        'recebe_email':$('#editar-fornecedores-recebe_email')[0].checked,
        'telefone':$('#editar-fornecedores-telefone').val(),
        'csrfmiddlewaretoken':$('[name=csrfmiddlewaretoken]').val()
    }
    $.ajax({
        type: 'POST',
        url: `atualizar/${$('#editar-fornecedores-id').val()}/`,
        data:formData,
        success: function(response) {
            $('.editar-error-fornecedores').text("");
            $('#editar-error-fornecedores-generico')[0].style = "display:none;";

            if(response.sucesso != false){
                var modal_buscado = document.getElementById('editar_fornecedores');
                var modal_editar_fornecedores = bootstrap.Modal.getInstance(modal_buscado)
                modal_editar_fornecedores.hide();
                $.ajax({
                    type: 'GET',
                    url: `buscar`,
                    success: function(response) {
                        recarrega_tabela(response.data,'ativo')
                    },
                    error: function(error) {
                        console.log(error)
                    }
                });
                $('#alerta_mensagem_sucesso').text(response.mensagem);
                abrir_alerta("container_alerta_sucesso");
            }

            if(response.sucesso == false){
                if(response.mensagem){
                    $('#editar-error-fornecedores-generico')[0].style = "display:block;";
                    $('#editar-error-fornecedores-generico-text').text(response.mensagem);
                }
                if(response.errors){
                    for (let campos in response.errors){
                        $('#editar-error-fornecedores-'+campos).text(response.errors[campos].join(', '));
                    }
                }
            }
        },
        error: function(error) {
            console.log(error)
        }
    });  

}

function excluir_fornecedores(){
    let formData = {
        'csrfmiddlewaretoken':$('[name=csrfmiddlewaretoken]').val()
    }
    $.ajax({
        type: 'POST',
        url: `deletar/${$('#excluir-fornecedores-id').val()}/`,
        data:formData,
        success: function(response) {
            $('#excluir-error-fornecedores-generico')[0].style = "display:none;";
            
            if(response.sucesso == true){
                var modal_buscado = document.getElementById('excluir_fornecedores');
                var modal_excluir_fornecedores = bootstrap.Modal.getInstance(modal_buscado)
                modal_excluir_fornecedores.hide();
                $.ajax({
                    type: 'GET',
                    url: `buscar`,
                    success: function(response) {
                        recarrega_tabela(response.data,'ativo')
                    },
                    error: function(error) {
                        console.log(error)
                    }
                });
                $('#alerta_mensagem_sucesso').text(response.mensagem);
                abrir_alerta("container_alerta_sucesso");
            }
        
            if(response.sucesso == false){
                $('#excluir-error-fornecedores-generico')[0].style = "display:block;";
                $('#excluir-error-fornecedores-generico-text').text(response.mensagem);
            }
        },  
        error: function(error) {
            console.log(error)
        }
    });   
}

function recarrega_tabela(data,tipo){
    var tabela_fornecedores = $(".tabela-fornecedores").DataTable();
    let nova_tabela = []
    data.forEach((data) =>{
        const dataAtual = new Date(data.data_criado);
        const dataFormatada = dataAtual.toLocaleDateString('pt-BR');
        let nova_linha = [
            data.ativo? "<button class='figure small pe-1'><i class='fa-solid fa-circle' style='color: rgb(32, 218, 100);'></i></button>" 
            :"<button class='figure small pe-1'><i class='fa-solid fa-circle' style='color: #ba2525;'></i></button>",
            data.id || "N/A",
            data.nome || "N/A",
            data.email || "N/A",
            data.telefone || "N/A",
            dataFormatada || "N/A",
            tipo == 'ativo'?"<button class='icone medium me-1' data-bs-placement='right' title='Editar fornecedores' onclick='modal_editar_fornecedores("+ data.id +")'><i class='fa-solid fa-pen-to-square' style='color: #1968a4;'></i></button><button class='icone medium' data-bs-placement='right' title='Excluir clientes' onclick='modal_excluir_fornecedores("+ data.id +")'><i class='fa-solid fa-trash' style='color: #df3030;'></i></button>"
            :"<button class='icone medium me-1' data-bs-placement='right' title='Editar fornecedores'><i class='fa-solid fa-pen-to-square' style='color: #1968a4;'></i></button><button class='icone medium' data-bs-placement='right' title='Excluir fornecedores'><i class='fa-solid fa-trash' style='color: #df3030;'></i></button>"
        ]
        nova_tabela.push(nova_linha)
    });
    tabela_fornecedores.clear();
    tabela_fornecedores.rows.add(nova_tabela).draw();
}

$(document).ready(function (){
    let button_search = $(".dt-search")[0];
    let select = document.createElement("select");
    const option1 = new Option('ativo', 'ativo');
    const option2 = new Option('desativo', 'desativo');
    select.add(option1)
    select.add(option2)
    select.style = "border-radius:50px;color:#666;text-align:center;"
    select.classList = "ms-2 py-1";
    select.addEventListener('change', () => {
        let url
        if(select.value == 'ativo'){
            url = 'buscar'
        }else{
            url = 'buscar_removidos'
        }
        $.ajax({
            type: 'GET',
            url: url,
            success: function(response) {
                recarrega_tabela(response.data,select.value)
            },  
            error: function(error) {
                console.log(error)
            }
        });  
    });
    button_search.appendChild(select)
    $(document).on('show.bs.modal','.modal' , function (event){
        var zIndex = 1040 + (10 * $('.modal:visible').length);
        $(this).css('z-index',zIndex);
        setTimeout(function (){
            $('.modal-backdrop').not('.modal-stack').css('z-index',zIndex - 1).addClass('modal-stack');
        },0);
    });
});
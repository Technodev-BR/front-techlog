const tabela = document.getElementsByClassName("tabela-locais");
const linhas = tabela[0].getElementsByTagName("tbody");

let locais_clientes_list = []

function verifica_replica(id){
    const result = locais_clientes_list.filter((local_cliente) => local_cliente.id == id)
    if(locais_clientes_list.length == 0){
        return false;
    }
    if(result.length == 0){
        return false;
    }
    return true;
}

function list_clientes_id(){
    let list_id = []
    locais_clientes_list.forEach((cliente) => {
        list_id.push(cliente.id)
    });
    return list_id
}

function removeAll_locais_clientes(){
    if(locais_clientes_list.length > 0){
        locais_clientes_list.forEach((local_cliente) => {
            pop_locais_clientes(local_cliente.id)
        });
    }
}

function pop_locais_clientes(id){
    let novo_locais_clientes_list = locais_clientes_list.filter(local_cliente => local_cliente.id !== id);
    locais_clientes_list = novo_locais_clientes_list
    atualizar_list_clientes('cadastrar')
    atualizar_list_clientes('editar')
}

function push_locais_clientes(id, nome){
    locais_clientes_list.push({
        'id':id,
        "nome":nome
    });
    atualizar_list_clientes('cadastrar')
    atualizar_list_clientes('editar')
}

function modal_cadastrar_locais(){
    $('#cadastrar_locais').modal("show");

    $('#cadastrar-locais-nome').val('');
    $('#cadastrar-error-locais-nome').text('');
  
    $('#cadastrar-locais-cep').val('');
    $('#cadastrar-error-locais-cep').text('');

    $('#cadastrar-locais-estado_uf').val('');
    $('#cadastrar-error-locais-estado_uf').text('');

    $('#cadastrar-locais-cidade').val('');
    $('#cadastrar-error-locais-cidade').text('');

    $('#cadastrar-locais-rua').val('');
    $('#cadastrar-error-locais-rua').text('');

    $('#cadastrar-error-locais-generico')[0].style = "display:none;";
    $('#cadastrar-error-locais-generico-text').text('');
    $('#cadastrar-locais-clientes_list').val('');
   
    removeAll_locais_clientes();
    fechar_alerta("container_alerta_sucesso");
}

function modal_adicionar_locais_clientes(){
    $('#adicionar_locais_clientes').modal("show");
    $('#adicionar-error-locais_clientes').text('')
    $('#adicionar-locais-clientes-text').val('')
}

function modal_editar_locais(id){
    $('#editar_locais').modal("show");
    
    removeAll_locais_clientes();
    
    $.ajax({
        type: 'GET',
        url: `buscar_by_Id/${id}/`,
        success: function(response) {
            if(response.data){
                $('#editar-locais-id').val(response.data.id);
                $('#editar-locais-nome').val(response.data.nome);
                $('#editar-error-locais-nome').text('');
              
                $('#editar-locais-cep').val(response.data.cep);
                $('#editar-error-locais-cep').text('');
            
                $('#editar-locais-estado_uf').val(response.data.estado_uf);
                $('#editar-error-locais-estado_uf').text('');
            
                $('#editar-locais-cidade').val(response.data.cidade);
                $('#editar-error-locais-cidade').text('');
            
                $('#editar-locais-rua').val(response.data.rua);
                $('#editar-error-locais-rua').text('');

                $('#editar-error-locais-generico')[0].style = "display:none;";
                $('#editar-error-locais-generico-text').text('');
                $('#editar-locais-clientes_list').val('');
            }
        },  
        error: function(error) {
            console.log(error)
        }
    });  
    
    $.ajax({
        type: 'GET',
        url: '/locais_clientes/buscar',
        success: function(response) {
            if(response.data){
                response.data.forEach((local_cliente) =>{
                    if(local_cliente.local_id == id){
                        $.ajax({
                            type: 'GET',
                            url: `/clientes/buscar_by_Id/${local_cliente.cliente_id}/`,
                            success: function(response) {
                                if(response.data){
                                    push_locais_clientes(response.data.id,response.data.nome_fantasia);
                                }
                            },  
                            error: function(error) {
                                console.log(error)
                            }
                        });  
                    }
                });
            }
        },  
        error: function(error) {
            console.log(error)
        }
    });  
    fechar_alerta("container_alerta_sucesso");
}

function modal_excluir_locais(id){
    $('#excluir_locais').modal("show");
    $('#excluir-error-locais-generico')[0].style = "display:none;";
    $('#excluir-error-locais-generico-text').text('');

    removeAll_locais_clientes();

    $.ajax({
        type: 'GET',
        url: `buscar_by_Id/${id}/`,
        success: function(response) {
            const dataAtual = new Date(response.data.data_criado);
            const dataFormatada = dataAtual.toLocaleDateString('pt-BR');
            $('#excluir-locais-informacao').val(`${response.data.nome} - ${dataFormatada}`)
            $('#excluir-locais-id').val(response.data.id)
        },
        error: function(error) {
            console.log(error)
        }
    });

    const list_clientes_vinculados = document.getElementById('excluir_locais_body')
    const ul_locais_clientes = list_clientes_vinculados.getElementsByTagName('ul')[0]
    ul_locais_clientes.innerHTML = ""
    $.ajax({
        type: 'GET',
        url: `/locais_clientes/buscar_by_local_Id/${id}/`,
        success: function(response) {
            if(response.data.length == 0){
                let li = document.createElement('li')
                li.style = 'font-size:.8rem; color:red;text-align:center;'
                li.innerText = "Nenhum cliente vinculado"
                ul_locais_clientes.appendChild(li)
            }else{
                response.data.forEach((local_cliente) => {
                    let li = document.createElement('li')
                    li.classList = 'list-group-item d-flex justify-content-between align-items-center'
                    li.style = 'font-size:.8rem;'
                    li.innerHTML = ` <span style='overflow: hidden; text-overflow: ellipsis;'>${local_cliente.cliente_id} - ${local_cliente.cliente_nome}</span>`
                    ul_locais_clientes.appendChild(li)
                    push_locais_clientes(local_cliente.id,local_cliente.nome_fantasia);
                    
                });
            }
        },
        error: function(error) {
            console.log(error)
        }
    });

    fechar_alerta("container_alerta_sucesso");
}

function cadastrar_locais(){
    cliente_id = list_clientes_id()
    const input = document.getElementById('cadastrar-locais-clientes_list')
    input.value = cliente_id

    let formData = {
        'nome':$('#cadastrar-locais-nome').val(),
        'cep':$('#cadastrar-locais-cep').val(),
        'estado_uf':$('#cadastrar-locais-estado_uf').val(),
        'cidade':$('#cadastrar-locais-cidade').val(),
        'rua':$('#cadastrar-locais-rua').val(),
        'clientes_list':input.value,
        'csrfmiddlewaretoken':$('[name=csrfmiddlewaretoken]').val()
    }
    $.ajax({
        type: 'POST',
        url: 'cadastrar',
        data:formData,
        success: function(response) {
            if(response){
                $('.cadastrar-error-locais').text("");
                $('#cadastrar-error-locais-generico')[0].style = "display:none;";
              
                if(response.sucesso != false){
                    var modal_buscado = document.getElementById('cadastrar_locais');
                    var modal_cadastrar_locais = bootstrap.Modal.getInstance(modal_buscado)
                    modal_cadastrar_locais.hide();
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
                        $('#cadastrar-error-locais-generico')[0].style = "display:block;";
                        $('#cadastrar-error-locais-generico-text').text(response.mensagem);
                    }
                    
                    if(response.errors){
                        for (let campos in response.errors){
                            $('#cadastrar-error-locais-'+campos).text(response.errors[campos].join(', '));
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

function editar_locais(){
    cliente_id = list_clientes_id()
    const input = document.getElementById('editar-locais-clientes_list')
    input.value = cliente_id

    let formData = {
        'nome':$('#editar-locais-nome').val(),
        'cep':$('#editar-locais-cep').val(),
        'estado_uf':$('#editar-locais-estado_uf').val(),
        'cidade':$('#editar-locais-cidade').val(),
        'rua':$('#editar-locais-rua').val(),
        'clientes_list':input.value,
        'csrfmiddlewaretoken':$('[name=csrfmiddlewaretoken]').val()
    }
    let valor = $('#editar-locais-id').val();
    $.ajax({
        type: 'POST',
        url: `atualizar/${valor}/`,
        data:formData,
        success: function(response) {
            if(response){
                $('.editar-error-locais').text("");
                $('#editar-error-locais-generico')[0].style = "display:none;";
                
                if(response.sucesso == true){
                    var modal_buscado = document.getElementById('editar_locais');
                    var modal_editar_locais = bootstrap.Modal.getInstance(modal_buscado);
                    modal_editar_locais.hide();
                    $.ajax({
                        type: 'GET',
                        url: 'buscar',
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
                        $('#editar-error-locais-generico')[0].style = "display:block;";
                        $('#editar-error-locais-generico-text').text(response.mensagem);
                    }
                    
                    if(response.errors){
                        for (let campos in response.errors){
                            $('#editar-error-locais-'+campos).text(response.errors[campos].join(', '));
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

function excluir_locais(){
    let id = $('#excluir-locais-id').val();
    let cliente_id = list_clientes_id();
    const input = document.getElementById('excluir-locais-clientes_list')
    input.value = cliente_id

    let formData = {
        'list_id':input.value,
        'csrfmiddlewaretoken':$('[name=csrfmiddlewaretoken]').val()
    }
    $.ajax({
        type: 'POST',
        url: `/locais_clientes/deletar_by_list_Id`,
        data:formData,
        success: function(response) {
            $('#excluir-error-locais-generico')[0].style = "display:none;";

            if(response.sucesso == true){
                $.ajax({
                    type: 'POST',
                    url: `deletar/${id}/`,
                    data:{'csrfmiddlewaretoken':$('[name=csrfmiddlewaretoken]').val()},
                    success: function(response) {
                        if(response.sucesso == true){
                            var modal_buscado = document.getElementById('excluir_locais');
                            var modal_excluir_locais = bootstrap.Modal.getInstance(modal_buscado);
                            modal_excluir_locais.hide();
                            $.ajax({
                                type: 'GET',
                                url: 'buscar',
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
                            $('#excluir-error-locais-generico')[0].style = "display:block;";
                            $('#excluir-error-locais-generico-text').text(response.mensagem);
                        }
                    },  
                    error: function(error) {
                        console.log(error)
                    }
                });
            }

            if(response.sucesso == false){
                if(response.mensagem){
                    $('#excluir-error-locais-generico')[0].style = "display:block;";
                    $('#excluir-error-locais-generico-text').text(response.mensagem);
                }
            }
        },  
        error: function(error) {
            console.log(error)
        }
    });  
}

function atualizar_list_clientes(acao){
    const list_locais_clientes = document.getElementById(acao + '-list-locais-cliente')
    const ul_locais_clientes = list_locais_clientes.getElementsByTagName('ul')[0]
    ul_locais_clientes.innerHTML = ""
    locais_clientes_list.forEach((local_cliente) => {
        let li = document.createElement('li')
        li.innerHTML = `<li class='list-group-item d-flex justify-content-between align-items-center' style='font-size:.8rem;'><span style='overflow: hidden; text-overflow: ellipsis;'>${local_cliente.nome} </span><i class='fa-solid fa-trash' style='color: #df3030;cursor:pointer;' onclick='pop_locais_clientes(${local_cliente.id})'></i></li>`
        ul_locais_clientes.appendChild(li)
    });
}

function adicionar_locais_clientes(){
    let select_option = document.getElementById("adicionar-locais-clientes-text")
    $('#adicionar-error-locais_clientes').text('')
    if(select_option.value && select_option.value != ""){
        if(!verifica_replica(select_option.value)){
            $.ajax({
                type: 'GET',
                url: `/clientes/buscar_by_Id/${select_option.value}/`,
                success: function(response) {
                    if(response.data){
                        push_locais_clientes(response.data.id,response.data.nome_fantasia)
                        var generic_modal = document.getElementById("adicionar_locais_clientes")
                        var modal = bootstrap.Modal.getInstance(generic_modal)
                        modal.hide();
                    }
                },
                error: function(error) {
                    console.log(error)
                }
            });
        }else{
            $('#adicionar-error-locais_clientes').text('Cliente já adicionado')
        }
    }else{
        $('#adicionar-error-locais_clientes').text('Por favor selecione uma opção')
    }   
}

function recarrega_tabela(data,tipo){
    var tabela_local = $(".tabela-locais").DataTable();
    let nova_tabela = []

    data.forEach((local) =>{
       
        const dataAtual = new Date(local.data_criado);
        const dataFormatada = dataAtual.toLocaleDateString('pt-BR');
        let nova_linha = [
            local.ativo? "<button class='figure small pe-1'><i class='fa-solid fa-circle' style='color: rgb(32, 218, 100);'></i></button>" 
            :"<button class='figure small pe-1'><i class='fa-solid fa-circle' style='color: #ba2525;'></i></button>",
            local.id || "N/A",
            local.nome || "N/A",
            local.cep || "N/A",
            local.estado_uf || "N/A",
            local.cidade || "N/A",
            dataFormatada || "N/A",
            tipo == 'ativo'?"<button class='icone medium me-1' data-bs-placement='right' title='Editar locais' onclick='modal_editar_locais("+ local.id +")'><i class='fa-solid fa-pen-to-square' style='color: #1968a4;'></i></button><button class='icone medium' data-bs-placement='right' title='Excluir locais' onclick='modal_excluir_locais("+ local.id +")'><i class='fa-solid fa-trash' style='color: #df3030;'></i></button>"
            :"<button class='icone medium me-1' data-bs-placement='right' title='Editar locais'><i class='fa-solid fa-pen-to-square' style='color: #1968a4;'></i></button><button class='icone medium' data-bs-placement='right' title='Excluir locais'><i class='fa-solid fa-trash' style='color: #df3030;'></i></button>"
        ]
        nova_tabela.push(nova_linha)
        
    });
    tabela_local.clear();
    tabela_local.rows.add(nova_tabela).draw();
}

$(document).ready(function (){
    
    atualizar_list_clientes('cadastrar')
    atualizar_list_clientes('editar')
    
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
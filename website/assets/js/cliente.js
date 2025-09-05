const tabela = document.getElementsByClassName("tabela-clientes");
const linhas = tabela[0].getElementsByTagName("tbody");

let operacoes_list = []

function pop_operacoes(id){
    let novo_operacoes_list = operacoes_list.filter(operacao => operacao.id !== id);
    operacoes_list = novo_operacoes_list
}

function push_operacoes(id){
    $.ajax({
        type: 'GET',
        url: `/operacoes/buscar_by_Id/${id}/`,
        success: function(response) { 
            if(response.data.id){
                operacoes_list.push(
                    response.data
                );
            }  
        },  
        error: function(error) {
            console.log(error)
        }
    });  
}

function removeAll_operacoes(){
    if(operacoes_list.length > 0){
        operacoes_list.forEach((operacao) => {
            pop_operacoes(operacao.id)
        });
    }
}

function atualizar_operacoes_modal(data){
    const form_operacoes = document.getElementById('editar-list-operacoes')
    const ul_form_operacoes = form_operacoes.getElementsByTagName('ul')[0]
    ul_form_operacoes.innerHTML = ""
    data.forEach((data) => {
        let li = document.createElement('li')
        li.innerHTML = `<li class='list-group-item d-flex justify-content-between align-items-center' style='font-size:.8rem;'><span style='overflow: hidden; text-overflow: ellipsis;'>${data.nome} </span><span class='d-flex ms-1'><i class='fa-solid fa-pen-to-square me-2' style='color: #1968a4;cursor:pointer;' onclick='modal_editar_operacoes(${data.id})'></i><i class='fa-solid fa-trash' style='color: #df3030;cursor:pointer;' onclick='modal_excluir_operacoes(${data.id})'></i></span></li>`
        ul_form_operacoes.appendChild(li)
    });
}

function modal_cadastrar_clientes(){
    $('#cadastrar_clientes').modal("show");

    $('#cadastrar-clientes-nome_fantasia').val('');
    $('#cadastrar-error-clientes-nome_fantasia').text('');
    
    $('#cadastrar-clientes-razao_social').val('');
    $('#cadastrar-error-clientes-razao_social').text('');
    
    $('#cadastrar-clientes-cnpj').val('');
    $('#cadastrar-error-clientes-cnpj').text('');
    
    $('#cadastrar-clientes-telefone').val('');
    $('#cadastrar-error-clientes-telefone').text('');
    
    $('#cadastrar-clientes-email').val('');
    $('#cadastrar-error-clientes-email').text('');
    
    $('#cadastrar-clientes-uf').val('');
    $('#cadastrar-error-clientes-uf').text('');
    
    $('#cadastrar-clientes-cidade').val('');
    $('#cadastrar-error-clientes-cidade').text('');
    
    $('#cadastrar-clientes-rua').val('');
    $('#cadastrar-error-clientes-rua').text('');

    $('#cadastrar-error-clientes-generico')[0].style = "display:none;";
    $('#cadastrar-error-clientes-generico-text').text('');
    fechar_alerta("container_alerta_sucesso");
}

function modal_cadastrar_operacoes(){
    $('#cadastrar_operacoes').modal("show");
    const id = $('#editar-clientes-id').val();
    $.ajax({
        type: 'GET',
        url: `buscar_by_Id/${id}/`,
        success: function(response) {
            if(response.data.id){ 
                const dataAtual = new Date(response.data.data_criado);
                const dataFormatada = dataAtual.toLocaleDateString('pt-BR');
                $('#cadastrar-operacoes-clientes-informacao').val(`${response.data.nome_fantasia} - ${dataFormatada}`);
                $('#cadastrar-operacoes-clientes-id').val(`${response.data.id}`);
                
                $('#cadastrar-operacoes-nome').val('');
                $('#cadastrar-error-operacoes-nome').text('');
            
                $('#cadastrar-error-operacoes-generico')[0].style = "display:none;";
                $('#cadastrar-error-operacoes-generico-text').text('');
            } 
        },  
        error: function(error) {
            console.log(error)
        }
    });  
    fechar_alerta("container_alerta_sucesso");
}

function modal_editar_clientes(id){
    $('#editar_clientes').modal("show");
    $.ajax({
        type: 'GET',
        url: `buscar_by_Id/${id}/`,
        success: function(response) {
            if(response.data.id){ 
                $('#editar-clientes-id').val(response.data.id);
                $('#editar-clientes-nome_fantasia').val(response.data.nome_fantasia);
                $('#editar-error-clientes-nome_fantasia').text('');
                
                $('#editar-clientes-razao_social').val(response.data.razao_social);
                $('#editar-error-clientes-razao_social').text('');
                
                $('#editar-clientes-cnpj').val(response.data.cnpj);
                $('#editar-error-clientes-cnpj').text('');
                
                $('#editar-clientes-telefone').val(response.data.telefone);
                $('#editar-error-clientes-telefone').text('');
                
                $('#editar-clientes-email').val(response.data.email);
                $('#editar-error-clientes-email').text('');
                
                $('#editar-clientes-recebe_email')[0].checked = response.data.recebe_email;
                
                $('#editar-clientes-uf').val(response.data.uf);
                $('#editar-error-clientes-uf').text('');
                
                $('#editar-clientes-cidade').val(response.data.cidade);
                $('#editar-error-clientes-cidade').text('');
                
                $('#editar-clientes-rua').val(response.data.rua);
                $('#editar-error-clientes-rua').text('');
            
                $('#editar-error-clientes-generico')[0].style = "display:none;";
                $('#editar-error-clientes-generico-text').text('');
          
                $.ajax({
                    type: 'GET',
                    url: `/operacoes/buscar_by_cliente_Id/${response.data.id}/`,
                    success: function(response) {
                        atualizar_operacoes_modal(response.data)
                    },  
                    error: function(error) {
                        console.log(error)
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

function modal_editar_operacoes(id){
    $('#editar_operacoes').modal("show");
    const cliente_id = $('#editar-clientes-id').val();
    $.ajax({
        type: 'GET',
        url: `buscar_by_Id/${cliente_id}/`,
        success: function(response) {
            if(response.data.id){ 
                const dataAtual = new Date(response.data.data_criado);
                const dataFormatada = dataAtual.toLocaleDateString('pt-BR');
                $('#editar-operacoes-clientes-informacao').val(`${response.data.nome_fantasia} - ${dataFormatada}`);
                $('#editar-operacoes-clientes-id').val(`${response.data.id}`);
            } 
        },  
        error: function(error) {
            console.log(error)
        }
    });  
   
    $.ajax({
        type: 'GET',
        url: `/operacoes/buscar_by_Id/${id}/`,
        success: function(response) {
            if(response.data.id){ 
                $('#editar-operacoes-operacao_id').val(response.data.id);
                $('#editar-operacoes-nome').val(response.data.nome);
                $('#editar-error-operacoes-nome').text('');
            
                $('#editar-error-operacoes-generico')[0].style = "display:none;";
                $('#editar-error-operacoes-generico-text').text('');
            } 
        },  
        error: function(error) {
            console.log(error)
        }
    });  
    fechar_alerta("container_alerta_sucesso");
}

function modal_excluir_clientes(id){
    $('#excluir_clientes').modal("show");
    $('#excluir-error-clientes-generico')[0].style = "display:none;";
    $('#excluir-error-clientes-generico-text').text('');
    
    removeAll_operacoes();

    $.ajax({
        type: 'GET',
        url: `buscar_by_Id/${id}/`,
        success: function(response) {
            if(response.data.id){ 
                const dataAtual = new Date(response.data.data_criado);
                const dataFormatada = dataAtual.toLocaleDateString('pt-BR');
                $('#excluir-clientes-informacao').val(`${response.data.nome_fantasia} - ${dataFormatada}`);
                $('#excluir-clientes-id').val(`${response.data.id}`);
            } 
        },  
        error: function(error) {
            console.log(error)
        }
    });  

    const body = document.getElementById('excluir_clientes_body')
    const ul_operacoes = body.getElementsByTagName('ul')[0]
    ul_operacoes.innerHTML = ""
    $.ajax({
        type: 'GET',
        url: `/operacoes/buscar_by_cliente_Id/${id}/`,
        success: function(response) {
            if(response.data.length == 0){
                let li = document.createElement('li')
                li.style = 'font-size:.8rem; color:red;text-align:center;'
                li.innerText = "Nenhuma operação vinculado"
                ul_operacoes.appendChild(li)
            }else{
                response.data.forEach((operacao) => {
                    let li = document.createElement('li')
                    li.classList = 'list-group-item d-flex justify-content-between align-items-center'
                    li.style = 'font-size:.8rem;'
                    li.innerHTML = ` <span style='overflow: hidden; text-overflow: ellipsis;'>${operacao.id} - ${operacao.nome}</span>`
                    ul_operacoes.appendChild(li) 
                    push_operacoes(operacao.id);
                });
            }
        },  
        error: function(error) {
            console.log(error)
        }
    });  
    fechar_alerta("container_alerta_sucesso");
}

function modal_excluir_operacoes(id){
    $('#excluir_operacoes').modal("show");
    $.ajax({
        type: 'GET',
        url: `/operacoes/buscar_by_Id/${id}/`,
        success: function(response) {
            if(response.data.id){ 
                const dataAtual = new Date(response.data.data_criado);
                const dataFormatada = dataAtual.toLocaleDateString('pt-BR');
                $('#excluir-operacoes-operacao_id').val(response.data.id);
                $('#excluir-operacoes-informacao').val(`${response.data.nome} - ${dataFormatada}`);
                $('#excluir-error-operacoes-generico')[0].style = "display:none;";
                $('#excluir-error-operacoes-generico-text').text('');
            } 
        },  
        error: function(error) {
            console.log(error)
        }
    });  
    fechar_alerta("container_alerta_sucesso")
}

function cadastrar_clientes(){
    let formData = {
        'nome_fantasia': $('#cadastrar-clientes-nome_fantasia').val(),
        'razao_social':$('#cadastrar-clientes-razao_social').val(),
        'cnpj':$('#cadastrar-clientes-cnpj').val(),
        'telefone':$('#cadastrar-clientes-telefone').val(),
        'email':$('#cadastrar-clientes-email').val(),
        'recebe_email':$('#cadastrar-clientes-recebe_email')[0].checked,
        'uf':$('#cadastrar-clientes-uf').val(),
        'cidade':$('#cadastrar-clientes-cidade').val(),
        'rua':$('#cadastrar-clientes-rua').val(),
        'csrfmiddlewaretoken':$('[name=csrfmiddlewaretoken]').val()
    }
    $.ajax({
        type: 'POST',
        url: 'cadastrar',
        data:formData,
        success: function(response) {
            $('.cadastrar-error-clientes').text("");
            $('#cadastrar-error-clientes-generico')[0].style = "display:none;";
            
            if(response.sucesso != false){
                var modal_buscado = document.getElementById('cadastrar_clientes');
                var modal_cadastrar_clientes = bootstrap.Modal.getInstance(modal_buscado)
                modal_cadastrar_clientes.hide();
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
                    $('#cadastrar-error-clientes-generico')[0].style = "display:block;";
                    $('#cadastrar-error-clientes-generico-text').text(response.mensagem);
                }
                if(response.errors){
                    for (let campos in response.errors){
                        $('#cadastrar-error-clientes-'+campos).text(response.errors[campos].join(', '));
                    }
                }
            }
            
        },  
        error: function(error) {
            console.log(error)
        }
    });  
}

function cadastrar_operacoes(){
    let formData = {
        'nome': $('#cadastrar-operacoes-nome').val(),
        'cliente': $('#cadastrar-operacoes-clientes-id').val(),
        'csrfmiddlewaretoken':$('[name=csrfmiddlewaretoken]').val()
    }
    $.ajax({
        type: 'POST',
        url: '/operacoes/cadastrar',
        data:formData,
        success: function(response) {
            if(response){ 
                $('.cadastrar-error-operacoes').text("");
                $('#cadastrar-error-operacoes-generico')[0].style = "display:none;";
                
                if(response.sucesso != false){
                    var modal_buscado = document.getElementById('cadastrar_operacoes');
                    var modal_cadastrar_operacoes = bootstrap.Modal.getInstance(modal_buscado)
                    modal_cadastrar_operacoes.hide();
                    $.ajax({
                        type: 'GET',
                        url: `/operacoes/buscar_by_cliente_Id/${$('#editar-clientes-id').val()}/`,
                        success: function(response) {
                            atualizar_operacoes_modal(response.data)
                        },  
                        error: function(error) {
                            console.log(error)
                        }
                    });
                }
                if(response.sucesso == false){
                    if(response.mensagem){
                        $('#cadastrar-error-operacoes-generico')[0].style = "display:block;";
                        $('#cadastrar-error-operacoes-generico-text').text(response.mensagem);
                    }
                    if(response.errors){
                        for (let campos in response.errors){
                            $('#cadastrar-error-operacoes-'+campos).text(response.errors[campos].join(', '));
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

function editar_clientes(){
    let formData = {
        'nome_fantasia': $('#editar-clientes-nome_fantasia').val(),
        'razao_social':$('#editar-clientes-razao_social').val(),
        'cnpj':$('#editar-clientes-cnpj').val(),
        'telefone':$('#editar-clientes-telefone').val(),
        'email':$('#editar-clientes-email').val(),
        'recebe_email':$('#editar-clientes-recebe_email')[0].checked,
        'uf':$('#editar-clientes-uf').val(),
        'cidade':$('#editar-clientes-cidade').val(),
        'rua':$('#editar-clientes-rua').val(),
        'csrfmiddlewaretoken':$('[name=csrfmiddlewaretoken]').val()
    }
    $.ajax({
        type: 'POST',
        url: `atualizar/${$('#editar-clientes-id').val()}/`,
        data:formData,
        success: function(response) {
            if(response){ 
                $('.editar-error-clientes').text("");
                $('#editar-error-clientes-generico')[0].style = "display:none;";
                
                if(response.sucesso != false){
                    var modal_buscado = document.getElementById('editar_clientes');
                    var modal_editar_clientes = bootstrap.Modal.getInstance(modal_buscado)
                    modal_editar_clientes.hide();
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
                        $('#editar-error-clientes-generico')[0].style = "display:block;";
                        $('#editar-error-clientes-generico-text').text(response.mensagem);
                    }
                    if(response.errors){
                        for (let campos in response.errors){
                            $('#editar-error-clientes-'+campos).text(response.errors[campos].join(', '));
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

function editar_operacoes(){
    let formData = {
        'nome': $('#editar-operacoes-nome').val(),
        'cliente': $('#editar-operacoes-clientes-id').val(),
        'csrfmiddlewaretoken':$('[name=csrfmiddlewaretoken]').val()
    }
    $.ajax({
        type: 'POST',
        url: `/operacoes/atualizar/${$('#editar-operacoes-operacao_id').val()}/`,
        data:formData,
        success: function(response) {
            if(response){ 
                $('.editar-error-operacoes').text("");
                $('#editar-error-operacoes-generico')[0].style = "display:none;";
                
                if(response.sucesso != false){
                    var modal_buscado = document.getElementById('editar_operacoes');
                    var modal_editar_operacoes = bootstrap.Modal.getInstance(modal_buscado)
                    modal_editar_operacoes.hide();
                    $.ajax({
                        type: 'GET',
                        url: `/operacoes/buscar_by_cliente_Id/${$('#editar-clientes-id').val()}/`,
                        success: function(response) {
                            atualizar_operacoes_modal(response.data)
                        },  
                        error: function(error) {
                            console.log(error)
                        }
                    });
                   
                }
                if(response.sucesso == false){
                    if(response.mensagem){
                        $('#editar-error-operacoes-generico')[0].style = "display:block;";
                        $('#editar-error-operacoes-generico-text').text(response.mensagem);
                    }
                    if(response.errors){
                        for (let campos in response.errors){
                            $('#editar-error-operacoes-'+campos).text(response.errors[campos].join(', '));
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

function excluir_clientes(){
    let formData = {
        'csrfmiddlewaretoken':$('[name=csrfmiddlewaretoken]').val()
    }
    $.ajax({
        type: 'POST',
        url: `deletar/${$('#excluir-clientes-id').val()}/`,
        data:formData,
        success: function(response) {
            $('#excluir-error-clientes-generico')[0].style = "display:none;";
            
            if(response.sucesso == true){
                var modal_buscado = document.getElementById('excluir_clientes');
                var modal_excluir_clientes = bootstrap.Modal.getInstance(modal_buscado)
                modal_excluir_clientes.hide();
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
                $('#excluir-error-clientes-generico')[0].style = "display:block;";
                $('#excluir-error-clientes-generico-text').text(response.mensagem);
            }
        },  
        error: function(error) {
            console.log(error)
        }
    });    
}

function excluir_operacoes(){
    let formData = {
        'csrfmiddlewaretoken':$('[name=csrfmiddlewaretoken]').val()
    }
    $.ajax({
        type: 'POST',
        url: `/operacoes/deletar/${$('#excluir-operacoes-operacao_id').val()}/`,
        data:formData,
        success: function(response) {
            $('#excluir-error-operacoes-generico')[0].style = "display:none;";
            
            if(response.sucesso == true){
                var modal_buscado = document.getElementById('excluir_operacoes');
                var modal_excluir_operacoes = bootstrap.Modal.getInstance(modal_buscado)
                modal_excluir_operacoes.hide();
                $.ajax({
                    type: 'GET',
                    url: `/operacoes/buscar_by_cliente_Id/${$('#editar-clientes-id').val()}/`,
                    success: function(response) {
                        atualizar_operacoes_modal(response.data)
                    },  
                    error: function(error) {
                        console.log(error)
                    }
                });
            }
        
            if(response.sucesso == false){
                $('#excluir-error-operacoes-generico')[0].style = "display:block;";
                $('#excluir-error-operacoes-generico-text').text(response.mensagem);
            }
        },  
        error: function(error) {
            console.log(error)
        }
    });  
}

function recarrega_tabela(data,tipo){
    var tabela_cliente = $(".tabela-clientes").DataTable();
    let nova_tabela = []
    data.forEach((data) =>{
        const dataAtual = new Date(data.data_criado);
        const dataFormatada = dataAtual.toLocaleDateString('pt-BR');
        let nova_linha = [
            data.ativo? "<button class='figure small pe-1'><i class='fa-solid fa-circle' style='color: rgb(32, 218, 100);'></i></button>" 
            :"<button class='figure small pe-1'><i class='fa-solid fa-circle' style='color: #ba2525;'></i></button>",
            data.id || "N/A",
            data.razao_social || "N/A",
            data.cnpj || "N/A",
            data.email || "N/A",
            data.cep || "N/A",
            dataFormatada || "N/A",
            tipo == 'ativo'?"<button class='icone medium me-1' data-bs-placement='right' title='Editar clientes' onclick='modal_editar_clientes("+ data.id +")'><i class='fa-solid fa-pen-to-square' style='color: #1968a4;'></i></button><button class='icone medium' data-bs-placement='right' title='Excluir clientes' onclick='modal_excluir_clientes("+ data.id +")'><i class='fa-solid fa-trash' style='color: #df3030;'></i></button>"
            :"<button class='icone medium me-1' data-bs-placement='right' title='Editar clientes'><i class='fa-solid fa-pen-to-square' style='color: #1968a4;'></i></button><button class='icone medium' data-bs-placement='right' title='Excluir clientes'><i class='fa-solid fa-trash' style='color: #df3030;'></i></button>"
        ]
        nova_tabela.push(nova_linha)
    });
    tabela_cliente.clear();
    tabela_cliente.rows.add(nova_tabela).draw();
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

$(document).on("input", "#cadastrar-clientes-cnpj", function (e) {
    this.value = this.value.replace(/[^0-9]/g, '').replace(/(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})$/, "$1.$2.$3/$4-$5");
});

$(document).on("input", "#editar-clientes-cnpj", function (e) {
    this.value = this.value.replace(/[^0-9]/g, '').replace(/(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})$/, "$1.$2.$3/$4-$5");
});
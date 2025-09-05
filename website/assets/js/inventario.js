const tabela = document.getElementsByClassName("tabela-iscas");
const linhas = tabela[0].getElementsByTagName("tbody");

let isca_list = []

function list_isca_id(){
    let list_id = []
    isca_list.forEach((isca) => {
        list_id.push(isca.id)
    });
    return list_id
}

function removeAll_iscas(){
    if(isca_list.length > 0){
        isca_list.forEach((isca) => {
            if(isca.id){
                pop_iscas(isca.id)
            }
        });
    }
}

function pop_iscas(id){
    let novo_isca_list = isca_list.filter(isca => isca.id !== parseInt(id));
    isca_list = novo_isca_list
}

function push_iscas(id){
    if(id){
        $.ajax({
            type: 'GET',
            url: `buscar_by_Id/${id}/`,
            success: function(response) { 
                if(response.data.id){
                    isca_list.push(
                        response.data
                    );
                }
            },
            error: function(error) {
                console.log(error)
            }
        });
    }  
}

function modal_cadastrar_iscas(){
    $('#cadastrar_iscas').modal("show");

    $('#cadastrar-iscas-numero_isca').val('');
    $('#cadastrar-error-iscas-numero_isca').text('');

    $('#cadastrar-iscas-local_cliente').val('');
    $('#cadastrar-error-iscas-local_cliente').text('');

    $('#cadastrar-iscas-fornecedor').val('');
    $('#cadastrar-error-iscas-fornecedor').text('');

    $('#cadastrar-iscas-comunicacao').val('');
    $('#cadastrar-error-iscas-comunicacao').text('');

    $('#cadastrar-iscas-modelo').val('');
    $('#cadastrar-error-iscas-modelo').text('');

    $('#cadastrar-iscas-operacao').val('');
    $('#cadastrar-error-iscas-operacao').text('');

    $('#canvas-foto')[0].style = "display:none;"
    $('#erro_msg')[0].style = "display:none;"
    $('#cadastrar-error-iscas-generico')[0].style = "display:none;";
    $('#cadastrar-error-iscas-generico-text').text('');
    fechar_alerta("container_alerta_sucesso");
}

function verificar_iscas_selecionadas(){
    fechar_alerta("container_alerta_erro");
    fechar_alerta("container_alerta_sucesso");
    let result = true
    if(isca_list.length > 0){
        isca_list.forEach((isca) => {
            if(isca.status !== "Almoxarifado"){
                result = false;
            }
        });
        if(result){
            modal_cadastrar_solicitacoes();
        }else{
            $('#alerta_mensagem_erro').text(`Iscas não podem ser usadas`);
            abrir_alerta("container_alerta_erro");
        }
    }else{
        $('#alerta_mensagem_erro').text(`Nenhuma isca foi selecionada`);
        abrir_alerta("container_alerta_erro");
    }
}

function modal_cadastrar_solicitacoes(){
    $('#cadastrar_solicitacoes').modal("show");
    $('#cadastrar-error-solicitacoes-generico')[0].style = "display:none;";
    $('#cadastrar-error-solicitacoes-generico-text').text('');
    const body = document.getElementById('cadastrar_solicitacoes_body')
    const ul_list_iscas = body.getElementsByTagName('ul')[0]
    ul_list_iscas.innerHTML = ""
    isca_list.forEach((isca) => {
        const dataAtual = new Date(isca.data_criado);
        const dataFormatada = dataAtual.toLocaleDateString('pt-BR');
        let div = document.createElement('div');
        div.className = "mt-2"
        div.innerHTML = `<div class='row mt-2 m-0 p-0'><div class='col-8 ps-0'> <label for="informacao">Numero da isca</label><input type='text' class='form-control' name='informacao' value='${isca.numero_isca} - ${dataFormatada}' readonly></div><div class='col-4 px-0'><label for="id">Codigo</label><input type='text' name='id' class='form-control' value='${isca.id}' readonly></div></div>` 
        ul_list_iscas.appendChild(div);
    });
}

function modal_editar_iscas(id){
    $('#editar-iscas-foto')[0].style = "display:none;"
    $('#editar_iscas').modal("show");
    $.ajax({
        type: 'GET',
        url: `buscar_by_Id/${id}/`,
        success: function(response) {
            if(response.data){
                $('#editar-iscas-id').val(response.data.id);
                if(response.data.foto){
                    $('#editar-iscas-foto')[0].style = "display:block;"
                    let context = $('#editar-iscas-foto')[0].getContext('2d') 
                    var img = new Image();
                    img.src = "/uploads/"+response.data.foto;
                    img.onload = function(){
                        context.drawImage(img,0,0)
                    }
                }
                $('#editar-iscas-numero_isca').val(response.data.numero_isca)
                $('#editar-error-iscas-numero_isca').text('')
                
                $('#editar-iscas-cadastrante').val(response.data.usuario_cadastrante)
                
                $('#editar-iscas-local_cliente').val(response.data.local_cliente_id)
                $('#editar-error-iscas-local_cliente').text('')
            
                $('#editar-iscas-fornecedor').val(response.data.fornecedor_id)
                $('#editar-error-iscas-fornecedor').text('')
            
                $('#editar-iscas-comunicacao').val(response.data.comunicacao)
                $('#editar-error-iscas-comunicacao').text('')
            
                $('#editar-iscas-modelo').val(response.data.modelo)
                $('#editar-error-iscas-modelo').text('')
            
                $('#editar-iscas-operacao').val(response.data.operacao_id)
                $('#editar-error-iscas-operacao').text('')
                
                $('#editar-error-iscas-generico')[0].style = "display:none;"
                $('#editar-error-iscas-generico-text').text('')
            }
        },  
        error: function(error) {
            console.log(error)
        }
    });  
    fechar_alerta("container_alerta_sucesso");
}

function modal_excluir_iscas(id){
    $('#excluir_iscas').modal("show");
    $('#excluir-error-iscas-generico')[0].style = "display:none;";
    $('#excluir-error-iscas-generico-text').text('');
    $.ajax({
        type: 'GET',
        url: `buscar_by_Id/${id}/`,
        success: function(response) {
            $('#excluir-iscas-informacao').val(`${response.data.numero_isca} - ${response.data.fornecedor_nome}`)
            $('#excluir-iscas-id').val(response.data.id)
        },
        error: function(error) {
            console.log(error)
        }
    });
    fechar_alerta("container_alerta_sucesso");
}

let foto = null
function cadastrar_iscas(){
    const formData = new FormData()
    formData.append('numero_isca',$('#cadastrar-iscas-numero_isca').val())
    formData.append('local_cliente',$('#cadastrar-iscas-local_cliente').val())
    formData.append('fornecedor',$('#cadastrar-iscas-fornecedor').val())
    formData.append('comunicacao',$('#cadastrar-iscas-comunicacao').val())
    formData.append('modelo',$('#cadastrar-iscas-modelo').val())
    formData.append('operacao',$('#cadastrar-iscas-operacao').val())
    foto?formData.append('foto',foto,`foto_isca_${$('#cadastrar-iscas-numero_isca').val()}.png`):null
    formData.append('csrfmiddlewaretoken',$('[name=csrfmiddlewaretoken]').val())
   
    $.ajax({
        type: 'POST',
        url: 'cadastrar',
        processData: false,
        contentType:false,
        data:formData,
        success: function(response) {
            if(response){
                $('.cadastrar-error-iscas').text("");
                $('#cadastrar-error-iscas-generico')[0].style = "display:none;";
              
                if(response.sucesso != false){
                    var modal_buscado = document.getElementById('cadastrar_iscas');
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
                        $('#cadastrar-error-iscas-generico')[0].style = "display:block;";
                        $('#cadastrar-error-iscas-generico-text').text(response.mensagem);
                    }
                    
                    if(response.errors){
                        for (let campos in response.errors){
                            $('#cadastrar-error-iscas-'+campos).text(response.errors[campos].join(', '));
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

function cadastrar_solicitacoes(){
    isca_id = list_isca_id();
    let input = document.getElementById("cadastrar-solicitacoes-iscas_list");
    input.value = isca_id;
    let formData = {
        'isca_list':input.value,
        'csrfmiddlewaretoken':$('[name=csrfmiddlewaretoken]').val()
    }
    $.ajax({
        type: 'POST',
        url: '/solicitacoes/cadastrar_range',
        data:formData,
        success: function(response) {
            if(response){
                $('#cadastrar-error-solicitacoes-generico')[0].style = "display:none;";
              
                if(response.sucesso != false){
                    var modal_buscado = document.getElementById('cadastrar_solicitacoes');
                    var modal_cadastrar_solicitacao = bootstrap.Modal.getInstance(modal_buscado)
                    modal_cadastrar_solicitacao.hide();
                    $.ajax({
                        type: 'GET',
                        url: `buscar`,
                        success: function(response) {
                            recarrega_tabela(response.data,'ativo')
                            removeAll_iscas();
                        },  
                        error: function(error) {
                            console.log(error)
                        }
                    });  
                    $('#alerta_mensagem_sucesso').text(response.mensagem);
                    abrir_alerta("container_alerta_sucesso");
                    window.location.href = window.origin + "/solicitacoes/index"
                }

                if(response.sucesso == false){
                    if(response.mensagem){
                        $('#cadastrar-error-solicitacoes-generico')[0].style = "display:block;";
                        $('#cadastrar-error-solicitacoes-generico-text').text(response.mensagem);
                    }
                }
            }
        },  
        error: function(error) {
            console.log(error)
        }
    });  
}

function editar_iscas(){
    let valor = $('#editar-iscas-id').val();
    let formData = {
        'numero_isca':$('#editar-iscas-numero_isca').val(),
        'local_cliente':$('#editar-iscas-local_cliente').val(),
        'usuario_cadastrante':$('#editar-iscas-cadastrante').val(),
        'fornecedor':$('#editar-iscas-fornecedor').val(),
        'comunicacao':$('#editar-iscas-comunicacao').val(),
        'modelo':$('#editar-iscas-modelo').val(),
        'operacao':$('#editar-iscas-operacao').val(),
        'csrfmiddlewaretoken':$('[name=csrfmiddlewaretoken]').val()
    }
    $.ajax({
        type: 'POST',
        url: `atualizar/${valor}/`,
        data:formData,
        success: function(response) {
            if(response){
                $('.editar-error-iscas').text("");
                $('#editar-error-iscas-generico')[0].style = "display:none;";
                if(response.sucesso == true){
                    var modal_buscado = document.getElementById('editar_iscas');
                    var modal_editar_iscas = bootstrap.Modal.getInstance(modal_buscado);
                    modal_editar_iscas.hide();
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
                        $('#editar-error-iscas-generico')[0].style = "display:block;";
                        $('#editar-error-iscas-generico-text').text(response.mensagem);
                    }
                    
                    if(response.errors){
                        for (let campos in response.errors){
                            $('#editar-error-iscas-'+campos).text(response.errors[campos].join(', '));
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

function excluir_iscas(){
    let id = $('#excluir-iscas-id').val();
    $.ajax({
        type: 'POST',
        url: `deletar/${id}/`,
        data:{'csrfmiddlewaretoken':$('[name=csrfmiddlewaretoken]').val()},
        success: function(response) {
            if(response.sucesso == true){
                var modal_buscado = document.getElementById('excluir_iscas');
                var modal_excluir_iscas = bootstrap.Modal.getInstance(modal_buscado);
                modal_excluir_iscas.hide();
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
                $('#excluir-error-iscas-generico')[0].style = "display:block;";
                $('#excluir-error-iscas-generico-text').text(response.mensagem);
            }
        },  
        error: function(error) {
            console.log(error)
        }
    });
}

function recarrega_tabela(data,tipo){
    const tabela_isca = $(".tabela-iscas").DataTable();
    let nova_tabela = []
    data.forEach((data) => {
        let color_status
        if(data.status == "Almoxarifado"){
            color_status = "rgb(32, 218, 100);"
        }else if(data.status == "Descartado" || data.status == "Reprovado" || data.status == "Usado"){
            color_status = "#ba2525;"
        }else{
            color_status = "goldenrod;"
        }
        const dataAtual = new Date(data.data_criado);
        const dataFormatada = dataAtual.toLocaleDateString('pt-BR');
        let nova_linha = [
            "<input type='checkbox' name='checkbox-isca' value="+data.id+">",
            data.ativo? "<button class='figure pe-1'><i class='fa-solid fa-tower-broadcast' style='color: #2caf46;'></i></button><button class='text-reduzido numero_isca'>"+data.numero_isca || "N/A"+"</button>"
            :"<button class='figure pe-1'><i class='fa-solid fa-tower-broadcast' style='color: #ba2525;'></i></button><button class='text-reduzido'>"+data.numero_isca || "N/A"+"</button>",
            data.fornecedor_nome || "N/A",
            data.comunicacao || "N/A",
            data.modelo || "N/A",
            "<button class='figure small'><i class='fa-solid fa-circle' style='color:"+color_status+"'></i></button> <button class='text'>"+data.status || "N/A"+"</button>",
            data.local_nome || "N/A",
            data.operacao_cliente_nome || "N/A",
            data.operacao_nome || "N/A",
            dataFormatada || "N/A",
            tipo == 'ativo'?"<button class='icone medium me-1' data-bs-placement='right' title='Editar locais' onclick='modal_editar_iscas("+ data.id +")'><i class='fa-solid fa-pen-to-square' style='color: #1968a4;'></i></button><button class='icone medium' data-bs-placement='right' title='Excluir locais' onclick='modal_excluir_iscas("+ data.id +")'><i class='fa-solid fa-trash' style='color: #df3030;'></i></button>"
            :"<button class='icone medium me-1' data-bs-placement='right' title='Editar locais'><i class='fa-solid fa-pen-to-square' style='color: #1968a4;'></i></button><button class='icone medium' data-bs-placement='right' title='Excluir locais'><i class='fa-solid fa-trash' style='color: #df3030;'></i></button>"
        ]
        nova_tabela.push(nova_linha)
    });
    tabela_isca.clear();
    tabela_isca.rows.add(nova_tabela).draw();
    removeAll_iscas();
}

$(linhas).on('click', 'tr', function () {
    let checkbox = this.getElementsByTagName("input")[0]
    if(checkbox){
        checkbox.checked = checkbox.checked === true? false : true;
        if(this.classList[0] === "selected-linha"){
            this.classList.remove("selected-linha")
            pop_iscas(checkbox.value)
            
        }else{
            this.classList.add("selected-linha")
            push_iscas(checkbox.value)
        }
    }
});

$(linhas).on('click', 'input', function () {
    this.checked = this.checked === true? false : true; 
});

$(document).ready(function (){
    const tabela_iscas = $(".tabela-iscas").DataTable();
    tabela_iscas.order([[5,'desc']]);
    tabela_iscas.draw()
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
                removeAll_iscas();
            },  
            error: function(error) {
                console.log(error)
            }
        });  
    });
    button_search.appendChild(select)
});

const video = document.getElementById('video-codebar');
const canvas = document.getElementById('canvas-foto');
const context = canvas.getContext('2d');
let streaming = false
let camerastream = null

function abrir_camera(){
    const modal_qrcode = document.getElementById('modal-qrcode');
    const erroMsg = document.getElementById('erro_msg');
    if(navigator.mediaDevices && navigator.mediaDevices.getUserMedia){
        navigator.mediaDevices.getUserMedia({ 
            video: {
                frameRate:{ideal:40},
                resizeMode:"crop-and-scale",
                facingMode:"environment"},
                advanced: [{ focusMode:"continuous"},{zoom :2.0}]
            }
        ).then(function (stream){
            video.srcObject = stream
            video.play()
            
            streaming = true
            camerastream = stream
            erroMsg.style.display = 'none';
            modal_qrcode.style.display = 'block';
            verificar_qrcode();
        }).catch(function (){
            erroMsg.style.display = 'block';
        });
    }else{
        erroMsg.style.display = 'block';
    }
}

function fechar_video(){
    const modal_qrcode = document.getElementById('modal-qrcode');
    if(camerastream){
        let tracks = camerastream.getTracks();
        tracks.forEach(track => track.stop());
        video.srcObject = null;
        streaming = false
        if(streaming == false && video.srcObject == null){
            modal_qrcode.style.display = 'none';
        }
    }
}

function verificar_qrcode(){
    const canvas_controle = document.createElement('canvas')
    const context_controle = canvas_controle.getContext('2d');
    foto = null
    setInterval (function (){
        if(streaming){
            canvas_controle.width = video.videoWidth
            canvas_controle.height = video.videoHeight
            context_controle.drawImage(video, 0, 0, canvas_controle.width, canvas_controle.height);
            const dataURL = canvas_controle.toDataURL('image/png');
            let formData = {
                'image':dataURL,
                'csrfmiddlewaretoken':$('[name=csrfmiddlewaretoken]').val()
            }
            $.ajax({
                type: 'POST',
                url: `leitor_qrcode`,
                data:formData,
                success: function(response) {
                    if(response.sucesso == true){
                        if(video && streaming){
                            canvas.width = video.videoWidth
                            canvas.height = video.videoHeight
                            context.drawImage(video,0,0)
                            $('#cadastrar-iscas-numero_isca').val(response.data)
                            $('#canvas-foto')[0].style = "display:block;"
                            setTimeout(function(){
                                if(canvas && canvas.style.display == 'block'){
                                    canvas.toBlob(function (blob){
                                        foto = blob
                                    })
                                }
                                fechar_video();
                            },500)
                        }
                       return;
                    }
                },  
                error: function(error) {
                    console.log(error)
                }
            });
        }
    }, 1500)
}

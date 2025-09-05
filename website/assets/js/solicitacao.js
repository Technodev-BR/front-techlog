const tabela = document.getElementsByClassName("tabela-solicitacao");
const linhas = tabela[0].getElementsByTagName("tbody");
const foto_data_implatacao = []

function verificar_implantacao(id,numero_isca,id_isca){
    $.ajax({
        type: 'GET',
        url: `buscar_by_Id/${id}/`,
        success: function(response) { 
            if(response.data.isca_numero){
                $.ajax({
                    type: 'GET',
                    url: `/rastreamentos/buscar_by_isca_Id/${response.data.isca_id}/`,
                    success: function(response) {
                        if(response.data.id){
                            $('#editar-rastreamentos-modal_titulo').text("Editar Rastreamento")
                            $('#editar-rastreamentos-data_saida').prop("readonly", false);
                            $('#editar-rastreamentos-nota_fiscal').prop("readonly", false);
                            $('#editar-rastreamentos-motorista').prop("readonly", false);
                            $('#editar-rastreamentos-placa').prop("readonly", false);
                            $('#editar-rastreamentos-rota_insercao').prop("readonly", false);
                            $('#editar-rastreamentos-rota_maior_valor').prop("readonly", false);
                            $('#editar-rastreamentos-valor_sm').prop("readonly", false);
                            $('#editar-rastreamentos-volume').prop("readonly", false);
                            $('#editar-rastreamentos-manifesto').prop("readonly", false);
                            $('#editar-rastreamentos-sm').prop("readonly", false);
                            for (let index = 0; index < $('.icon-required').length; index++) {
                                $('.icon-required')[index].style.display = "none"  
                            }
                            modal_editar_rastreamentos(response.data,response.data.isca_id,false)
                        }

                        if(response.data.id == undefined){
                            modal_cadastrar_rastreamentos(numero_isca,id_isca)
                        }
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
}

function verificar_inicio_sm(id){
    $.ajax({
        type: 'GET',
        url: `buscar_by_Id/${id}/`,
        success: function(response) { 
            if(response.data.isca_numero){
                $.ajax({
                    type: 'GET',
                    url: `/rastreamentos/buscar_by_isca_Id/${response.data.isca_id}/`,
                    success: function(response) {
                        if(response.data.id && response.data.resultado != 'Em viagem'){
                            $('#editar-rastreamentos-modal_titulo').text("Iniciar Rastreamento")
                            $('#editar-rastreamentos-data_saida').prop("readonly", true);
                            $('#editar-rastreamentos-nota_fiscal').prop("readonly", true);
                            $('#editar-rastreamentos-motorista').prop("readonly", true);
                            $('#editar-rastreamentos-placa').prop("readonly", true);
                            $('#editar-rastreamentos-rota_insercao').prop("readonly", true);
                            $('#editar-rastreamentos-rota_maior_valor').prop("readonly", true);
                            $('#editar-rastreamentos-valor_sm').prop("readonly", true);
                            $('#editar-rastreamentos-volume').prop("readonly", true);
                            $('#editar-rastreamentos-manifesto').prop("readonly", true);
                            $('#editar-rastreamentos-sm').prop("readonly", true);
                            for (let index = 0; index < $('.icon-required').length; index++) {
                                 $('.icon-required')[index].style.display = "inline-block"  
                            }
                            modal_editar_rastreamentos(response.data,response.data.id_isca,true)
                        }
                        if(response.data.id && response.data.resultado === 'Em viagem'){
                            $('#alerta_mensagem_erro').text('Viagem já foi iniciada');
                            abrir_alerta("container_alerta_erro");        
                        }

                        if(response.data.id == undefined){
                            $('#alerta_mensagem_erro').text('Faça uma implantação antes');
                            abrir_alerta("container_alerta_erro");        
                        }
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
}

function modal_cadastrar_rastreamentos(numero_isca,id_isca){
    $('#cadastrar_rastreamentos').modal("show");
    $('#cadastrar-rastreamentos-isca').val(numero_isca)
    $('#cadastrar-rastreamentos-isca-id').val(id_isca)
    
    const data_atual = new Date();
    const data_formatada = data_atual.toISOString().split('T')[0];
    $('#cadastrar-rastreamentos-data_implantacao').val(data_formatada)
    
    $('#cadastrar-rastreamentos-data_saida').val('')
    $('#cadastrar-error-rastreamentos-data_saida').text('')
    
    $('#cadastrar-rastreamentos-nota_fiscal').val('')
    $('#cadastrar-error-rastreamentos-nota_fiscal').text('')
    
    $('#cadastrar-rastreamentos-motorista').val('')
    $('#cadastrar-error-rastreamentos-motorista').text('')
    
    $('#cadastrar-rastreamentos-placa').val('')
    $('#cadastrar-error-rastreamentos-placa').text('')
    
    $('#cadastrar-rastreamentos-rota_insercao').val('')
    $('#cadastrar-error-rastreamentos-rota_insercao').text('')
    
    $('#cadastrar-rastreamentos-rota_maior_valor').val('')
    $('#cadastrar-error-rastreamentos-rota_maior_valor').text('')
    
    $('#cadastrar-rastreamentos-valor_sm').val('')
    $('#cadastrar-error-rastreamentos-valor_sm').text('')
    
    $('#cadastrar-rastreamentos-volume').val('')
    $('#cadastrar-error-rastreamentos-volume').text('')
    
    $('#cadastrar-rastreamentos-manifesto').val('')
    $('#cadastrar-error-rastreamentos-manifesto').text('')
    
    $('#cadastrar-rastreamentos-sm').val('')
    $('#cadastrar-error-rastreamentos-sm').text('')
    $("#cadastrar-rastreamentos-foto").removeClass("disabled")
    limpa_fotos_implantacao()
    fechar_alerta("container_alerta_sucesso")
    fechar_alerta("container_alerta_erro")
}

function modal_editar_rastreamentos(data,id_isca,inicio_sm){
    if(inicio_sm){
        $('#editar-rastreamentos-button_enviar').attr('onclick','iniciar_rastreamentos();')
    }else{
        $('#editar-rastreamentos-button_enviar').attr('onclick','editar_rastreamentos();')
    }
    $('#editar_rastreamentos').modal("show");
    $('#editar-rastreamentos-isca').val(data.isca_numero)
    $('#editar-rastreamentos-isca-id').val(id_isca)
    $('#editar-rastreamentos-id').val(data.id)
    
    const data_implatacao = new Date(data.data_implantacao);
    const data_implatacao_formatada = data_implatacao.toISOString().split('T')[0];
    $('#editar-rastreamentos-data_implantacao').val(data_implatacao_formatada)
    
    $('#editar-rastreamentos-data_saida').val('')
    if(data.data_saida != 'None'){
        const data_saida = new Date(data.data_saida);
        const data_saida_formatada = data_saida.toISOString().split('T')[0];
        $('#editar-rastreamentos-data_saida').val(data_saida_formatada)
    }
    $('#editar-error-rastreamentos-data_saida').text('')
    $('#foto0')[0].style = "display:none!important;"
    if(data.anexos.length > 0){
        $('#foto0')[0].style = "display:block;"
        let context0 = $('#canvas-foto0')[0].getContext('2d') 
        var img0 = new Image();
        img0.src = "/uploads/"+data.anexos[0].foto;
        img0.onload = function(){
            context0.drawImage(img0,0,0)
        }
   
    }
    $('#foto1')[0].style = "display:none!important;"
    if(data.anexos.length > 1){
        $('#foto1')[0].style = "display:block;"
        let context1 = $('#canvas-foto1')[0].getContext('2d') 
        var img1 = new Image();
        img1.src = "/uploads/"+data.anexos[1].foto;
        img1.onload = function(){
            context1.drawImage(img1,0,0)
        }
   
    }
    $('#foto2')[0].style = "display:none!important;"
    if(data.anexos.length > 2){
        $('#foto2')[0].style = "display:block;"
        let context2 = $('#canvas-foto2')[0].getContext('2d') 
        var img2 = new Image();
        img2.src = "/uploads/"+data.anexos[2].foto;
        img2.onload = function(){
            context2.drawImage(img2,0,0)
        }
   
    }
    $('#editar-rastreamentos-nota_fiscal').val(data.nota_fiscal)
    $('#editar-error-rastreamentos-nota_fiscal').text('')
    
    $('#editar-rastreamentos-motorista').val(data.motorista)
    $('#editar-error-rastreamentos-motorista').text('')
    
    $('#editar-rastreamentos-placa').val(data.placa)
    $('#editar-error-rastreamentos-placa').text('')
    
    $('#editar-rastreamentos-rota_insercao').val(data.rota_insercao)
    $('#editar-error-rastreamentos-rota_insercao').text('')
    
    $('#editar-rastreamentos-rota_maior_valor').val(data.rota_maior_valor)
    $('#editar-error-rastreamentos-rota_maior_valor').text('')
    
    $('#editar-rastreamentos-valor_sm').val(data.valor_sm)
    $('#editar-error-rastreamentos-valor_sm').text('')
    
    $('#editar-rastreamentos-volume').val(data.volume)
    $('#editar-error-rastreamentos-volume').text('')
    
    $('#editar-rastreamentos-manifesto').val(data.manifesto)
    $('#editar-error-rastreamentos-manifesto').text('')
    
    $('#editar-rastreamentos-sm').val(data.sm)
    $('#editar-error-rastreamentos-sm').text('')
    fechar_alerta("container_alerta_sucesso")
    fechar_alerta("container_alerta_erro")
}

function open_modal_checkin(id){
    $('#cadastrar_checkin').modal("show");
    $.ajax({
        type: 'GET',
        url: `buscar_by_Id/${id}/`,
        success: function(response) { 
            if(response.data.id){
                $('#cadastrar-checklists-checkin-numero_isca').val(response.data.isca_numero);
                $('#cadastrar-checklists-checkin-id').val(response.data.id);
            }
        },
        error: function(error) {
            console.log(error)
        }
    });

    $('#cadastrar-checklists-checkin-descricao').val('');
    $('#cadastrar-error-checklists-checkin-descricao').text('');
    $('#cadastrar-error-checklists-checkin-email').text('');
    
    $('#cadastrar-checklists-checkin-resultado').val('');
    $('#cadastrar-error-checklists-checkin-resultado').text('');
    $("#cadastrar-checklists-checkin-button_email").removeClass("disabled") 
    $('#cadastrar-error-checklists-checkin-generico')[0].style = "display:none;";
    $('#cadastrar-error-checklists-checkin-generico-text').text("");
    fechar_alerta("container_alerta_sucesso");
    fechar_alerta("container_alerta_erro");
}

function open_modal_checkout(id){
    $('#cadastrar_checkout').modal("show");

    $.ajax({
        type: 'GET',
        url: `buscar_by_Id/${id}/`,
        success: function(response) { 
            if(response.data.id){
                $('#cadastrar-checklists-checkout-numero_isca').val(response.data.isca_numero);
                $('#cadastrar-checklists-checkout-id').val(response.data.id);
            }
        },
        error: function(error) {
            console.log(error)
        }
    });

    $('#cadastrar-checklists-checkout-descricao').val('');
    $('#cadastrar-error-checklists-checkout-descricao').text('');

    $('#cadastrar-checklists-checkout-resultado').val('');
    $('#cadastrar-error-checklists-checkout-resultado').text('');
   
    $('#cadastrar-error-checklists-checkout-generico')[0].style = "display:none;";
    $('#cadastrar-error-checklists-checkout-generico-text').text("");
    fechar_alerta("container_alerta_sucesso");
    fechar_alerta("container_alerta_erro");
}
function enviar_email_checkin(etapa){
    let formData = {
        'etapa':etapa,
        'solicitacao':$('#cadastrar-checklists-checkin-id').val(),
        'csrfmiddlewaretoken':$('[name=csrfmiddlewaretoken]').val()
    }
    $.ajax({
        type: 'POST',
        url: '/checklists/email_checklist',
        data:formData,
        success: function(response) {
            if(response.sucesso != false){
                $("#cadastrar-error-checklists-checkin-email").text(response.mensagem) 
                $("#cadastrar-checklists-checkin-button_email").addClass("disabled") 
            }
        },
        error: function(error) {
            console.log(error)
        }
    }); 
}

function cadastrar_checkin(){
    let formData = {
        'descricao':$('#cadastrar-checklists-checkin-descricao').val(),
        'resultado':$('#cadastrar-checklists-checkin-resultado').val(),
        'etapa':"Checkin",
        'solicitacao':$('#cadastrar-checklists-checkin-id').val(),
        'csrfmiddlewaretoken':$('[name=csrfmiddlewaretoken]').val()
    }
    $.ajax({
        type: 'POST',
        url: '/checklists/cadastrar',
        data:formData,
        success: function(response) {
            if(response){
                $('.cadastrar-error-checklists-checkin').text("");
                $('#cadastrar-error-checklists-checkin-generico')[0].style = "display:none;";
              
                if(response.sucesso != false){
                    var modal_buscado = document.getElementById('cadastrar_checkin');
                    var modal_cadastrar_checkin = bootstrap.Modal.getInstance(modal_buscado)
                    modal_cadastrar_checkin.hide();
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
                        $('#cadastrar-error-checklists-checkin-generico')[0].style = "display:block;";
                        $('#cadastrar-error-checklists-checkin-generico-text').text(response.mensagem);
                    }
                    
                    if(response.errors){
                        for (let campos in response.errors){
                            $('#cadastrar-error-checklists-checkin-'+campos).text(response.errors[campos].join(', '));
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


function enviar_email_checkout(etapa){
    let formData = {
        'etapa':etapa,
        'solicitacao':$('#cadastrar-checklists-checkout-id').val(),
        'csrfmiddlewaretoken':$('[name=csrfmiddlewaretoken]').val()
    }
    $.ajax({
        type: 'POST',
        url: '/checklists/email_checklist',
        data:formData,
        success: function(response) {
            if(response.sucesso != false){
                $("#cadastrar-error-checklists-checkout-email").text(response.mensagem) 
                $("#cadastrar-checklists-checkout-button_email").addClass("disabled") 
            }
        },
        error: function(error) {
            console.log(error)
        }
    }); 
}

function cadastrar_checkout(){
    let formData = {
        'descricao':$('#cadastrar-checklists-checkout-descricao').val(),
        'resultado':$('#cadastrar-checklists-checkout-resultado').val(),
        'etapa':"Checkout",
        'solicitacao':$('#cadastrar-checklists-checkout-id').val(),
        'csrfmiddlewaretoken':$('[name=csrfmiddlewaretoken]').val()
    }
    $.ajax({
        type: 'POST',
        url: '/checklists/cadastrar',
        data:formData,
        success: function(response) {
            if(response){ 
                $('.cadastrar-error-checklists-checkout').text("");
                $('#cadastrar-error-checklists-checkout-generico')[0].style = "display:none;";
                
                if(response.sucesso != false){
                    var modal_buscado = document.getElementById('cadastrar_checkout');
                    var modal_cadastrar_checkout = bootstrap.Modal.getInstance(modal_buscado)
                    modal_cadastrar_checkout.hide();
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
                        $('#cadastrar-error-checklists-checkout-generico')[0].style = "display:block;";
                        $('#cadastrar-error-checklists-checkout-generico-text').text(response.mensagem);
                    }
                    
                    if(response.errors){
                        for (let campos in response.errors){
                            $('#cadastrar-error-checklists-checkout-'+campos).text(response.errors[campos].join(', '));
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

function cadastrar_rastreamentos(){
    let formFoto = new FormData()
    foto_data_implatacao.forEach((foto,index) =>{
        formFoto.append('foto'+index,foto,`foto_implantacao_${$('#cadastrar-rastreamentos-isca-id').val()}.png`)
    })
    formFoto.append('isca',$('#cadastrar-rastreamentos-isca-id').val())
    formFoto.append('data_implantacao',$('#cadastrar-rastreamentos-data_implantacao').val())
    formFoto.append('data_saida',$('#cadastrar-rastreamentos-data_saida').val())
    formFoto.append('nota_fiscal',$('#cadastrar-rastreamentos-nota_fiscal').val()) 
    formFoto.append('motorista',$('#cadastrar-rastreamentos-motorista').val())
    formFoto.append('placa',$('#cadastrar-rastreamentos-placa').val())
    formFoto.append('rota_insercao',$('#cadastrar-rastreamentos-rota_insercao').val())
    formFoto.append('rota_maior_valor',$('#cadastrar-rastreamentos-rota_maior_valor').val())
    formFoto.append('valor_sm',$('#cadastrar-rastreamentos-valor_sm').val())
    formFoto.append('volume',$('#cadastrar-rastreamentos-volume').val())
    formFoto.append('manifesto',$('#cadastrar-rastreamentos-manifesto').val())
    formFoto.append('sm',$('#cadastrar-rastreamentos-sm').val())
    formFoto.append('csrfmiddlewaretoken',$('[name=csrfmiddlewaretoken]').val())
    
    $.ajax({
        type: 'POST',
        url: '/rastreamentos/cadastrar',
        processData: false,
        contentType:false,
        data:formFoto,
        success: function(response) {
            $('.cadastrar-error-rastreamentos').text("");
            $('#cadastrar-error-rastreamentos-generico')[0].style = "display:none;";
            
            if(response.sucesso != false){
                var modal_buscado = document.getElementById('cadastrar_rastreamentos');
                var modal_cadastrar_rastreamentos = bootstrap.Modal.getInstance(modal_buscado)
                modal_cadastrar_rastreamentos.hide();
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
                    $('#cadastrar-error-rastreamentos-generico')[0].style = "display:block;";
                    $('#cadastrar-error-rastreamentos-generico-text').text(response.mensagem);
                }
                if(response.errors){
                    for (let campos in response.errors){
                        $('#cadastrar-error-rastreamentos-'+campos).text(response.errors[campos].join(', '));
                    }
                }
            }
        },  
        error: function(error) {
            console.log(error)
        }
    });  
}

function editar_rastreamentos(){
    let formData = {
        'isca':$('#editar-rastreamentos-isca-id').val(),
        'data_implantacao':$('#editar-rastreamentos-data_implantacao').val(),
        'data_saida':$('#editar-rastreamentos-data_saida').val(),
        'nota_fiscal':$('#editar-rastreamentos-nota_fiscal').val(), 
        'motorista':$('#editar-rastreamentos-motorista').val(),
        'placa':$('#editar-rastreamentos-placa').val(),
        'rota_insercao':$('#editar-rastreamentos-rota_insercao').val(),
        'rota_maior_valor':$('#editar-rastreamentos-rota_maior_valor').val(),
        'valor_sm':$('#editar-rastreamentos-valor_sm').val(),
        'volume':$('#editar-rastreamentos-volume').val(),
        'manifesto':$('#editar-rastreamentos-manifesto').val(),
        'sm':$('#editar-rastreamentos-sm').val(),
        'csrfmiddlewaretoken':$('[name=csrfmiddlewaretoken]').val()
    }
    $.ajax({
        type: 'POST',
        url: `/rastreamentos/atualizar/${$('#editar-rastreamentos-id').val()}/`,
        data:formData,
        success: function(response) {
            $('.editar-error-rastreamentos').text("");
            $('#editar-error-rastreamentos-generico')[0].style = "display:none;";
            if(response.sucesso != false){
                var modal_buscado = document.getElementById('editar_rastreamentos');
                var modal_editar_rastreamentos = bootstrap.Modal.getInstance(modal_buscado)
                modal_editar_rastreamentos.hide();
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
                    $('#editar-error-rastreamentos-generico')[0].style = "display:block;";
                    $('#editar-error-rastreamentos-generico-text').text(response.mensagem);
                }
                if(response.errors){
                    for (let campos in response.errors){
                        $('#editar-error-rastreamentos-'+campos).text(response.errors[campos].join(', '));
                    }
                }
            }
        },  
        error: function(error) {
            console.log(error)
        }
    }); 
}

function iniciar_rastreamentos(){
    let invalidos = 0;
    let campos = ['isca','data_implantacao','data_saida','nota_fiscal','motorista','placa','rota_insercao','rota_maior_valor','volume','valor_sm','manifesto','sm']
    for (let campo in campos){
        if(!$('#editar-rastreamentos-'+campos[campo]).val()){
            $('#editar-error-rastreamentos-'+campos[campo]).text('Esse campo é obrigatorio');
            invalidos++;
        }        
    }
    let formData = {
        'csrfmiddlewaretoken':$('[name=csrfmiddlewaretoken]').val()
    }
    if(invalidos == 0){
        $.ajax({
            type: 'POST',
            url: `/rastreamentos/iniciar_rastreio/${$('#editar-rastreamentos-id').val()}/`,
            data:formData,
            success: function(response) {
                $('.editar-error-rastreamentos').text("");
                $('#editar-error-rastreamentos-generico')[0].style = "display:none;";
                if(response.sucesso != false){
                    var modal_buscado = document.getElementById('editar_rastreamentos');
                    var modal_editar_rastreamentos = bootstrap.Modal.getInstance(modal_buscado)
                    modal_editar_rastreamentos.hide();
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
                        $('#editar-error-rastreamentos-generico')[0].style = "display:block;";
                        $('#editar-error-rastreamentos-generico-text').text(response.mensagem);
                    }
                }
            },  
            error: function(error) {
                console.log(error)
            }
        }); 
    }
}

function bloqueio_modal(){
    fechar_alerta("container_alerta_erro")
    $('#alerta_mensagem_erro').text("Botão desativado!");
    abrir_alerta("container_alerta_erro");
}

function recarrega_tabela(data,tipo){
    if(tipo !== 'desativo'){
        window.location.href = window.origin + "/solicitacoes/index"
        return;
    }
    const tabela_solicitacao = $(".tabela-solicitacao").DataTable();
    let nova_tabela = []
    data.forEach((data) =>{
        let class_action_checkin
        let class_action_checkout
        let color_checkin
        let color_checkout
        let color_resultado
        let modal_checkin = "bloqueio_modal()"
        let modal_checkout = "bloqueio_modal()"

        //checkin
        if(data.checkin == "Checkin Pendente"){
            color_checkin = "goldenrod !important;"
            modal_checkin = "open_modal_checkin("+data.id+")"
        }
        else if(data.checkin == "Checkin Aprovado"){
            color_checkin = "#58ca7e;"
        }
        else{
            color_checkin = "rgb(218, 44, 32)!important;"
        }

        if(data.checkin == "Checkin Pendente"){
            class_action_checkin = "checkin button-default"
        }else{
            class_action_checkin = "button-desativado"
        }

        //checkout
        if(data.checkout == "Checkout Reprovado"){
            color_checkout = "rgb(218, 44, 32)!important;"
        }
        else if(data.checkout == "Checkout Aprovado"){
            color_checkout = "#58ca7e;"
        }
        else{
            color_checkout = "goldenrod !important;"
        }

        if(data.checkout == "Checkout Pendente"){
            class_action_checkout = "checkout button-default"
            modal_checkout = "open_modal_checkout("+data.id+")"
        }else{
            class_action_checkout = "button-desativado"
        }

        if(data.resultado == "Aprovado"){
            color_resultado = "#58ca7e;"
        }else if(data.resultado == "Reprovado"){
            color_resultado = "rgb(218, 44, 32);"
        }else{
            color_resultado = "goldenrod;"
        }

        const dataAtual = new Date(data.data_criado);
        const dataFormatada = dataAtual.toLocaleDateString('pt-BR');
        let nova_linha = [
            data.ativo?"<button class='figure small pe-1'><i class='fa-solid fa-circle' style='color: rgb(32, 218, 100);#ba2525;'></i></button>"
            :"<button class='figure small pe-1'><i class='fa-solid fa-circle' style='color: #ba2525;'></i></button>",
            data.id || "N/A",
            "<button class='text-reduzido'>"+ data.isca_numero || "N/A" +"</button>",
            "<button class='figure'><i class='fa-regular fa-clipboard' style='color:"+color_checkin+"'></i></button><button class='text checkin-solicitacao'>"+ data.checkin || "N/A" +"</button>",
            "<button class='figure'><i class='fa-solid fa-clipboard' style='color:"+color_checkout+"'></i></button><button class='text checkout-solicitacao'>"+ data.checkout || "N/A" +"</button>",
            "<button class='figure small'><i class='fa-solid fa-circle' style='color:"+color_resultado+"'></i></button><button class='text'>"+data.resultado || "N/A"+"</button>",
            dataFormatada || "N/A",
            ""
        ]
        nova_tabela.push(nova_linha)
        
    });
    tabela_solicitacao.context[0].aoHeader[0][5].cell.textContent = "Resultado"
   
    if(tipo != 'desativo'){
        tabela_solicitacao.context[0].aoHeader[0][5].cell.textContent = "Implantação"
    }
   
    tabela_solicitacao.clear();
    tabela_solicitacao.rows.add(nova_tabela).draw();
}

$('#cadastrar-checklists-checkout-resultado').on('click', function (){
    if($('#cadastrar-checklists-checkout-resultado').val() === "Aprovado"){
        $(".form-cadastrar-rastreamentos").css({"display":"block"})
    }else{
        $(".form-cadastrar-rastreamentos").css({"display":"none"})
        $('#cadastrar-rastreamentos-checkout-sm').val("")
        $('#cadastrar-rastreamentos-checkout-placa').val("")
        $('#cadastrar-rastreamentos-checkout-manifesto').val("")
        $('#cadastrar-rastreamentos-checkout-nf').val("")
        $('#cadastrar-rastreamentos-checkout-valor_sm').val("")
        $('#cadastrar-rastreamentos-checkout-motorista').val("")
    }
});

$(document).ready(function (){
    const data_atual = new Date();
    const data_formatada = data_atual.toISOString().split('T')[0];
    $("#cadastrar-rastreamentos-data_saida")[0].min = data_formatada
    $("#editar-rastreamentos-data_saida")[0].min = data_formatada
    const tabela_solicitacao = $(".tabela-solicitacao").DataTable();
    tabela_solicitacao.order([[4,'desc']]);
    tabela_solicitacao.draw()
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
});


const video = document.getElementById('video-foto-implantacao');
let streaming = false
let camerastream = null

function abrir_camera(){
    const modal_foto = document.getElementById('modal-foto-implantacao');
    const erroMsg = document.getElementById('cadastrar-error-rastreamentos-foto');
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
            modal_foto.style.display = 'block';
        }).catch(function (){
            erroMsg.style.display = 'block';
        });
    }else{
        erroMsg.style.display = 'block';
    }
}

function fechar_video(){
    const modal_foto = document.getElementById('modal-foto-implantacao');
    if(camerastream){
        let tracks = camerastream.getTracks();
        tracks.forEach(track => track.stop());
        video.srcObject = null;
        streaming = false
        if(streaming == false && video.srcObject == null){
            modal_foto.style.display = 'none';
        }
    }
}

function limpa_fotos_implantacao(){
    if(foto_data_implatacao.length > 0){
        foto_data_implatacao.forEach((foto) => {
            if(foto){
                foto_data_implatacao.pop()
            }
        });
    }
}


function tirar_foto(){    
    const modal_foto = document.getElementById('cadastrar_solicitacoes_body');
    const canvas = document.createElement('canvas');
    const div = document.createElement('div');
    div.classList = "form-control col-3 my-2 d-flex justify-content-center"
    const context = canvas.getContext('2d');
    if(video && streaming){
        div.appendChild(canvas)
        modal_foto.appendChild(div)
        canvas.width = 240
        canvas.height = 260
        context.drawImage(video,0,0,canvas.width, canvas.height);
        if(canvas){
            canvas.toBlob(function (blob){
                foto_data_implatacao.push(blob)
                if(foto_data_implatacao.length > 2){
                    $("#cadastrar-rastreamentos-foto").addClass("disabled")
                }
                fechar_video()
            })
        }
    }
}

$(document).on("input", "#cadastrar-rastreamentos-valor_sm", function (e) {
    this.value = this.value.replace(/[^0-9]/g, '').replace(/(\d{1,2})$/, '.$1');
});

$(document).on("input", "#cadastrar-rastreamentos-volume", function (e) {
    this.value = this.value.replace(/[^0-9]/g, '');
});

$(document).on("input", "#cadastrar-rastreamentos-manifesto", function (e) {
    this.value = this.value.replace(/[^0-9]/g, '').replace(/(\d{1,3})$/, '.$1');
});

$(document).on("input", "#editar-rastreamentos-valor_sm", function (e) {
    this.value = this.value.replace(/[^0-9]/g, '').replace(/(\d{1,2})$/, '.$1');
});

$(document).on("input", "#editar-rastreamentos-volume", function (e) {
    this.value = this.value.replace(/[^0-9]/g, '');
});

$(document).on("input", "#editar-rastreamentos-manifesto", function (e) {
    this.value = this.value.replace(/[^0-9]/g, '').replace(/(\d{1,3})$/, '.$1');
});

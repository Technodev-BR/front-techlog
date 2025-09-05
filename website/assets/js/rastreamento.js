const tabela = document.getElementsByClassName("tabela-rastreamentos");
const linhas = tabela[0].getElementsByTagName("tbody");

let rastreamento_list = []

function rastreamento_list_id(){
    let list_id = []
    rastreamento_list.forEach((rastreio) => {
        list_id.push(rastreio.id)
    });
    return list_id
}

function removeAll_rastreios(){
    if(rastreamento_list.length > 0){
        rastreamento_list.forEach((rastreio) => {
            if(rastreio.id){
                pop_rastreios(rastreio.id)
            }
        });
    }
}

function pop_rastreios(id){
    let novo_rastreamento_list =  rastreamento_list.filter(rastreio => rastreio.id !== parseInt(id));
    rastreamento_list = novo_rastreamento_list
}

function push_rastreios(id){
    if(id){
        $.ajax({
            type: 'GET',
            url: `buscar_by_Id/${id}/`,
            success: function(response) { 
                if(response.data.id){
                    rastreamento_list.push(
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

function recarrega_tabela(data,tipo){
    const tabela_rastreio = $(".tabela-rastreamentos").DataTable();
    let nova_tabela = []
    data.forEach((data) =>{
        let color_status

        if(data.resultado == "Em viagem"){
            color_status = "rgb(32, 218, 100);"
        }
        else if(data.resultado == "Implantada"){
            color_status = "goldenrod;"
        }
        else{
            color_status = "#ba2525;"
        }
        
        const data_implantacao = new Date(data.data_implantacao);
        const data_implantacao_formatada = data_implantacao.toLocaleDateString('pt-BR');
        
        
        const data_saida = new Date(data.data_saida)
        let data_saida_formatada = null
        if(data_saida != 'Invalid Date') {
            data_saida_formatada = data_saida.toLocaleDateString('pt-BR')
        }    
        
        let nova_linha = [
            tipo == 'ativo'?"<input type='checkbox' name='checkbox-rastreamento' value="+data.id+">"
            :"<input type='checkbox' name='checkbox-rastreamento' value="+data.id+">",
            data.ativo? "<button class='figure pe-1'><i class='fa-solid fa-truck' style='color: #2caf46;'></i></button><button class='text-reduzido'>"+ (data.sm || "N/A") + "</button>"
            :"<button class='figure pe-1'><i class='fa-solid fa-truck' style='color: #ba2525;'></i></button><button class='text-reduzido'>"+ (data.sm || "N/A") + "</button>",
            data.nota_fiscal || "N/A",
            "<button class='text-reduzido'>"+(data.isca_numero || "N/A")+"</button>",
            data.rota_insercao || "N/A",
            data.rota_maior_valor || "N/A",
            "<button class='figure small pe-1 me-1'><i class='fa-solid fa-circle' style='color:" +color_status+";'></i></button><button class='text status ps-0'>"+(data.resultado || "N/A")+"</button>",
            "R$ "+(data.valor_sm || "N/A"),
            data.volume || "N/A",
            data.motorista || "N/A",
            data.placa || "N/A",
            data.manifesto || "N/A",
            data_implantacao_formatada || "N/A",
            data_saida_formatada || "N/A",
        ]
        nova_tabela.push(nova_linha)
    });
    tabela_rastreio.clear();
    tabela_rastreio.rows.add(nova_tabela).draw();
    removeAll_rastreios();
}

function verificar_rastreios_selecionados(){
    fechar_alerta("container_alerta_erro");
    fechar_alerta("container_alerta_sucesso");
    let result = true
    if(rastreamento_list.length > 0){
        rastreamento_list.forEach((rastreio) => {
            if(rastreio.ativo !== true ){
                result = false;
            }
        });
        if(result){
            modal_excluir_rastreamentos();
        }else{
            $('#alerta_mensagem_erro').text(`rastreamento já foi finalizado`);
            abrir_alerta("container_alerta_erro");
        }
    }else{
        $('#alerta_mensagem_erro').text(`Nenhum rastreio foi selecionado`);
        abrir_alerta("container_alerta_erro");
    }
}

function modal_excluir_rastreamentos(){
    $('#excluir_rastreamentos').modal("show");
    $('#excluir-error-rastreamentos-generico')[0].style = "display:none;";
    $('#excluir-error-rastreamentos-generico-text').text('');
    if(rastreamento_list.length){
        let body = document.getElementById("excluir_rastreamentos_body");
        const ul_list_rastreamentos = body.getElementsByTagName('ul')[0]
        ul_list_rastreamentos.innerHTML = ""
        rastreamento_list.forEach((rastreio) => {
            const dataAtual = new Date(rastreio.data_criado);
            const dataFormatada = dataAtual.toLocaleDateString('pt-BR');
            let div = document.createElement('div');
            div.className = "mt-2"
            div.innerHTML = `<div class='row mt-2 m-0 p-0'><div class='col-8 ps-0'> <label for="informacao">Numero da SM</label><input type='text' class='form-control' name='informacao' value='${(rastreio.sm || "N/A")} - ${dataFormatada}' readonly></div><div class='col-4 px-0'><label for="id">Codigo</label><input type='text' name='id' class='form-control' value='${rastreio.id}' readonly></div></div>` 
            ul_list_rastreamentos.appendChild(div);
        });
    }
    fechar_alerta("container_alerta_sucesso");
}

function excluir_rastreamentos(){
    let rastreamento_id = rastreamento_list_id();
    let input = document.getElementById("excluir-rastreamentos-list_id");
    input.value = rastreamento_id;
    let formData = {
        'rastreamentos_list':input.value,
        'csrfmiddlewaretoken':$('[name=csrfmiddlewaretoken]').val()
    }
    $.ajax({
        type: 'POST',
        url: 'deletar_range',
        data:formData,
        success: function(response) {
            if(response){
                $('#excluir-error-rastreamentos-generico')[0].style = "display:none;";
              
                if(response.sucesso != false){
                    var modal_buscado = document.getElementById('excluir_rastreamentos');
                    var modal_excluir_rastreamentos = bootstrap.Modal.getInstance(modal_buscado)
                    modal_excluir_rastreamentos.hide();
                    $.ajax({
                        type: 'GET',
                        url: `buscar`,
                        success: function(response) {
                            recarrega_tabela(response.data,'ativo')
                            removeAll_rastreios();
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
                        $('#excluir-error-rastreamentos-generico')[0].style = "display:block;";
                        $('#excluir-error-rastreamentos-generico-text').text(response.mensagem);
                    }
                }
            }
        },  
        error: function(error) {
            console.log(error)
        }
    });  
}

$(linhas).on('click', 'tr', function () {
    let checkbox = this.getElementsByTagName("input")[0]
    if(checkbox){
        checkbox.checked = checkbox.checked === true? false : true;
        if(this.classList[0] === "selected-linha"){
            this.classList.remove("selected-linha")
            pop_rastreios(checkbox.value)
            
        }else{
            this.classList.add("selected-linha")
            push_rastreios(checkbox.value)
        }
    }
});

$(linhas).on('click', 'input', function () {
    this.checked = this.checked === true? false : true; 
});

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
                removeAll_rastreios();
            },  
            error: function(error) {
                console.log(error)
            }
        });  
    });
    button_search.appendChild(select)
});
  
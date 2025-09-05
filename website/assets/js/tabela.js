function abrir_alerta(nome_id){
    alerta = document.getElementById(nome_id)
    alerta.classList.add("mostrar_alerta")  
    return;
}

function fechar_alerta(nome_id){
    alerta = document.getElementById(nome_id)
    alerta.classList.remove("mostrar_alerta")
    return;
}

var pageSize = 10

new DataTable('.table', {
    order: [[1, 'asc']],
    responsive: true,
    "fnDrawCallback": function() {
        
        $(".dt-search").on("keyup","input", function(){
            var tabela = $('.table').DataTable()
           
            if(tabela.page.info().length === 10){

                if(this.value && this.value != ""){
                    tabela.page.len(-1).draw();
                }
 
            }

            if(tabela.page.info().length === -1){

                if(!this.value && this.value === ""){  
                    tabela.page.len(10).draw();
                }
 
            }
            
        })
        
    },
    pageLength: pageSize,
    "lengthMenu": [[5, 10, 25, 50, 100, -1], [5, 10, 25, 50, 100, "Tudo"]],
    layout: {
        style:"width:100%",
        topEnd:null,
        topStart:null,
        top: [
            'search',
            {
                buttons: [
                {
                    extend: 'excel',
                    text: '<i class="fa-solid fa-file-csv"></i> Exportar CSV ',
                    className: 'button-base button-csv',
                    titleAttr: 'CSV',
                    exportOptions: {
                        modifier: {
                            search: 'none'
                        }
                    }
                },
                {
                    extend: 'pdf',
                    text: '<i class="fa-regular fa-file-pdf"></i> Exportar PDF ',
                    className: 'button-base button-pdf',
                    orientation : 'landscape',
                    pageSize : 'A2',
                    alignment: "center", 
                    titleAttr: 'PDF',
                    exportOptions: {
                        stripHtml: true,  
                        modifier: {
                            page: 'current'
                        }
                    },
                    customize: function(doc) {
                        doc.content[1].table.widths = Array(doc.content[1].table.body[0].length + 1).join('*').split('');
                        doc.defaultStyle.alignment = 'center';
                        doc.styles.tableHeader.alignment = 'center';
                    },
                    messageBottom: function () {
                        if(linhas[0].getElementsByTagName('td')[0].className === "dt-empty"){
                            return `\n Nenhum registro foi encontrado`;
                        }else{
                            let quantidade = linhas[0].getElementsByTagName("tr").length;
                            return `\n Total de Registros: ${quantidade}`;
                        }
                    }
                }
            ]},
            'pageLength'
        ],
    },
    language:{
        search: "",
        searchPlaceholder: "Digite para buscar...",
        "sEmptyTable": "Nenhum registro encontrado",
        "sInfo": "Mostrando _START_ / _END_ total de _TOTAL_ registros",
        "sInfoEmpty": "Mostrando 0 / 0 total de 0 registros",
        "sInfoFiltered": "(Filtrados de _MAX_ registros)",
        "sInfoPostFix": "",
        "sInfoThousands": ".",
        "sLengthMenu": "_MENU_ paginas",
        "sLoadingRecords": "Carregando...",
        "sProcessing": "Processando...",
        "sZeroRecords": "Nenhum registro encontrado",
        "thousands": ".",
        "oPaginate": {
            "sNext": ">",
            "sPrevious": "<",
            "sFirst": "<<",
            "sLast": ">>"
        },
        "oAria": {
            "sSortAscending": ": Ordenar colunas de forma ascendente",
            "sSortDescending": ": Ordenar colunas de forma descendente"
        },
        "decimal": ","
    },
});

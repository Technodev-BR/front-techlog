from .models import FornecedorModel,COMUNICACAO

def context_fornecedores(request):
    context = {}
    
    try:
        fornecedores = FornecedorModel.objects.filter(ativo=True)
        context['context_fornecedores'] = fornecedores
        context['context_comunicacoes'] = COMUNICACAO
    except Exception as ex:
        print(ex)
        
    return context

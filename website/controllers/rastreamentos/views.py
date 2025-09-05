from typing import Union
from django.db import IntegrityError
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from controllers.login.auth import administrador, administrador_or_supervisor, usuario_login_by_user_id
from controllers.login.authorized import rastreamentos_usuario
from controllers.rastreamentos.forms import RastreamentoForm
from controllers.rastreamentos.models import RastreamentoModel,RastreamentoAnexoModel
from controllers.solicitacoes.models import SolicitacoesModel
from controllers.checklists.models import ChecklistModel
from controllers.iscas.models import IscaModel
from controllers.login.send_message import alerta_inicio_viagem,alerta_fim_viagem
from threading import Thread

@login_required()
def index(request: HttpRequest) -> Union[HttpResponse, HttpResponseRedirect]:  
    context = {}  
    usuario_login = usuario_login_by_user_id(request.user.id)
    rastreamentos = rastreamentos_usuario(usuario_login,True)
    context['rastreamentos_list'] = rastreamentos
    context['titulo_page'] = "Rastreamentos"
    context['nav_rastreamento'] = True
    return render(request, "pages/rastreamento.html", context)

@login_required()
def buscar(request: HttpRequest):
    try:
        data = []
        usuario_login = usuario_login_by_user_id(request.user.id)
        rastreamentos = rastreamentos_usuario(usuario_login,True)
        for rastreamento in rastreamentos:
            newData = {
                'id':rastreamento.id,
                'sm':f'{rastreamento.sm}',
                'nota_fiscal':f'{rastreamento.nota_fiscal}',
                'manifesto':f'{rastreamento.manifesto}',
                'volume':rastreamento.volume,
                'valor_sm':rastreamento.valor_sm,
                'motorista':f'{rastreamento.motorista}',
                'rota_maior_valor':f'{rastreamento.rota_maior_valor}',
                'rota_insercao':f'{rastreamento.rota_insercao}',
                'placa':f'{rastreamento.placa}',
                'isca_id':rastreamento.isca.id,
                'isca_numero':rastreamento.isca.numero_isca,
                'resultado':f'{rastreamento.resultado}',
                'data_implantacao':f'{rastreamento.data_implantacao}',
                'data_saida':f'{rastreamento.data_saida}',
                'data_criado':f'{rastreamento.data_criado}',
                'data_alterado':f'{rastreamento.data_alterado}',
                'ativo':rastreamento.ativo
            }
            data.append(newData)
        return JsonResponse({'data': data})
    except Exception as ex:
        print(ex)
        
@login_required()
def buscar_removidos(request: HttpRequest):
    try:
        data = []
        usuario_logado = usuario_login_by_user_id(request.user.id)
        rastreamentos = rastreamentos_usuario(usuario_logado,False)
        for rastreamento in rastreamentos:
            newData = {
                'id':rastreamento.id,
                'sm':f'{rastreamento.sm}',
                'nota_fiscal':f'{rastreamento.nota_fiscal}',
                'manifesto':f'{rastreamento.manifesto}',
                'volume':rastreamento.volume,
                'valor_sm':rastreamento.valor_sm,
                'motorista':f'{rastreamento.motorista}',
                'rota_maior_valor':f'{rastreamento.rota_maior_valor}',
                'rota_insercao':f'{rastreamento.rota_insercao}',
                'placa':f'{rastreamento.placa}',
                'isca_id':rastreamento.isca.id,
                'isca_numero':rastreamento.isca.numero_isca,
                'resultado':f'{rastreamento.resultado}',
                'data_implantacao':f'{rastreamento.data_implantacao}',
                'data_saida':f'{rastreamento.data_saida}',
                'data_criado':f'{rastreamento.data_criado}',
                'data_alterado':f'{rastreamento.data_alterado}',
                'ativo':rastreamento.ativo
            }
            data.append(newData)
        return JsonResponse({'data': data})
    except Exception as ex:
        print(ex)
        
@login_required
def buscar_by_Id(request: HttpRequest, id : int):
    try:
        data = []
        usuario_login = usuario_login_by_user_id(request.user.id)
        rastreamentos = rastreamentos_usuario(usuario_login,True)
        for rastreamento in rastreamentos:
            if(id == rastreamento.id):
               
                data = {
                    'id':rastreamento.id,
                    'sm':f'{rastreamento.sm}',
                    'nota_fiscal':f'{rastreamento.nota_fiscal}',
                    'manifesto':f'{rastreamento.manifesto}',
                    'volume':rastreamento.volume,
                    'valor_sm':rastreamento.valor_sm,
                    'motorista':f'{rastreamento.motorista}',
                    'rota_maior_valor':f'{rastreamento.rota_maior_valor}',
                    'rota_insercao':f'{rastreamento.rota_insercao}',
                    'placa':f'{rastreamento.placa}',
                    'isca_id':rastreamento.isca.id,
                    'isca_numero':rastreamento.isca.numero_isca,
                    'resultado':f'{rastreamento.resultado}',
                    'data_implantacao':f'{rastreamento.data_implantacao}',
                    'data_saida':f'{rastreamento.data_saida}',
                    'data_criado':f'{rastreamento.data_criado}',
                    'data_alterado':f'{rastreamento.data_alterado}',
                    'ativo':rastreamento.ativo
                }
        return JsonResponse({'data': data})
    except Exception as ex:
        print(ex)
        
@login_required
def buscar_by_isca_Id(request: HttpRequest, id : int):
    try:
        data = []
        usuario_login = usuario_login_by_user_id(request.user.id)
        rastreamentos = rastreamentos_usuario(usuario_login,True)
        for rastreamento in rastreamentos:
            if(id == rastreamento.isca.id):
                anexos = RastreamentoAnexoModel.objects.filter(rastreamento__id=rastreamento.id)
                list_anexos = []
                for anexo in anexos:
                    new = {"foto":anexo.foto.name}
                    list_anexos.append(new)
                data = {
                    'id':rastreamento.id,
                    'sm':f'{rastreamento.sm}',
                    'nota_fiscal':f'{rastreamento.nota_fiscal}',
                    'manifesto':f'{rastreamento.manifesto}',
                    'volume':rastreamento.volume,
                    'valor_sm':rastreamento.valor_sm,
                    'motorista':f'{rastreamento.motorista}',
                    'rota_maior_valor':f'{rastreamento.rota_maior_valor}',
                    'rota_insercao':f'{rastreamento.rota_insercao}',
                    'placa':f'{rastreamento.placa}',
                    'anexos':list_anexos,
                    'isca_id':rastreamento.isca.id,
                    'isca_numero':rastreamento.isca.numero_isca,
                    'resultado':f'{rastreamento.resultado}',
                    'data_implantacao':f'{rastreamento.data_implantacao}',
                    'data_saida':f'{rastreamento.data_saida}',
                    'data_criado':f'{rastreamento.data_criado}',
                    'data_alterado':f'{rastreamento.data_alterado}',
                    'ativo':rastreamento.ativo
                }
        return JsonResponse({'data': data})
    except Exception as ex:
        print(ex)

@login_required
def cadastrar(request: HttpRequest) -> Union[HttpResponse, HttpResponseRedirect]:    
    try:    
        if(request.method == 'POST'):
            request.POST._mutable=True
            foto0 = None
            foto1 = None
            foto2 = None
            if(len(request.FILES) > 0):
                foto0 = request.FILES["foto0"]
            if(len(request.FILES) > 1):
                foto1 = request.FILES["foto1"]
            if(len(request.FILES) > 2):
                foto2 = request.FILES["foto2"]
            request.POST['resultado'] = "Implantada"
            form = RastreamentoForm(request.POST or None)
            if(form.is_valid()):
                form_new = form.save(commit=False)
                form_new.ativo = True
                resultado = form.save()
                if(foto0 != None):
                    novo = RastreamentoAnexoModel(foto=foto0,rastreamento=resultado)
                    novo.save()
                if(foto1 != None):
                    novo = RastreamentoAnexoModel(foto=foto1,rastreamento=resultado)
                    novo.save()
                if(foto2 != None):
                    novo = RastreamentoAnexoModel(foto=foto2,rastreamento=resultado)
                    novo.save()
                
                solicitacao = SolicitacoesModel.objects.get(isca__id=resultado.isca.id, ativo=True)
                solicitacao.implantacao = "Implantada"
                solicitacao.save()
                return JsonResponse({'sucesso':True, 'mensagem':"Rastreamento criado com sucesso", "id":resultado.id})
            else:
                errors = {field: [error for error in form.errors[field]] for field in form.errors}
                return JsonResponse({'sucesso':False, 'errors':errors})
            
    except Exception as ex:
        print(ex)
        
    return redirect("rastreamentos:index")

@login_required
def atualizar(request: HttpRequest, id : int) -> Union[HttpResponse, HttpResponseRedirect]:
    try:
        if(request.method == 'POST'):
            rastreamento = get_object_or_404(RastreamentoModel,id=id,ativo=True)
            form = RastreamentoForm(request.POST or None, instance=rastreamento)
            if(form.is_valid()):
                new_post = form.save(commit=False)
                new_post.ativo = True
                resultado = form.save()
                return JsonResponse({'sucesso':True, 'mensagem':"Rastreamento atualizado com sucesso", "id":resultado.id})  
            else:
                errors = {field: [error for error in form.errors[field]] for field in form.errors}
                return JsonResponse({'sucesso':False, 'errors':errors})
    
    except IntegrityError as ex:
        return JsonResponse({'sucesso':False, 'mensagem':"Rastreamento ativo já existe"})
    except Exception as ex:
        print(ex)
             
    return redirect("rastreamentos:index")

@login_required
def iniciar_rastreio(request: HttpRequest, id : int) -> Union[HttpResponse, HttpResponseRedirect]:
    try:
        if(request.method == 'POST'):
            rastreamento = get_object_or_404(RastreamentoModel,id=id,ativo=True)
            if(rastreamento and ChecklistModel.objects.filter(etapa="Checkout",resultado="Aprovado",solicitacao__isca__id=rastreamento.isca.id,solicitacao__ativo=True).exists()):
                rastreamento.ativo = True
                rastreamento.resultado = "Em viagem"
                rastreamento.save()
                
                processo = Thread(target=alerta_inicio_viagem, args=["CONTROLE DE ISCAS - INICIO VIAGEM",rastreamento,request.user.username])
                processo.start()
                
                solicitacao = SolicitacoesModel.objects.get(isca__id=rastreamento.isca.id, ativo=True)
                solicitacao.viagem = "Iniciada"
                solicitacao.save()
                
                isca = IscaModel.objects.get(id=rastreamento.isca.id,ativo=True)
                isca.status = 'Em rastreamento'
                isca.save()
                
                return JsonResponse({'sucesso':True, 'mensagem':"Rastreamento atualizado com sucesso"})  
            else:
                return JsonResponse({'sucesso':False, 'mensagem':"Solicitação com checkout pendente"})
    
    except IntegrityError as ex:
        print(ex)
    except Exception as ex:
        print(ex)
             
    return redirect("rastreamentos:index")

@login_required
def deletar_range(request: HttpRequest) -> Union[HttpResponse, HttpResponseRedirect]:
    try:
        if(request.method == 'POST'): 
           
            rastreamentos_id = request.POST.getlist('rastreamentos_list') or None
            rastreios_list_unica = rastreamentos_id[0]
            rastreios_list = rastreios_list_unica.split(",")
            
            if(len(rastreamentos_id) > 0 and rastreamentos_id[0] != ""):
                for rastreio_id in rastreios_list:
                    rastreamento = get_object_or_404(RastreamentoModel,id=int(rastreio_id),ativo=True)
                    if(rastreamento.resultado != "Implantada"):
                        processo = Thread(target=alerta_fim_viagem, args=["CONTROLE DE ISCAS - FINALIZANDO VIAGEM",rastreamento,request.user.username])
                        processo.start()
                    rastreamento.resultado = "Finalizado"
                    rastreamento.ativo = False
                    rastreamento.save()
                    
                    
                    solicitacao = get_object_or_404(SolicitacoesModel,isca_id=int(rastreamento.isca.id),ativo=True)
                    solicitacao.ativo = False
                    solicitacao.save()
                    
                    isca = get_object_or_404(IscaModel,id=solicitacao.isca.id,ativo=True)
                    if(isca.modelo != "Retornável"):
                        isca.status = "Usado"
                        isca.ativo = False
                    isca.save()
            else:
                return JsonResponse({'sucesso':False, 'mensagem':"Nenhum rastreio foi finalizado"})
            
            return JsonResponse({'sucesso':True, 'mensagem':"Rastreamentos finalizado com sucesso"})         
    except Exception as ex:
        print(ex)
       
    return redirect("rastreamentos:index") 
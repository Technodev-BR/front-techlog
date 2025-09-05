from typing import Union
from django.db import IntegrityError
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from controllers.login.auth import administrador_or_supervisor, usuario_login_by_user_id
from controllers.login.authorized import solicitacoes_usuario
from controllers.login.send_message import alerta_nova_solicitacao
from .models import SolicitacoesModel
from controllers.iscas.models import IscaModel
from threading import Thread

@login_required()
def index(request: HttpRequest) -> Union[HttpResponse, HttpResponseRedirect]:  
    context = {}  
    usuario_login = usuario_login_by_user_id(request.user.id)
    solicitacoes = solicitacoes_usuario(usuario_login,True)
    
    context['solicitacoes_list'] = solicitacoes
    context['titulo_page'] = "Solicitação Checklist"
    context['nav_solicitacao'] = True
    return render(request, "pages/solicitacao.html", context)

@login_required()
def buscar(request: HttpRequest):
    try:
        data = []
        usuario_login = usuario_login_by_user_id(request.user.id)
        solicitacoes = solicitacoes_usuario(usuario_login,True)
        for solicitacao in solicitacoes:
            newData = {
                'id':solicitacao.id,
                'checkin':f'{solicitacao.checkin}',
                'checkout':f'{solicitacao.checkout}',
                'resultado':f'{solicitacao.resultado}',
                'isca_id':solicitacao.isca.id,
                'isca_numero':f'{solicitacao.isca.numero_isca}',
                'data_criado':f'{solicitacao.data_criado}',
                'data_alterado':f'{solicitacao.data_alterado}',
                'ativo':solicitacao.ativo
            }
            data.append(newData)
        return JsonResponse({'data': data})
    except Exception as ex:
        print(ex)
        
@login_required()
def buscar_removidos(request: HttpRequest):
    try:
        data = []
        usuario_login = usuario_login_by_user_id(request.user.id)
        solicitacoes = solicitacoes_usuario(usuario_login,False)
        for solicitacao in solicitacoes:
            newData = {
                'id':solicitacao.id,
                'checkin':f'{solicitacao.checkin}',
                'checkout':f'{solicitacao.checkout}',
                'resultado':f'{solicitacao.resultado}',
                'isca_id':solicitacao.isca.id,
                'isca_numero':f'{solicitacao.isca.numero_isca}',
                'data_criado':f'{solicitacao.data_criado}',
                'data_alterado':f'{solicitacao.data_alterado}',
                'ativo':solicitacao.ativo
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
        solicitacoes = solicitacoes_usuario(usuario_login,True)
        for solicitacao in solicitacoes:
            if(id == solicitacao.id):
                data = {
                    'id':solicitacao.id,
                    'checkin':f'{solicitacao.checkin}',
                    'checkout':f'{solicitacao.checkout}',
                    'resultado':f'{solicitacao.resultado}',
                    'isca_id':solicitacao.isca.id,
                    'isca_numero':f'{solicitacao.isca.numero_isca}',
                    'data_criado':f'{solicitacao.data_criado}',
                    'data_alterado':f'{solicitacao.data_alterado}',
                    'ativo':solicitacao.ativo
                }
        return JsonResponse({'data': data})
    except Exception as ex:
        print(ex)

@login_required
def cadastrar_range(request: HttpRequest) -> Union[HttpResponse, HttpResponseRedirect]:
    try:
        if(request.method == 'POST'):            
            iscas = request.POST.getlist('isca_list') or None
            isca_list_unica = iscas[0]
            list_isca = isca_list_unica.split(",")
            
            if(len(list_isca) > 0):
                for isca_id in list_isca:    
                    new_post = SolicitacoesModel(isca=IscaModel.objects.get(id=isca_id,ativo=True))
                    new_post.isca.status = "Em checkin"
                    resultado = new_post.save()
                    
                processo = Thread(target=alerta_nova_solicitacao, args=[list_isca,request.user.username])
                processo.start()
                
                return JsonResponse({'sucesso':True, 'mensagem':"Solicitação cadastrada com sucesso", 'id':resultado.id})
            
            return JsonResponse({'sucesso':False, 'mensagem':"Não foi possivel cadastrada"})
                    
    except IntegrityError as ex:
        print(ex)
        return JsonResponse({'sucesso':False, 'mensagem':"Solicitação ativo já existe"})
    
    except Exception as ex:
        print(ex)     
        
    return redirect("solicitacoes:index") 

@login_required
def atualizar_checkin(request, id : int) -> Union[HttpResponse, HttpResponseRedirect]: 
    solicitacao = get_object_or_404(SolicitacoesModel, pk=id,ativo=True)       
    try:
        if(solicitacao.checkin):
            solicitacao.checkin = "Checkin Pendente"
            solicitacao.isca.status = "Em Checkin"
            solicitacao.save()
               
    except Exception as ex:
        print(ex)
        
    return redirect("solicitacoes:index")

@login_required
def atualizar_checkout(request, id : int) -> Union[HttpResponse, HttpResponseRedirect]: 
    solicitacao = get_object_or_404(SolicitacoesModel, pk=id,ativo=True)       
    try:
        if(solicitacao.checkout):
            solicitacao.checkout = "Checkout Pendente"
            solicitacao.isca.status = "Em Checkout"
            solicitacao.save()
               
    except Exception as ex:
        print(ex)
        
    return redirect("solicitacoes:index")

@login_required
def deletar(request: HttpRequest, id : int) -> Union[HttpResponse, HttpResponseRedirect]:
    solicitacao = get_object_or_404(SolicitacoesModel,id=id,ativo=True)
    try:
        usuario_login = usuario_login_by_user_id(request.user.id)
        if not(administrador_or_supervisor(usuario=usuario_login)):
            return redirect("solicitacoes:index")  
        
        if(solicitacao):
            solicitacao.ativo = False
            solicitacao.save()
                
    except Exception as ex:
        print(ex)

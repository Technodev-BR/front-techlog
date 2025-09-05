from typing import Union
from django.db import IntegrityError
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from controllers.login.auth import usuario_login_by_user_id
from controllers.login.authorized import checklists_usuario
from controllers.rastreamentos.models import RastreamentoModel
from controllers.login.send_message import email_checklists_aprovacao,alerta_isca_reprovada
from .models import SolicitacoesModel
from controllers.iscas.models import IscaModel
from threading import Thread
from .forms import ChecklistForm

@login_required()
def buscar(request: HttpRequest):
    try:
        data = []
        usuario_login = usuario_login_by_user_id(request.user.id)
        checklists = checklists_usuario(usuario_login)
        for checklist in checklists:
            newData = {
                'id':checklist.id,
                'etapa':f'{checklist.etapa}',
                'posicionamento':f'{checklist.posicionamento}',
                'descricao':f'{checklist.descricao}',
                'resultado':f'{checklist.resultado}',
                'usuario_responsavel':f'{checklist.usuario_responsavel}',
                'data_realizado':f'{checklist.data_realizado}',
                'data_alterado':f'{checklist.data_alterado}',
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
        checklists = checklists_usuario(usuario_login)
        for checklist in checklists:
            if(id == checklist.id):
                data = {
                   'id':checklist.id,
                    'etapa':f'{checklist.etapa}',
                    'posicionamento':f'{checklist.posicionamento}',
                    'descricao':f'{checklist.descricao}',
                    'resultado':f'{checklist.resultado}',
                    'usuario_responsavel':f'{checklist.usuario_responsavel}',
                    'data_realizado':f'{checklist.data_realizado}',
                    'data_alterado':f'{checklist.data_alterado}',
                }
        return JsonResponse({'data': data})
    except Exception as ex:
        print(ex)

@login_required
def cadastrar(request: HttpRequest) -> Union[HttpResponse, HttpResponseRedirect]:    
    try:
        if(request.method == 'POST'):
            form = ChecklistForm(request.POST or None)
            if(form.is_valid()):
                form_new = form.save(commit=False)
                form_new.usuario_responsavel = request.user.username
                resultado = form.save()
                
                isca = IscaModel.objects.get(id=resultado.solicitacao.isca.id,ativo=True)
              
                if(resultado.etapa == "Checkout" and resultado.resultado == "Reprovado" and RastreamentoModel.objects.filter(isca__id=resultado.solicitacao.isca.id,ativo=True,resultado="Implantada").exists()):
                    rastreamento = RastreamentoModel.objects.get(isca__id=resultado.solicitacao.isca.id,ativo=True,resultado="Implantada")
                    rastreamento.resultado = "Finalizada"
                    rastreamento.ativo = False
                    resultado = rastreamento.save()
                    
                if(resultado.etapa == "Checkout" and resultado.resultado == "Reprovado"):
                    processo = Thread(target=alerta_isca_reprovada, args=["CONTROLE DE ISCAS - ISCA REPROVADA CHECKOUT",isca,request.user.username])
                    processo.start()
                elif(resultado.etapa == "Checkin" and resultado.resultado == "Reprovado"):
                    processo = Thread(target=alerta_isca_reprovada, args=["CONTROLE DE ISCAS - ISCA REPROVADA CHECKIN",isca,request.user.username])
                    processo.start()
            else:
                errors = {field: [error for error in form.errors[field]] for field in form.errors}
                return JsonResponse({'sucesso':False, 'errors':errors})
            
            return JsonResponse({'sucesso':True, 'mensagem':"Checklists cadastrado com sucesso", "id":resultado.id})
         
    except IntegrityError as ex:
        print(ex)
        return JsonResponse({'sucesso':False, 'mensagem':"Checklist já existe"})
               
    except Exception as ex:
        print(ex)
             
    return redirect("solicitacoes:index")

@login_required
def email_checklist(request: HttpRequest) -> Union[HttpResponse, HttpResponseRedirect]: 
    solicitacao = get_object_or_404(SolicitacoesModel, pk=request.POST["solicitacao"],ativo=True)       
    try:
        isca = IscaModel.objects.get(id=solicitacao.isca.id,ativo=True)
        if(request.POST["etapa"] == "Checkin"):
            titulo = "CONTROLE DE ISCAS - SOLICITAÇÃO CHECKIN"
        else:
            titulo = "CONTROLE DE ISCAS - SOLICITAÇÃO CHECKOUT"
        processo = Thread(target=email_checklists_aprovacao, args=[titulo,isca,request.user.username])
        processo.start()
        return JsonResponse({'sucesso':True, 'mensagem':"Email enviado com sucesso"}) 
               
    except Exception as ex:
        print(ex)
        
    return redirect("solicitacoes:index")

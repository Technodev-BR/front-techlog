from typing import Union
from django.db import IntegrityError
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from controllers.login.auth import administrador, administrador_or_supervisor, usuario_login_by_user_id
from controllers.login.authorized import operacoes_usuario, rastreamentos_usuario
from controllers.iscas.models import IscaModel
from .models import OperacaoModel
from .forms import OperacaoForm

@login_required()
def buscar(request: HttpRequest):
    try:
        data = []
        usuario_login = usuario_login_by_user_id(request.user.id)
        operacoes = operacoes_usuario(usuario_login)
        for operacao in operacoes:
            newData = {
                'id':operacao.id,
                'nome':f'{operacao.nome}',
                'cliente_id':operacao.cliente.id,
                'data_criado':f'{operacao.data_criado}',
                'data_alterado':f'{operacao.data_alterado}',
                'ativo':operacao.ativo
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
        operacoes = operacoes_usuario(usuario_login)
        for operacao in operacoes:
            if(id == operacao.id):
                data = {
                   'id':operacao.id,
                    'nome':f'{operacao.nome}',
                    'cliente_id':operacao.cliente.id,
                    'data_criado':f'{operacao.data_criado}',
                    'data_alterado':f'{operacao.data_alterado}',
                    'ativo':operacao.ativo
                }
        return JsonResponse({'data': data})
    except Exception as ex:
        print(ex)
        

@login_required
def buscar_by_cliente_Id(request: HttpRequest, id : int):
    try:
        data = []
        usuario_login = usuario_login_by_user_id(request.user.id)
        operacoes = operacoes_usuario(usuario_login)
        for operacao in operacoes:
            if(id == operacao.cliente.id):
                newData = {
                   'id':operacao.id,
                    'nome':f'{operacao.nome}',
                    'cliente_id':operacao.cliente.id,
                    'data_criado':f'{operacao.data_criado}',
                    'data_alterado':f'{operacao.data_alterado}',
                    'ativo':operacao.ativo
                }
                data.append(newData)
        return JsonResponse({'data': data})

    except Exception as ex:
        print(ex)

@login_required
def cadastrar(request: HttpRequest) -> Union[HttpResponse, HttpResponseRedirect]:
    try:
        if request.method == "POST":
            usuario_login = usuario_login_by_user_id(request.user.id)
            if not(administrador_or_supervisor(usuario=usuario_login)):
                 return JsonResponse({'sucesso':False, 'mensagem':"Apenas administradores ou supervisores podem cadastrar"})
                        
            form = OperacaoForm(request.POST or None)     
            if(form.is_valid()):
                new_post = form.save(commit=False)
                new_post.ativo = True
                resultado = form.save()
                return JsonResponse({'sucesso':True, 'mensagem':"Operação cadastrada com sucesso", "id":resultado.id})  
            else:
                errors = {field: [error for error in form.errors[field]] for field in form.errors}
                return JsonResponse({'sucesso':False, 'errors':errors})
    except IntegrityError as ex:
        print(ex)
        return JsonResponse({'sucesso':False, 'mensagem':"Operação ativa já existe"})
    except Exception as ex:
        print(ex)
    return redirect("clientes:index")

@login_required
def atualizar(request: HttpRequest, id : int) -> Union[HttpResponse, HttpResponseRedirect]:
    try:
        if(request.method == 'POST'):
            usuario_login = usuario_login_by_user_id(request.user.id)
            if not(administrador_or_supervisor(usuario=usuario_login)):
                return JsonResponse({'sucesso':False, 'mensagem':"Apenas administradores ou supervisores podem atualizar"}) 
            
            operacao = get_object_or_404(OperacaoModel,id=id,ativo=True)
            form = OperacaoForm(request.POST or None, instance=operacao)
            if(form.is_valid()):
                new_post = form.save(commit=False)
                new_post.ativo = True
                resultado = form.save()
                return JsonResponse({'sucesso':True, 'mensagem':"Operação atualizado com sucesso", "id":resultado.id})  
            else:
                errors = {field: [error for error in form.errors[field]] for field in form.errors}
                return JsonResponse({'sucesso':False, 'errors':errors})
    except IntegrityError as ex:
        print(ex)
        return JsonResponse({'sucesso':False, 'mensagem':"Operação ativa já existe"})
    except Exception as ex:
        print(ex)
             
    return redirect("clientes:index")  

@login_required
def deletar(request: HttpRequest, id : int) -> Union[HttpResponse, HttpResponseRedirect]:
    operacao = get_object_or_404(OperacaoModel,id=id,ativo=True)
    try:
        if request.method == "POST":
            usuario_login = usuario_login_by_user_id(request.user.id)
            if not(administrador(usuario=usuario_login)):
                return JsonResponse({'sucesso':False, 'mensagem':"Apenas administradores podem excluir"}) 
            
            if(operacao and not IscaModel.objects.filter(operacao_id=operacao.id, ativo=True).exists()):
                operacao.ativo = False
                operacao.save()
            else:
                return JsonResponse({'sucesso':False, 'mensagem':"Existe Iscas ativos com essa operação"})
            
            return JsonResponse({'sucesso':True, 'mensagem':"Operação removido com sucesso"})         
    except Exception as ex:
        print(ex)
       
    return redirect("clientes:index") 
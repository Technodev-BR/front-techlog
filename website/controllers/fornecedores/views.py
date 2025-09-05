from typing import Union
from django.db import IntegrityError
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from controllers.iscas.models import IscaModel
from controllers.login.auth import administrador, administrador_or_supervisor, usuario_login_by_user_id
from .models import FornecedorModel
from .forms import FornecedorForm

@login_required()
def index(request: HttpRequest) -> Union[HttpResponse, HttpResponseRedirect]:  
    context = {}
    usuario = usuario_login_by_user_id(request.user.id)
    if not(administrador_or_supervisor(usuario=usuario)):
        return redirect("home")  
    fornecedores = FornecedorModel.objects.filter(ativo=True)
    context['fornecedores_list'] = fornecedores
    context['titulo_page'] = "Fornecedores"
    context['nav_fornecedor'] = True
    return render(request, "pages/fornecedor.html", context=context)

@login_required()
def buscar(request: HttpRequest):
    try:
        data = []
        fornecedores = FornecedorModel.objects.filter(ativo=True)
        for fornecedor in fornecedores:
            newData = {
                'id':fornecedor.id,
                'nome':f'{fornecedor.nome}',
                'email':f'{fornecedor.email}',
                'recebe_email': fornecedor.recebe_email,
                'telefone':f'{fornecedor.telefone}',
                'data_criado':f'{fornecedor.data_criado}',
                'data_alterado':f'{fornecedor.data_alterado}',
                'ativo':fornecedor.ativo
            }
            data.append(newData)
        return JsonResponse({'data': data})
    except Exception as ex:
        print(ex)

@login_required()
def buscar_removidos(request: HttpRequest):
    try:
        data = []
        fornecedores = FornecedorModel.objects.filter(ativo=False)
        for fornecedor in fornecedores:
            newData = {
                'id':fornecedor.id,
                'nome':f'{fornecedor.nome}',
                'email':f'{fornecedor.email}',
                'recebe_email': fornecedor.recebe_email,
                'telefone':f'{fornecedor.telefone}',
                'data_criado':f'{fornecedor.data_criado}',
                'data_alterado':f'{fornecedor.data_alterado}',
                'ativo':fornecedor.ativo
            }
            data.append(newData)
        return JsonResponse({'data': data})
    except Exception as ex:
        print(ex)

@login_required
def buscar_by_Id(request: HttpRequest, id : int):
    try:
        fornecedor = FornecedorModel.objects.get(id=id,ativo=True)
        data = {
            'id':fornecedor.id,
            'nome':f'{fornecedor.nome}',
            'email':f'{fornecedor.email}',
            'recebe_email': fornecedor.recebe_email,
            'telefone':f'{fornecedor.telefone}',
            'data_criado':f'{fornecedor.data_criado}',
            'data_alterado':f'{fornecedor.data_alterado}',
            'ativo':fornecedor.ativo
        }
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
              
            form = FornecedorForm(request.POST or None)     
            if(form.is_valid()):
                new_post = form.save(commit=False)
                new_post.ativo = True
                resultado = form.save()
                return JsonResponse({'sucesso':True, 'mensagem':"Fornecedor cadastrada com sucesso", "id":resultado.id})  
            else:
                errors = {field: [error for error in form.errors[field]] for field in form.errors}
                return JsonResponse({'sucesso':False, 'errors':errors})
    
    except IntegrityError as ex:
        return JsonResponse({'sucesso':False, 'mensagem':"Fornecedor ativo já existe"})
    except Exception as ex:
        print(ex)
             
    return redirect("fornecedores:index")

@login_required
def atualizar(request: HttpRequest, id : int) -> Union[HttpResponse, HttpResponseRedirect]:
    try:
        if(request.method == 'POST'):
            usuario_login = usuario_login_by_user_id(request.user.id)
            if not(administrador_or_supervisor(usuario=usuario_login)):
                return JsonResponse({'sucesso':False, 'mensagem':"Apenas administradores ou supervisores podem atualizar"})
            
            fornecedor = get_object_or_404(FornecedorModel,id=id,ativo=True)
            form = FornecedorForm(request.POST or None, instance=fornecedor)
            if(form.is_valid()):
                new_post = form.save(commit=False)
                new_post.ativo = True
                resultado = form.save()
                return JsonResponse({'sucesso':True, 'mensagem':"Fornecedor atualizado com sucesso", "id":resultado.id})  
            else:
                errors = {field: [error for error in form.errors[field]] for field in form.errors}
                return JsonResponse({'sucesso':False, 'errors':errors})
    
    except IntegrityError as ex:
        return JsonResponse({'sucesso':False, 'mensagem':"Fornecedor ativo já existe"})
    except Exception as ex:
        print(ex)
       
    return redirect("fornecedores:index")  

@login_required
def deletar(request: HttpRequest, id : int) -> Union[HttpResponse, HttpResponseRedirect]:
    fornecedor = get_object_or_404(FornecedorModel,id=id,ativo=True)
    try:
        if(request.method == 'POST'):
            usuario_login = usuario_login_by_user_id(request.user.id)
            if not(administrador(usuario=usuario_login)):
                return JsonResponse({'sucesso':False, 'mensagem':"Apenas administradores podem excluir"})
            
            if(fornecedor and not IscaModel.objects.filter(fornecedor__id=fornecedor.id, ativo=True).exists()):
                fornecedor.ativo = False
                fornecedor.save()
            else:
                return JsonResponse({'sucesso':False, 'mensagem':"Existe iscas ativas com esse fornecedor"})
                
            return JsonResponse({'sucesso':True, 'mensagem':"Fornecedor removido com sucesso"})    
    except Exception as ex:
        print(ex)
       
    return redirect("fornecedores:index") 
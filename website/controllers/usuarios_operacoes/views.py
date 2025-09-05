from typing import Union
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from controllers.login.auth import administrador, usuario_login_by_user_id,administrador_or_supervisor
from controllers.usuarios_operacoes.forms import UsuariosOperacaoForm
from controllers.usuarios_operacoes.models import UsuariosOperacaoModel

@login_required()
def buscar(request: HttpRequest):
    try:
        data = []
        usuarios_operacoes = UsuariosOperacaoModel.objects.filter(ativo=True)
        for usuario_operacao in usuarios_operacoes:
            newData = {
                'id':usuario_operacao.id,
                'usuario_id':usuario_operacao.usuario.id,
                'operacao_id':usuario_operacao.operacao.id,
                'data_criado':f'{usuario_operacao.data_criado}',
                'data_alterado':f'{usuario_operacao.data_alterado}',
                'ativo':usuario_operacao.ativo
            }
            data.append(newData)
        print(data)
        return JsonResponse({'data': data})

    except Exception as ex:
        print(ex)

@login_required
def buscar_by_Id(request: HttpRequest,id):
    try:
        usuario_operacao = UsuariosOperacaoModel.objects.get(id=id,ativo=True)
        data = {
            'id':usuario_operacao.id,
            'usuario_id':usuario_operacao.usuario.id,
            'operacao_id':usuario_operacao.operacao.id,
            'data_criado':f'{usuario_operacao.data_criado}',
            'data_alterado':f'{usuario_operacao.data_alterado}',
            'ativo':usuario_operacao.ativo
        }
        print(data)
        return JsonResponse({'data': data})
    
    except Exception as ex:
        print(ex)

@login_required
def cadastrar(request: HttpRequest) -> Union[HttpResponse, HttpResponseRedirect]:
    try:
        context = {} 
    
        if request.method == "POST":
            usuario = usuario_login_by_user_id(request.user.id)
            if not(administrador_or_supervisor(usuario=usuario)):
                return redirect('usuarios:index')  
            
            form = UsuariosOperacaoForm(request.POST or None)     
            if(form.is_valid()):
                resultado = form.save()
                print(resultado)
                
                form = UsuariosOperacaoModel()
                context['form'] = form
                return render(request, "pages/usuario.html", context=context)  
                
            context['form'] = form
            return render(request, "cadastrar/cadastrar_usuario_operacao.html", context=context)  
    
    except Exception as ex:
        print(ex)
             
    return redirect('usuarios:index')

@login_required
def atualizar(request: HttpRequest,id) -> Union[HttpResponse, HttpResponseRedirect]:
    usuario_operacao = get_object_or_404(UsuariosOperacaoModel,id=id,ativo=True)
    try:
        context = {} 
        
        if(request.method == 'POST'):
            usuario_login = usuario_login_by_user_id(request.user.id)
            if not(administrador_or_supervisor(usuario=usuario_login)):
                return redirect("solicitacoes:index")  
        
            form = UsuariosOperacaoModel(request.POST or None, instance=usuario_operacao)
            if(form.is_valid()):
                form.data_alterado = timezone.now()
                resultado = form.save()
                print(resultado)
                form = UsuariosOperacaoModel()
                context['form'] = form
                return render(request, "pages/usuario.html", context=context)  
            
            context['form'] = form
            return render(request, "editar/editar_usuario_operacao.html", context=context)  
    except Exception as ex:
        print(ex)
       
    return redirect('usuarios:index')

@login_required
def deletar(request: HttpRequest,id) -> Union[HttpResponse, HttpResponseRedirect]:
    usuario_operacao = get_object_or_404(UsuariosOperacaoModel,id=id,ativo=True)
    try:
        usuario_login = usuario_login_by_user_id(request.user.id)
        if not(administrador(usuario=usuario_login)):
            return redirect("solicitacoes:index")  
        
        if(usuario_operacao):
            usuario_operacao.ativo = False
            usuario_operacao.data_alterado = timezone.now()
            usuario_operacao.save()
                
    except Exception as ex:
        print(ex)
       
    return redirect('usuarios:index')

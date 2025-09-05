from typing import Union
from django.db import IntegrityError
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from controllers.login.auth import administrador, usuario_login_by_user_id,administrador_or_supervisor
from .models import UsuarioModel
from .forms import UsuarioForm

@login_required()
def index(request: HttpRequest) -> Union[HttpResponse, HttpResponseRedirect]:  
    context = {}
    
    usuario = usuario_login_by_user_id(request.user.id)
    if not(administrador_or_supervisor(usuario=usuario)):
        return redirect("home")  
    
    usuarios = UsuarioModel.objects.filter(ativo=True)
    context['usuarios_list'] = usuarios
    context['titulo_page'] = "Usuarios"
    context['nav_usuario'] = True
    
    return render(request, "pages/usuario.html", context=context)

@login_required()
def buscar(request: HttpRequest):
    try:
        data = []
        
        usuarios = UsuarioModel.objects.filter(ativo=True)
        for usuario in usuarios:
            newData = {
                'id':usuario.id,
                'user_id':request.user.id,
                'nome':f'{usuario.user.username}',
                'email':f'{usuario.email}',
                'roles':f'{usuario.roles}',
                'data_criado':f'{usuario.data_criado}',
                'data_alterado':f'{usuario.data_alterado}',
                'ativo':usuario.ativo
            }
            data.append(newData)
            
        print(data)
        return JsonResponse({'data': data})

    except Exception as ex:
        print(ex)

@login_required
def buscar_by_Id(request: HttpRequest, id : int):
    try:
        usuario = UsuarioModel.objects.get(id=id,ativo=True)
        data = {
            'id':usuario.id,
            'user_id':request.user.id,
            'nome':f'{usuario.user.username}',
            'email':f'{usuario.email}',
            'roles':f'{usuario.roles}',
            'data_criado':f'{usuario.data_criado}',
            'data_alterado':f'{usuario.data_alterado}',
            'ativo':usuario.ativo
        }
        print(data)
        return JsonResponse({'data': data})
    
    except Exception as ex:
        print(ex)

@login_required
def cadastrar(request: HttpRequest):
    try:
        if request.method == "POST":
            usuario_login = usuario_login_by_user_id(request.user.id)
            
            if not(administrador_or_supervisor(usuario=usuario_login)):
                return JsonResponse({'sucesso':False, 'mensagem':"Apenas administradores ou supervisores podem cadastrar"})
            
            form = UsuarioForm(request.POST or None)     
            if(form.is_valid()):
                usuarioForm = form.save(commit=False)
                usuarioForm.ativo = True
                form.save()
            else:
                errors = {field: [error for error in form.errors[field]] for field in form.errors}
                return JsonResponse({'sucesso':False, 'errors':errors})
            return render(request, "pages/usuario.html")
        
    except IntegrityError as ex:
        print(ex)
        return JsonResponse({'sucesso':False, 'error':"Usuario ativo já existe"})
    except Exception as ex:
        print(ex)
        
    return redirect("usuarios:index") 

@login_required
def atualizar(request: HttpRequest, id : int) -> Union[HttpResponse, HttpResponseRedirect]:
    usuario = get_object_or_404(UsuarioModel,id=id,ativo=True)
    try:
        context = {} 
        
        if(request.method == 'POST'):
            usuario_login = usuario_login_by_user_id(request.user.id)
            if not(administrador_or_supervisor(usuario=usuario_login)):
                return JsonResponse({'sucesso':False, 'mensagem':"Apenas administradores ou supervisores podem atualizar"})
            
            form = UsuarioForm(request.POST or None, instance=usuario)
            if(form.is_valid()):
                resultado = form.save()
                print(resultado)
                form = UsuarioForm()
                context['form'] = form
                return render(request, "pages/usuario.html", context=context)  
            
            context['form'] = form
            return render(request, "editar/editar_usuario.html", context=context) 
        
    except Exception as ex:
        print(ex)
    form = UsuarioForm()
    context['form'] = form
    return render(request, "editar/editar_usuario.html", context=context) 

@login_required
def deletar(request: HttpRequest, id : int) -> Union[HttpResponse, HttpResponseRedirect]:
    usuario = get_object_or_404(UsuarioModel,id=id,ativo=True)
    try:
        usuario_login = usuario_login_by_user_id(request.user.id)
        if not(administrador(usuario=usuario_login)):
            return JsonResponse({'sucesso':False, 'mensagem':"Apenas administradores podem excluir"})
        
        if(usuario):
            usuario.ativo = False
            usuario.save()
                
    except Exception as ex:
        print(ex)
       
    return redirect("usuarios:index") 
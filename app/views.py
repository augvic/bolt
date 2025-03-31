# ================================================== #

# ~~ Imports.
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
import getpass

# ================================================== #

# ~~ Database list view.
def database(request):
    matricula = getpass.getuser()
    tabelas_permitidas = DatabaseAuth.objects.filter(usuario=matricula).values_list("tabela", flat=True)
    return render(request, "database/database.html", {"tabelas_permitidas": tabelas_permitidas})

# ================================================== #

# ~~ Database Comercial view.
def database_comercial(request):

    # ~~ Coleta usuário do sistema e coleta todas as tabelas que ele tem acesso.
    matricula = getpass.getuser()
    tabelas_permitidas = DatabaseAuth.objects.filter(usuario=matricula).values_list("tabela", flat=True)

    # ~~ Verifica se usuário tem acesso à tabela comercial.
    if "comercial" in tabelas_permitidas:
        assistentes = Comercial.objects.all()
        return render(request, "database/database_comercial.html", {"assistentes": assistentes})
    
    # ~~ Se não tiver, redireciona para a raiz database.
    else:
        return redirect("database")

# ================================================== #

# ~~ Database Comercial inserir view.
def database_comercial_inserir(request):

    # ~~ Coleta usuário do sistema e coleta todas as tabelas que ele tem acesso.
    matricula = getpass.getuser()
    tabelas_permitidas = DatabaseAuth.objects.filter(usuario=matricula).values_list("tabela", flat=True)

    # ~~ Verifica se usuário tem acesso à tabela comercial.
    if "comercial" in tabelas_permitidas:
        if request.method == "POST":
            assistente = request.POST
            assistente = Comercial(
                nome=assistente.get("nome"),
                escritorio=assistente.get("escritorio"),
                codigo_zage=assistente.get("codigo_zage"),
                codigo_assistente=assistente.get("codigo_assistente"),
                codigo_fornecedor=assistente.get("codigo_fornecedor"),
                email=assistente.get("email"),
                superior=assistente.get("superior")
            )
            assistente.save()
            return redirect("database_comercial")
        else:
            return redirect("database_comercial")

    # ~~ Se não tiver, redireciona para a raiz database.
    else:
        return redirect("database")

# ================================================== #

# ~~ Database Comercial delete view.
def database_comercial_delete(request, assistente_id):

    # ~~ Coleta usuário do sistema e coleta todas as tabelas que ele tem acesso.
    matricula = getpass.getuser()
    tabelas_permitidas = DatabaseAuth.objects.filter(usuario=matricula).values_list("tabela", flat=True)

    # ~~ Verifica se usuário tem acesso à tabela comercial.
    if "comercial" in tabelas_permitidas:
        assistente = get_object_or_404(Comercial, id=assistente_id)
        assistente.delete()
        return redirect("database_comercial")

    # ~~ Se não tiver, redireciona para a raiz database.
    else:
        return redirect("database")

# ================================================== #

# ~~ Database Comercial edit view.
def database_comercial_edit(request, assistente_id):

    # ~~ Coleta usuário do sistema e coleta todas as tabelas que ele tem acesso.
    matricula = getpass.getuser()
    tabelas_permitidas = DatabaseAuth.objects.filter(usuario=matricula).values_list("tabela", flat=True)

    # ~~ Verifica se usuário tem acesso à tabela comercial.
    if "comercial" in tabelas_permitidas:
        if request.method == "POST":
            novos_dados = request.POST
            assistente = get_object_or_404(Comercial, id=assistente_id)
            assistente.nome = novos_dados.get("nome")
            assistente.escritorio = novos_dados.get("escritorio")
            assistente.codigo_zage = novos_dados.get("codigo_zage")
            assistente.codigo_assistente = novos_dados.get("codigo_assistente")
            assistente.codigo_fornecedor = novos_dados.get("codigo_fornecedor")
            assistente.email = novos_dados.get("email")
            assistente.superior = novos_dados.get("superior")
            assistente.save()
            return redirect("database_comercial")
        else:
            return redirect("database_comercial")

    # ~~ Se não tiver, redireciona para a raiz database.
    else:
        return redirect("database")

# ================================================== #

# ~~ Financeiro view.
def financeiro(request):
    return render(request, "financeiro/financeiro.html")

# ================================================== #

# ~~ Inicio view.
def inicio(request):
    return render(request, "inicio/inicio.html")

# ================================================== #
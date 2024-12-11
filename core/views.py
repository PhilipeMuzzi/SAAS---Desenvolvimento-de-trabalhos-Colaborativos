from django.contrib.auth import authenticate, login
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .forms import RegisterForm, ProjetoForm, AnotacaoForm, IdeiaForm, TarefaForm
from .models import Projeto, Convite, Tarefa, Anotacao, Ideia
from django.contrib.auth.models import User
from django.http import JsonResponse


# ------------------------------------- /registration/ ------------------------------------------
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Credenciais inválidas. Tente novamente.')
            return redirect('user_login')

    return render(request, 'registration/login.html')
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            login(request, user)

            return redirect('index')
    else:
        form = RegisterForm()

    return render(request, 'registration/registro.html', {'form': form})

@login_required
def index(request):
    projetos = Projeto.objects.all()
    return render(request, 'index.html', {'projetos': projetos})


# --------------------------------------------------------------------------------------

def detalhes_projeto(request, projeto_id):
    projeto = get_object_or_404(Projeto, id=projeto_id)
    ideias = Ideia.objects.filter(projeto=projeto)
    tarefas = Tarefa.objects.filter(projeto=projeto)
    anotacoes = Anotacao.objects.filter(projeto=projeto)

    print(f"Projeto: {projeto}")
    print(f"Ideias: {ideias}")
    print(f"Tarefas: {tarefas}")
    print(f"Anotações: {anotacoes}")

    return render(request, 'detalhes_projeto.html', {
        'projeto': projeto,
        'ideias': ideias,
        'tarefas': tarefas,
        'anotacoes': anotacoes
    })

@login_required
def criar_projeto(request):
    if request.method == 'POST':
        form = ProjetoForm(request.POST)
        if form.is_valid():
            projeto = form.save(commit=False)
            projeto.responsavel = request.user
            projeto.save()
            return redirect('index')
    else:
        form = ProjetoForm()

    return render(request, 'criar_projeto.html', {'form': form})

@login_required
def adicionar_tarefa(request, projeto_id):
    projeto = Projeto.objects.get(id=projeto_id)

    if request.method == 'POST':
        form = TarefaForm(request.POST)
        if form.is_valid():
            tarefa = form.save(commit=False)
            tarefa.projeto = projeto
            tarefa.criado_por = request.user
            tarefa.save()
            return redirect('detalhes_projeto', projeto_id=projeto.id)
    else:
        form = TarefaForm()

    return render(request, 'adicionar_tarefa.html', {'form': form, 'projeto': projeto})

def adicionar_nota(request, projeto_id):
    projeto = Projeto.objects.get(id=projeto_id)

    if request.method == 'POST':
        form = AnotacaoForm(request.POST)
        if form.is_valid():
            nota = form.save(commit=False)
            nota.projeto = projeto
            nota.criado_por = request.user
            nota.save()
            return redirect('detalhes_projeto', projeto_id=projeto.id)
    else:
        form = AnotacaoForm()

    return render(request, 'adicionar_nota.html', {'form': form, 'projeto': projeto})

def adicionar_ideia(request, projeto_id):
    projeto = Projeto.objects.get(id=projeto_id)

    if request.method == 'POST':
        form = IdeiaForm(request.POST)
        if form.is_valid():
            ideia = form.save(commit=False)
            ideia.projeto = projeto
            ideia.sugerido_por = request.user
            ideia.save()
            return redirect('detalhes_projeto', projeto_id=projeto.id)
    else:
        form = IdeiaForm()

    return render(request, 'adicionar_ideia.html', {'form': form, 'projeto': projeto})


def enviar_convite(request, projeto_id, usuario_id):
    projeto = get_object_or_404(Projeto, id=projeto_id, criado_por=request.user)
    usuario_convidado = get_object_or_404(User, id=usuario_id)

    if Convite.objects.filter(projeto=projeto, usuario_convidado=usuario_convidado, status='pendente').exists():
        messages.error(request, "Convite já enviado!")
        return redirect('detalhes_projeto', projeto_id=projeto.id)

    Convite.objects.create(projeto=projeto, usuario_convidado=usuario_convidado)
    messages.success(request, f"Convite enviado para {usuario_convidado.username}!")
    return redirect('detalhes_projeto', projeto_id=projeto.id)

def notificacoes(request):
    convites = Convite.objects.filter(convidado=request.user, status='pendente')
    return render(request, 'notificacoes.html', {'convites': convites})

def aceitar_convite(request, convite_id):
    convite = get_object_or_404(Convite, id=convite_id, usuario_convidado=request.user)
    convite.status = 'aceito'
    convite.save()
    convite.projeto.membros.add(request.user)
    return JsonResponse({'mensagem': 'Convite aceito com sucesso!'})


def recusar_convite(request, convite_id):
    convite = get_object_or_404(Convite, id=convite_id, usuario_convidado=request.user)
    convite.status = 'recusado'
    convite.save()
    return JsonResponse({'mensagem': 'Convite recusado com sucesso!'})


@login_required
def excluir_projeto(request, projeto_id):
    projeto = get_object_or_404(Projeto, id=projeto_id)

    if projeto.responsavel == request.user:
        projeto.delete()
        return redirect('index')
    else:

        return redirect('acesso_negado')



#------------------------------------/DadosProjetos/-------------------------------------------------------------

def relatorios(request, projeto_id):
    tarefas = Tarefa.objects.filter(projeto_id=projeto_id)
    tarefas_concluidas = tarefas.filter(status='concluída').count()
    tarefas_pendentes = tarefas.filter(status='pendente').count()

    context = {
        'tarefas_concluidas': tarefas_concluidas,
        'tarefas_pendentes': tarefas_pendentes,
        'labels': ['Concluídas', 'Pendentes'],
        'data': [tarefas_concluidas, tarefas_pendentes],
    }
    return render(request, 'DadosProjetos/relatorios.html', context)


@login_required
def anotacoes_projeto(request, projeto_id):
    projeto = get_object_or_404(Projeto, id=projeto_id, usuario=request.user)
    tarefas = Tarefa.objects.filter(projeto=projeto)
    return render(request, 'DadosProjetos/anotacoes.html', {'projeto': projeto, 'tarefas': tarefas})

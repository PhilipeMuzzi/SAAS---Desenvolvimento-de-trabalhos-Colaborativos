from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Projeto(models.Model):
    PENDENTE = 'pendente'
    EM_EXECUCAO = 'em execução'
    CONCLUIDO = 'concluído'

    STATUS_CHOICES = [
        (PENDENTE, 'Pendente'),
        (EM_EXECUCAO, 'Em execução'),
        (CONCLUIDO, 'Concluído'),
    ]

    nome = models.CharField(max_length=200)
    descricao = models.TextField()
    data_criacao = models.DateTimeField(default=timezone.now)
    responsavel = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDENTE)
    data_inicio = models.DateTimeField(default=timezone.now)
    data_termino = models.DateTimeField(null=True)

    def __str__(self):
        return self.nome

class Ideia(models.Model):
    conteudo = models.TextField()
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE)
    sugerido_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Ideia de {self.sugerido_por.username} no projeto {self.projeto.nome}'

class Tarefa(models.Model):
    nome = models.CharField(max_length=100)
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE)
    concluida = models.BooleanField(default=False)

class Anotacao(models.Model):
    conteudo = models.TextField()
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, related_name="anotacoes")
    criado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Anotação de {self.criado_por.username} no projeto {self.projeto.nome}'

class Convite(models.Model):
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE)
    convidado = models.ForeignKey(User, on_delete=models.CASCADE, related_name='convites_recebidos', null=True)
    enviado_por = models.ForeignKey(User, on_delete=models.CASCADE, related_name='convites_enviados', null=True)
    status = models.CharField(max_length=10, choices=[('pendente', 'Pendente'), ('aceito', 'Aceito'), ('recusado', 'Recusado')], default='pendente')

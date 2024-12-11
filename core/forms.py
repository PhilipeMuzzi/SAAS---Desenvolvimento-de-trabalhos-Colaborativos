from django.contrib.auth.models import User
from django import forms
from core.models import Projeto, Ideia, Anotacao, Tarefa



#registro dos usuarios no sistema

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("As senhas não coincidem.")
        return cleaned_data


# form do projeto...
class ProjetoForm(forms.ModelForm):
    class Meta:
        model = Projeto
        fields = ['nome', 'descricao', 'data_inicio', 'data_termino', 'status']

    data_inicio = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    data_termino = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    status = forms.ChoiceField(choices=Projeto.STATUS_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))


# form para adicionar  tarefa
class TarefaForm(forms.ModelForm):
    class Meta:
        model = Tarefa
        fields = ['nome', 'concluida']



# form para adicionar nota
class AnotacaoForm(forms.ModelForm):
    class Meta:
        model = Anotacao
        fields = ['conteudo']


# para adicionar ideia no projeto
class IdeiaForm(forms.ModelForm):
    class Meta:
        model = Ideia
        fields = ['conteudo']

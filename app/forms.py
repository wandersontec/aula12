from django import forms
from .models import PlanoAlimentar, ProgramaTreino


class BootstrapModelForm(forms.ModelForm):
    """Aplica classes do Bootstrap a todos os campos."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for campo in self.fields.values():
            campo.widget.attrs['class'] = 'form-select' if isinstance(campo.widget, forms.Select) else 'form-control'


class ProgramaTreinoForm(BootstrapModelForm):
    class Meta:
        model = ProgramaTreino
        fields = ['nome', 'objetivo', 'nivel', 'duracao_semanas', 'descricao', 'imagem', 'plano_sugerido']


class PlanoAlimentarForm(BootstrapModelForm):
    class Meta:
        model = PlanoAlimentar
        fields = ['nome', 'objetivo', 'calorias_dia', 'descricao', 'imagem']

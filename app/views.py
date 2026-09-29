from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import PlanoAlimentarForm, ProgramaTreinoForm
from .models import PlanoAlimentar, ProgramaTreino


def home_view(request):
    context = {
        'programas': ProgramaTreino.objects.order_by('-criado_em')[:3],
        'planos': PlanoAlimentar.objects.order_by('-criado_em')[:3],
    }
    return render(request, 'home.html', context)


# ---------- helpers (evitam repetir Create/Update/Delete para cada model) ----------
def _salvar(request, form_class, instancia, prefixo, titulo):
    form = form_class(request.POST or None, instance=instancia)
    if form.is_valid():
        obj = form.save()
        return redirect(f'{prefixo}_detalhe', id=obj.id)
    voltar = reverse(f'{prefixo}_detalhe', args=[instancia.id]) if instancia else reverse(f'{prefixo}s')
    return render(request, 'form.html', {'form': form, 'titulo': titulo, 'voltar': voltar})


def _excluir(request, obj, prefixo):
    if request.method == 'POST':  # exclusão só com intenção clara (POST)
        obj.delete()
        return redirect(f'{prefixo}s')
    voltar = reverse(f'{prefixo}_detalhe', args=[obj.id])
    return render(request, 'confirmar_exclusao.html', {'objeto': obj, 'voltar': voltar})


# ---------- Programas de treino ----------
def programas_view(request):
    programas = ProgramaTreino.objects.all()
    return render(request, 'programas.html', {'programas': programas})


def programa_detalhe_view(request, id):
    qs = ProgramaTreino.objects.select_related('plano_sugerido').prefetch_related('itens')
    return render(request, 'programa_detalhe.html', {'programa': get_object_or_404(qs, id=id)})


@login_required
def programa_criar_view(request):
    return _salvar(request, ProgramaTreinoForm, None, 'programa', 'Novo programa de treino')


@login_required
def programa_editar_view(request, id):
    programa = get_object_or_404(ProgramaTreino, id=id)
    return _salvar(request, ProgramaTreinoForm, programa, 'programa', f'Editar: {programa.nome}')


@login_required
def programa_excluir_view(request, id):
    return _excluir(request, get_object_or_404(ProgramaTreino, id=id), 'programa')


# ---------- Planos alimentares ----------
def planos_view(request):
    return render(request, 'planos.html', {'planos': PlanoAlimentar.objects.all()})


def plano_detalhe_view(request, id):
    qs = PlanoAlimentar.objects.prefetch_related('refeicoes', 'programas')
    return render(request, 'plano_detalhe.html', {'plano': get_object_or_404(qs, id=id)})


@login_required
def plano_criar_view(request):
    return _salvar(request, PlanoAlimentarForm, None, 'plano', 'Novo plano alimentar')


@login_required
def plano_editar_view(request, id):
    plano = get_object_or_404(PlanoAlimentar, id=id)
    return _salvar(request, PlanoAlimentarForm, plano, 'plano', f'Editar: {plano.nome}')


@login_required
def plano_excluir_view(request, id):
    return _excluir(request, get_object_or_404(PlanoAlimentar, id=id), 'plano')


# ---------- Conta ----------
@login_required
def perfil_view(request):
    return render(request, 'perfil.html')


def cadastro_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        login(request, form.save())
        return redirect('home')
    return render(request, 'cadastro.html', {'form': form})

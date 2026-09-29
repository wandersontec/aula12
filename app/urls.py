from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),

    path('programas/', views.programas_view, name='programas'),
    path('programas/novo/', views.programa_criar_view, name='programa_criar'),
    path('programas/<int:id>/', views.programa_detalhe_view, name='programa_detalhe'),
    path('programas/<int:id>/editar/', views.programa_editar_view, name='programa_editar'),
    path('programas/<int:id>/excluir/', views.programa_excluir_view, name='programa_excluir'),

    path('planos/', views.planos_view, name='planos'),
    path('planos/novo/', views.plano_criar_view, name='plano_criar'),
    path('planos/<int:id>/', views.plano_detalhe_view, name='plano_detalhe'),
    path('planos/<int:id>/editar/', views.plano_editar_view, name='plano_editar'),
    path('planos/<int:id>/excluir/', views.plano_excluir_view, name='plano_excluir'),

    path('perfil/', views.perfil_view, name='perfil'),
    path('cadastro/', views.cadastro_view, name='cadastro'),
]

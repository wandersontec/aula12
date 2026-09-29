from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import PlanoAlimentar, ProgramaTreino

DADOS_PROGRAMA = {'nome': 'Novo', 'objetivo': 'forca', 'nivel': 'iniciante', 'duracao_semanas': 4,
                  'descricao': '', 'imagem': '', 'plano_sugerido': ''}


class BaseTest(TestCase):
    def setUp(self):
        self.plano = PlanoAlimentar.objects.create(nome='Plano', objetivo='hipertrofia', calorias_dia=2500)
        self.programa = ProgramaTreino.objects.create(nome='Prog', objetivo='forca', nivel='avancado',
                                                      plano_sugerido=self.plano)
        self.user = User.objects.create_user('ana', password='senha-forte-123')


class LeituraPublicaTest(BaseTest):
    def test_paginas_publicas(self):
        for nome, args in [('home', []), ('programas', []), ('planos', []), ('cadastro', []), ('login', []),
                           ('programa_detalhe', [self.programa.id]), ('plano_detalhe', [self.plano.id])]:
            self.assertEqual(self.client.get(reverse(nome, args=args)).status_code, 200, nome)

    def test_detalhe_inexistente_404(self):
        self.assertEqual(self.client.get(reverse('programa_detalhe', args=[999])).status_code, 404)

    def test_botoes_ocultos_para_anonimo(self):
        r = self.client.get(reverse('programa_detalhe', args=[self.programa.id]))
        self.assertNotContains(r, reverse('programa_editar', args=[self.programa.id]))
        self.assertNotContains(r, reverse('programa_excluir', args=[self.programa.id]))

    def test_botoes_visiveis_para_logado(self):
        self.client.force_login(self.user)
        r = self.client.get(reverse('programa_detalhe', args=[self.programa.id]))
        self.assertContains(r, reverse('programa_editar', args=[self.programa.id]))


class ProtecaoTest(BaseTest):
    def test_views_de_acao_exigem_login(self):
        urls = [reverse('programa_criar'), reverse('plano_criar'), reverse('perfil'),
                reverse('programa_editar', args=[self.programa.id]),
                reverse('programa_excluir', args=[self.programa.id]),
                reverse('plano_editar', args=[self.plano.id]),
                reverse('plano_excluir', args=[self.plano.id])]
        for url in urls:
            for metodo in (self.client.get, self.client.post):
                r = metodo(url)
                self.assertEqual(r.status_code, 302, url)
                self.assertTrue(r.url.startswith('/accounts/login/'), url)

    def test_anonimo_nao_cria_nem_exclui(self):
        self.client.post(reverse('programa_criar'), DADOS_PROGRAMA)
        self.client.post(reverse('programa_excluir', args=[self.programa.id]))
        self.assertEqual(ProgramaTreino.objects.count(), 1)


class CrudTest(BaseTest):
    def setUp(self):
        super().setUp()
        self.client.force_login(self.user)

    def test_criar(self):
        r = self.client.post(reverse('programa_criar'), DADOS_PROGRAMA)
        novo = ProgramaTreino.objects.get(nome='Novo')
        self.assertRedirects(r, reverse('programa_detalhe', args=[novo.id]))

    def test_editar(self):
        self.client.post(reverse('programa_editar', args=[self.programa.id]), {**DADOS_PROGRAMA, 'nome': 'Editado'})
        self.programa.refresh_from_db()
        self.assertEqual(self.programa.nome, 'Editado')

    def test_excluir_get_nao_apaga_e_post_apaga(self):
        url = reverse('programa_excluir', args=[self.programa.id])
        self.assertEqual(self.client.get(url).status_code, 200)
        self.assertEqual(ProgramaTreino.objects.count(), 1)
        self.assertRedirects(self.client.post(url), reverse('programas'))
        self.assertEqual(ProgramaTreino.objects.count(), 0)

    def test_form_invalido_mostra_erros(self):
        r = self.client.post(reverse('plano_criar'), {'nome': ''})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(PlanoAlimentar.objects.count(), 1)

    def test_logout_via_post(self):
        self.client.post(reverse('logout'))
        self.assertEqual(self.client.get(reverse('perfil')).status_code, 302)


class CadastroTest(TestCase):
    def test_cadastro_loga_o_usuario(self):
        r = self.client.post(reverse('cadastro'), {'username': 'novo', 'password1': 'Senha-forte-987', 'password2': 'Senha-forte-987'})
        self.assertRedirects(r, reverse('home'))
        self.assertTrue(User.objects.filter(username='novo').exists())

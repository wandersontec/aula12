from django.db import models
from django.db.models import Sum
from django.templatetags.static import static

# tipo string -> CharField(max_length=*) | inteiro -> PositiveIntegerField()
# texto longo -> TextField() | relação -> ForeignKey()


class Objetivo(models.TextChoices):
    HIPERTROFIA = 'hipertrofia', 'Hipertrofia'
    EMAGRECIMENTO = 'emagrecimento', 'Emagrecimento'
    FORCA = 'forca', 'Força'
    CONDICIONAMENTO = 'condicionamento', 'Condicionamento'


class ImagemMixin(models.Model):
    imagem = models.CharField(max_length=500, blank=True, default='')  # URL ou caminho em static/

    class Meta:
        abstract = True

    @property
    def imagem_url(self):
        if not self.imagem:
            return ''
        return self.imagem if self.imagem.startswith(('http://', 'https://')) else static(self.imagem)


class PlanoAlimentar(ImagemMixin):
    nome = models.CharField(max_length=120)
    objetivo = models.CharField(max_length=20, choices=Objetivo.choices)
    calorias_dia = models.PositiveIntegerField()
    descricao = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['nome']

    def __str__(self):
        return self.nome

    @property
    def total_calorias(self):
        return self.refeicoes.aggregate(t=Sum('calorias'))['t'] or 0


class Refeicao(models.Model):
    class Tipo(models.TextChoices):
        CAFE = 'cafe', 'Café da manhã'
        LANCHE = 'lanche', 'Lanche'
        ALMOCO = 'almoco', 'Almoço'
        JANTAR = 'jantar', 'Jantar'
        CEIA = 'ceia', 'Ceia'

    plano = models.ForeignKey(PlanoAlimentar, on_delete=models.CASCADE, related_name='refeicoes')
    tipo = models.CharField(max_length=10, choices=Tipo.choices)
    descricao = models.CharField(max_length=250)
    calorias = models.PositiveIntegerField()
    proteina_g = models.PositiveIntegerField(default=0)
    carbo_g = models.PositiveIntegerField(default=0)
    gordura_g = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'{self.get_tipo_display()} — {self.plano}'


class ProgramaTreino(ImagemMixin):
    class Nivel(models.TextChoices):
        INICIANTE = 'iniciante', 'Iniciante'
        INTERMEDIARIO = 'intermediario', 'Intermediário'
        AVANCADO = 'avancado', 'Avançado'

    nome = models.CharField(max_length=120)
    objetivo = models.CharField(max_length=20, choices=Objetivo.choices)
    nivel = models.CharField(max_length=15, choices=Nivel.choices)
    duracao_semanas = models.PositiveSmallIntegerField(default=8)
    descricao = models.TextField(blank=True)
    plano_sugerido = models.ForeignKey(PlanoAlimentar, null=True, blank=True,
                                       on_delete=models.SET_NULL, related_name='programas')
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['nome']

    def __str__(self):
        return self.nome


class ItemTreino(models.Model):
    programa = models.ForeignKey(ProgramaTreino, on_delete=models.CASCADE, related_name='itens')
    dia = models.PositiveSmallIntegerField(help_text='Número do treino (1 = Treino A, 2 = Treino B...)')
    exercicio = models.CharField(max_length=120)
    series = models.PositiveSmallIntegerField()
    repeticoes = models.CharField(max_length=20, help_text='Ex.: 8-12')
    descanso_seg = models.PositiveSmallIntegerField(default=60)

    class Meta:
        ordering = ['dia', 'id']

    def __str__(self):
        return f'{self.exercicio} ({self.programa})'

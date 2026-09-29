from django.core.management.base import BaseCommand

from app.models import ItemTreino, PlanoAlimentar, ProgramaTreino, Refeicao


class Command(BaseCommand):
    help = 'Cadastra dados de exemplo (programas de treino e planos alimentares).'

    def handle(self, *args, **options):
        if PlanoAlimentar.objects.exists() or ProgramaTreino.objects.exists():
            self.stdout.write('Já existem dados; nada a fazer.')
            return

        leve = PlanoAlimentar.objects.create(
            nome='Definição Leve', objetivo='emagrecimento', calorias_dia=1700,
            descricao='Déficit calórico moderado com boa saciedade e proteína alta.')
        massa = PlanoAlimentar.objects.create(
            nome='Massa Magra', objetivo='hipertrofia', calorias_dia=2950,
            descricao='Superávit calórico com carboidrato ao redor do treino.')

        refeicoes = {
            leve: [
                ('cafe', 'Omelete de 2 ovos com aveia e fruta', 350, 25, 35, 12),
                ('lanche', 'Iogurte natural com chia', 150, 10, 15, 5),
                ('almoco', 'Frango grelhado, arroz integral e salada', 550, 45, 55, 12),
                ('lanche', 'Fruta e castanhas', 200, 5, 20, 10),
                ('jantar', 'Peixe assado com legumes', 450, 38, 30, 15),
            ],
            massa: [
                ('cafe', 'Panqueca de banana com whey e pasta de amendoim', 600, 40, 70, 18),
                ('lanche', 'Sanduíche de frango com queijo', 450, 30, 45, 14),
                ('almoco', 'Carne magra, arroz, feijão e legumes', 800, 55, 95, 20),
                ('lanche', 'Batata-doce com ovos', 450, 25, 55, 10),
                ('jantar', 'Salmão, macarrão integral e brócolis', 650, 45, 60, 22),
            ],
        }
        for plano, itens in refeicoes.items():
            for tipo, desc, kcal, p, c, g in itens:
                Refeicao.objects.create(plano=plano, tipo=tipo, descricao=desc,
                                        calorias=kcal, proteina_g=p, carbo_g=c, gordura_g=g)

        programas = [
            (dict(nome='Full Body Iniciante', objetivo='condicionamento', nivel='iniciante',
                  duracao_semanas=8, plano_sugerido=leve,
                  descricao='Treino de corpo inteiro, 3x por semana, alternando os treinos A e B.'),
             [(1, 'Agachamento livre', 3, '12', 60), (1, 'Supino com halteres', 3, '12', 60),
              (1, 'Remada curvada', 3, '12', 60), (1, 'Prancha', 3, '30s', 45),
              (2, 'Leg press', 3, '12', 60), (2, 'Desenvolvimento com halteres', 3, '12', 60),
              (2, 'Puxada frontal', 3, '12', 60), (2, 'Abdominal', 3, '15', 45)]),
            (dict(nome='ABC Hipertrofia', objetivo='hipertrofia', nivel='intermediario',
                  duracao_semanas=12, plano_sugerido=massa,
                  descricao='Divisão ABC: A peito e tríceps, B costas e bíceps, C pernas.'),
             [(1, 'Supino reto', 4, '8-10', 90), (1, 'Supino inclinado', 3, '10', 75),
              (1, 'Tríceps testa', 3, '12', 60),
              (2, 'Puxada frontal', 4, '8-10', 90), (2, 'Remada baixa', 3, '10', 75),
              (2, 'Rosca direta', 3, '12', 60),
              (3, 'Agachamento', 4, '8', 120), (3, 'Leg press', 3, '12', 90),
              (3, 'Stiff', 3, '10', 90)]),
            (dict(nome='Força 5x5', objetivo='forca', nivel='avancado', duracao_semanas=10,
                  descricao='Foco em cargas altas nos movimentos básicos.'),
             [(1, 'Agachamento', 5, '5', 180), (1, 'Supino reto', 5, '5', 180),
              (2, 'Levantamento terra', 5, '5', 180), (2, 'Desenvolvimento militar', 5, '5', 150)]),
        ]
        for dados, itens in programas:
            programa = ProgramaTreino.objects.create(**dados)
            for dia, ex, series, reps, desc in itens:
                ItemTreino.objects.create(programa=programa, dia=dia, exercicio=ex,
                                          series=series, repeticoes=reps, descanso_seg=desc)
        self.stdout.write(self.style.SUCCESS('Dados de exemplo cadastrados.'))

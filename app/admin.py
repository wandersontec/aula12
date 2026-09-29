from django.contrib import admin
from .models import ItemTreino, PlanoAlimentar, ProgramaTreino, Refeicao


class ItemTreinoInline(admin.TabularInline):
    model = ItemTreino
    extra = 1


class RefeicaoInline(admin.TabularInline):
    model = Refeicao
    extra = 1


@admin.register(ProgramaTreino)
class ProgramaTreinoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'objetivo', 'nivel', 'duracao_semanas')
    inlines = [ItemTreinoInline]


@admin.register(PlanoAlimentar)
class PlanoAlimentarAdmin(admin.ModelAdmin):
    list_display = ('nome', 'objetivo', 'calorias_dia')
    inlines = [RefeicaoInline]


admin.site.register(ItemTreino)
admin.site.register(Refeicao)

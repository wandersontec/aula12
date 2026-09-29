# FitPulse — Academia Fitness (Desafio Django, Aula 12)

Aplicação Django para uma academia: **programas de treino** (com exercícios, séries e repetições) e **planos alimentares** (com refeições e macros). Cada programa pode sugerir um plano alimentar.

## O que faz

- Home, listagem, detalhes de programas e planos (leitura pública)
- Criar, editar e excluir programas e planos (**somente logado**, exclusão via POST com confirmação)
- Login/logout nativos do Django, cadastro de usuário e perfil
- Exercícios e refeições são cadastrados pelo painel `/admin/` (inlines dentro de cada programa/plano)
- Bootstrap 5 + herança de templates (`base.html`)

## Como rodar

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed           # dados de exemplo (opcional)
python manage.py createsuperuser
python manage.py runserver
```

Acesse http://127.0.0.1:8000 e o admin em http://127.0.0.1:8000/admin/.

## Testes

```bash
python manage.py test
```

## Estrutura

```
config/   configurações e urls do projeto
app/      models, views, forms, urls, templates/, static/style.css
```

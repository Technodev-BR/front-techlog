#!/bin/sh

# Coletar arquivos estáticos
python manage.py collectstatic --noinput

# Criar migrações e aplicar
python manage.py makemigrations --noinput
python manage.py migrate --noinput

# Criar superuser fixo (só se não existir)
echo "from django.contrib.auth import get_user_model; User = get_user_model(); \
if not User.objects.filter(username='admin').exists(): \
    User.objects.create_superuser('admin','admin@example.com','admin123')" | python manage.py shell

# Rodar servidor de desenvolvimento
python manage.py runserver 0.0.0.0:5000

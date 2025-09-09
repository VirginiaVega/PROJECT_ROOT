"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
#For render
from django.core.management import execute_from_command_line

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

#for render star
try:
    print("🔄 Ejecutando migraciones automáticamente...")
    execute_from_command_line(['manage.py', 'migrate'])
    print("✅ Migraciones completadas")
except Exception as e:
    print(f"❌ Error en migraciones: {e}")
#for render end





application = get_wsgi_application()

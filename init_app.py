#!/usr/bin/env python
"""
Script de inicialização para o deploy no Render.
Executa migrações e cria superusuário automaticamente.
"""

import os
import sys
import django
from django.core.management import execute_from_command_line

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

def main():
    print("Iniciando script de inicialização...")
    
    # Executar migrações
    print("Executando migrações...")
    execute_from_command_line(['manage.py', 'migrate'])
    
    # Criar superusuário
    print("Criando superusuário...")
    execute_from_command_line(['manage.py', 'create_superuser'])
    
    print("Inicialização concluída!")

if __name__ == '__main__':
    main()
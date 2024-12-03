# core/IdolPass/admin.py
from django.contrib import admin
from .models import Concert, Ticket

# Registrar los modelos para que aparezcan en el panel de administración
admin.site.register(Concert)
admin.site.register(Ticket)

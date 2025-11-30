from django.contrib import admin
from .models import Property, Client, Task, Collaborator


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ['address', 'price', 'property_type', 'status', 'listing_date']
    list_filter = ['status', 'property_type', 'listing_date']
    search_fields = ['address', 'description']


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'client_type']
    list_filter = ['client_type']
    search_fields = ['name', 'email']


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'due_date', 'status', 'priority']
    list_filter = ['status', 'priority', 'due_date']
    search_fields = ['title', 'description']


@admin.register(Collaborator)
class CollaboratorAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'role']
    list_filter = ['role']
    search_fields = ['name', 'email']
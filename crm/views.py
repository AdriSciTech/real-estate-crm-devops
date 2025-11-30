"""
Views for the CRM application.
Refactored to use service layer and reduce code duplication.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Property, Client, Task, Collaborator
from .forms import PropertyForm, ClientForm, TaskForm, CollaboratorForm
from .services import (
    PropertyService, ClientService, TaskService,
    CollaboratorService, DashboardService
)
from .constants import Messages


def home(request):
    """Home page view with dashboard statistics."""
    context = DashboardService.get_dashboard_stats()
    return render(request, 'crm/home.html', context)


# =============================================================================
# Property Views
# =============================================================================

def property_list(request):
    """List all properties with filtering options."""
    # Extract filter parameters
    status_filter = request.GET.get('status', '')
    type_filter = request.GET.get('property_type', '')
    search_query = request.GET.get('search', '')
    
    # Use service to filter properties
    properties = PropertyService.filter_properties(
        status=status_filter or None,
        property_type=type_filter or None,
        search_query=search_query or None
    )
    
    context = {
        'properties': properties,
        'status_choices': Property.STATUS_CHOICES,
        'type_choices': Property.PROPERTY_TYPE_CHOICES,
        'current_status': status_filter,
        'current_type': type_filter,
        'search_query': search_query,
    }
    return render(request, 'crm/property_list.html', context)


def property_detail(request, pk):
    """Display detailed view of a property."""
    property_obj = get_object_or_404(Property, pk=pk)
    return render(request, 'crm/property_detail.html', {'property': property_obj})


def property_create(request):
    """Create a new property."""
    if request.method == 'POST':
        form = PropertyForm(request.POST)
        if form.is_valid():
            property_obj = form.save()
            messages.success(
                request,
                Messages.PROPERTY_CREATED.format(property_obj.address)
            )
            return redirect('property_detail', pk=property_obj.pk)
    else:
        form = PropertyForm()
    
    return render(request, 'crm/property_form.html', {
        'form': form,
        'title': 'Create New Property'
    })


def property_update(request, pk):
    """Update an existing property."""
    property_obj = get_object_or_404(Property, pk=pk)
    
    if request.method == 'POST':
        form = PropertyForm(request.POST, instance=property_obj)
        if form.is_valid():
            property_obj = form.save()
            messages.success(
                request,
                Messages.PROPERTY_UPDATED.format(property_obj.address)
            )
            return redirect('property_detail', pk=property_obj.pk)
    else:
        form = PropertyForm(instance=property_obj)
    
    return render(request, 'crm/property_form.html', {
        'form': form,
        'title': f'Update Property: {property_obj.address}',
        'property': property_obj
    })


def property_delete(request, pk):
    """Delete a property."""
    property_obj = get_object_or_404(Property, pk=pk)
    
    if request.method == 'POST':
        address = property_obj.address
        property_obj.delete()
        messages.success(request, Messages.PROPERTY_DELETED.format(address))
        return redirect('property_list')
    
    return render(request, 'crm/property_confirm_delete.html', {'property': property_obj})


# =============================================================================
# Client Views
# =============================================================================

def client_list(request):
    """List all clients with search and filtering."""
    search_query = request.GET.get('search', '')
    client_type = request.GET.get('client_type', '')
    
    clients = ClientService.filter_clients(
        client_type=client_type or None,
        search_query=search_query or None
    )
    
    context = {
        'clients': clients,
        'search_query': search_query,
        'current_type': client_type,
        'type_choices': Client.CLIENT_TYPE_CHOICES,
    }
    return render(request, 'crm/client_list.html', context)


def client_detail(request, pk):
    """Display client details."""
    client = get_object_or_404(Client, pk=pk)
    return render(request, 'crm/client_detail.html', {'client': client})


def client_create(request):
    """Create a new client."""
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save()
            messages.success(request, Messages.CLIENT_CREATED.format(client.name))
            return redirect('client_detail', pk=client.pk)
    else:
        form = ClientForm()
    
    return render(request, 'crm/client_form.html', {
        'form': form,
        'title': 'Add New Client'
    })


def client_update(request, pk):
    """Update client information."""
    client = get_object_or_404(Client, pk=pk)
    
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            messages.success(request, Messages.CLIENT_UPDATED.format(client.name))
            return redirect('client_detail', pk=client.pk)
    else:
        form = ClientForm(instance=client)
    
    return render(request, 'crm/client_form.html', {
        'form': form,
        'title': f'Edit Client: {client.name}'
    })


def client_delete(request, pk):
    """Delete a client."""
    client = get_object_or_404(Client, pk=pk)
    
    if request.method == 'POST':
        client_name = client.name
        client.delete()
        messages.success(request, Messages.CLIENT_DELETED.format(client_name))
        return redirect('client_list')
    
    return render(request, 'crm/client_confirm_delete.html', {'client': client})


# =============================================================================
# Task Views
# =============================================================================

def task_list(request):
    """List all tasks with filtering options."""
    status_filter = request.GET.get('status', '')
    priority_filter = request.GET.get('priority', '')
    search_query = request.GET.get('search', '')
    
    tasks = TaskService.filter_tasks(
        status=status_filter or None,
        priority=priority_filter or None,
        search_query=search_query or None
    )
    
    context = {
        'tasks': tasks,
        'status_choices': Task.STATUS_CHOICES,
        'priority_choices': Task.PRIORITY_CHOICES,
        'current_status': status_filter,
        'current_priority': priority_filter,
        'search_query': search_query,
    }
    return render(request, 'crm/task_list.html', context)


def task_detail(request, pk):
    """Display task details."""
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'crm/task_detail.html', {'task': task})


def task_create(request):
    """Create a new task."""
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save()
            messages.success(request, Messages.TASK_CREATED.format(task.title))
            return redirect('task_detail', pk=task.pk)
    else:
        form = TaskForm()
    
    return render(request, 'crm/task_form.html', {
        'form': form,
        'title': 'Create New Task'
    })


def task_update(request, pk):
    """Update a task."""
    task = get_object_or_404(Task, pk=pk)
    
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save()
            messages.success(request, Messages.TASK_UPDATED.format(task.title))
            return redirect('task_detail', pk=task.pk)
    else:
        form = TaskForm(instance=task)
    
    return render(request, 'crm/task_form.html', {
        'form': form,
        'title': f'Update Task: {task.title}'
    })


def task_delete(request, pk):
    """Delete a task."""
    task = get_object_or_404(Task, pk=pk)
    
    if request.method == 'POST':
        title = task.title
        task.delete()
        messages.success(request, Messages.TASK_DELETED.format(title))
        return redirect('task_list')
    
    return render(request, 'crm/task_confirm_delete.html', {'task': task})


# =============================================================================
# Collaborator Views
# =============================================================================

def collaborator_list(request):
    """List all collaborators."""
    role_filter = request.GET.get('role', '')
    search_query = request.GET.get('search', '')
    
    collaborators = CollaboratorService.filter_collaborators(
        role=role_filter or None,
        search_query=search_query or None
    )
    
    context = {
        'collaborators': collaborators,
        'role_choices': Collaborator.ROLE_CHOICES,
        'current_role': role_filter,
        'search_query': search_query,
    }
    return render(request, 'crm/collaborator_list.html', context)


def collaborator_detail(request, pk):
    """Display collaborator details."""
    collaborator = get_object_or_404(Collaborator, pk=pk)
    return render(request, 'crm/collaborator_detail.html', {'collaborator': collaborator})


def collaborator_create(request):
    """Create a new collaborator."""
    if request.method == 'POST':
        form = CollaboratorForm(request.POST)
        if form.is_valid():
            collaborator = form.save()
            messages.success(
                request,
                Messages.COLLABORATOR_CREATED.format(collaborator.name)
            )
            return redirect('collaborator_detail', pk=collaborator.pk)
    else:
        form = CollaboratorForm()
    
    return render(request, 'crm/collaborator_form.html', {
        'form': form,
        'title': 'Add New Collaborator'
    })


def collaborator_update(request, pk):
    """Update collaborator information."""
    collaborator = get_object_or_404(Collaborator, pk=pk)
    
    if request.method == 'POST':
        form = CollaboratorForm(request.POST, instance=collaborator)
        if form.is_valid():
            collaborator = form.save()
            messages.success(
                request,
                Messages.COLLABORATOR_UPDATED.format(collaborator.name)
            )
            return redirect('collaborator_detail', pk=collaborator.pk)
    else:
        form = CollaboratorForm(instance=collaborator)
    
    return render(request, 'crm/collaborator_form.html', {
        'form': form,
        'title': f'Update Collaborator: {collaborator.name}'
    })


def collaborator_delete(request, pk):
    """Delete a collaborator."""
    collaborator = get_object_or_404(Collaborator, pk=pk)
    
    if request.method == 'POST':
        name = collaborator.name
        collaborator.delete()
        messages.success(request, Messages.COLLABORATOR_DELETED.format(name))
        return redirect('collaborator_list')
    
    return render(request, 'crm/collaborator_confirm_delete.html', {'collaborator': collaborator})
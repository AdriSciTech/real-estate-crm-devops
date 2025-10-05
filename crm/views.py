from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Property, Client, Task, Collaborator
from .forms import PropertyForm, ClientForm, TaskForm, CollaboratorForm


def home(request):
    """Home page view."""
    # Get counts for dashboard
    context = {
        'property_count': Property.objects.count(),
        'client_count': Client.objects.count(),
        'task_count': Task.objects.filter(status='PENDING').count(),
        'collaborator_count': Collaborator.objects.count(),
    }
    return render(request, 'crm/home.html', context)


# Property Views
def property_list(request):
    """List all properties with filtering options."""
    properties = Property.objects.all()
    
    # Filter by status if provided
    status_filter = request.GET.get('status')
    if status_filter:
        properties = properties.filter(status=status_filter)
    
    # Filter by property type if provided
    type_filter = request.GET.get('property_type')
    if type_filter:
        properties = properties.filter(property_type=type_filter)
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        properties = properties.filter(
            Q(address__icontains=search_query) |
            Q(description__icontains=search_query)
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
    property = get_object_or_404(Property, pk=pk)
    return render(request, 'crm/property_detail.html', {'property': property})


def property_create(request):
    """Create a new property."""
    if request.method == 'POST':
        form = PropertyForm(request.POST)
        if form.is_valid():
            property = form.save()
            messages.success(request, f'Property "{property.address}" created successfully!')
            return redirect('property_detail', pk=property.pk)
    else:
        form = PropertyForm()
    
    return render(request, 'crm/property_form.html', {
        'form': form,
        'title': 'Create New Property'
    })


def property_update(request, pk):
    """Update an existing property."""
    property = get_object_or_404(Property, pk=pk)
    
    if request.method == 'POST':
        form = PropertyForm(request.POST, instance=property)
        if form.is_valid():
            property = form.save()
            messages.success(request, f'Property "{property.address}" updated successfully!')
            return redirect('property_detail', pk=property.pk)
    else:
        form = PropertyForm(instance=property)
    
    return render(request, 'crm/property_form.html', {
        'form': form,
        'title': f'Update Property: {property.address}',
        'property': property
    })


def property_delete(request, pk):
    """Delete a property."""
    property = get_object_or_404(Property, pk=pk)
    
    if request.method == 'POST':
        address = property.address
        property.delete()
        messages.success(request, f'Property "{address}" deleted successfully!')
        return redirect('property_list')
    
    return render(request, 'crm/property_confirm_delete.html', {'property': property})


# Client Views
def client_list(request):
    """List all clients with search and filtering."""
    clients = Client.objects.all()
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        clients = clients.filter(
            Q(name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(phone__icontains=search_query)
        )
    
    # Filter by client type
    client_type = request.GET.get('client_type', '')
    if client_type:
        clients = clients.filter(client_type=client_type)
    
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
            messages.success(request, f'Client "{client.name}" has been created.')
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
            messages.success(request, f'Client "{client.name}" has been updated.')
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
        messages.success(request, f'Client "{client_name}" has been deleted.')
        return redirect('client_list')
    
    return render(request, 'crm/client_confirm_delete.html', {'client': client})


# Task Views
def task_list(request):
    """List all tasks with filtering options."""
    tasks = Task.objects.all()
    
    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        tasks = tasks.filter(status=status_filter)
    
    # Filter by priority
    priority_filter = request.GET.get('priority')
    if priority_filter:
        tasks = tasks.filter(priority=priority_filter)
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        tasks = tasks.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
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
            messages.success(request, f'Task "{task.title}" created successfully!')
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
            messages.success(request, f'Task "{task.title}" updated successfully!')
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
        messages.success(request, f'Task "{title}" deleted successfully!')
        return redirect('task_list')
    
    return render(request, 'crm/task_confirm_delete.html', {'task': task})


# Collaborator Views
def collaborator_list(request):
    """List all collaborators."""
    collaborators = Collaborator.objects.all()
    
    # Filter by role
    role_filter = request.GET.get('role')
    if role_filter:
        collaborators = collaborators.filter(role=role_filter)
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        collaborators = collaborators.filter(
            Q(name__icontains=search_query) |
            Q(email__icontains=search_query)
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
            messages.success(request, f'Collaborator "{collaborator.name}" created successfully!')
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
            messages.success(request, f'Collaborator "{collaborator.name}" updated successfully!')
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
        messages.success(request, f'Collaborator "{name}" deleted successfully!')
        return redirect('collaborator_list')
    
    return render(request, 'crm/collaborator_confirm_delete.html', {'collaborator': collaborator})
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Property, Collaborator
from .forms import PropertyForm
from django.db import models
from .models import Client  # Add this if not already imported
from .forms import ClientForm  # We'll create this next



# Client Views
def client_list(request):
    clients = Client.objects.all()
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        clients = clients.filter(
            models.Q(name__icontains=search_query) |
            models.Q(email__icontains=search_query) |
            models.Q(phone__icontains=search_query)
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
    client = get_object_or_404(Client, pk=pk)
    return render(request, 'crm/client_detail.html', {'client': client})

def client_create(request):
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
    client = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        client_name = client.name
        client.delete()
        messages.success(request, f'Client "{client_name}" has been deleted.')
        return redirect('client_list')
    
    return render(request, 'crm/client_confirm_delete.html', {'client': client})


def home(request):
    """Home page view."""
    return render(request, 'crm/home.html')


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



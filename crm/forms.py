from django import forms
from django.core.exceptions import ValidationError
from .models import Property, Client, Task, Collaborator
from decimal import Decimal
from datetime import date




class PropertyForm(forms.ModelForm):
    """Form for creating and updating properties."""
    
    class Meta:
        model = Property
        fields = [
            'address', 'price', 'property_type', 'status', 
            'listing_date', 'collaborator', 'bedrooms', 
            'bathrooms', 'square_feet', 'description'
        ]
        widgets = {
            'address': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Enter full property address'}),
            'price': forms.NumberInput(attrs={'step': '0.01', 'min': '0', 'placeholder': '0.00'}),
            'listing_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Property description...'}),
            'bedrooms': forms.NumberInput(attrs={'min': '0', 'placeholder': 'Number of bedrooms'}),
            'bathrooms': forms.NumberInput(attrs={'step': '0.5', 'min': '0', 'placeholder': '0.0'}),
            'square_feet': forms.NumberInput(attrs={'min': '0', 'placeholder': 'Total square feet'}),
        }
    
    def clean_price(self):
        """Validate that price is positive."""
        price = self.cleaned_data.get('price')
        if price and price <= 0:
            raise ValidationError('Price must be greater than 0.')
        return price
    
    def clean_listing_date(self):
        """Validate that listing date is not in the future."""
        listing_date = self.cleaned_data.get('listing_date')
        if listing_date and listing_date > date.today():
            raise ValidationError('Listing date cannot be in the future.')
        return listing_date


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'email', 'phone', 'client_type', 'notes']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter client name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'client@email.com'}),
            'phone': forms.TextInput(attrs={'placeholder': '(555) 123-4567'}),
            'notes': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Enter client notes, preferences, or requirements...'
            }),
        }
    
    def clean_phone(self):
        """Basic phone number validation."""
        phone = self.cleaned_data.get('phone')
        if phone:
            # Remove common formatting characters
            cleaned_phone = ''.join(filter(str.isdigit, phone))
            if len(cleaned_phone) < 10:
                raise ValidationError('Phone number must have at least 10 digits.')
        return phone


class TaskForm(forms.ModelForm):
    """Form for creating and updating tasks."""
    
    class Meta:
        model = Task
        fields = [
            'title', 'description', 'due_date', 'status', 
            'priority', 'property', 'client', 'assigned_to'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Task title'}),
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Task description...'}),
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def clean_due_date(self):
        """Validate due date for new tasks."""
        due_date = self.cleaned_data.get('due_date')
        status = self.cleaned_data.get('status')
        
        # Only validate future dates for new/pending tasks
        if not self.instance.pk and due_date and due_date < date.today():
            raise ValidationError('Due date cannot be in the past for new tasks.')
        
        return due_date
    
    def clean(self):
        """Validate that task is assigned to either property or client (not both)."""
        cleaned_data = super().clean()
        property = cleaned_data.get('property')
        client = cleaned_data.get('client')
        
        if property and client:
            raise ValidationError('A task can be assigned to either a property or a client, not both.')
        
        return cleaned_data


class CollaboratorForm(forms.ModelForm):
    """Form for creating and updating collaborators."""
    
    class Meta:
        model = Collaborator
        fields = ['name', 'email', 'role']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Full name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'collaborator@email.com'}),
        }
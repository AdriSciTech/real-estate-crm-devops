"""
Forms for the CRM application.
Provides validation and widget configuration for model forms.
"""

from django import forms
from django.core.exceptions import ValidationError
from datetime import date

from .models import Property, Client, Task, Collaborator
from .constants import ValidationConstants


class BaseModelForm(forms.ModelForm):
    """Base form class with common functionality."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add common CSS classes to all form fields
        for field_name, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'


class PropertyForm(BaseModelForm):
    """Form for creating and updating properties."""
    
    class Meta:
        model = Property
        fields = [
            'address', 'price', 'property_type', 'status',
            'listing_date', 'collaborator', 'bedrooms',
            'bathrooms', 'square_feet', 'description'
        ]
        widgets = {
            'address': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': 'Enter full property address'
            }),
            'price': forms.NumberInput(attrs={
                'step': '0.01',
                'min': '0',
                'placeholder': '0.00'
            }),
            'listing_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Property description...'
            }),
            'bedrooms': forms.NumberInput(attrs={
                'min': '0',
                'placeholder': 'Number of bedrooms'
            }),
            'bathrooms': forms.NumberInput(attrs={
                'step': '0.5',
                'min': '0',
                'placeholder': '0.0'
            }),
            'square_feet': forms.NumberInput(attrs={
                'min': '0',
                'placeholder': 'Total square feet'
            }),
        }
    
    def clean_price(self):
        """Validate that price is positive."""
        price = self.cleaned_data.get('price')
        if price is not None and price <= 0:
            raise ValidationError('Price must be greater than 0.')
        return price
    
    def clean_listing_date(self):
        """Validate that listing date is not in the future."""
        listing_date = self.cleaned_data.get('listing_date')
        if listing_date and listing_date > date.today():
            raise ValidationError('Listing date cannot be in the future.')
        return listing_date
    
    def clean_bedrooms(self):
        """Validate bedrooms is non-negative."""
        bedrooms = self.cleaned_data.get('bedrooms')
        if bedrooms is not None and bedrooms < 0:
            raise ValidationError('Bedrooms cannot be negative.')
        return bedrooms
    
    def clean_square_feet(self):
        """Validate square feet is non-negative."""
        square_feet = self.cleaned_data.get('square_feet')
        if square_feet is not None and square_feet < 0:
            raise ValidationError('Square feet cannot be negative.')
        return square_feet


class ClientForm(BaseModelForm):
    """Form for creating and updating clients."""
    
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
        """Validate phone number has minimum digits."""
        phone = self.cleaned_data.get('phone')
        if phone:
            # Remove common formatting characters
            cleaned_phone = ''.join(filter(str.isdigit, phone))
            if len(cleaned_phone) < ValidationConstants.MIN_PHONE_DIGITS:
                raise ValidationError(
                    f'Phone number must have at least {ValidationConstants.MIN_PHONE_DIGITS} digits.'
                )
        return phone
    
    def clean_name(self):
        """Validate name is not empty or whitespace only."""
        name = self.cleaned_data.get('name')
        if name and not name.strip():
            raise ValidationError('Name cannot be empty or whitespace only.')
        return name.strip() if name else name


class TaskForm(BaseModelForm):
    """Form for creating and updating tasks."""
    
    class Meta:
        model = Task
        fields = [
            'title', 'description', 'due_date', 'status',
            'priority', 'related_property', 'client', 'assigned_to'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Task title'}),
            'description': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Task description...'
            }),
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'related_property': 'Property',
        }
    
    def clean_due_date(self):
        """Validate due date for new tasks."""
        due_date = self.cleaned_data.get('due_date')
        
        # Only validate future dates for new tasks
        if not self.instance.pk and due_date and due_date < date.today():
            raise ValidationError('Due date cannot be in the past for new tasks.')
        
        return due_date
    
    def clean_title(self):
        """Validate title is not empty or whitespace only."""
        title = self.cleaned_data.get('title')
        if title and not title.strip():
            raise ValidationError('Title cannot be empty or whitespace only.')
        return title.strip() if title else title
    
    def clean(self):
        """Validate that task is assigned to either property or client (not both)."""
        cleaned_data = super().clean()
        related_property = cleaned_data.get('related_property')
        client = cleaned_data.get('client')
        
        if related_property and client:
            raise ValidationError(
                'A task can be assigned to either a property or a client, not both.'
            )
        
        return cleaned_data


class CollaboratorForm(BaseModelForm):
    """Form for creating and updating collaborators."""
    
    class Meta:
        model = Collaborator
        fields = ['name', 'email', 'role']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Full name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'collaborator@email.com'}),
        }
    
    def clean_name(self):
        """Validate name is not empty or whitespace only."""
        name = self.cleaned_data.get('name')
        if name and not name.strip():
            raise ValidationError('Name cannot be empty or whitespace only.')
        return name.strip() if name else name
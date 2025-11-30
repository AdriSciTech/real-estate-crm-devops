"""
Unit tests for CRM forms.
Tests form validation, cleaning, and widget configuration.
"""
import pytest
from datetime import date, timedelta
from decimal import Decimal

from crm.forms import PropertyForm, ClientForm, TaskForm, CollaboratorForm
from crm.models import Property, Client, Task, Collaborator
from crm.constants import PropertyType, PropertyStatus, ClientType, TaskStatus


# =============================================================================
# PropertyForm Tests
# =============================================================================

class TestPropertyForm:
    """Tests for the PropertyForm."""
    
    def test_valid_property_form(self, db):
        """Test form with valid data."""
        form_data = {
            'address': '123 Test Street',
            'price': '450000.00',
            'property_type': PropertyType.HOUSE,
            'status': PropertyStatus.AVAILABLE,
            'listing_date': date.today(),
            'bedrooms': 3,
            'bathrooms': 2.5,
            'square_feet': 2000,
            'description': 'A nice house'
        }
        form = PropertyForm(data=form_data)
        assert form.is_valid(), form.errors
    
    def test_price_must_be_positive(self, db):
        """Test that price must be greater than zero."""
        form_data = {
            'address': '123 Test Street',
            'price': '-100.00',
            'property_type': PropertyType.HOUSE,
            'status': PropertyStatus.AVAILABLE,
            'listing_date': date.today(),
        }
        form = PropertyForm(data=form_data)
        assert not form.is_valid()
        assert 'price' in form.errors
    
    def test_price_zero_invalid(self, db):
        """Test that price cannot be zero."""
        form_data = {
            'address': '123 Test Street',
            'price': '0.00',
            'property_type': PropertyType.HOUSE,
            'status': PropertyStatus.AVAILABLE,
            'listing_date': date.today(),
        }
        form = PropertyForm(data=form_data)
        assert not form.is_valid()
        assert 'price' in form.errors
    
    def test_listing_date_not_future(self, db):
        """Test that listing date cannot be in the future."""
        form_data = {
            'address': '123 Test Street',
            'price': '450000.00',
            'property_type': PropertyType.HOUSE,
            'status': PropertyStatus.AVAILABLE,
            'listing_date': date.today() + timedelta(days=10),
        }
        form = PropertyForm(data=form_data)
        assert not form.is_valid()
        assert 'listing_date' in form.errors
    
    def test_bedrooms_non_negative(self, db):
        """Test that bedrooms cannot be negative."""
        form_data = {
            'address': '123 Test Street',
            'price': '450000.00',
            'property_type': PropertyType.HOUSE,
            'status': PropertyStatus.AVAILABLE,
            'listing_date': date.today(),
            'bedrooms': -1,
        }
        form = PropertyForm(data=form_data)
        assert not form.is_valid()
        assert 'bedrooms' in form.errors
    
    def test_square_feet_non_negative(self, db):
        """Test that square_feet cannot be negative."""
        form_data = {
            'address': '123 Test Street',
            'price': '450000.00',
            'property_type': PropertyType.HOUSE,
            'status': PropertyStatus.AVAILABLE,
            'listing_date': date.today(),
            'square_feet': -100,
        }
        form = PropertyForm(data=form_data)
        assert not form.is_valid()
        assert 'square_feet' in form.errors
    
    def test_optional_fields(self, db):
        """Test form with only required fields."""
        form_data = {
            'address': '123 Test Street',
            'price': '450000.00',
            'property_type': PropertyType.HOUSE,
            'status': PropertyStatus.AVAILABLE,
            'listing_date': date.today(),
        }
        form = PropertyForm(data=form_data)
        assert form.is_valid(), form.errors


# =============================================================================
# ClientForm Tests
# =============================================================================

class TestClientForm:
    """Tests for the ClientForm."""
    
    def test_valid_client_form(self, db):
        """Test form with valid data."""
        form_data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'phone': '(555) 123-4567',
            'client_type': ClientType.BUYER,
            'notes': 'Test notes'
        }
        form = ClientForm(data=form_data)
        assert form.is_valid(), form.errors
    
    def test_phone_minimum_digits(self, db):
        """Test that phone must have at least 10 digits."""
        form_data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'phone': '123456',  # Only 6 digits
            'client_type': ClientType.BUYER,
        }
        form = ClientForm(data=form_data)
        assert not form.is_valid()
        assert 'phone' in form.errors
    
    def test_phone_accepts_formatted(self, db):
        """Test that phone accepts formatted numbers."""
        form_data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'phone': '(555) 123-4567',  # 10 digits with formatting
            'client_type': ClientType.BUYER,
        }
        form = ClientForm(data=form_data)
        assert form.is_valid(), form.errors
    
    def test_name_whitespace_only_invalid(self, db):
        """Test that name cannot be whitespace only."""
        form_data = {
            'name': '   ',
            'email': 'john@example.com',
            'phone': '1234567890',
            'client_type': ClientType.BUYER,
        }
        form = ClientForm(data=form_data)
        assert not form.is_valid()
        assert 'name' in form.errors
    
    def test_name_gets_stripped(self, db):
        """Test that name is stripped of whitespace."""
        form_data = {
            'name': '  John Doe  ',
            'email': 'john@example.com',
            'phone': '1234567890',
            'client_type': ClientType.BUYER,
        }
        form = ClientForm(data=form_data)
        assert form.is_valid()
        assert form.cleaned_data['name'] == 'John Doe'
    
    def test_invalid_email(self, db):
        """Test that invalid email is rejected."""
        form_data = {
            'name': 'John Doe',
            'email': 'not-an-email',
            'phone': '1234567890',
            'client_type': ClientType.BUYER,
        }
        form = ClientForm(data=form_data)
        assert not form.is_valid()
        assert 'email' in form.errors


# =============================================================================
# TaskForm Tests
# =============================================================================

class TestTaskForm:
    """Tests for the TaskForm."""
    
    def test_valid_task_form(self, db):
        """Test form with valid data."""
        form_data = {
            'title': 'Follow up call',
            'description': 'Call client about property',
            'due_date': date.today() + timedelta(days=7),
            'status': TaskStatus.PENDING,
            'priority': 'MEDIUM',
        }
        form = TaskForm(data=form_data)
        assert form.is_valid(), form.errors
    
    def test_due_date_past_invalid_new_task(self, db):
        """Test that due date in past is invalid for new tasks."""
        form_data = {
            'title': 'Past task',
            'due_date': date.today() - timedelta(days=5),
            'status': TaskStatus.PENDING,
            'priority': 'MEDIUM',
        }
        form = TaskForm(data=form_data)
        assert not form.is_valid()
        assert 'due_date' in form.errors
    
    def test_due_date_past_valid_existing_task(self, db, task):
        """Test that past due date is valid when updating existing task."""
        form_data = {
            'title': 'Updated task',
            'due_date': date.today() - timedelta(days=5),
            'status': TaskStatus.COMPLETE,
            'priority': 'HIGH',
        }
        form = TaskForm(data=form_data, instance=task)
        assert form.is_valid(), form.errors
    
    def test_title_whitespace_only_invalid(self, db):
        """Test that title cannot be whitespace only."""
        form_data = {
            'title': '   ',
            'due_date': date.today() + timedelta(days=7),
            'status': TaskStatus.PENDING,
            'priority': 'MEDIUM',
        }
        form = TaskForm(data=form_data)
        assert not form.is_valid()
        assert 'title' in form.errors
    
    def test_property_and_client_both_invalid(self, db, property_obj, client):
        """Test that task cannot have both property and client."""
        form_data = {
            'title': 'Test task',
            'due_date': date.today() + timedelta(days=7),
            'status': TaskStatus.PENDING,
            'priority': 'MEDIUM',
            'related_property': property_obj.pk,
            'client': client.pk,
        }
        form = TaskForm(data=form_data)
        assert not form.is_valid()
        assert '__all__' in form.errors
    
    def test_property_only_valid(self, db, property_obj):
        """Test that task with only property is valid."""
        form_data = {
            'title': 'Property task',
            'due_date': date.today() + timedelta(days=7),
            'status': TaskStatus.PENDING,
            'priority': 'MEDIUM',
            'related_property': property_obj.pk,
        }
        form = TaskForm(data=form_data)
        assert form.is_valid(), form.errors
    
    def test_client_only_valid(self, db, client):
        """Test that task with only client is valid."""
        form_data = {
            'title': 'Client task',
            'due_date': date.today() + timedelta(days=7),
            'status': TaskStatus.PENDING,
            'priority': 'MEDIUM',
            'client': client.pk,
        }
        form = TaskForm(data=form_data)
        assert form.is_valid(), form.errors


# =============================================================================
# CollaboratorForm Tests
# =============================================================================

class TestCollaboratorForm:
    """Tests for the CollaboratorForm."""
    
    def test_valid_collaborator_form(self, db):
        """Test form with valid data."""
        form_data = {
            'name': 'Jane Agent',
            'email': 'jane@example.com',
            'role': 'AGENT',
        }
        form = CollaboratorForm(data=form_data)
        assert form.is_valid(), form.errors
    
    def test_name_whitespace_only_invalid(self, db):
        """Test that name cannot be whitespace only."""
        form_data = {
            'name': '   ',
            'email': 'jane@example.com',
            'role': 'AGENT',
        }
        form = CollaboratorForm(data=form_data)
        assert not form.is_valid()
        assert 'name' in form.errors
    
    def test_invalid_email(self, db):
        """Test that invalid email is rejected."""
        form_data = {
            'name': 'Jane Agent',
            'email': 'not-an-email',
            'role': 'AGENT',
        }
        form = CollaboratorForm(data=form_data)
        assert not form.is_valid()
        assert 'email' in form.errors
    
    def test_all_roles_valid(self, db):
        """Test all role choices are valid."""
        from crm.constants import CollaboratorRole
        for role_code, role_name in CollaboratorRole.CHOICES:
            form_data = {
                'name': f'Test {role_name}',
                'email': f'{role_code.lower()}@example.com',
                'role': role_code,
            }
            form = CollaboratorForm(data=form_data)
            assert form.is_valid(), f"Role {role_code} failed: {form.errors}"
"""
Unit tests for CRM models.
Tests model creation, validation, methods, and properties.
"""
import pytest
from datetime import date, timedelta
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import IntegrityError

from crm.models import Collaborator, Property, Client, Task
from crm.constants import (
    CollaboratorRole, PropertyType, PropertyStatus,
    ClientType, TaskStatus, TaskPriority
)


# =============================================================================
# Collaborator Model Tests
# =============================================================================

class TestCollaboratorModel:
    """Tests for the Collaborator model."""
    
    def test_create_collaborator(self, db):
        """Test creating a collaborator with valid data."""
        collaborator = Collaborator.objects.create(
            name='Test Agent',
            email='test@example.com',
            role=CollaboratorRole.AGENT
        )
        assert collaborator.pk is not None
        assert collaborator.name == 'Test Agent'
        assert collaborator.email == 'test@example.com'
        assert collaborator.role == CollaboratorRole.AGENT
    
    def test_collaborator_str(self, collaborator):
        """Test collaborator string representation."""
        assert str(collaborator) == 'John Agent (Real Estate Agent)'
    
    def test_collaborator_unique_email(self, db, collaborator):
        """Test that email must be unique."""
        with pytest.raises(IntegrityError):
            Collaborator.objects.create(
                name='Another Agent',
                email=collaborator.email,
                role=CollaboratorRole.AGENT
            )
    
    def test_collaborator_default_role(self, db):
        """Test default role is AGENT."""
        collaborator = Collaborator.objects.create(
            name='New Agent',
            email='new@example.com'
        )
        assert collaborator.role == CollaboratorRole.AGENT
    
    def test_collaborator_ordering(self, db, collaborator, manager):
        """Test collaborators are ordered by name."""
        collaborators = list(Collaborator.objects.all())
        assert collaborators[0].name == 'Jane Manager'
        assert collaborators[1].name == 'John Agent'
    
    def test_active_properties_count(self, db, collaborator, property_obj):
        """Test active_properties_count property."""
        assert collaborator.active_properties_count == 1
    
    def test_pending_tasks_count(self, db, collaborator, task):
        """Test pending_tasks_count property."""
        assert collaborator.pending_tasks_count == 1


# =============================================================================
# Property Model Tests
# =============================================================================

class TestPropertyModel:
    """Tests for the Property model."""
    
    def test_create_property(self, db):
        """Test creating a property with valid data."""
        property_obj = Property.objects.create(
            address='100 Main St',
            price=Decimal('500000.00'),
            property_type=PropertyType.HOUSE,
            status=PropertyStatus.AVAILABLE,
            listing_date=date.today()
        )
        assert property_obj.pk is not None
        assert property_obj.address == '100 Main St'
        assert property_obj.price == Decimal('500000.00')
    
    def test_property_str(self, property_obj):
        """Test property string representation."""
        expected = '123 Test Street, Test City, TC 12345 - $450,000.00'
        assert str(property_obj) == expected
    
    def test_property_default_status(self, db):
        """Test default status is AVAILABLE."""
        property_obj = Property.objects.create(
            address='Test Address',
            price=Decimal('100000.00'),
            property_type=PropertyType.CONDO,
            listing_date=date.today()
        )
        assert property_obj.status == PropertyStatus.AVAILABLE
    
    def test_property_is_available(self, property_obj, sold_property):
        """Test is_available property."""
        assert property_obj.is_available is True
        assert sold_property.is_available is False
    
    def test_property_mark_as_sold(self, db, property_obj):
        """Test mark_as_sold method."""
        property_obj.mark_as_sold()
        property_obj.refresh_from_db()
        assert property_obj.status == PropertyStatus.SOLD
    
    def test_property_mark_as_pending(self, db, property_obj):
        """Test mark_as_pending method."""
        property_obj.mark_as_pending()
        property_obj.refresh_from_db()
        assert property_obj.status == PropertyStatus.PENDING
    
    def test_property_ordering(self, db, property_obj, sold_property):
        """Test properties are ordered by listing date descending."""
        properties = list(Property.objects.all())
        # property_obj has today's date, sold_property is 30 days ago
        assert properties[0] == property_obj
        assert properties[1] == sold_property
    
    def test_property_interested_clients_count(self, db, property_obj, client):
        """Test interested_clients_count property."""
        assert property_obj.interested_clients_count == 0
        client.properties_interested.add(property_obj)
        assert property_obj.interested_clients_count == 1
    
    def test_property_price_validator(self, db):
        """Test price minimum value validator."""
        with pytest.raises(ValidationError):
            property_obj = Property(
                address='Test',
                price=Decimal('-100.00'),
                property_type=PropertyType.HOUSE,
                listing_date=date.today()
            )
            property_obj.full_clean()


# =============================================================================
# Client Model Tests
# =============================================================================

class TestClientModel:
    """Tests for the Client model."""
    
    def test_create_client(self, db):
        """Test creating a client with valid data."""
        client = Client.objects.create(
            name='John Buyer',
            email='john@example.com',
            phone='1234567890',
            client_type=ClientType.BUYER
        )
        assert client.pk is not None
        assert client.name == 'John Buyer'
    
    def test_client_str(self, client):
        """Test client string representation."""
        assert str(client) == 'Test Buyer (Buyer)'
    
    def test_client_unique_email(self, db, client):
        """Test that email must be unique."""
        with pytest.raises(IntegrityError):
            Client.objects.create(
                name='Another Buyer',
                email=client.email,
                phone='9876543210',
                client_type=ClientType.BUYER
            )
    
    def test_client_is_buyer(self, client, seller_client):
        """Test is_buyer property."""
        assert client.is_buyer is True
        assert seller_client.is_buyer is False
    
    def test_client_is_seller(self, client, seller_client):
        """Test is_seller property."""
        assert client.is_seller is False
        assert seller_client.is_seller is True
    
    def test_client_both_type(self, db):
        """Test client with BOTH type."""
        both_client = Client.objects.create(
            name='Both Client',
            email='both@example.com',
            phone='5555555555',
            client_type=ClientType.BOTH
        )
        assert both_client.is_buyer is True
        assert both_client.is_seller is True
    
    def test_client_ordering(self, db, client, seller_client):
        """Test clients are ordered by name."""
        clients = list(Client.objects.all())
        assert clients[0].name == 'Test Buyer'
        assert clients[1].name == 'Test Seller'
    
    def test_total_properties_interested(self, db, client, property_obj, sold_property):
        """Test total_properties_interested property."""
        assert client.total_properties_interested == 0
        client.properties_interested.add(property_obj, sold_property)
        assert client.total_properties_interested == 2


# =============================================================================
# Task Model Tests
# =============================================================================

class TestTaskModel:
    """Tests for the Task model."""
    
    def test_create_task(self, db):
        """Test creating a task with valid data."""
        task = Task.objects.create(
            title='Test Task',
            description='Test description',
            due_date=date.today() + timedelta(days=7),
            status=TaskStatus.PENDING,
            priority=TaskPriority.HIGH
        )
        assert task.pk is not None
        assert task.title == 'Test Task'
    
    def test_task_str(self, task):
        """Test task string representation."""
        expected_date = date.today() + timedelta(days=7)
        expected = f'Follow up with client - Due: {expected_date}'
        assert str(task) == expected
    
    def test_task_default_status(self, db):
        """Test default status is PENDING."""
        task = Task.objects.create(
            title='New Task',
            due_date=date.today()
        )
        assert task.status == TaskStatus.PENDING
    
    def test_task_default_priority(self, db):
        """Test default priority is MEDIUM."""
        task = Task.objects.create(
            title='New Task',
            due_date=date.today()
        )
        assert task.priority == TaskPriority.MEDIUM
    
    def test_task_is_overdue(self, task, overdue_task, completed_task):
        """Test is_overdue property."""
        assert task.is_overdue is False  # Future due date
        assert overdue_task.is_overdue is True  # Past due date, pending
        assert completed_task.is_overdue is False  # Past due date but completed
    
    def test_task_is_high_priority(self, task, overdue_task):
        """Test is_high_priority property."""
        assert task.is_high_priority is True
        assert overdue_task.is_high_priority is False
    
    def test_task_mark_complete(self, db, task):
        """Test mark_complete method."""
        task.mark_complete()
        task.refresh_from_db()
        assert task.status == TaskStatus.COMPLETE
    
    def test_task_mark_in_progress(self, db, task):
        """Test mark_in_progress method."""
        task.mark_in_progress()
        task.refresh_from_db()
        assert task.status == TaskStatus.IN_PROGRESS
    
    def test_task_ordering(self, db, task, overdue_task, completed_task):
        """Test tasks are ordered by due_date then priority descending."""
        tasks = list(Task.objects.all())
        # Should be ordered by due_date first
        assert tasks[0] == overdue_task
        assert tasks[1] == completed_task
        assert tasks[2] == task
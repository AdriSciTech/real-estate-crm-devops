"""
Pytest configuration and fixtures for the CRM application tests.
"""
import pytest
from datetime import date, timedelta
from decimal import Decimal

from crm.models import Property, Client, Task, Collaborator
from crm.constants import (
    PropertyType, PropertyStatus, ClientType,
    TaskStatus, TaskPriority, CollaboratorRole
)


@pytest.fixture
def collaborator(db):
    """Create a test collaborator."""
    return Collaborator.objects.create(
        name='John Agent',
        email='john.agent@test.com',
        role=CollaboratorRole.AGENT
    )


@pytest.fixture
def manager(db):
    """Create a test manager collaborator."""
    return Collaborator.objects.create(
        name='Jane Manager',
        email='jane.manager@test.com',
        role=CollaboratorRole.MANAGER
    )


@pytest.fixture
def property_obj(db, collaborator):
    """Create a test property."""
    return Property.objects.create(
        address='123 Test Street, Test City, TC 12345',
        price=Decimal('450000.00'),
        property_type=PropertyType.HOUSE,
        status=PropertyStatus.AVAILABLE,
        listing_date=date.today(),
        collaborator=collaborator,
        bedrooms=3,
        bathrooms=Decimal('2.5'),
        square_feet=2000,
        description='A beautiful test property'
    )


@pytest.fixture
def sold_property(db):
    """Create a sold test property."""
    return Property.objects.create(
        address='456 Sold Lane, Test City, TC 12345',
        price=Decimal('550000.00'),
        property_type=PropertyType.CONDO,
        status=PropertyStatus.SOLD,
        listing_date=date.today() - timedelta(days=30),
        bedrooms=2,
        bathrooms=Decimal('2.0'),
        square_feet=1500,
    )


@pytest.fixture
def client(db):
    """Create a test client."""
    return Client.objects.create(
        name='Test Buyer',
        email='buyer@test.com',
        phone='(555) 123-4567',
        client_type=ClientType.BUYER,
        notes='Test client notes'
    )


@pytest.fixture
def seller_client(db):
    """Create a test seller client."""
    return Client.objects.create(
        name='Test Seller',
        email='seller@test.com',
        phone='(555) 987-6543',
        client_type=ClientType.SELLER,
    )


@pytest.fixture
def task(db, property_obj, collaborator):
    """Create a test task."""
    return Task.objects.create(
        title='Follow up with client',
        description='Call client about property viewing',
        due_date=date.today() + timedelta(days=7),
        status=TaskStatus.PENDING,
        priority=TaskPriority.HIGH,
        related_property=property_obj,
        assigned_to=collaborator
    )


@pytest.fixture
def overdue_task(db, client):
    """Create an overdue test task."""
    return Task.objects.create(
        title='Overdue task',
        description='This task is overdue',
        due_date=date.today() - timedelta(days=5),
        status=TaskStatus.PENDING,
        priority=TaskPriority.MEDIUM,
        client=client
    )


@pytest.fixture
def completed_task(db):
    """Create a completed test task."""
    return Task.objects.create(
        title='Completed task',
        description='This task is complete',
        due_date=date.today() - timedelta(days=2),
        status=TaskStatus.COMPLETE,
        priority=TaskPriority.LOW,
    )
"""
Unit tests for CRM services.
Tests service layer business logic.
"""
import pytest
from datetime import date, timedelta
from decimal import Decimal

from crm.services import (
    PropertyService, ClientService, TaskService,
    CollaboratorService, DashboardService
)
from crm.models import Property, Client, Task, Collaborator
from crm.constants import (
    PropertyType, PropertyStatus, ClientType,
    TaskStatus, TaskPriority, CollaboratorRole
)


# =============================================================================
# PropertyService Tests
# =============================================================================

class TestPropertyService:
    """Tests for the PropertyService."""
    
    def test_get_all_properties(self, db, property_obj, sold_property):
        """Test getting all properties."""
        properties = PropertyService.get_all()
        assert properties.count() == 2
    
    def test_filter_by_status(self, db, property_obj, sold_property):
        """Test filtering properties by status."""
        available = PropertyService.filter_properties(status=PropertyStatus.AVAILABLE)
        sold = PropertyService.filter_properties(status=PropertyStatus.SOLD)
        
        assert available.count() == 1
        assert sold.count() == 1
        assert available.first() == property_obj
        assert sold.first() == sold_property
    
    def test_filter_by_type(self, db, property_obj, sold_property):
        """Test filtering properties by type."""
        houses = PropertyService.filter_properties(property_type=PropertyType.HOUSE)
        condos = PropertyService.filter_properties(property_type=PropertyType.CONDO)
        
        assert houses.count() == 1
        assert condos.count() == 1
    
    def test_filter_by_search(self, db, property_obj, sold_property):
        """Test filtering properties by search query."""
        results = PropertyService.filter_properties(search_query='Test Street')
        assert results.count() == 1
        assert results.first() == property_obj
    
    def test_filter_multiple_criteria(self, db, property_obj, sold_property):
        """Test filtering with multiple criteria."""
        results = PropertyService.filter_properties(
            status=PropertyStatus.AVAILABLE,
            property_type=PropertyType.HOUSE
        )
        assert results.count() == 1
        assert results.first() == property_obj
    
    def test_get_available_properties(self, db, property_obj, sold_property):
        """Test getting only available properties."""
        available = PropertyService.get_available_properties()
        assert available.count() == 1
        assert property_obj in available
        assert sold_property not in available
    
    def test_get_properties_by_collaborator(self, db, property_obj, sold_property, collaborator):
        """Test getting properties by collaborator."""
        properties = PropertyService.get_properties_by_collaborator(collaborator.pk)
        assert properties.count() == 1
        assert property_obj in properties
    
    def test_get_property_statistics(self, db, property_obj, sold_property):
        """Test property statistics."""
        stats = PropertyService.get_property_statistics()
        assert stats['total'] == 2
        assert stats['available'] == 1
        assert stats['sold'] == 1


# =============================================================================
# ClientService Tests
# =============================================================================

class TestClientService:
    """Tests for the ClientService."""
    
    def test_get_all_clients(self, db, client, seller_client):
        """Test getting all clients."""
        clients = ClientService.get_all()
        assert clients.count() == 2
    
    def test_filter_by_type(self, db, client, seller_client):
        """Test filtering clients by type."""
        buyers = ClientService.filter_clients(client_type=ClientType.BUYER)
        sellers = ClientService.filter_clients(client_type=ClientType.SELLER)
        
        assert buyers.count() == 1
        assert sellers.count() == 1
    
    def test_filter_by_search(self, db, client, seller_client):
        """Test filtering clients by search query."""
        results = ClientService.filter_clients(search_query='Buyer')
        assert results.count() == 1
        assert results.first() == client
    
    def test_filter_by_email(self, db, client, seller_client):
        """Test filtering clients by email."""
        results = ClientService.filter_clients(search_query='seller@test.com')
        assert results.count() == 1
        assert results.first() == seller_client
    
    def test_get_buyers(self, db, client, seller_client):
        """Test getting buyers."""
        buyers = ClientService.get_buyers()
        assert client in buyers
        assert seller_client not in buyers
    
    def test_get_sellers(self, db, client, seller_client):
        """Test getting sellers."""
        sellers = ClientService.get_sellers()
        assert seller_client in sellers
        assert client not in sellers


# =============================================================================
# TaskService Tests
# =============================================================================

class TestTaskService:
    """Tests for the TaskService."""
    
    def test_get_all_tasks(self, db, task, overdue_task, completed_task):
        """Test getting all tasks."""
        tasks = TaskService.get_all()
        assert tasks.count() == 3
    
    def test_filter_by_status(self, db, task, overdue_task, completed_task):
        """Test filtering tasks by status."""
        pending = TaskService.filter_tasks(status=TaskStatus.PENDING)
        complete = TaskService.filter_tasks(status=TaskStatus.COMPLETE)
        
        assert pending.count() == 2
        assert complete.count() == 1
    
    def test_filter_by_priority(self, db, task, overdue_task, completed_task):
        """Test filtering tasks by priority."""
        high = TaskService.filter_tasks(priority=TaskPriority.HIGH)
        medium = TaskService.filter_tasks(priority=TaskPriority.MEDIUM)
        low = TaskService.filter_tasks(priority=TaskPriority.LOW)
        
        assert high.count() == 1
        assert medium.count() == 1
        assert low.count() == 1
    
    def test_filter_by_search(self, db, task, overdue_task, completed_task):
        """Test filtering tasks by search query."""
        results = TaskService.filter_tasks(search_query='Follow up')
        assert results.count() == 1
        assert results.first() == task
    
    def test_get_pending_tasks(self, db, task, overdue_task, completed_task):
        """Test getting pending tasks."""
        pending = TaskService.get_pending_tasks()
        assert pending.count() == 2
        assert task in pending
        assert overdue_task in pending
        assert completed_task not in pending
    
    def test_get_overdue_tasks(self, db, task, overdue_task, completed_task):
        """Test getting overdue tasks."""
        overdue = TaskService.get_overdue_tasks()
        assert overdue.count() == 1
        assert overdue_task in overdue
        assert task not in overdue  # Not overdue (future due date)
        assert completed_task not in overdue  # Not overdue (completed)
    
    def test_get_tasks_by_property(self, db, task, property_obj):
        """Test getting tasks by property."""
        tasks = TaskService.get_tasks_by_property(property_obj.pk)
        assert task in tasks
    
    def test_get_tasks_by_client(self, db, overdue_task, client):
        """Test getting tasks by client."""
        tasks = TaskService.get_tasks_by_client(client.pk)
        assert overdue_task in tasks


# =============================================================================
# CollaboratorService Tests
# =============================================================================

class TestCollaboratorService:
    """Tests for the CollaboratorService."""
    
    def test_get_all_collaborators(self, db, collaborator, manager):
        """Test getting all collaborators."""
        collaborators = CollaboratorService.get_all()
        assert collaborators.count() == 2
    
    def test_filter_by_role(self, db, collaborator, manager):
        """Test filtering collaborators by role."""
        agents = CollaboratorService.filter_collaborators(role=CollaboratorRole.AGENT)
        managers = CollaboratorService.filter_collaborators(role=CollaboratorRole.MANAGER)
        
        assert agents.count() == 1
        assert managers.count() == 1
    
    def test_filter_by_search(self, db, collaborator, manager):
        """Test filtering collaborators by search query."""
        results = CollaboratorService.filter_collaborators(search_query='John')
        assert results.count() == 1
        assert results.first() == collaborator
    
    def test_get_agents(self, db, collaborator, manager):
        """Test getting agents."""
        agents = CollaboratorService.get_agents()
        assert collaborator in agents
        assert manager not in agents
    
    def test_get_collaborator_workload(self, db, collaborator, property_obj, task):
        """Test getting collaborator workload."""
        workload = CollaboratorService.get_collaborator_workload(collaborator.pk)
        assert workload['properties'] == 1
        assert workload['pending_tasks'] == 1


# =============================================================================
# DashboardService Tests
# =============================================================================

class TestDashboardService:
    """Tests for the DashboardService."""
    
    def test_get_dashboard_stats(self, db, property_obj, sold_property, client, 
                                  seller_client, task, overdue_task, completed_task,
                                  collaborator, manager):
        """Test getting dashboard statistics."""
        stats = DashboardService.get_dashboard_stats()
        
        assert stats['property_count'] == 2
        assert stats['client_count'] == 2
        assert stats['pending_task_count'] == 2
        assert stats['collaborator_count'] == 2
        assert stats['available_properties'] == 1
        assert stats['overdue_tasks'] == 1
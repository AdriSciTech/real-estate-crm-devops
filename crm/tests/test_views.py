"""
Integration tests for CRM views.
Tests view responses, templates, and context data.
"""
import pytest
from datetime import date, timedelta
from decimal import Decimal

from django.test import Client as TestClient
from django.urls import reverse

from crm.models import Property, Client, Task, Collaborator
from crm.constants import (
    PropertyType, PropertyStatus, ClientType,
    TaskStatus, TaskPriority, CollaboratorRole
)


@pytest.fixture
def test_client():
    """Create a Django test client."""
    return TestClient()


# =============================================================================
# Home View Tests
# =============================================================================

class TestHomeView:
    """Tests for the home view."""
    
    def test_home_page_loads(self, db, test_client):
        """Test that home page loads successfully."""
        response = test_client.get(reverse('home'))
        assert response.status_code == 200
    
    def test_home_uses_correct_template(self, db, test_client):
        """Test that home uses the correct template."""
        response = test_client.get(reverse('home'))
        assert 'crm/home.html' in [t.name for t in response.templates]
    
    def test_home_contains_stats(self, db, test_client, property_obj, client, task, collaborator):
        """Test that home page contains statistics."""
        response = test_client.get(reverse('home'))
        assert 'property_count' in response.context
        assert 'client_count' in response.context


# =============================================================================
# Property View Tests
# =============================================================================

class TestPropertyViews:
    """Tests for property views."""
    
    def test_property_list_view(self, db, test_client, property_obj, sold_property):
        """Test property list view."""
        response = test_client.get(reverse('property_list'))
        assert response.status_code == 200
        assert len(response.context['properties']) == 2
    
    def test_property_list_filter_by_status(self, db, test_client, property_obj, sold_property):
        """Test filtering property list by status."""
        response = test_client.get(
            reverse('property_list'),
            {'status': PropertyStatus.AVAILABLE}
        )
        assert response.status_code == 200
        assert len(response.context['properties']) == 1
    
    def test_property_list_search(self, db, test_client, property_obj, sold_property):
        """Test searching property list."""
        response = test_client.get(
            reverse('property_list'),
            {'search': 'Test Street'}
        )
        assert response.status_code == 200
        assert len(response.context['properties']) == 1
    
    def test_property_detail_view(self, db, test_client, property_obj):
        """Test property detail view."""
        response = test_client.get(
            reverse('property_detail', kwargs={'pk': property_obj.pk})
        )
        assert response.status_code == 200
        assert response.context['property'] == property_obj
    
    def test_property_detail_404(self, db, test_client):
        """Test property detail returns 404 for non-existent property."""
        response = test_client.get(
            reverse('property_detail', kwargs={'pk': 99999})
        )
        assert response.status_code == 404
    
    def test_property_create_get(self, db, test_client):
        """Test property create form GET."""
        response = test_client.get(reverse('property_create'))
        assert response.status_code == 200
        assert 'form' in response.context
    
    def test_property_create_post(self, db, test_client):
        """Test property create form POST."""
        data = {
            'address': 'New Property Address',
            'price': '500000.00',
            'property_type': PropertyType.HOUSE,
            'status': PropertyStatus.AVAILABLE,
            'listing_date': date.today().isoformat(),
        }
        response = test_client.post(reverse('property_create'), data)
        assert response.status_code == 302  # Redirect after success
        assert Property.objects.filter(address='New Property Address').exists()
    
    def test_property_update_get(self, db, test_client, property_obj):
        """Test property update form GET."""
        response = test_client.get(
            reverse('property_update', kwargs={'pk': property_obj.pk})
        )
        assert response.status_code == 200
        assert response.context['property'] == property_obj
    
    def test_property_update_post(self, db, test_client, property_obj):
        """Test property update form POST."""
        data = {
            'address': 'Updated Address',
            'price': '600000.00',
            'property_type': PropertyType.HOUSE,
            'status': PropertyStatus.PENDING,
            'listing_date': date.today().isoformat(),
        }
        response = test_client.post(
            reverse('property_update', kwargs={'pk': property_obj.pk}),
            data
        )
        assert response.status_code == 302
        property_obj.refresh_from_db()
        assert property_obj.address == 'Updated Address'
        assert property_obj.status == PropertyStatus.PENDING
    
    def test_property_delete_get(self, db, test_client, property_obj):
        """Test property delete confirmation page."""
        response = test_client.get(
            reverse('property_delete', kwargs={'pk': property_obj.pk})
        )
        assert response.status_code == 200
    
    def test_property_delete_post(self, db, test_client, property_obj):
        """Test property delete POST."""
        pk = property_obj.pk
        response = test_client.post(
            reverse('property_delete', kwargs={'pk': pk})
        )
        assert response.status_code == 302
        assert not Property.objects.filter(pk=pk).exists()


# =============================================================================
# Client View Tests
# =============================================================================

class TestClientViews:
    """Tests for client views."""
    
    def test_client_list_view(self, db, test_client, client, seller_client):
        """Test client list view."""
        response = test_client.get(reverse('client_list'))
        assert response.status_code == 200
        assert len(response.context['clients']) == 2
    
    def test_client_list_filter_by_type(self, db, test_client, client, seller_client):
        """Test filtering client list by type."""
        response = test_client.get(
            reverse('client_list'),
            {'client_type': ClientType.BUYER}
        )
        assert response.status_code == 200
        assert len(response.context['clients']) == 1
    
    def test_client_detail_view(self, db, test_client, client):
        """Test client detail view."""
        response = test_client.get(
            reverse('client_detail', kwargs={'pk': client.pk})
        )
        assert response.status_code == 200
        assert response.context['client'] == client
    
    def test_client_create_post(self, db, test_client):
        """Test client create form POST."""
        data = {
            'name': 'New Client',
            'email': 'newclient@test.com',
            'phone': '1234567890',
            'client_type': ClientType.BUYER,
        }
        response = test_client.post(reverse('client_create'), data)
        assert response.status_code == 302
        assert Client.objects.filter(name='New Client').exists()
    
    def test_client_update_post(self, db, test_client, client):
        """Test client update form POST."""
        data = {
            'name': 'Updated Name',
            'email': client.email,
            'phone': '9876543210',
            'client_type': ClientType.BOTH,
        }
        response = test_client.post(
            reverse('client_update', kwargs={'pk': client.pk}),
            data
        )
        assert response.status_code == 302
        client.refresh_from_db()
        assert client.name == 'Updated Name'
    
    def test_client_delete_post(self, db, test_client, client):
        """Test client delete POST."""
        pk = client.pk
        response = test_client.post(
            reverse('client_delete', kwargs={'pk': pk})
        )
        assert response.status_code == 302
        assert not Client.objects.filter(pk=pk).exists()


# =============================================================================
# Task View Tests
# =============================================================================

class TestTaskViews:
    """Tests for task views."""
    
    def test_task_list_view(self, db, test_client, task, overdue_task, completed_task):
        """Test task list view."""
        response = test_client.get(reverse('task_list'))
        assert response.status_code == 200
        assert len(response.context['tasks']) == 3
    
    def test_task_list_filter_by_status(self, db, test_client, task, completed_task):
        """Test filtering task list by status."""
        response = test_client.get(
            reverse('task_list'),
            {'status': TaskStatus.COMPLETE}
        )
        assert response.status_code == 200
        assert len(response.context['tasks']) == 1
    
    def test_task_list_filter_by_priority(self, db, test_client, task, overdue_task):
        """Test filtering task list by priority."""
        response = test_client.get(
            reverse('task_list'),
            {'priority': TaskPriority.HIGH}
        )
        assert response.status_code == 200
        assert len(response.context['tasks']) == 1
    
    def test_task_detail_view(self, db, test_client, task):
        """Test task detail view."""
        response = test_client.get(
            reverse('task_detail', kwargs={'pk': task.pk})
        )
        assert response.status_code == 200
        assert response.context['task'] == task
    
    def test_task_create_post(self, db, test_client):
        """Test task create form POST."""
        data = {
            'title': 'New Task',
            'due_date': (date.today() + timedelta(days=7)).isoformat(),
            'status': TaskStatus.PENDING,
            'priority': TaskPriority.MEDIUM,
        }
        response = test_client.post(reverse('task_create'), data)
        assert response.status_code == 302
        assert Task.objects.filter(title='New Task').exists()
    
    def test_task_update_post(self, db, test_client, task):
        """Test task update form POST."""
        data = {
            'title': 'Updated Task',
            'due_date': task.due_date.isoformat(),
            'status': TaskStatus.IN_PROGRESS,
            'priority': TaskPriority.HIGH,
        }
        response = test_client.post(
            reverse('task_update', kwargs={'pk': task.pk}),
            data
        )
        assert response.status_code == 302
        task.refresh_from_db()
        assert task.title == 'Updated Task'
        assert task.status == TaskStatus.IN_PROGRESS
    
    def test_task_delete_post(self, db, test_client, task):
        """Test task delete POST."""
        pk = task.pk
        response = test_client.post(
            reverse('task_delete', kwargs={'pk': pk})
        )
        assert response.status_code == 302
        assert not Task.objects.filter(pk=pk).exists()


# =============================================================================
# Collaborator View Tests
# =============================================================================

class TestCollaboratorViews:
    """Tests for collaborator views."""
    
    def test_collaborator_list_view(self, db, test_client, collaborator, manager):
        """Test collaborator list view."""
        response = test_client.get(reverse('collaborator_list'))
        assert response.status_code == 200
        assert len(response.context['collaborators']) == 2
    
    def test_collaborator_list_filter_by_role(self, db, test_client, collaborator, manager):
        """Test filtering collaborator list by role."""
        response = test_client.get(
            reverse('collaborator_list'),
            {'role': CollaboratorRole.AGENT}
        )
        assert response.status_code == 200
        assert len(response.context['collaborators']) == 1
    
    def test_collaborator_detail_view(self, db, test_client, collaborator):
        """Test collaborator detail view."""
        response = test_client.get(
            reverse('collaborator_detail', kwargs={'pk': collaborator.pk})
        )
        assert response.status_code == 200
        assert response.context['collaborator'] == collaborator
    
    def test_collaborator_create_post(self, db, test_client):
        """Test collaborator create form POST."""
        data = {
            'name': 'New Agent',
            'email': 'newagent@test.com',
            'role': CollaboratorRole.AGENT,
        }
        response = test_client.post(reverse('collaborator_create'), data)
        assert response.status_code == 302
        assert Collaborator.objects.filter(name='New Agent').exists()
    
    def test_collaborator_update_post(self, db, test_client, collaborator):
        """Test collaborator update form POST."""
        data = {
            'name': 'Updated Name',
            'email': collaborator.email,
            'role': CollaboratorRole.MANAGER,
        }
        response = test_client.post(
            reverse('collaborator_update', kwargs={'pk': collaborator.pk}),
            data
        )
        assert response.status_code == 302
        collaborator.refresh_from_db()
        assert collaborator.name == 'Updated Name'
        assert collaborator.role == CollaboratorRole.MANAGER
    
    def test_collaborator_delete_post(self, db, test_client, collaborator):
        """Test collaborator delete POST."""
        pk = collaborator.pk
        response = test_client.post(
            reverse('collaborator_delete', kwargs={'pk': pk})
        )
        assert response.status_code == 302
        assert not Collaborator.objects.filter(pk=pk).exists()
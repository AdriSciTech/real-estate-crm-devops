"""
Service layer for the CRM application.
Handles business logic separate from views (Single Responsibility Principle).
"""

from django.db.models import Q
from typing import Optional, Dict, Any
from .models import Property, Client, Task, Collaborator
from .constants import PropertyStatus, TaskStatus


class BaseService:
    """Base service class with common functionality."""
    
    model = None
    
    @classmethod
    def get_all(cls):
        """Get all instances."""
        return cls.model.objects.all()
    
    @classmethod
    def get_by_id(cls, pk: int):
        """Get instance by primary key."""
        return cls.model.objects.get(pk=pk)
    
    @classmethod
    def create(cls, **kwargs):
        """Create a new instance."""
        return cls.model.objects.create(**kwargs)
    
    @classmethod
    def update(cls, instance, **kwargs):
        """Update an existing instance."""
        for key, value in kwargs.items():
            setattr(instance, key, value)
        instance.save()
        return instance
    
    @classmethod
    def delete(cls, instance):
        """Delete an instance."""
        instance.delete()


class PropertyService(BaseService):
    """Service for Property-related operations."""
    
    model = Property
    
    @classmethod
    def filter_properties(
        cls,
        status: Optional[str] = None,
        property_type: Optional[str] = None,
        search_query: Optional[str] = None
    ):
        """
        Filter properties based on criteria.
        Consolidates filtering logic that was duplicated in views.
        """
        queryset = cls.get_all()
        
        if status:
            queryset = queryset.filter(status=status)
        
        if property_type:
            queryset = queryset.filter(property_type=property_type)
        
        if search_query:
            queryset = queryset.filter(
                Q(address__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        
        return queryset
    
    @classmethod
    def get_available_properties(cls):
        """Get all available properties."""
        return cls.model.objects.filter(status=PropertyStatus.AVAILABLE)
    
    @classmethod
    def get_properties_by_collaborator(cls, collaborator_id: int):
        """Get properties assigned to a specific collaborator."""
        return cls.model.objects.filter(collaborator_id=collaborator_id)
    
    @classmethod
    def get_property_statistics(cls) -> Dict[str, int]:
        """Get property statistics for dashboard."""
        return {
            'total': cls.model.objects.count(),
            'available': cls.model.objects.filter(status=PropertyStatus.AVAILABLE).count(),
            'pending': cls.model.objects.filter(status=PropertyStatus.PENDING).count(),
            'sold': cls.model.objects.filter(status=PropertyStatus.SOLD).count(),
        }


class ClientService(BaseService):
    """Service for Client-related operations."""
    
    model = Client
    
    @classmethod
    def filter_clients(
        cls,
        client_type: Optional[str] = None,
        search_query: Optional[str] = None
    ):
        """Filter clients based on criteria."""
        queryset = cls.get_all()
        
        if client_type:
            queryset = queryset.filter(client_type=client_type)
        
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(email__icontains=search_query) |
                Q(phone__icontains=search_query)
            )
        
        return queryset
    
    @classmethod
    def get_buyers(cls):
        """Get all buyers."""
        return cls.model.objects.filter(
            Q(client_type='BUYER') | Q(client_type='BOTH')
        )
    
    @classmethod
    def get_sellers(cls):
        """Get all sellers."""
        return cls.model.objects.filter(
            Q(client_type='SELLER') | Q(client_type='BOTH')
        )


class TaskService(BaseService):
    """Service for Task-related operations."""
    
    model = Task
    
    @classmethod
    def filter_tasks(
        cls,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        search_query: Optional[str] = None,
        assigned_to: Optional[int] = None
    ):
        """Filter tasks based on criteria."""
        queryset = cls.get_all()
        
        if status:
            queryset = queryset.filter(status=status)
        
        if priority:
            queryset = queryset.filter(priority=priority)
        
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        
        if assigned_to:
            queryset = queryset.filter(assigned_to_id=assigned_to)
        
        return queryset
    
    @classmethod
    def get_pending_tasks(cls):
        """Get all pending tasks."""
        return cls.model.objects.filter(status=TaskStatus.PENDING)
    
    @classmethod
    def get_overdue_tasks(cls):
        """Get all overdue tasks."""
        from datetime import date
        return cls.model.objects.filter(
            due_date__lt=date.today()
        ).exclude(
            status__in=[TaskStatus.COMPLETE, TaskStatus.CANCELLED]
        )
    
    @classmethod
    def get_tasks_by_property(cls, property_id: int):
        """Get tasks related to a specific property."""
        return cls.model.objects.filter(related_property_id=property_id)
    
    @classmethod
    def get_tasks_by_client(cls, client_id: int):
        """Get tasks related to a specific client."""
        return cls.model.objects.filter(client_id=client_id)


class CollaboratorService(BaseService):
    """Service for Collaborator-related operations."""
    
    model = Collaborator
    
    @classmethod
    def filter_collaborators(
        cls,
        role: Optional[str] = None,
        search_query: Optional[str] = None
    ):
        """Filter collaborators based on criteria."""
        queryset = cls.get_all()
        
        if role:
            queryset = queryset.filter(role=role)
        
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(email__icontains=search_query)
            )
        
        return queryset
    
    @classmethod
    def get_agents(cls):
        """Get all agents."""
        return cls.model.objects.filter(role='AGENT')
    
    @classmethod
    def get_collaborator_workload(cls, collaborator_id: int) -> Dict[str, int]:
        """Get workload statistics for a collaborator."""
        collaborator = cls.model.objects.get(pk=collaborator_id)
        return {
            'properties': collaborator.properties.count(),
            'pending_tasks': collaborator.tasks.filter(status=TaskStatus.PENDING).count(),
            'in_progress_tasks': collaborator.tasks.filter(status=TaskStatus.IN_PROGRESS).count(),
        }


class DashboardService:
    """Service for dashboard statistics."""
    
    @classmethod
    def get_dashboard_stats(cls) -> Dict[str, Any]:
        """Get all dashboard statistics."""
        return {
            'property_count': Property.objects.count(),
            'client_count': Client.objects.count(),
            'pending_task_count': Task.objects.filter(status=TaskStatus.PENDING).count(),
            'collaborator_count': Collaborator.objects.count(),
            'available_properties': Property.objects.filter(
                status=PropertyStatus.AVAILABLE
            ).count(),
            'overdue_tasks': TaskService.get_overdue_tasks().count(),
        }
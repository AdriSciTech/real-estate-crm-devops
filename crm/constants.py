"""
Constants for the CRM application.
Centralizes all hardcoded values to follow DRY principle and improve maintainability.
"""

# Collaborator Roles
class CollaboratorRole:
    AGENT = 'AGENT'
    MANAGER = 'MANAGER'
    ADMIN = 'ADMIN'
    ASSISTANT = 'ASSISTANT'
    
    CHOICES = [
        (AGENT, 'Real Estate Agent'),
        (MANAGER, 'Manager'),
        (ADMIN, 'Administrator'),
        (ASSISTANT, 'Assistant'),
    ]
    
    @classmethod
    def get_display(cls, role):
        """Get display name for a role."""
        role_dict = dict(cls.CHOICES)
        return role_dict.get(role, role)


# Property Types
class PropertyType:
    HOUSE = 'HOUSE'
    CONDO = 'CONDO'
    TOWNHOUSE = 'TOWNHOUSE'
    LAND = 'LAND'
    COMMERCIAL = 'COMMERCIAL'
    
    CHOICES = [
        (HOUSE, 'House'),
        (CONDO, 'Condominium'),
        (TOWNHOUSE, 'Townhouse'),
        (LAND, 'Land'),
        (COMMERCIAL, 'Commercial'),
    ]
    
    @classmethod
    def get_display(cls, property_type):
        """Get display name for a property type."""
        type_dict = dict(cls.CHOICES)
        return type_dict.get(property_type, property_type)


# Property Status
class PropertyStatus:
    AVAILABLE = 'AVAILABLE'
    PENDING = 'PENDING'
    SOLD = 'SOLD'
    RENTED = 'RENTED'
    WITHDRAWN = 'WITHDRAWN'
    
    CHOICES = [
        (AVAILABLE, 'Available'),
        (PENDING, 'Pending'),
        (SOLD, 'Sold'),
        (RENTED, 'Rented'),
        (WITHDRAWN, 'Withdrawn'),
    ]
    
    @classmethod
    def get_display(cls, status):
        """Get display name for a status."""
        status_dict = dict(cls.CHOICES)
        return status_dict.get(status, status)


# Client Types
class ClientType:
    BUYER = 'BUYER'
    SELLER = 'SELLER'
    BOTH = 'BOTH'
    
    CHOICES = [
        (BUYER, 'Buyer'),
        (SELLER, 'Seller'),
        (BOTH, 'Buyer/Seller'),
    ]
    
    @classmethod
    def get_display(cls, client_type):
        """Get display name for a client type."""
        type_dict = dict(cls.CHOICES)
        return type_dict.get(client_type, client_type)


# Task Status
class TaskStatus:
    PENDING = 'PENDING'
    IN_PROGRESS = 'IN_PROGRESS'
    COMPLETE = 'COMPLETE'
    CANCELLED = 'CANCELLED'
    
    CHOICES = [
        (PENDING, 'Pending'),
        (IN_PROGRESS, 'In Progress'),
        (COMPLETE, 'Complete'),
        (CANCELLED, 'Cancelled'),
    ]
    
    @classmethod
    def get_display(cls, status):
        """Get display name for a status."""
        status_dict = dict(cls.CHOICES)
        return status_dict.get(status, status)


# Task Priority
class TaskPriority:
    LOW = 'LOW'
    MEDIUM = 'MEDIUM'
    HIGH = 'HIGH'
    
    CHOICES = [
        (LOW, 'Low'),
        (MEDIUM, 'Medium'),
        (HIGH, 'High'),
    ]
    
    @classmethod
    def get_display(cls, priority):
        """Get display name for a priority."""
        priority_dict = dict(cls.CHOICES)
        return priority_dict.get(priority, priority)


# Validation Constants
class ValidationConstants:
    MIN_PHONE_DIGITS = 10
    MIN_PRICE = 0
    MAX_PRICE_DIGITS = 12
    MAX_NAME_LENGTH = 100
    MAX_TITLE_LENGTH = 200
    MAX_ROLE_LENGTH = 20
    MAX_STATUS_LENGTH = 20
    MAX_TYPE_LENGTH = 20
    MAX_PRIORITY_LENGTH = 10
    MAX_PHONE_LENGTH = 20


# Success Messages
class Messages:
    PROPERTY_CREATED = 'Property "{}" created successfully!'
    PROPERTY_UPDATED = 'Property "{}" updated successfully!'
    PROPERTY_DELETED = 'Property "{}" deleted successfully!'
    
    CLIENT_CREATED = 'Client "{}" has been created.'
    CLIENT_UPDATED = 'Client "{}" has been updated.'
    CLIENT_DELETED = 'Client "{}" has been deleted.'
    
    TASK_CREATED = 'Task "{}" created successfully!'
    TASK_UPDATED = 'Task "{}" updated successfully!'
    TASK_DELETED = 'Task "{}" deleted successfully!'
    
    COLLABORATOR_CREATED = 'Collaborator "{}" created successfully!'
    COLLABORATOR_UPDATED = 'Collaborator "{}" updated successfully!'
    COLLABORATOR_DELETED = 'Collaborator "{}" deleted successfully!'
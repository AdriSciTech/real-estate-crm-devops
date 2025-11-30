"""
Unit tests for CRM constants.
Tests constant classes and their utility methods.
"""
import pytest

from crm.constants import (
    CollaboratorRole, PropertyType, PropertyStatus,
    ClientType, TaskStatus, TaskPriority, ValidationConstants, Messages
)


class TestCollaboratorRole:
    """Tests for CollaboratorRole constants."""
    
    def test_choices_exist(self):
        """Test that choices are defined."""
        assert len(CollaboratorRole.CHOICES) > 0
    
    def test_all_constants_in_choices(self):
        """Test all constants are in choices."""
        choice_values = [c[0] for c in CollaboratorRole.CHOICES]
        assert CollaboratorRole.AGENT in choice_values
        assert CollaboratorRole.MANAGER in choice_values
        assert CollaboratorRole.ADMIN in choice_values
        assert CollaboratorRole.ASSISTANT in choice_values
    
    def test_get_display(self):
        """Test get_display method."""
        assert CollaboratorRole.get_display(CollaboratorRole.AGENT) == 'Real Estate Agent'
        assert CollaboratorRole.get_display(CollaboratorRole.MANAGER) == 'Manager'
    
    def test_get_display_unknown(self):
        """Test get_display with unknown value returns the value."""
        assert CollaboratorRole.get_display('UNKNOWN') == 'UNKNOWN'


class TestPropertyType:
    """Tests for PropertyType constants."""
    
    def test_choices_exist(self):
        """Test that choices are defined."""
        assert len(PropertyType.CHOICES) > 0
    
    def test_all_constants_in_choices(self):
        """Test all constants are in choices."""
        choice_values = [c[0] for c in PropertyType.CHOICES]
        assert PropertyType.HOUSE in choice_values
        assert PropertyType.CONDO in choice_values
        assert PropertyType.TOWNHOUSE in choice_values
        assert PropertyType.LAND in choice_values
        assert PropertyType.COMMERCIAL in choice_values
    
    def test_get_display(self):
        """Test get_display method."""
        assert PropertyType.get_display(PropertyType.HOUSE) == 'House'
        assert PropertyType.get_display(PropertyType.CONDO) == 'Condominium'


class TestPropertyStatus:
    """Tests for PropertyStatus constants."""
    
    def test_choices_exist(self):
        """Test that choices are defined."""
        assert len(PropertyStatus.CHOICES) > 0
    
    def test_all_constants_in_choices(self):
        """Test all constants are in choices."""
        choice_values = [c[0] for c in PropertyStatus.CHOICES]
        assert PropertyStatus.AVAILABLE in choice_values
        assert PropertyStatus.PENDING in choice_values
        assert PropertyStatus.SOLD in choice_values
        assert PropertyStatus.RENTED in choice_values
        assert PropertyStatus.WITHDRAWN in choice_values
    
    def test_get_display(self):
        """Test get_display method."""
        assert PropertyStatus.get_display(PropertyStatus.AVAILABLE) == 'Available'
        assert PropertyStatus.get_display(PropertyStatus.SOLD) == 'Sold'


class TestClientType:
    """Tests for ClientType constants."""
    
    def test_choices_exist(self):
        """Test that choices are defined."""
        assert len(ClientType.CHOICES) > 0
    
    def test_all_constants_in_choices(self):
        """Test all constants are in choices."""
        choice_values = [c[0] for c in ClientType.CHOICES]
        assert ClientType.BUYER in choice_values
        assert ClientType.SELLER in choice_values
        assert ClientType.BOTH in choice_values
    
    def test_get_display(self):
        """Test get_display method."""
        assert ClientType.get_display(ClientType.BUYER) == 'Buyer'
        assert ClientType.get_display(ClientType.BOTH) == 'Buyer/Seller'


class TestTaskStatus:
    """Tests for TaskStatus constants."""
    
    def test_choices_exist(self):
        """Test that choices are defined."""
        assert len(TaskStatus.CHOICES) > 0
    
    def test_all_constants_in_choices(self):
        """Test all constants are in choices."""
        choice_values = [c[0] for c in TaskStatus.CHOICES]
        assert TaskStatus.PENDING in choice_values
        assert TaskStatus.IN_PROGRESS in choice_values
        assert TaskStatus.COMPLETE in choice_values
        assert TaskStatus.CANCELLED in choice_values
    
    def test_get_display(self):
        """Test get_display method."""
        assert TaskStatus.get_display(TaskStatus.PENDING) == 'Pending'
        assert TaskStatus.get_display(TaskStatus.IN_PROGRESS) == 'In Progress'


class TestTaskPriority:
    """Tests for TaskPriority constants."""
    
    def test_choices_exist(self):
        """Test that choices are defined."""
        assert len(TaskPriority.CHOICES) > 0
    
    def test_all_constants_in_choices(self):
        """Test all constants are in choices."""
        choice_values = [c[0] for c in TaskPriority.CHOICES]
        assert TaskPriority.LOW in choice_values
        assert TaskPriority.MEDIUM in choice_values
        assert TaskPriority.HIGH in choice_values
    
    def test_get_display(self):
        """Test get_display method."""
        assert TaskPriority.get_display(TaskPriority.LOW) == 'Low'
        assert TaskPriority.get_display(TaskPriority.HIGH) == 'High'


class TestValidationConstants:
    """Tests for ValidationConstants."""
    
    def test_min_phone_digits(self):
        """Test MIN_PHONE_DIGITS is defined."""
        assert ValidationConstants.MIN_PHONE_DIGITS == 10
    
    def test_max_name_length(self):
        """Test MAX_NAME_LENGTH is defined."""
        assert ValidationConstants.MAX_NAME_LENGTH == 100
    
    def test_max_title_length(self):
        """Test MAX_TITLE_LENGTH is defined."""
        assert ValidationConstants.MAX_TITLE_LENGTH == 200


class TestMessages:
    """Tests for Messages constants."""
    
    def test_property_messages(self):
        """Test property-related messages."""
        assert '{}' in Messages.PROPERTY_CREATED
        assert '{}' in Messages.PROPERTY_UPDATED
        assert '{}' in Messages.PROPERTY_DELETED
    
    def test_client_messages(self):
        """Test client-related messages."""
        assert '{}' in Messages.CLIENT_CREATED
        assert '{}' in Messages.CLIENT_UPDATED
        assert '{}' in Messages.CLIENT_DELETED
    
    def test_task_messages(self):
        """Test task-related messages."""
        assert '{}' in Messages.TASK_CREATED
        assert '{}' in Messages.TASK_UPDATED
        assert '{}' in Messages.TASK_DELETED
    
    def test_collaborator_messages(self):
        """Test collaborator-related messages."""
        assert '{}' in Messages.COLLABORATOR_CREATED
        assert '{}' in Messages.COLLABORATOR_UPDATED
        assert '{}' in Messages.COLLABORATOR_DELETED
    
    def test_message_formatting(self):
        """Test messages can be formatted."""
        formatted = Messages.PROPERTY_CREATED.format('123 Main St')
        assert '123 Main St' in formatted
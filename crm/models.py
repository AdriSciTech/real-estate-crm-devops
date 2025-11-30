"""
Models for the Real Estate CRM application.
Follows SOLID principles with clear separation of concerns.
"""

from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

from .constants import (
    CollaboratorRole, PropertyType, PropertyStatus,
    ClientType, TaskStatus, TaskPriority, ValidationConstants
)


class TimeStampedModel(models.Model):
    """
    Abstract base model that provides self-updating created_at and updated_at fields.
    Follows DRY principle by centralizing timestamp logic.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True


class Collaborator(TimeStampedModel):
    """Model representing a collaborator (agent/staff member)."""
    
    # Class-level choices for Django admin and forms
    ROLE_CHOICES = CollaboratorRole.CHOICES
    
    name = models.CharField(max_length=ValidationConstants.MAX_NAME_LENGTH)
    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=ValidationConstants.MAX_ROLE_LENGTH,
        choices=CollaboratorRole.CHOICES,
        default=CollaboratorRole.AGENT
    )
    
    def __str__(self):
        return f"{self.name} ({self.get_role_display()})"
    
    class Meta:
        ordering = ['name']
    
    @property
    def active_properties_count(self):
        """Returns count of active properties assigned to this collaborator."""
        return self.properties.exclude(status=PropertyStatus.WITHDRAWN).count()
    
    @property
    def pending_tasks_count(self):
        """Returns count of pending tasks assigned to this collaborator."""
        return self.tasks.filter(status=TaskStatus.PENDING).count()


class Property(TimeStampedModel):
    """Model representing a real estate property listing."""
    
    # Class-level choices for Django admin and forms
    PROPERTY_TYPE_CHOICES = PropertyType.CHOICES
    STATUS_CHOICES = PropertyStatus.CHOICES
    
    address = models.TextField()
    price = models.DecimalField(
        max_digits=ValidationConstants.MAX_PRICE_DIGITS,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    property_type = models.CharField(
        max_length=ValidationConstants.MAX_TYPE_LENGTH,
        choices=PropertyType.CHOICES
    )
    status = models.CharField(
        max_length=ValidationConstants.MAX_STATUS_LENGTH,
        choices=PropertyStatus.CHOICES,
        default=PropertyStatus.AVAILABLE
    )
    listing_date = models.DateField()
    collaborator = models.ForeignKey(
        Collaborator,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='properties'
    )
    bedrooms = models.IntegerField(null=True, blank=True)
    bathrooms = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        null=True,
        blank=True
    )
    square_feet = models.IntegerField(null=True, blank=True)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.address} - ${self.price:,.2f}"
    
    class Meta:
        ordering = ['-listing_date']
        verbose_name_plural = "Properties"
    
    @property
    def is_available(self):
        """Check if property is available."""
        return self.status == PropertyStatus.AVAILABLE
    
    @property
    def interested_clients_count(self):
        """Returns count of clients interested in this property."""
        return self.interested_clients.count()
    
    def mark_as_sold(self):
        """Mark property as sold."""
        self.status = PropertyStatus.SOLD
        self.save(update_fields=['status', 'updated_at'])
    
    def mark_as_pending(self):
        """Mark property as pending."""
        self.status = PropertyStatus.PENDING
        self.save(update_fields=['status', 'updated_at'])


class Client(TimeStampedModel):
    """Model representing a client (buyer/seller)."""
    
    # Class-level choices for Django admin and forms
    CLIENT_TYPE_CHOICES = ClientType.CHOICES
    
    name = models.CharField(max_length=ValidationConstants.MAX_NAME_LENGTH)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=ValidationConstants.MAX_PHONE_LENGTH)
    client_type = models.CharField(
        max_length=ValidationConstants.MAX_TYPE_LENGTH,
        choices=ClientType.CHOICES
    )
    properties_interested = models.ManyToManyField(
        Property,
        related_name='interested_clients',
        blank=True
    )
    properties_owned = models.ManyToManyField(
        Property,
        related_name='owners',
        blank=True
    )
    notes = models.TextField(blank=True)
    created_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} ({self.get_client_type_display()})"
    
    class Meta:
        ordering = ['name']
    
    @property
    def is_buyer(self):
        """Check if client is a buyer."""
        return self.client_type in [ClientType.BUYER, ClientType.BOTH]
    
    @property
    def is_seller(self):
        """Check if client is a seller."""
        return self.client_type in [ClientType.SELLER, ClientType.BOTH]
    
    @property
    def total_properties_interested(self):
        """Returns total count of properties client is interested in."""
        return self.properties_interested.count()


class Task(TimeStampedModel):
    """Model representing a task/reminder."""
    
    # Class-level choices for Django admin and forms
    STATUS_CHOICES = TaskStatus.CHOICES
    PRIORITY_CHOICES = TaskPriority.CHOICES
    
    title = models.CharField(max_length=ValidationConstants.MAX_TITLE_LENGTH)
    description = models.TextField(blank=True)
    due_date = models.DateField()
    status = models.CharField(
        max_length=ValidationConstants.MAX_STATUS_LENGTH,
        choices=TaskStatus.CHOICES,
        default=TaskStatus.PENDING
    )
    priority = models.CharField(
        max_length=ValidationConstants.MAX_PRIORITY_LENGTH,
        choices=TaskPriority.CHOICES,
        default=TaskPriority.MEDIUM
    )
    related_property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='tasks'
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='tasks'
    )
    assigned_to = models.ForeignKey(
        Collaborator,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tasks'
    )
    
    def __str__(self):
        return f"{self.title} - Due: {self.due_date}"
    
    class Meta:
        ordering = ['due_date', '-priority']
    
    @property
    def is_overdue(self):
        """Check if task is overdue."""
        from datetime import date
        return self.due_date < date.today() and self.status not in [
            TaskStatus.COMPLETE, TaskStatus.CANCELLED
        ]
    
    @property
    def is_high_priority(self):
        """Check if task is high priority."""
        return self.priority == TaskPriority.HIGH
    
    def mark_complete(self):
        """Mark task as complete."""
        self.status = TaskStatus.COMPLETE
        self.save(update_fields=['status', 'updated_at'])
    
    def mark_in_progress(self):
        """Mark task as in progress."""
        self.status = TaskStatus.IN_PROGRESS
        self.save(update_fields=['status', 'updated_at'])
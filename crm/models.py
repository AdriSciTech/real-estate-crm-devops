from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class Collaborator(models.Model):
    """Model representing a collaborator (agent/staff member)."""
    ROLE_CHOICES = [
        ('AGENT', 'Real Estate Agent'),
        ('MANAGER', 'Manager'),
        ('ADMIN', 'Administrator'),
        ('ASSISTANT', 'Assistant'),
    ]
    
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='AGENT')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.role})"
    
    class Meta:
        ordering = ['name']


class Property(models.Model):
    """Model representing a real estate property listing."""
    PROPERTY_TYPE_CHOICES = [
        ('HOUSE', 'House'),
        ('CONDO', 'Condominium'),
        ('TOWNHOUSE', 'Townhouse'),
        ('LAND', 'Land'),
        ('COMMERCIAL', 'Commercial'),
    ]
    
    STATUS_CHOICES = [
        ('AVAILABLE', 'Available'),
        ('PENDING', 'Pending'),
        ('SOLD', 'Sold'),
        ('RENTED', 'Rented'),
        ('WITHDRAWN', 'Withdrawn'),
    ]
    
    address = models.TextField()
    price = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='AVAILABLE')
    listing_date = models.DateField()
    collaborator = models.ForeignKey(
        Collaborator, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='properties'
    )
    bedrooms = models.IntegerField(null=True, blank=True)
    bathrooms = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    square_feet = models.IntegerField(null=True, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.address} - ${self.price:,.2f}"
    
    class Meta:
        ordering = ['-listing_date']
        verbose_name_plural = "Properties"


class Client(models.Model):
    """Model representing a client (buyer/seller)."""
    CLIENT_TYPE_CHOICES = [
        ('BUYER', 'Buyer'),
        ('SELLER', 'Seller'),
        ('BOTH', 'Buyer/Seller'),
    ]
    
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    client_type = models.CharField(max_length=10, choices=CLIENT_TYPE_CHOICES)
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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.client_type})"
    
    class Meta:
        ordering = ['name']


class Task(models.Model):
    """Model representing a task/reminder."""
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETE', 'Complete'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    PRIORITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='MEDIUM')
    property = models.ForeignKey(
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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} - Due: {self.due_date}"
    
    class Meta:
        ordering = ['due_date', '-priority']
from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
from django.core.exceptions import ValidationError

class Flower(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=0)
    image = models.ImageField(upload_to='flowers/' ,blank=True, null=True)
    quantity_available = models.IntegerField()
    date_added = models.DateField(auto_now_add=True)
    category = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Denied', 'Denied'),
    ]

    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    date_ordered = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    delivery_address = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"Order #{self.id} - {self.customer.username}"

    def update_total_price(self):
        # Calculate the total price based on the sum of all OrderItem subtotals
        self.total_price = sum(item.subtotal for item in self.orderitem_set.all())
        self.save()

class OrderItem(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    flower = models.ForeignKey('Flower', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, editable=False)

    def __str__(self):
        return f"{self.quantity} x {self.flower.name} in Order #{self.order.id}"

    def clean(self):
        # Check if subtotal is not already provided
        if not self.subtotal:
            # Calculate subtotal based on quantity and price
            if self.quantity is not None and self.flower is not None and self.flower.price is not None:
                self.subtotal = Decimal(self.quantity) * self.flower.price
            else:
                raise ValidationError({'subtotal': 'Subtotal calculation failed. Ensure quantity and price are provided.'})

        # Check if quantity is within available quantity
        if self.quantity is not None and self.flower is not None and self.quantity > self.flower.quantity_available:
            raise ValidationError({'quantity': 'Quantity exceeds available quantity for this flower.'})

    def save(self, *args, **kwargs):
        self.clean()  # Run the clean method before saving
        super().save(*args, **kwargs)

        # Update the related Order's total_price
        self.order.update_total_price()

    def update_subtotal(self):
        # Recalculate subtotal based on quantity and price
        if self.quantity is not None and self.flower is not None and self.flower.price is not None:
            self.subtotal = Decimal(self.quantity) * self.flower.price
            self.save()
        else:
            raise ValueError('Cannot update subtotal. Ensure quantity, flower, and flower price are provided.')

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    phone_number = models.CharField(max_length=11)
    address = models.TextField()
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    birthday = models.DateField(null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], blank=True, null=True)

    def __str__(self):
        return self.user.username
    
class Review(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    flower = models.ForeignKey(Flower, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
      return f"Review by {self.customer.username} for {self.flower.name}"
 

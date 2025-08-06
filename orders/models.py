from django.db import models
from django.contrib.auth.models import User
from products.models import Product
import datetime
import random
import string

def order_ID():
    # Get day abbreviation: e.g., "Mon", "Tue", "Wed"
    prefix = datetime.datetime.now().strftime("%a").upper()  # → "WED" for Wednesday
    suffix = "R"
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    random_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=3))
    return f"{prefix}-{timestamp}{random_code}{suffix}"


class Order(models.Model):
    STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    order_id = models.CharField(default=order_ID, max_length=30,unique=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    def __str__(self):
        return f"Order #{self.order_id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()

    def total(self):
        return self.price * self.quantity
    def __str__(self):
        return f"{self.quantity} × {self.product.name if self.product else 'Deleted Product'} (Order #{self.order.order_id})"

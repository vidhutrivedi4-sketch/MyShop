from django.db import models
from django.contrib.auth.models import User


# CATEGORY MODEL
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# PRODUCT MODEL
# PRODUCT MODEL
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    description = models.TextField(blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


# ORDER MODEL
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

    status = models.CharField(
        max_length=20,
        default='Placed'
    )

    def __str__(self):
        return f"Order {self.id}"


# ORDER ITEM MODEL
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
from django.db import models
from django.contrib.auth.models import User

class Productdetails(models.Model):
    
    image = models.ImageField(upload_to='products/')
    product_name = models.CharField(max_length=200)
    price = models.IntegerField()
    quantity = models.CharField()
    description = models.TextField()

    def __str__(self):
        return self.product_name

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Productdetails, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'product')

class cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Productdetails, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.username} - {self.product.product_name} (Quantity: {self.quantity})"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Productdetails, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"


class UserProfile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )

    phone = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )

    address = models.TextField(
        blank=True,
        null=True
    )

    city = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    state = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    country = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.user.username
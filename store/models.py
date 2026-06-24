from django.db import models

from django.contrib.auth.models import User
from django.core.validators import RegexValidator
class Category(models.Model):
    name=models.CharField(max_length=50,unique=True)
    slug=models.SlugField(unique=True)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    name=models.CharField(max_length=60)
    image=models.ImageField(upload_to='images/',null=True,blank=True)
    description=models.TextField()
    price=models.DecimalField(max_digits=10,decimal_places=2)
    stock=models.PositiveIntegerField()
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return f"{self.name}->{self.stock}"
    
class Address(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    full_name=models.CharField(max_length=40)
    email=models.EmailField()
    mobile_validate=RegexValidator(regex=r'^[6-9][0-9]{9}$',message='Enter a valid 10-digit mobile number')
    mobile=models.CharField(max_length=15,validators=[mobile_validate])
    address_line = models.TextField()
    state = models.CharField(max_length=50)
    city=models.CharField(max_length=50)
    pincode=models.CharField(max_length=10)

    def __str__(self):
        return f"{self.user.username}-{self.city}"
    
class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Cart"
    
    @property
    def total(self):
        return sum(item.subtotal for item in self.items.all())

class Cartitem(models.Model):
    cart=models.ForeignKey(Cart,related_name='items',on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    class Meta:
        unique_together = ('cart', 'product')

    def __str__(self):
        return f"{self.product.name}-{self.quantity}"
    
    @property
    def subtotal(self):
        return self.product.price * self.quantity


class Order(models.Model):
    order_status = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('packed', 'Packed'),
        ('shipped', 'Shipped'),
        ('out_for_delivery', 'Out For Delivery'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    user=models.ForeignKey(User,on_delete=models.CASCADE)
    totalamount=models.DecimalField(max_digits=10,decimal_places=2)
    status=models.CharField(max_length=40,choices=order_status,default='pending')
    address=models.ForeignKey(Address,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Order"
    
    @property
    def total(self):
        return sum(item.price * item.quantity for item in self.items.all())
    
class OrderItem(models.Model):
    order=models.ForeignKey(Order,related_name='items',on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    price=models.DecimalField(max_digits=10,decimal_places=2)

    def __str__(self):
        return f"{self.product.name}-{self.quantity}"
    
    @property
    def subtotal(self):
        return self.price * self.quantity
    
    def save(self, *args, **kwargs):
        if self.pk is None:
            if self.product.stock < self.quantity:
                raise ValueError("Not enough stock available")

            self.product.stock -= self.quantity
            self.product.save()

        super().save(*args, **kwargs)
        
    

class Payment(models.Model):
    payment_method = [
        ('upi', 'UPI'),
        ('cod', 'Cash On Delivery'),
    ]

    payment_status = [
        ('pending', 'Pending'),
        ('verified', 'Verified'),
        ('success', 'Success'),
        ('failure', 'Failure'),
    ]

    order=models.OneToOneField(Order,on_delete=models.CASCADE)
    totalamount=models.DecimalField(max_digits=10,decimal_places=2)
    method=models.CharField(max_length=10,choices=payment_method)
    status=models.CharField(max_length=15,choices=payment_status,default='pending')
    transaction_id=models.CharField(max_length=200,blank=True,null=True,unique=True)
    created_at=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.order.user.username}--{self.status}"
    



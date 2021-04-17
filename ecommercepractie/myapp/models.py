from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    full_name=models.CharField(max_length=100)
    address=models.CharField(max_length=100)
    joined_on=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name

class Category(models.Model):
    title=models.CharField(max_length=100)
    image=models.ImageField(upload_to="cat_pics",blank=True)
    slug=models.SlugField(unique=True,blank=True)
    def __str__(self):
        return self.title

class Product(models.Model):
    title=models.CharField(max_length=100)
    slug=models.SlugField(unique=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    image=models.ImageField(upload_to="post_pics")
    mark_price=models.PositiveIntegerField()
    sell_price=models.PositiveIntegerField()
    description=models.TextField()
    warranty=models.CharField(max_length=100)
    return_policy=models.CharField(max_length=100)
    viewcount=models.PositiveIntegerField()

    def __str__(self):
        return self.title
class ProductImage(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    image=models.ImageField(upload_to='post_pics')

    def __str__(self):
        return self.product.title

class Cart(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True,blank=True)
    total=models.PositiveIntegerField()
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Cart "+str(self.id)

class CartProduct(models.Model):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    rate=models.PositiveIntegerField()
    quantity=models.PositiveIntegerField()
    subtotal=models.PositiveIntegerField()

    def __str__(self):
        return "Cart: "+str(self.cart.id)+str(self.id)

ORDER_STATUS=(('order received','Order Received'),
              ('order processing','Order Processing'),
              ('on the way','On The Way'),
              ('order completed','Order Completed'),

)

class Order(models.Model):
    cart=models.OneToOneField(Cart,on_delete=models.CASCADE)
    order_by=models.CharField(max_length=264,blank=True)
    shipping_address=models.CharField(max_length=100)
    mobile=models.CharField(max_length=100)
    email=models.EmailField()
    subtotal=models.PositiveIntegerField()
    discount=models.PositiveIntegerField()
    total=models.PositiveIntegerField()
    order_status=models.CharField(max_length=264,choices=ORDER_STATUS)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Order "+str(self.id)

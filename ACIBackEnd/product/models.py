from django.db import models
from shared.models import ACIModel
from django.utils import timezone

from shared.exception import ACIValidationError


from copy import deepcopy

# Create your models here.

def get_local_timezone():
    return timezone.localdate(timezone.now())

class Product(ACIModel):
    class Meta:
        db_table = 'products'
        verbose_name = 'Produkt'
        verbose_name_plural = 'Produktet'

    sku_code = models.CharField(unique=True, max_length=100)
    buy_price = models.FloatField()
    sell_price = models.FloatField()
    description = models.TextField(null=True, blank=True)
    brand = models.ForeignKey('Brand', related_name='products', on_delete=models.CASCADE)
    stock = models.PositiveIntegerField()
    discount = models.FloatField(default=0)
    has_discount = models.BooleanField(default=False)
    name = models.CharField(max_length=100)
    main_image = models.ImageField(upload_to='images/', null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.discount > 100 or self.discount < 0:
            raise ACIValidationError("Ca je tu bo mer jau, e nxorre kompanin berrnut")
        if self.discount > 0:
            self.has_discount = True
        else:
            self.has_discount = False
        if self.discount > 1:
            self.discount = self.discount / 100
        super(Product, self).save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.name} {str(self.brand)}"

class ProductBuyOrder(ACIModel):
    class Meta:
        db_table = 'product_buy_order'
        
    product = models.ForeignKey(Product, related_name='product_buy_orders', on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)


class Brand(ACIModel):
    class Meta:
        db_table = 'brand'
        verbose_name = 'brand'
        verbose_name_plural = 'brandet'

    name = models.CharField(max_length=100, unique=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.name


class Category(ACIModel):
    class Meta:
        db_table = 'category'
        verbose_name = 'Kategori'
        verbose_name_plural = 'Kategoritë'

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class ProductCategory(ACIModel):
    class Meta:
        db_table = 'product_category'
        unique_together = ('product', 'category')

    product = models.ForeignKey(Product, related_name='product_categories', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', related_name='product_categories', on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.product) + " " + str(self.category)


class Order(ACIModel):
    class Meta:
        db_table = 'transaction_order'
        verbose_name = 'Order'
        verbose_name_plural = 'Orderat'

    transaction_time = models.DateTimeField(auto_now_add=True)
    client_secret = models.CharField(null=True, blank=True, max_length=100)
    is_paid_online = models.BooleanField(default=False)
    printed_recipt = models.BooleanField(default=False)
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=100, null=True, blank=True)
    is_admin = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.client_secret:
            self.is_paid_online = True
        return super(Order, self).save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.email} {self.transaction_time}"

class OrderProduct(ACIModel):
    class Meta:
        db_table = 'order_product'
        verbose_name = 'Order_Product'
        verbose_name_plural = 'Order_Productet'
        unique_together = ('order', 'product')

    order = models.ForeignKey(Order, related_name='order_products', on_delete=models.CASCADE)
    product: Product = models.ForeignKey(Product, related_name='order_products', on_delete=models.CASCADE)
    product_count = models.IntegerField()
    sell_price = models.FloatField()
    buy_price = models.FloatField(null=True, blank=True)
    discount = models.FloatField()
    total_price = models.FloatField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            if self.product_count > self.product.stock:
                raise ACIValidationError("Sbohet Fjal, Ik mshpi")
            if not self.order.is_admin:
                self.sell_price = self.product.sell_price
                self.discount = self.product.discount
            if self.discount > 1:
                self.discount = self.discount / 100
            self.buy_price = self.product.buy_price
            self.total_price = (self.sell_price - self.sell_price * self.discount) * self.product_count
            product_popularity, exists = ProductPopularity.objects.get_or_create(product=self.product)
            if exists:
                product_popularity.product_count = models.F('product_count') + self.product_count
            else:
                product_popularity.product_count = product_popularity.product_count + self.product_count
            product_popularity.save()
            self.product.stock = self.product.stock - self.product_count
            self.product.save()
        return super(OrderProduct, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.product} {self.order}"

class ProductPopularity(ACIModel):
    class Meta:
        db_table = 'product_popularity'

    product = models.ForeignKey(Product, related_name='product_popularities', on_delete=models.CASCADE)
    product_count = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.product} {self.product_count}" 


class ProductImage(ACIModel):
    class Meta:
        db_table = 'product_image'
        verbose_name = 'Imazh Produkti'
        verbose_name_plural = 'Imazhet e Produktit'

    image = models.ImageField(upload_to='images/')
    product = models.ForeignKey(Product, related_name='product_images', on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Image {self.product}"





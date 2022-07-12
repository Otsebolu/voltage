from django.db import models
from django.contrib.auth.models import User

# Create your models here.

STATUS = [
    ('new', 'new'),
    ('pending', 'pending'), 
    ('processing', 'processing'),
    ('resolved', 'resolved'),
      ]
class Contact(models.Model):
    full_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    message = models.TextField()
    admin_note = models.TextField()
    status = models.CharField(max_length=50, choices = STATUS, default ='new')
    message_date = models.DateTimeField(auto_now_add=True)
    admin_update = models.DateTimeField(auto_now=True)




#customise by letting each person name to show at the DB
    def __str__(self):
        return self.full_name


#customise name of the table 
    class Meta:
        db_table = 'contact'
        managed = True
        verbose_name = 'Contact'
        verbose_name_plural = 'Contact'


class Product(models.Model):
    title = models.CharField(max_length=250)    # title= name of product
    img = models.ImageField(upload_to ='product', default='prod.jpg')
    price = models.IntegerField()
    max_quantity = models.IntegerField()
    min_quantity =models.IntegerField(default=1, editable=False)
    display = models.BooleanField()
    latest = models.BooleanField(default=False)
    trending = models.BooleanField(default=False)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title
    
    class Meta:
        db_table = 'product'
        managed = True
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


class Profile(models.Model):    #adding additional information in the form not in the default Django <User> model. create a new model"Profile"
    user = models.OneToOneField(User, on_delete=models.CASCADE)   #to connect Profile table to User Model, Relationship field
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=225)
    state = models.CharField(max_length=255)
    pix = models.ImageField(upload_to='profile', default='avatar.png') #optional to inherit default image avatar
    

    def __str__(self):
        # return self.user.username #to turn this code on,comment <pix = models.ImageField ...> above and comment <return self.first_name> below
        return self.first_name

    class Meta:
        db_table = 'profile'
        managed = True
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

class Shopcart(models.Model):    # Shopcart() creaing a basket for shopping
    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)  #editable=False so admin cannot edit it
    product = models.ForeignKey(Product, on_delete=models.CASCADE, editable=True)
    quantity = models.IntegerField()
    price = models.IntegerField(editable=False)
    amount = models.FloatField(blank=True, null=True)
    order_no =models.CharField(max_length=255,editable=True)
    paid = models.BooleanField(default=False, editable=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=True)

    def __str__(self):
        return self.product.title








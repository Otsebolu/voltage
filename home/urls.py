from django.urls import path
from . import views
from .views import CheckoutView


urlpatterns = [
    path('', views.index, name='index'),
    path('contact', views.contact, name='contact'),  #for form only in the contact in contact.html
    path('products', views.products, name='products'), #create a url path for product
    path('details/<str:id>', views.details, name='details'),
    path('signout', views.signout, name = 'signout'),
    path('signin', views.signin, name = 'signin'),
    path('signup', views.signup, name='signup'),
    path('profile', views.profile, name='profile'),
    path('profile_update', views.profile_update, name='profile_update'),
    path('password', views.password, name='password'),
    path('shopcart', views.shopcart, name='shopcart'),
    path('displaycart', views.displaycart, name='displaycart'),
    path('deleteitem', views.deleteitem, name='deleteitem'),
    path('increase', views.increase, name='increase'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('pay', views.pay, name='pay'),
    path('callback', views.callback, name='callback'),  #after payment it redirects u to callback
]
import uuid
import json
import requests

# from multiprocessing import context
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import View
 
from .forms import * #ContactForm, SignupForm, ProfileUpdate, ShopcartForm
from .models import * #Product, Profile, Shopcart
   #ends here for tuesday class

# Create your views here.

def index(request):
    # return  HttpResponse("Hey there I gladly welcome me to Django!")
    latest = Product.objects.filter(latest=True)   #reading from the db
    trending = Product.objects.filter(trending=True)
    # trending = Product.objects.all()

    context = {
        'vic':latest,
        'math': trending,
    }

    return render(request, 'index.html', context)

def contact(request):
    form = ContactForm() #instantiate the <ContactForm> from forms.py for a GET request. in my own words, create a copy of contactform.   
    if request.method == 'POST':  #make a POST REQUEST     in my words,  get form ready for users to fill form, 
        form = ContactForm(request.POST)   #instantiate the contactform for a POST request.   in my words, form shd get set to post 
        if form.is_valid(): # Django will validate the form, in my words, check if form is valid or ok for submission
            form.save() # if valid, save the data to the DB
            messages.success(request, 'I don receive your message')   #added later on monday class 13/6/22
            return redirect('index') #return to index once the post action is carried out
    return render(request, 'index.html')


def products(request):
    product = Product.objects.all()   #query the db to display all the products

    context = {
        'product':product,
    }
    return render(request, 'products.html', context)



def details(request, id):
    detail = Product.objects.get(pk=id)


    context = {
        'detail':detail,

    }

    return render(request, 'details.html', context)



#Authentication

#to logout/signout
def signout(request):
    logout(request)
    return redirect('signin')


def signin(request):
    if request.method == 'POST':
        usernamee =request.POST['username']
        passwrodd = request.POST['password']
        user = authenticate(request, username=usernamee, password=passwrodd)

        if user is not None:                 # <if user> is used also
            login(request, user)
            messages.success(request, 'Signin Successful')
            return redirect('index')
        else:
            messages.error(request, 'Username/Password incorrect. Kindly supply valid details')
            return redirect('signin')
    return render(request, 'signin.html')

def signup(request):
    form = SignupForm()    #instantiate the <SignupForm> from forms.py for a GET request
    if request.method == 'POST':    #make a POST REQUEST
        phone = request.POST['phone']       #from templates-signup.html
        address = request.POST['address']   #from templates-signup.html
        state = request.POST['state']       #from templates-signup.html
        form = SignupForm(request.POST)  #instantiate the Signupform for a POST request
        if form.is_valid():              # Django will validate the form
            newuser = form.save()        # if valid, save the data to the DB     
            userprofile = Profile(user = newuser)    #Links <User> table and <Profile>, inserting a new user into the profile table,  populating the Profile at the DB(BACKEND)
            userprofile.first_name = newuser.first_name    #Links <User> table and <Profile> 
            userprofile.last_name = newuser.last_name      #Links <User> table and <Profile> 
            userprofile.email = newuser.email               #Links <User> table and <Profile> 
            userprofile.phone = phone                       #Links <User> table and <Profile> 
            userprofile.address = address                   #Links <User> table and <Profile> 
            userprofile.state = state                       #Links <User> table and <Profile> 
            userprofile.save()
            login(request, newuser)
            messages.success(request, 'Signup Successful!')
            return redirect('index')
        else:
            messages.error(request, form.errors)
            return redirect('signup')
    return render(request, 'signup.html')
    

#Authentication done


 
@login_required(login_url='signin')
def profile(request):                                                       #populating the Profile at theFRONTEND/WEBSITE. When a new user registers/signs up/logs in, and then click the <Profile> menu button 
    profile = Profile.objects.get(user__username = request.user.username)   #user:from Profile model, username: from Users table at the DB, thats BACKEND

    context = {
        'profile':profile
    }

    return render(request, 'profile.html', context)

@login_required(login_url='signin')
def profile_update(request):
    profile=Profile.objects.get(user__username = request.user.username)
    update=ProfileUpdate(instance=request.user.profile)#instantiate the form for a GET request along with the user's details
    if request.method=='POST':
        update = ProfileUpdate(request.POST, request.FILES, instance= request.user.profile)
        if  update.is_valid():
            update.save()
            messages.success(request,'Profile update successful')
            return redirect('profile')
        else:
            messages.error(request, update.errors)
            return redirect('profile_update')

    context = {
        'profile':profile,
        'update':update,
    }
    return render(request, 'profile_update.html',context)


@login_required(login_url='signin')
def password(request):
    profile=Profile.objects.get(user__username = request.user.username)
    form = PasswordChangeForm(request.user)
    if request.method =='POST':    #POST is from the form in the template
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request,user)
            messages.success(request, 'Password change succesful.')
            return redirect('profile')
        else: 
            messages.error(request, form.errors)
            return redirect('password')
    
    context = {
        'form':form
    }
    return render(request, 'password.html', context)

# shopcart
def shopcart(request):      #loading ur basket/cart
    if request.method =='POST': #make a POST REQUEST
        quant = int(request.POST['quantity'])  ##from templates details.html
        item_id = request.POST['product_id'] ##from templates details.html
        item = Product.objects.get(pk=item_id)  # doing a get request from DB, querying the DB to get a particular product id or item id
        order_num = Profile.objects.get(user__username = request.user.username) #getting the owner of the particular product id
        cart_no = order_num.id  #tying the owner of an item/product to a cart/basket

    cart =Shopcart.objects.filter(user__username = request.user.username, paid=False) #Shopper with unpaid items. shopper having loaded items or loading items into basket/cart
    if cart:  #existing Shopcart with a select item(s)
        basket = Shopcart.objects.filter(product=item.id, user__username = request.user.username).first() #existing Shopcart with a select item(s). basket represents added items at the backend, one line at backend is items in basket due for payment
        if basket:                                                                                #.first() takes care of .get(which increases a particular item) and .filter (adds a new item).  .first() takes care of both .get and .filter= adds a new item and increases a particular item
            basket.quantity += quant # (incrementing the quantity of items in basket)
            basket.amount = basket.price * quant 
            basket.save()
            messages.success(request, 'Product added to Shopcart')
            return redirect('products')
        else:
            newitem=Shopcart()
            newitem.user=request.user
            newitem.product=item
            newitem.quantity=quant
            newitem.price=item.price
            newitem.amount = item.price * quant 
            newitem.order_no= cart_no
            newitem.paid=False
            newitem.save()
            messages.success(request,'items added to cart')
            return redirect('products')
            

    else:
        newcart = Shopcart() #create a new shopcart instance from shopcart model. Shopcart()= an empty basket. #CREATE AN ORDER FOR THE FIRST TIME
        newcart.user =request.user #saving into the fields at db
        newcart.product = item    #saving into the fields at db
        newcart.quantity = quant   #saving into the fields at db    used to collect value from template
        newcart.price = item.price   #saving into the fields at db
        newcart.amount = item.price * quant 
        newcart.order_no = cart_no  #saving into the fields at db
        newcart.paid = False      #saving into the fields at db
        newcart.save()
        messages.success(request, 'Item added to Shopcart.')
        return redirect('products')
       

    return redirect('products')



@login_required(login_url='signin')
def displaycart(request):  # pulling out itens for payment
    trolley = Shopcart.objects.filter(user__username=request.user.username, paid=False)
    profile = Profile.objects.get(user__username= request.user.username) #querying profile to pulll data fromn DB into Delivery

    
    subtotal = 0
    vat = 0
    total = 0

    for cart in trolley:
        subtotal += cart.price * cart.quantity
    
    vat =  0.075 * subtotal
    total = vat + subtotal


    context = {
        'trolley':trolley,
        'profile':profile,
        'subtotal':subtotal,
        'vat':vat,
        'total':total,

    }
    return render(request, 'displaycart.html', context)

@login_required(login_url='signin')
def deleteitem(request):   #removing items from the cart incase of no enough money or anything
    item_id = request.POST['item_id']   #item_id to come from template, display.html 
    item_delete = Shopcart.objects.get(pk=item_id)    
    item_delete.delete()
    messages.success(request, 'item deleted successfully.')
    return redirect('displaycart')

#All the 3 functions above constitute create an order########   
@login_required(login_url='signin')
def increase(request):
    if request.method =='POST':
        the_item = request.POST['itemid']     #POST['itemid'] = pulling data from templates(displaycart.html) Line51 <name="itemid"> and posting to DB. <name> :To post
        the_quant = int(request.POST['quant'])       #POST['itemid'] = pulling data from templates(displaycart.html) Line52 <name= "quant">  and posting to DB. <name> :To post
        modify= Shopcart.objects.get(pk=the_item)     
        modify.quantity += the_quant
        modify.amount = modify.price * modify.quantity
        modify.save() 
    return redirect('displaycart')
 
# shopcart done

#value="{{item.id}} templates(displaycart.html)  LINE 51 : <value> To retrieve from BD


#checkout using class based view and axios get request . Asynchronous technique
class CheckoutView(View):       #using class to generate fxn instead of function def
    def get(self, request, *args, **kwargs):
        summary = Shopcart.objects.filter(user__username = request.user.username, paid=False)        #we query the <Shopcart> table to retrieve data for the <checkout>
    
        subtotal = 0
        vat = 0
        total = 0

        for cart in summary:
            subtotal += cart.price * cart.quantity
        
        vat =  0.075 * subtotal
        total = vat + subtotal


        context = {
            'summary':summary,
            'total':total,
        }

        return render(request, 'checkout.html', context)  

#checkout using class based view and axios get request done
@login_required(login_url='signin')
def pay(request):
    # integrating to paystack
    api_key = 'sk_test_fc4d2dd13504de35c670a839bcfe7af0e45e2ecb'
    curl = 'https://api.paystack.co/transaction/initialize'
    cburl = 'http://3.91.232.247/callback'     # paste the public ipv4 "ip address" from aws here when deploying, on my local pc: this url must tally with the one running the server. we can use this one if server link is having error. if u change the port at the server at terminal, change this port as well :http://127.0.0.1:8000/callback
    user = User.objects.get(username = request.user.username)
    email = user.email
    total = float(request.POST['total']) * 100
    cart_no = user.profile.id
    transac_code = str(uuid.uuid4())
 

    headers = {'Authorization': f'Bearer {api_key}'}
    data = {'reference': transac_code, 'amount':int(total), 'email':email, 'order_number':cart_no, 'callback_url':cburl, 'currency':'NGN'}

    #integrating to paystack

    try:
        r = requests.post(curl, headers=headers, json=data)
    except Exception:
        messages.error(request, 'Network busy, refresh and try again')
    else:
        transback = json.loads(r.text)
        rdurl = transback['data']['authorization_url']
        return redirect(rdurl)
    return redirect('displaycart')

def callback(request):
    profile=Profile.objects.get(user__username = request.user.username)
    cart = Shopcart.objects.filter(user__username = request.user.username,  paid =False)    #started here 11/07/22

    for pro in cart:
        pro.paid = True
        pro.save()

        stock= Product.objects.get(pk=pro.product.id)
        stock.max_quantity -= pro.quantity
        stock.save()
    
    
    context = {
        'profile':profile,
    }
    return render(request, 'callback.html', context)

def readcart(request):
    cart = Shopcart.objects.filter(user__username = request.user.username, paid =  False)

    cartcount = 0
    for count in cart:
        cartcount += count.quantity

    context = {
        ' cartcount' :  cartcount
    }

    return context


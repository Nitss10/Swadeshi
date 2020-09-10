from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.hashers import make_password

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Agent, User, Manufacturer, Category, Product
from .serializer import AgentSerializer
# Create your views here.


# ----- Login/Signup ------

def login_agent(request):
    if request.method == 'POST' :
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        if user is not None:
            if user.is_agent == True:
                login(request, user)
                return redirect('agent_dashboard')
            else:
                messages.info(request, 'Email or password incorrect!')
                return redirect('agent_login')
        else:
            messages.info(request, 'Email or password incorrect!')
            return redirect('agent_login')
    else:
        if request.user.is_authenticated: 
            if request.user.is_agent:
                return redirect('agent_login')
        return render(request, 'local/loginagent.html')
    
def logout_agent(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('/')
    else:
        return redirect('agent_login') 

def signup_agent(request):
    if request.method == 'POST' :
        name = request.POST['name']
        email = request.POST['email']
        mobile = request.POST['mobile']
        password = request.POST['password']
        address = request.POST['address']
        aadhar = request.POST['aadhar']
        pincode = request.POST['pincode']
        image = request.FILES['image']

        if User.objects.filter(mobile = mobile).exists():
            return render(request, 'local/signup.html', {"errmsg": "Mobile No. already taken"})
        if User.objects.filter(email = email).exists():
            return render(request, 'local/signup.html', {"errmsg": "You already have an account"})
        password = make_password(password)
        user = User.objects.create(name = name, mobile= mobile, is_agent= True, password= password, email= email)
        user.save()
        agent = Agent.objects.create(user_id=user, address=address, aadhar= aadhar, pincode= pincode, image= image)
        agent.save()
        login(request, user)
        return redirect('agent_dashboard')
    else:
        if request.user.is_authenticated:
            return redirect('/')
        else:
            return render(request, 'local/signup.html') 

def register_manufacturer(request):
    if request.method == 'POST' and request.user.is_authenticated and request.user.is_agent:
        name = request.POST['name']
        company_name = request.POST['company_name']
        email = request.POST['email']
        mobile = request.POST['mobile']
        address = request.POST['address']
        aadhar = request.POST['aadhar']
        pincode = request.POST['pincode']
        image = request.FILES['image']

        if Manufacturer.objects.filter(mobile = mobile).exists():
            return render(request, 'local/manufacturer.html', {"errmsg": "Mobile No. already taken"})
        if Manufacturer.objects.filter(email = email).exists():
            return render(request, 'local/manufacturer.html', {"errmsg": "You already have an account"})
        agent = Agent.objects.get(user_id = request.user)
        manu = Manufacturer.objects.create(agent_id = agent , name = name, company_name=company_name, mobile= mobile, email= email, address=address, aadhar= aadhar, pincode= pincode, image= image)
        manu.save()
        return redirect('manu_addprod', manu.id)
    else:
        return render(request, 'local/manufacturer.html') 

def add_product(request, manufacturer_id):
    manufacturer = Manufacturer.objects.get(id = manufacturer_id)
    if manufacturer:
        if request.method == 'POST' and request.user.is_authenticated and request.user.is_agent:
            name = request.POST['name']
            category_id = request.POST['category']
            quantity = request.POST['quantity']
            description = request.POST['description']
            price = request.POST['price']
            image = request.FILES['image']

            category =  Category.objects.get(id = category_id)
            if category:
                product = Product.objects.create(manufacturer_id = manufacturer , name = name, category=category, quantity= quantity, description= description, price=price, image= image)
                product.save()
                return  redirect('manu_prodlist', manufacturer.id)
            else:
                return render(request, 'local/product.html', {"manufacturer_id": manufacturer_id})
        elif request.method == 'GET':
            category =  Category.objects.all()
            return render(request, 'local/product.html', {"manufacturer_id": manufacturer_id, "categories": category})
        else:
            return redirect('/') 
    else:
        return redirect('/')

def product_list(request, manufacturer_id):
    manufacturer = Manufacturer.objects.get(id = manufacturer_id)
    if manufacturer and request.user.is_authenticated and request.user.is_agent:
        products = Product.objects.values('name', 'category', 'price', 'quantity', 'image').filter(manufacturer_id = manufacturer)
        prod_category = {}
        for product in products:
            if(prod_category.get(product['category'])):
                product['category'] = prod_category.get(product['category'])
            else:
                categoryobj =  Category.objects.get(id = product['category'])
                prod_category[product['category']] = categoryobj.name
                product['category'] = categoryobj.name

        return render(request, 'local/productlist.html', {"products": products})
    else:
        return redirect('/')



@api_view(['GET', 'POST'])
def agent_controller(request):
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer
    if request.method == 'GET':
        agents = Agent.objects.all()
        serializer = AgentSerializer(agents, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = AgentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def dashboard(request):
     return render(request, 'local/dashboard.html')
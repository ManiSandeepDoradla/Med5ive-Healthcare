from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.views.decorators.cache import never_cache , cache_control
# Create your views here.
@never_cache
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def login(request):
    if request.method =='POST':
        username = request.POST['userName']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,"invalid credintials")
            return redirect('login')
    else:
        return render(request,'login.html')
def register(request):
    if request.method =='POST':
        username=request.POST['userName']
        first_name=request.POST['firstName']
        last_name=request.POST['lastName']
        passwor1=request.POST['password']
        passwor2=request.POST['Re-enter password']
        sap_id=request.POST['sapId']
        email=request.POST['officeMail']
        if passwor1==passwor2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'user name exits')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'email exits')
                return redirect('register')
            else:
                user=User.objects.create_user(id=sap_id,email=email,password=passwor1,first_name=first_name,last_name=last_name,username=username)
                user.save()
                print('user created')
                messages.info(request,"user created")
                return redirect('login')
        else:
            messages.info(request,'password not matching')
            return redirect('register') 
        return redirect('/')
    else:
        return render(request,'register.html')
def logout(request):
    auth.logout(request)
    return redirect('/')
def logout_view(request):
    auth.logout(request)
    messages.info(request , "logged out")
    return redirect('login')
from django.shortcuts import render,redirect
from .forms import PlayerRegistrationForm,LoginForm,RegisterForm,PlayerRegistration
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from django.contrib.messages import success,warning,error
from django.contrib.auth import logout,login

def index(request):
    context = {}
    return render(request,"core/index.html",context)

@login_required
def register_form(request):
    
    if len(PlayerRegistration.objects.filter(user=request.user)) != 0:
        error(request,"You Alredy Registered")
        print("Alredy Exist")
        return redirect('index') 
    
    if request.method == 'POST':
        form = PlayerRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            player_registration = form.save(commit=False)
            player_registration.user = request.user       
            player_registration.save()                    
            return redirect('success_page')               
    else:
        form = PlayerRegistrationForm(initial={'player_name': f'{request.user.get_full_name()}'})
        
        
    return render(request,"core/form.html",{
        "form": form
    })



def user_login(request):
    if request.user.is_authenticated:
        return redirect("index")
    
    if request.POST:
        form = LoginForm(data=request.POST)
        
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            success(request,f"Welcome back {user.get_full_name()} !!")
            
            return redirect("index")
    else:
        form = LoginForm()
        
    return render(request,"auth/login.html",{
        "form": form
    })
    
def user_register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        
        if form.is_valid():
            user = form.save(commit=False) 
            user.email = user.username  
            user.save()  
            login(request, user)
            success(request,f"Welcome {user.get_full_name()}")
            return redirect("index")
    else:
        form = RegisterForm()
    return render(request, "auth/register.html", {
        "form": form
    })
    
@login_required
def user_logout(request):
    if request.POST:
        logout(request)
    return redirect("user_login")


def success_page(request):
    return render(request,'core/success.html')

# EXTRA'S
def about(request):
    return render(request,"core/about.html")


def contact(request):
    return render(request,"core/contactus.html")


def newsevents(request):
    return render(request,"core/newsevents.html")

# BLOGS

def commitie(request):
    return render(request,"core/blog/commitie.html")


def gallery(request):
    return render(request,"core/blog/imagegallery.html")

def vgallery(request):
    return render(request,"core/blog/videogallery.html")

def pp(request):
    return render(request,"core/blog/privacy-policy.html")

def tc(request):
    return render(request,"core/blog/tearms-and-condition.html")


def b1(request):
    return render(request,"core/blog/ispl-player-revealed.html")

def b2(request):
    return render(request,"core/blog/own-a-tspl-franchise-team.html")

def b3(request):
    return render(request,"core/blog/tennies-ball-cricket.html")

def b4(request):
    return render(request,"core/blog/tspl-t10-action.html")

def b5(request):
    return render(request,"core/blog/who-can-register.html")

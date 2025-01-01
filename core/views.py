from django.shortcuts import render,redirect
from .forms import PlayerRegistrationForm,LoginForm,RegisterForm,User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from django.contrib.messages import success,warning,error
from django.contrib.auth import logout,login

def index(request):
    context = {}
    return render(request,"core/index.html",context)

@login_required
def register_form(request):
    # user = User.objects.get(request.user)
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
        success(request,"You Have been loged Out!!")
    else:
        error(request,"Invalid Request !!")
    return redirect("user_login")


def success_page(request):
    return render(request,'core/success.html')
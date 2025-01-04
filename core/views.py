from django.shortcuts import render,redirect,HttpResponse
from .forms import PlayerRegistrationForm,LoginForm,RegisterForm,PlayerRegistration
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from django.contrib.messages import success,warning,error
from django.contrib.auth import logout,login
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest


client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


def index(request):
    context = {}
    return render(request,"core/index.html",context)


@login_required
def register_form(request):
    if PlayerRegistration.objects.filter(user=request.user).exists():
        error(request, "You already registered")
        return redirect('index')

    if request.method == 'POST':
        form = PlayerRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            player_registration = form.save(commit=False)
            player_registration.user = request.user
            player_registration.save()


            amount = 1 * 100
            order_currency = "INR"
            order_receipt = f"rcpt_{player_registration.id}"[:40]  # Ensuring max 40 chars
            
            try:
                razorpay_order = client.order.create({
                    "amount": amount,
                    "currency": order_currency,
                    "receipt": order_receipt,
                    "payment_capture": 1,
                })
            except razorpay.errors.BadRequestError as e:
                error(request, f"Failed to create Razorpay order: {str(e)}")
                return redirect("index")

            context = {
                "razorpay_order_id": razorpay_order["id"],
                "razorpay_key": settings.RAZORPAY_KEY_ID,
                "amount": amount,
                "currency": order_currency
            }
            return render(request, 'core/payment.html', context)

    else:
        form = PlayerRegistrationForm(initial={'player_name': request.user.get_full_name()})

    return render(request, "core/form.html", {"form": form})


@csrf_exempt
def payment_handler(request):
    if request.method == "POST":
        try:
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

            # verify the payment signature.
            result = client.utility.verify_payment_signature(
                params_dict)
            if result is not None:
                amount = 1 * 100  # Rs. 200
                try:

                    client.payment.capture(payment_id, amount)
                    return redirect("success_page")
                except Exception as e:
                    print(e)
                    # if there is an error while capturing payment.
                    return render(request, 'paymentfail.html')
            else:

                # if signature verification fails.
                return render(request, 'paymentfail.html')
        except:

            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()
    
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

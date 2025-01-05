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
from .models import Setting


client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


def index(request):
    context = {}
    return render(request,"core/index.html",context)


@login_required
def register_form(request):
    try:
        
        config = Setting.objects.all()
        config = config[0]
    except Exception as e:
        print(e)
        warning(request,"No Form Is Avilable")
        return redirect("index")
    
    if PlayerRegistration.objects.filter(user=request.user).exists():
        obj = PlayerRegistration.objects.filter(user=request.user)[0]
        if obj.is_paid:
            context = {
                    "id" : obj.tx_id,
                    "reg_id" : obj.user_id,
                    "amount" : float(config.amount),
                    "zone" : obj.zone,
                }
            success(request,"You Alredy Completed the Payment")
            return render(request,"core/success.html",context)
        else:
            success(request,"Complete the Pending Payment")
            amount = config.amount * 100
            order_currency = "INR"
            order_receipt = f"rcpt_{obj.id}"[:40] 
            
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
                "currency": order_currency,
                "callback_url" : f"https://tspl.hattricksolution.in/paymenthandler/{obj.id}"
            }
            return render(request, 'core/payment.html', context)

        
    if request.method == 'POST':
        
        form = PlayerRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            player_registration = form.save(commit=False)
            player_registration.user = request.user
            player_registration.save()

            amount = config.amount * 100
            order_currency = "INR"
            order_receipt = f"rcpt_{player_registration.id}"[:40] 
            
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
                "currency": order_currency,
                "callback_url" : f"https://tntenniscricket.in/paymenthandler/{player_registration.id}"
            }
            return render(request, 'core/payment.html', context)

    else:
        form = PlayerRegistrationForm(initial={'player_name': request.user.get_full_name(),"email": request.user.email})

    return render(request, "core/form.html", {"form": form})


@csrf_exempt
def payment_handler(request,id):
    if request.method == "POST":
        try:
            obj = PlayerRegistration.objects.get(id=id)
            if obj is None:
                return HttpResponseBadRequest()
            
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')

            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

            try:
                client.utility.verify_payment_signature(params_dict)
            except Exception as e:
                print("Signature verification failed:", e)
                return render(request, 'paymentfail.html',{"message":str(e)})
                

            payment_details = client.payment.fetch(payment_id)
            if payment_details['status'] == 'captured':
                print("Payment already captured.")
                
                context = {
                    "id" : payment_details['id'],
                    "reg_id" : obj.user_id,
                    "order_id" : payment_details['order_id'],
                    "amount" : float(payment_details['amount']/100),
                    "zone" : obj.zone,
                }
                obj.is_paid = True
                obj.tx_id =  payment_details['id']
                obj.save()
                return render(request,"core/success.html",context)

            amount = int(payment_details['amount'])
            try:
                client.payment.capture(payment_id, amount)
                
                print("Payment captured.")
                
                context = {
                    "id" : payment_details['id'],
                    "order_id" : payment_details['order_id']
                }
                obj.is_paid = True
                obj.tx_id =  payment_details['id']
                obj.save()
                return render(request,"core/success.html",context)
                
            except Exception as e:
                print("Capture failed:", e)
                
                return render(request, 'paymentfail.html',{"message":str(e)})

        except Exception as e:
            print("Unexpected error:", e)
            return HttpResponseBadRequest()
    else:
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
        "form": form,
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

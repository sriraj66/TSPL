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
from django.conf import settings
from .task import send_success_email
import logging

logger = logging.getLogger('core')

logger.info("Initing Payment Gateway")
client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
logger.info("Payment Gateway Inited")

def index(request):
    # context = {
    #     "id" : 'dsad',
    #     "reg_id" : "asdasd",
    #     "order_id" : "dsdsd",
    #     "amount" : "float(payment_details['amount']/100)",
    #     "zone" : "obj.zone",
    # }   
    # send_success_email(subject="Registration Completed", to=request.user.email, context=context)

    logger.info("Visiting Index Page")
    return render(request,"core/index.html")


@login_required
def register_form(request):
    try:
        try:
            config = Setting.objects.all()
            config = config[0]

            logger.info("Setting Found")
            if config.accept_response == False:
                success(request,"The Registration is Not yet Started.")
                logger.warning(f"The Form {config.amount} - Response : {config.accept_response} is not Started")
                return redirect("index")
            
        except Exception as e:
            print(e)
            warning(request,"No Form Is Avilable")
            logger.warning("No Form is Avilable")
            return redirect("index")
        
        
        if PlayerRegistration.objects.filter(user=request.user).exists():
            obj = PlayerRegistration.objects.filter(user=request.user)[0]
            if obj.is_paid:
                context = {
                        "id" : obj.tx_id,
                        "reg_id" : obj.reg_id,
                        "amount" : float(config.amount),
                        "zone" : obj.zone,
                    }
                
                success(request,"You Alredy Completed the Payment")
                logger.info("Registration Compleated")
                return render(request,"core/success.html",context)
            else:
                success(request,"Complete the Pending Payment")
                amount = config.amount * 100
                order_currency = "INR"
                order_receipt = f"rcpt_{obj.id}"[:40] 
                logger.info("Payment Initiated")
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
                    "callback_url" : f"https://tntenniscricket.in/paymenthandler/{obj.id}"

                }
                logger.info("Redirecting to The payment Page")
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
                logger.info("Payment Initiated")
                
                try:
                    razorpay_order = client.order.create({
                        "amount": amount,
                        "currency": order_currency,
                        "receipt": order_receipt,
                        "payment_capture": 1,
                    })
                except razorpay.errors.BadRequestError as e:
                    error(request, f"Failed to create Razorpay order: {str(e)}")
                    logger.error("Faild to Compleate Payment While Creating order : "+ str(e) )
                    return redirect("index")

                context = {
                    "razorpay_order_id": razorpay_order["id"],
                    "razorpay_key": settings.RAZORPAY_KEY_ID,
                    "amount": amount,
                    "currency": order_currency,
                    "callback_url" : f"https://tntenniscricket.in/paymenthandler/{player_registration.id}"
                }
                logger.info("Redirecting to The payment Page")
                
                return render(request, 'core/payment.html', context)

        else:
            form = PlayerRegistrationForm(initial={'player_name': request.user.get_full_name(),"email": request.user.email})
            logger.info("Form Generated")
        return render(request, "core/form.html", {"form": form, "config":config})
    except Exception as e:
        logger.error("Error In The Form : ",e)
        print(f"Error In the Form {e}")
        return redirect("index")

@csrf_exempt
def payment_handler(request,id):
    if request.method == "POST":
        try:
            obj = PlayerRegistration.objects.get(id=id)
            if obj is None:
                logger.error("Invalid Payment Request")
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
                logger.error(f"Signature verification failed: {e}")
                return render(request, 'paymentfail.html',{"message":str(e)})
                

            payment_details = client.payment.fetch(payment_id)
            if payment_details['status'] == 'captured':
                print("Payment already captured.")
                logger.info("Payment Allredy Captured")
                
                context = {
                    "id" : payment_details['id'],
                    "reg_id" : obj.reg_id,
                    "order_id" : payment_details['order_id'],
                    "amount" : float(payment_details['amount']/100),
                    "zone" : obj.zone,
                }
                obj.is_paid = True
                obj.tx_id =  payment_details['id']
                obj.save()
                logger.info("Sending Email to "+obj.user.email)
                send_success_email(subject="Registration Completed", to=obj.user.email, context=context)
                logger.info("Email Sended statrtd Redirection")

                return render(request,"core/success.html",context)

            amount = int(payment_details['amount'])
            try:
                client.payment.capture(payment_id, amount)
                
                print("Payment captured.")
                logger.info("Payment Captured")
                
                context = {
                    "id" : payment_details['id'],
                    "reg_id" : obj.reg_id,
                    "order_id" : payment_details['order_id'],
                    "amount" : float(payment_details['amount']/100),
                    "zone" : obj.zone,
                }
                obj.is_paid = True
                obj.tx_id =  payment_details['id']
                obj.save()
                logger.info("Sending Email to "+obj.user.email)

                send_success_email(subject="Registration Completed", to=obj.user.email, context=context)
                logger.info("Email Sended statrtd Redirection")

                return render(request,"core/success.html",context)
                
            except Exception as e:
                print("Capture failed:", e)
                logger.error("Capture Failed {e}")
                return render(request, 'paymentfail.html',{"message":str(e)})

        except Exception as e:
            print("Unexpected error:", e)
            logger.error(f"Unexpected Error {e}")
            return HttpResponseBadRequest()
    else:
        logger.error("Invalid Request")
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
            logger.info("User Loged In")
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
            logger.info("User Loged In")
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
        logger.info("User Loged out")
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

# SEO
from django.template.loader import get_template

def robot(request):
    logger.warning("Visited Robot.txt")
    
    # Load robots.txt from the templates folder
    template = get_template('robots.txt')
    robots_content = template.render()
    
    return HttpResponse(robots_content, content_type="text/plain")

def sitemap(request):
    logger.warning("Visited sitemap.xml")
    
    # Load sitemap.xml from the templates folder
    template = get_template('sitemap.xml')
    sitemap_content = template.render()
    
    return HttpResponse(sitemap_content, content_type="application/xml")
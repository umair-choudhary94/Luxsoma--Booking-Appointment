from django.shortcuts import render,redirect
from .models import *
from .forms import *
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.http import JsonResponse
import json
import stripe
from django.core.mail import send_mail
from django.conf import settings
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.shortcuts import get_object_or_404

def index(request):
    objects = Category.objects.all()
    context = {
        "objects" : objects
    }
    return render(request,"application/index.html",context)

def services(request):
    objects = Category.objects.all()
    context = {
        "objects" : objects
    }
    return render(request,"application/services.html",context)

def subcategories(request,category):
    obj = Category.objects.get(title=category)
    objects = Service.objects.filter(category=obj)

    context = {
        "objects" : objects
    }
    return render(request,"application/subservices.html",context)
def subcategoriesinfo(request,title):
    
    object = Service.objects.filter(title=title)

    context = {
        "object" : object
    }
    return render(request,"application/subservicesinfo.html",context)




def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            # Handle successful form submission (e.g., redirect to a thank you page)
    else:
        form = ContactForm()
    
    return render(request, 'application/contact.html', {'form': form})
def faq_view(request):
    
    
    return render(request, 'application/faq.html')
def sign_up(request):
    if request.method == "POST":
        Name = request.POST['username']
        Email = request.POST['email']
        Password = request.POST['password']
        Password2 = request.POST['password2']
        if Password == Password2:
            user=User.objects.create_user(username=Name,email=Email,password=Password)
            user.save()
       
            user = auth.authenticate(request, username=Name,password=Password)
            auth.login(request,user)
            return redirect('/')
        else:
            return redirect("/register")
    else:
        return render(request, 'application/sign-up.html')

# login 
def user_login(request):
    if request.method == 'POST':
        Name = request.POST['username']
        Password = request.POST['password']

        user = auth.authenticate(request, username=Name,password=Password)
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,'Your username or passwword is wrong!') 
            return redirect('login')
    else:
        return render(request, 'application/login.html')

# logout
def user_logout(request):
    auth.logout(request)
    return redirect('/')
def profile(request):
    person = User.objects.get(id=request.user.id)
    appointments = Appointment.objects.filter(user=person)
    context = {
        "person" : person,
        "appointments" : appointments,
        "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY
    }
    return render(request,"application/profile.html",context)

def book_appointment(request):
    objects = Category.objects.all()
    context = {
        "objects" : objects
    }
    return render(request,"application/bookappointment.html",context)

def services_json(request):
    category_id = request.GET.get('category')
    services = Service.objects.filter(category_id=category_id).values('id', 'title','price')
    data = list(services)
    return JsonResponse(data, safe=False)
def make_appointment(request):
    if request.method == 'POST':
        category_id = request.POST.get('category')
        service_id = request.POST.get('service')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        appointment_date = request.POST.get('appointment_date')

        # Create a new appointment instance
        appointment = Appointment(
            user=User.objects.get(id=request.user.id),
            service=Service.objects.get(id=service_id),
            appointment_date=appointment_date,
            start_time=start_time,
            end_time=end_time
        )
        appointment.save()

        # Redirect to a success page or perform additional actions
        return redirect('getcard')

    return redirect('/')  # Replace 'appointment_success' with the URL name of your success page

def gallery(request):
    objects = Gallery.objects.all()
    context = {
        "objects" : objects
    }
    return render(request,'application/gallery.html',context)

stripe.api_key = settings.STRIPE_SECRET_KEY

def  SuccessView(request,id):
    obj = Appointment.objects.get(id=id)
    # Update payment status to "Paid"
    obj.payment_status = 'Paid'
    obj.save()
    return redirect("/profile")

class CancelView(TemplateView):
    template_name = "cancel.html"


class ProductLandingPageView(TemplateView):
    template_name = "landing.html"

    def get_context_data(self, **kwargs):
        products = Appointment.objects.all()
        # product = Product.objects.all()
        context = super(ProductLandingPageView, self).get_context_data(**kwargs)
        context.update({
            "products": products,
            "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY
        })
        return context


# class CreateCheckoutSessionView(View):
#     def post(self, request, *args, **kwargs):
#         product_id = self.kwargs["pk"]
#         product = Appointment.objects.get(id=product_id)
#         YOUR_DOMAIN = "http://127.0.0.1:8000"
#         checkout_session = stripe.checkout.Session.create(
#             payment_method_types=['card'],
#             line_items=[
#                 {
#                     'price_data': {
#                         'currency': 'usd',
#                         'unit_amount':int(product.price * 100),
#                         'product_data': {
#                             'name': "Paying",
#                             # 'images': ['https://i.imgur.com/EHyR2nP.png'],
#                         },
#                     },
#                     'quantity': 1,
#                 },
#             ],
#             metadata={
#                 "product_id": product.id
#             },
#             mode='payment',
#             success_url=YOUR_DOMAIN + f'/success/{product_id}/',
#             cancel_url=YOUR_DOMAIN + '/cancel/',
#         )
#         return JsonResponse({
#             'id': checkout_session.id
#         })

# @csrf_exempt
# def stripe_webhook(request):
#     payload = request.body
#     sig_header = request.META['HTTP_STRIPE_SIGNATURE']
#     event = None

#     try:
#         event = stripe.Webhook.construct_event(
#             payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
#         )
#     except ValueError as e:
#         # Invalid payload
#         return HttpResponse(status=400)
#     except stripe.error.SignatureVerificationError as e:
#         # Invalid signature
#         return HttpResponse(status=400)

#     # Handle the checkout.session.completed event
#     if event['type'] == 'checkout.session.completed':
#         session = event['data']['object']

#         customer_email = session["customer_details"]["email"]
#         product_id = session["metadata"]["product_id"]

#         product = Appointment.objects.get(id=product_id)
        
#         send_mail(
#             subject="Here is your product",
#             message=f"Thanks for your purchase. Here is the product you ordered. The URL is {product.url}",
#             recipient_list=[customer_email],
#             from_email="matt@test.com"
#         )

#         # TODO - decide whether you want to send the file or the URL
    
#     elif event["type"] == "payment_intent.succeeded":
#         intent = event['data']['object']

#         stripe_customer_id = intent["customer"]
#         stripe_customer = stripe.Customer.retrieve(stripe_customer_id)

#         customer_email = stripe_customer['email']
#         product_id = intent["metadata"]["product_id"]

#         product = Appointment.objects.get(id=product_id)
        

#         send_mail(
#             subject="Here is your product",
#             message=f"Thanks for your purchase. Here is the product you ordered. The URL is {product.url}",
#             recipient_list=[customer_email],
#             from_email="matt@test.com"
#         )

#     return HttpResponse(status=200)


# class StripeIntentView(View):
#     def post(self, request, *args, **kwargs):
#         try:
#             req_json = json.loads(request.body)
#             customer = stripe.Customer.create(email=req_json['email'])
#             product_id = self.kwargs["pk"]
#             product = Appointment.objects.get(id=product_id)
#             intent = stripe.PaymentIntent.create(
#                 amount=product.price,
#                 currency='usd',
#                 customer=customer['id'],
#                 metadata={
#                     "product_id": product.id
#                 }
#             )
#             return JsonResponse({
#                 'clientSecret': intent['client_secret']
#             })
#         except Exception as e:
#             return JsonResponse({ 'error': str(e) })



class TermsConditionsView(TemplateView):
    template_name = 'terms_conditions.html'

class PrivacyPolicyView(TemplateView):
    template_name = 'privacy_policy.html'

class CookiesPolicyView(TemplateView):
    template_name = 'cookies_policy.html'
# views.py
from django.shortcuts import render

def cookie_banner_view(request):
    return render(request, 'cookie_banner.html')


@csrf_exempt  # Disable CSRF protection for simplicity. Make sure to handle CSRF protection in production.
def store_stripe_token(request):
    if request.method == 'POST':
        token_id = request.POST.get('stripeToken')
        # You can also receive other data associated with the token (e.g., payment ID, customer ID, etc.)

        try:
            # Check if the token already exists, or create a new entry for it
            token_obj, created = StripeToken.objects.get_or_create(
                token_id=token_id,
                user = request.user
                # Add other fields if necessary
            )

            return redirect("profile")

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
        
def process_payment(request,id):
    
    stripe.api_key = settings.STRIPE_SECRET_KEY

        # Token obtained from the client-side using Stripe.js or Elements
    obj = CreditCard.objects.get(user=request.user)
    
    obj2 = get_object_or_404(Appointment, id=id)
    amount_in_cents = int(obj2.price * 100)# $5 in cents (Stripe works with the smallest currency unit, e.g., cents for USD)

    token = stripe.Token.create(
        card={
            'number': obj.card_number,
            'exp_month':obj.exp_month,
            'exp_year': obj.exp_year,
            'cvc': obj.cvc,
        },
    )   
    charge = stripe.Charge.create(
        amount=amount_in_cents,
        currency='usd',
        source=token.id,
        description=f'Appointment Payment - ${amount_in_cents / 100:.2f}',
            # Add any other optional parameters as needed
    )

    obj2.payment_status = 'Paid'
    obj2.save()

            # You can associate the token with a user or a specific transaction here if needed.
            # For example, if you have a user model and the user is authenticated:
            # user = request.user
            # stripe_token_obj.user = user
            # stripe_token_obj.save()

    return render(request, 'application/paymentsuccess.html')
def cancel_appointment(request,id):
    
    stripe.api_key = settings.STRIPE_SECRET_KEY

        # Token obtained from the client-side using Stripe.js or Elements
    obj = CreditCard.objects.get(user=request.user)
    obj2 = get_object_or_404(Appointment, id=id)
    amount_in_cents = int(obj2.price * 100)
    actual_amount = int((amount_in_cents*50)/100)
    token = stripe.Token.create(
        card={
            'number': obj.card_number,
            'exp_month':obj.exp_month,
            'exp_year': obj.exp_year,
            'cvc': obj.cvc,
        },
    ) 
        
    charge = stripe.Charge.create(
        amount=actual_amount,
        currency='usd',
        source=token.id,
        description=f'Cancellation Payment - ${actual_amount / 100:.2f}',
            # Add any other optional parameters as needed
    )
    
    obj2.payment_status = 'Cancelled'
    obj2.save()

            # You can associate the token with a user or a specific transaction here if needed.
            # For example, if you have a user model and the user is authenticated:
            # user = request.user
            # stripe_token_obj.user = user
            # stripe_token_obj.save()

    return render(request, 'application/paymentcancel.html',) 
def credit_card_view(request):
    if request.method == 'POST':
        form = CreditCardForm(request.POST)
        if form.is_valid():
            credit_card = form.save(commit=False) 
            credit_card.user = request.user  
            credit_card.save()
            # Redirect or do further processing after saving the data.
            return redirect('profile')
    else:
        try:
            credit_card = CreditCard.objects.get(user=request.user)
            return redirect('profile')
        except CreditCard.DoesNotExist:
            
            form = CreditCardForm()

            return render(request, 'application/getcard.html', {'form': form})
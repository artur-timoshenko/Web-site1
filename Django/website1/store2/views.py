import json
import os
import stripe

from django.contrib.auth.models import auth
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.conf import settings
from .models import Banner, CartItem, PaymentIntent, Product, OrderItem, Customer
from .forms import SignInForm, SignUpForm
from django.contrib import messages


class HomePageView(TemplateView):
    def get(self, request, *args, **kwargs):
        context = {}

        banners = Banner.objects.all()
        context['banners'] = banners

        response = render(request=request, template_name='store2/index.html', context=context)

        return response


class SalesPageView(TemplateView):
    def get(self, request, *args, **kwargs):
        context = {}

        products = Product.objects.filter(~Q(salePercent=0))
        context['products'] = products

        response = render(request=request, template_name='store2/sales/index.html', context=context)

        return response


class NewPageView(TemplateView):
    def get(self, request, *args, **kwargs):
        context = {}

        products = Product.objects.filter(new=True)
        context['products'] = products

        response = render(request=request, template_name='store2/new/index.html', context=context)

        return response


class SeasonPageView(TemplateView):
    def get(self, request, *args, **kwargs):
        context = {}

        products = Product.objects.filter(season=True)
        context['products'] = products

        response = render(request=request, template_name='store2/season/index.html', context=context)

        return response


class CartPageView(TemplateView):
    def get(self, request, *args, **kwargs):
        context = {}

        if request.user.is_authenticated:
            cartItems = CartItem.objects.filter(user=request.user)
            context['cartItems'] = cartItems

            context['total'] = calculate_order_amount(request=request)

        response = render(request=request, template_name='store2/cart/index.html', context=context)

        return response


class SignInPageView(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/store2/')

        # cockies = request.COOKIES
        # GET = request.GET
        context = {}

        form = SignInForm()
        context['form'] = form

        response = render(request=request, template_name='store2/sign/sign-in.html', context=context)

        return response

    def post(self, request, *args, **kwargs):
        # cockies = request.COOKIES
        POST = request.POST

        form = SignInForm(request, data=POST)

        if form.is_valid():
            username = POST.get('username', '')
            password = POST.get('password', '')

            user = auth.authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)

                return redirect('/store2/')
            else:
                messages.error(request, 'Invalid username or password')
        else:
            messages.error(request, 'Invalid username or password')

        return redirect('/store2/sign-in/')


class SignUpPageView(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/store2/')

        context = {}

        form = SignUpForm()
        context['form'] = form

        response = render(request=request, template_name='store2/sign/sign-up.html', context=context)

        return response

    def post(self, request, *args, **kwargs):
        POST = request.POST

        form = SignUpForm(POST)

        if form.is_valid():
            form.save()

            user = auth.authenticate(request, username=POST.get('username', ''), password=POST.get('password1', ''))
            if user is not None:
                auth.login(request, user)

                return redirect('/store2/')
        else:
            for error_message in form.error_messages.values():
                messages.add_message(request, messages.ERROR, error_message)

            return redirect('/store2/sign-up/')

        return redirect('/store2/')

        # serializer = UserSerializer(data=request.POST)
        # if serializer.is_valid():
        #     serializer.save()


class SignOutPageView(TemplateView):
    def get(self, request, *args, **kwargs):
        auth.logout(request)

        return redirect('/store2/')

    def post(self, request, *args, **kwargs):
        auth.logout(request)

        return redirect('/store2/')


class StripeCompleteView(TemplateView):
    def get(self, request, *args, **kwargs):
        data = request.GET
        context = {}

        if settings.DEBUG and data.get('redirect_status', '') == 'succeeded':
            paymentIntentId = data.get('payment_intent', '')

            paymentIntent = PaymentIntent.objects.get(intent=paymentIntentId)
            paymentIntent.status = 'succeeded'
            paymentIntent.save()

            cartItems = CartItem.objects.filter(paymentIntent=paymentIntent)
            for cartItem in cartItems:
                OrderItem.objects.create(product=cartItem.product, quantity=cartItem.quantity,
                                         paymentIntent=cartItem.paymentIntent, user=cartItem.user)
                cartItem.delete()

        response = render(request=request, template_name='store2/stripe/complete.html', context=context)

        return response


def CartAdd(request):
    if request.method == 'POST':
        # POST = request.POST

        if request.user.is_authenticated:
            data = json.loads(request.body)

            try:
                productId = int(data.get('productId', 0))
                productQuantity = int(data.get('productQuantity', 0))
            except ValueError:
                return JsonResponse({'status': 'error', 'message': 'Invalid data'})

            product = Product.objects.get(id=productId)

            if not product:
                return JsonResponse({'status': 'error', 'message': 'Product does not exist'})

            try:
                cartItem = CartItem.objects.get(user=request.user, product=product)
                cartItem.quantity += productQuantity
                cartItem.save()
            except CartItem.DoesNotExist:
                CartItem.objects.create(user=request.user, product=product, quantity=productQuantity)

            return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Not logged in'})


def CartRemove(request):
    if request.method == 'POST':
        # POST = request.POST

        if request.user.is_authenticated:
            data = json.loads(request.body)

            product = Product.objects.get(id=data.get('productId'))

            if not product:
                return JsonResponse({'status': 'error', 'message': 'Product does not exist'})

            try:
                cartItem = CartItem.objects.get(user=request.user, product=product)
                cartItem.delete()
            except CartItem.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Cart item does not exist'})

            return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Not logged in'})


def CartChange(request):
    if request.method == 'POST':
        # POST = request.POST

        if request.user.is_authenticated:
            data = json.loads(request.body)
            # print(data)

            product = Product.objects.get(id=data.get('productId'))

            if not product:
                return JsonResponse({'status': 'error', 'message': 'Product does not exist'})

            try:
                cartItem = CartItem.objects.get(user=request.user, product=product)

                if data.get('value', '') == 'decrease':
                    if cartItem.quantity == 1:
                        cartItem.delete()
                    else:
                        cartItem.quantity -= 1
                        cartItem.save()
                elif data.get('value', '') == 'increase':
                    cartItem.quantity += 1
                    cartItem.save()
            except CartItem.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Cart item does not exist'})

            return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Not logged in'})


def StripeConfig(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': os.getenv('STRIPE_PUBLISHABLE_KEY')}
        return JsonResponse(stripe_config, safe=False)


@csrf_exempt
def StripeWebhook(request):
    endpoint_secret = os.getenv('STRIPE_ENDPOINT_SECRET')
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    if event['type'] == 'payment_intent.succeeded':
        paymentIntentId = event['data']['object']['id']

        paymentIntent = PaymentIntent.objects.get(intent=paymentIntentId)
        paymentIntent.status = 'succeeded'
        paymentIntent.save()

        cartItems = CartItem.objects.filter(paymentIntent=paymentIntent)
        for cartItem in cartItems:
            OrderItem.objects.create(product=cartItem.product, quantity=cartItem.quantity,
                                     paymentIntent=cartItem.paymentIntent, user=cartItem.user)
            cartItem.delete()

    return HttpResponse(status=200)


def calculate_order_amount(request):
    if not request.user.is_authenticated:
        return 0

    total = 0
    cartItems = CartItem.objects.filter(user=request.user)

    for cartItem in cartItems:
        total += cartItem.quantity * cartItem.product.price * (1 - cartItem.product.salePercent / 100)

    return total


def charge_customer(customer_id, amount):
    # Lookup the payment methods available for the customer
    payment_methods = stripe.PaymentMethod.list(
        customer=customer_id,
        type='card'
    )
    # Charge the customer and payment method immediately
    try:
        stripe.PaymentIntent.create(
            amount=amount,
            currency='usd',
            customer=customer_id,
            payment_method=payment_methods.data[0].id,
            off_session=True,
            confirm=True
        )
    except stripe.error.CardError as e:
        err = e.error
        # Error code will be authentication_required if authentication is needed
        print('Code is: %s' % err.code)
        payment_intent_id = err.payment_intent['id']
        payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)


def StripeCreatePayment(request):
    try:
        if not request.user.is_authenticated:
            return

        try:
            customer = Customer.objects.get(user=request.user)
        except Customer.DoesNotExist:
            customer = stripe.Customer.create(name=request.user.username, email=request.user.email)
            customer = Customer.objects.create(user=request.user, customerID=customer['id'])

        if not customer:
            return

        # data = json.loads(request.body)
        # Create a PaymentIntent with the order amount and currency
        amount = calculate_order_amount(request=request)

        intent = stripe.PaymentIntent.create(
            customer=customer.customerID,
            setup_future_usage='off_session',
            amount=int(amount * 100),
            currency='usd',
            # In the latest version of the API, specifying the `automatic_payment_methods` parameter is optional because Stripe enables its functionality by default.
            automatic_payment_methods={
                'enabled': True,
            },
        )

        paymentIntent = PaymentIntent.objects.create(intent=intent['id'], amount=amount, customer=customer)
        paymentIntent.save()

        cartItems = CartItem.objects.filter(user=request.user)
        for cartItem in cartItems:
            cartItem.paymentIntent = paymentIntent
            # cartItem.cart = None
            cartItem.save()

        return JsonResponse({
            'clientSecret': intent['client_secret'],
            # [DEV]: For demo purposes only, you should avoid exposing the PaymentIntent ID in the client-side code.
            'dpmCheckerLink': 'https://dashboard.stripe.com/settings/payment_methods/review?transaction_id={}'.format(
                intent['id']),
        })
    except Exception as e:
        return JsonResponse({'error': str(e)})


def StripeCreatePortalSession(request):
    if not request.user.is_authenticated:
        return

    try:
        customer = Customer.objects.get(user=request.user)
    except Customer.DoesNotExist:
        customer = stripe.Customer.create(name=request.user.username, email=request.user.email)
        customer = Customer.objects.create(user=request.user, customerID=customer['id'])

    if not customer:
        return

    return_url = 'http://localhost:8000/store2/'

    # 'cs_test_a13QbwYuk4laETM3BpCm80qnUys3DbDCPioKNHC9y2Q3UZPuMRBARDUuXt'

    portalSession = stripe.billing_portal.Session.create(
        customer=customer.customerID,
        return_url=return_url,
        locale='en',
    )
    return redirect(portalSession.url, code=303)

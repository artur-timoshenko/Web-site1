import json
import os
import stripe
from asgiref.sync import sync_to_async
from django.http import HttpResponse, JsonResponse, HttpRequest, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from django.contrib.auth.models import auth
from rest_framework import generics
from .filters import ProductFilter
from .forms import SignInForm, SignUpForm
from .models import Product, CartItem, PaymentIntent, OrderItem, Customer
from .serializers import UserSerializer
from .crypto import get_hashed_password, check_password
from django.contrib import messages
from django.conf import settings


# class ApiPageVew(generics.ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')


class HomePageView(TemplateView):
    def get(self, request, *args, **kwargs):
        context = {}

        if request.user.is_authenticated:
            cartItems = CartItem.objects.filter(user=request.user)

            context['cartItems'] = cartItems

        response = render(request=request, template_name='store/index.html', context=context)

        return response

    # def post(self, request, *args, **kwargs):
    #     serializer = UserSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()


class CatalogPageView(TemplateView):
    def get(self, request, *args, **kwargs):
        context = {}

        if request.user.is_authenticated:
            cartItems = CartItem.objects.filter(user=request.user)

            context['cartItems'] = cartItems

        try:
            page = int(request.GET.get('page', 1))
        except ValueError:
            page = 1

        if page < 1 or page > 99:
            page = 1

        itemsPerPage = 12
        minIndex = (page - 1) * itemsPerPage
        maxIndex = minIndex + itemsPerPage

        # print(request.GET)
        #
        productFilter = ProductFilter(request.GET, queryset=Product.objects.all())
        # products = [product async for product in productFilter.qs]
        context['products'] = productFilter.qs.order_by('price')[minIndex:maxIndex]
        context['form'] = productFilter.form
        context['productsCount'] = productFilter.qs.count()
        context['minIndex'] = minIndex + 1 if context['productsCount'] > 0 else 0
        context['maxIndex'] = maxIndex if maxIndex < context['productsCount'] else context['productsCount']
        context['previousPage'] = page - 1 if page > 1 else 1
        context['nextPage'] = page + 1 if maxIndex < context['productsCount'] else page
        context['currentPage'] = page
        # print(productFilter.form.fields)
        # fields = [element for element in productFilter.form]
        # widgets = [field for field in fields[0]]
        # smth = [field for field in widgets[0]]
        # context['filter'] = filter.qs
        # return render(request, 'store/index.html', {'filter': filter})

        # users = [user async for user in User.objects.all().filter(username='John Smith')]
        # serializer = UserSerializer(users, context={'request': request}, many=True)
        # context['users'] = serializer.data

        response = render(request=request, template_name='store/catalog/index.html', context=context)

        return response


class ProductPageView(TemplateView):
    def get(self, request, *args, **kwargs):
        id = self.kwargs.get('id', '')
        context = {}

        if request.user.is_authenticated:
            cartItems = CartItem.objects.filter(user=request.user)

            context['cartItems'] = cartItems

        product = Product.objects.get(id=id)
        context['product'] = product

        response = render(request=request, template_name='store/product/index.html', context=context)

        return response


class SignInPageView(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/store/catalog/')

        # cockies = request.COOKIES
        # GET = request.GET
        context = {}

        form = SignInForm()
        context['form'] = form

        response = render(request=request, template_name='store/sign/sign-in.html', context=context)

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

                return redirect('/store/')
            else:
                messages.error(request, 'Invalid username or password')
        else:
            messages.error(request, 'Invalid username or password')

        return redirect('/store/sign-in/')

        # password = POST.get('password', '')
        # user_password = 'test'  # TODO get user password from database
        #
        # if not check_password(f'{password}', get_hashed_password(user_password)):
        #     return HttpResponse(status=401)
        #
        # return HttpResponse(status=200)


class SignUpPageView(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/store/catalog/')

        context = {}

        form = SignUpForm()
        context['form'] = form

        response = render(request=request, template_name='store/sign/sign-up.html', context=context)

        return response

    def post(self, request, *args, **kwargs):
        POST = request.POST

        form = SignUpForm(POST)

        if form.is_valid():
            form.save()

            user = auth.authenticate(request, username=POST.get('username', ''), password=POST.get('password1', ''))
            if user is not None:
                auth.login(request, user)

                return redirect('/store/')
        else:
            for error_message in form.error_messages.values():
                messages.add_message(request, messages.ERROR, error_message)

            return redirect('/store/sign-up/')

        return redirect('/store/')

        # serializer = UserSerializer(data=request.POST)
        # if serializer.is_valid():
        #     serializer.save()


class SignOutPageView(TemplateView):
    def get(self, request, *args, **kwargs):
        auth.logout(request)

        return redirect('/store/')

    def post(self, request, *args, **kwargs):
        auth.logout(request)

        return redirect('/store/')


class CheckoutPageView(TemplateView):
    def get(self, request, *args, **kwargs):
        context = {}

        if request.user.is_authenticated:
            cartItems = CartItem.objects.filter(user=request.user)
            context['cartItems'] = cartItems

            context['total'] = calculate_order_amount(request=request)

            # if not cartItems.exists():
            #     return redirect('/store/catalog/')

        response = render(request=request, template_name='store/checkout/index.html', context=context)

        return response


class StripeSuccessView(TemplateView):
    def get(self, request, *args, **kwargs):
        context = {}

        response = render(request=request, template_name='store/success.html', context=context)

        return response


class StripeCancelledView(TemplateView):
    def get(self, request, *args, **kwargs):
        context = {}

        response = render(request=request, template_name='store/cancelled.html', context=context)

        return response


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

        response = render(request=request, template_name='store/complete.html', context=context)

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


def StripeCreateSession(request):
    if request.method == 'GET':
        domain_url = 'http://localhost:8000/store/stripe/'
        try:
            # Create new Checkout Session for the order
            # Other optional params include:
            # [billing_address_collection] - to display billing address details on the page
            # [customer] - if you have an existing Stripe Customer ID
            # [payment_intent_data] - capture the payment later
            # [customer_email] - prefill the email input in the form
            # For full details see https://stripe.com/docs/api/checkout/sessions/create

            # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
            checkout_session = stripe.checkout.Session.create(
                client_reference_id=request.user.id if request.user.is_authenticated else None,
                success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancelled/',
                payment_method_types=['card'],
                mode='payment',
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': 'T-shirt',
                        },
                        'unit_amount': 2500,
                    },
                    'quantity': 1,
                },
                    {
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {
                                'name': 'T-shirted',
                            },
                            'unit_amount': 2000,
                        },
                        'quantity': 1,
                    },
                ],
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})


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

    # Handle the checkout.session.completed event
    # if event['type'] == 'checkout.session.completed':
    #     print("Payment was successful.")

    # if event['type'] == 'payment_intent.created':
    #     # print(event['data']['payment_intent'])
    #     print(event['data']['object']['id'])

    # if event['type'] == 'payment_intent.':
    # print(event['type'])
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

        # cart = Cart.objects.get(user=request.user)

    return HttpResponse(status=200)


def calculate_order_amount(request):
    # Replace this constant with a calculation of the order's amount
    # Calculate the order total on the server to prevent
    # people from directly manipulating the amount on the client

    if not request.user.is_authenticated:
        return 0

    # try:
    #     total = Cart.objects.get(user=request.user).total
    # except Cart.DoesNotExist:
    #     total = 0
    #
    # return total

    total = 0
    cartItems = CartItem.objects.filter(user=request.user)

    # if cart.quantity == 0:
    #     return 0

    for cartItem in cartItems:
        total += cartItem.quantity * cartItem.product.price

    return total

    # return sum(item['amount'] for item in items)


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

    return_url = 'http://localhost:8000/store/'

    # 'cs_test_a13QbwYuk4laETM3BpCm80qnUys3DbDCPioKNHC9y2Q3UZPuMRBARDUuXt'

    portalSession = stripe.billing_portal.Session.create(
        customer=customer.customerID,
        return_url=return_url,
        locale='en',
    )
    return redirect(portalSession.url, code=303)

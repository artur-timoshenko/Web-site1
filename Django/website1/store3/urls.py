from django.urls import path, re_path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    re_path(r'^$', views.HomePageView.as_view(), name='HomePageView'),
    re_path(r'^cart/$', login_required(views.CartPageView.as_view(), login_url='/store3/sign-in/'), name='CartPageView'),
    re_path(r'^products/$', views.ProductsPageView.as_view(), name='ProductsPageView'),
    re_path(r'^sign-in/$', views.SignInPageView.as_view(), name='SignInPageView'),
    re_path(r'^sign-up/$', views.SignUpPageView.as_view(), name='SignUpPageView'),
    re_path(r'^sign-out/$', views.SignOutPageView.as_view(), name='SignOutPageView'),

    re_path(r'^cart/add/$', views.CartAdd, name='CartAdd'),
    re_path(r'^cart/remove/$', views.CartRemove, name='CartRemove'),
    re_path(r'^cart/change/$', views.CartChange, name='CartChange'),

    re_path(r'^stripe/complete/$', views.StripeCompleteView.as_view(), name='StripeCompleteView'),

    re_path(r'^stripe/config/$', views.StripeConfig, name='StripeConfig'),
    re_path(r'^stripe/payment/$', views.StripeCreatePayment, name='StripeCreatePayment'),
    re_path(r'^stripe/checkout/$', views.StripeCreateCheckoutSession, name='StripeCreateCheckoutSession'),
    re_path(r'^stripe/portal/$', login_required(views.StripeCreatePortalSession, login_url='/store3/sign-in/'), name='StripeCreatePortalSession'),
    re_path(r'^stripe/webhook/$', views.StripeWebhook, name='StripeWebhook'),
]

from django.urls import path, re_path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    re_path(r'^$', views.HomePageView.as_view(), name='HomePageView'),
    re_path(r'^sales/$', views.SalesPageView.as_view(), name='SalesPageView'),
    re_path(r'^new/$', views.NewPageView.as_view(), name='NewPageView'),
    re_path(r'^season/$', views.SeasonPageView.as_view(), name='SeasonPageView'),
    re_path(r'^cart/$', login_required(views.CartPageView.as_view(), login_url='/store2/sign-in/'), name='CartPageView'),

    re_path(r'^sign-in/$', views.SignInPageView.as_view(), name='SignInPageView'),
    re_path(r'^sign-up/$', views.SignUpPageView.as_view(), name='SignUpPageView'),
    re_path(r'^sign-out/$', views.SignOutPageView.as_view(), name='SignOutPageView'),

    re_path(r'^cart/add/$', views.CartAdd, name='CartAdd'),
    re_path(r'^cart/remove/$', views.CartRemove, name='CartRemove'),
    re_path(r'^cart/change/$', views.CartChange, name='CartChange'),

    re_path(r'^stripe/complete/$', views.StripeCompleteView.as_view(), name='StripeCompleteView'),
    re_path(r'^stripe/config/$', views.StripeConfig, name='StripeConfig'),
    re_path(r'^stripe/payment/$', views.StripeCreatePayment, name='StripeCreatePayment'),
    re_path(r'^stripe/webhook/$', views.StripeWebhook, name='StripeWebhook'),
    re_path(r'^stripe/portal/$', views.StripeCreatePortalSession, name='StripeCreatePortalSession'),
]

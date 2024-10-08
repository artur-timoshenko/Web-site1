from django.urls import path, re_path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    # re_path(r'^api/$', views.ApiPageVew.as_view(), name='ApiPageView'),

    re_path(r'^$', views.HomePageView.as_view(), name='HomePageView'),
    re_path(r'^catalog/$', views.CatalogPageView.as_view(), name='CatalogPageView'),
    re_path(r'^checkout/$', login_required(views.CheckoutPageView.as_view(), login_url='/store/sign-in/'), name='CheckoutPageView'),

    re_path(r'^sign-in/$', views.SignInPageView.as_view(), name='SignInPageView'),
    re_path(r'^sign-up/$', views.SignUpPageView.as_view(), name='SignUpPageView'),
    re_path(r'^sign-out/$', views.SignOutPageView.as_view(), name='SignOutPageView'),

    re_path(r'^product/(?P<id>[^\\/]+)/$', views.ProductPageView.as_view(), name='ProductPageView'),

    re_path(r'^cart/add/$', views.CartAdd, name='CartAdd'),
    re_path(r'^cart/remove/$', views.CartRemove, name='CartRemove'),
    re_path(r'^cart/change/$', views.CartChange, name='CartChange'),


    re_path(r'^stripe/success/$', views.StripeSuccessView.as_view(), name='StripeSuccessView'),
    re_path(r'^stripe/cancelled/$', views.StripeCancelledView.as_view(), name='StripeCancelledView'),
    re_path(r'^stripe/complete/$', views.StripeCompleteView.as_view(), name='StripeCompleteView'),
    re_path(r'^stripe/config/$', views.StripeConfig, name='StripeConfig'),
    re_path(r'^stripe/session/$', views.StripeCreateSession, name='StripeCreateSession'),
    re_path(r'^stripe/payment/$', views.StripeCreatePayment, name='StripeCreatePayment'),
    re_path(r'^stripe/webhook/$', views.StripeWebhook, name='StripeWebhook'),
    re_path(r'^stripe/portal/$', views.StripeCreatePortalSession, name='StripeCreatePortalSession'),
]

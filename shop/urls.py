from django.urls import path
from . import views
from django.urls import include


urlpatterns = [
    path("", views.home, name="ShopHome"),
    path("contact/", views.contact, name="ContactUs"),
    path("add_api/", views.add_api, name="add_api"),
    path("terms/", views.terms, name="terms"),
    path("error/", views.error, name="error"),
    path("signup", views.signup, name="signup"),
    path("handleLogin", views.handleLogin, name="handlelogin"),
    path("index", views.index, name="index"),
    path("settings", views.setting, name="settings"),
    path("handleLogout", views.handleLogout, name="handleLogout"),
    path("resendOTP", views.resendOTP, name="resendOTP"),
    path("key", views.key, name="key"),
    path("forgot", views.forgot, name="forgot"),
    path("webhook_alert", views.webhook_alert, name='webhook_alert'),

]

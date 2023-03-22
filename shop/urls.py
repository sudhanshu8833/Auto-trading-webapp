from django.urls import path
from . import views
from django.urls import include


urlpatterns = [
    path("", views.home, name="ShopHome"),
    path("contact/", views.contact, name="ContactUs"),
    path("add_api/", views.add_api, name="add_api"),
    path("strategy/", views.strategies, name="strategy"),
    path("personal/", views.personal, name="personal"),
    path("error/", views.error, name="error"),
    path("signup", views.signup, name="signup"),
    path("handleLogin", views.handleLogin, name="handlelogin"),
    path("index", views.index, name="index"),
    path("setting", views.setting, name="setting"),

    path("handleLogout", views.handleLogout, name="handleLogout"),
    path("resendOTP", views.resendOTP, name="resendOTP"),
    path("key", views.key, name="key"),
    path("forgot", views.forgot, name="forgot"),
    path("webhook_alert", views.webhook_alert, name="webhook_alert"),
    path("activate_bot/<str:passphrase>", views.activate_bot, name='activate_bot'),


    path("start_thread", views.start_thread, name="start_thread"),
]



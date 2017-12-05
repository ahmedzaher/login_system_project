from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'login', views.login, name='login'),
    url(r'successLogin', views.successLogin, name='successLogin'),
    url(r'forgetPassword', views.forgetPassword, name='forgetPassword'),
    url(r'sendResetCode', views.sendResetCode, name='sendResetCode'),
    url(r'recoverPassword', views.recoverPassword, name='recoverPassword'),
    url(r'profilePage', views.profilePage, name='profilePage'),
    url(r'changeName', views.changeName, name='changeName'),
    url(r'changePassword', views.changePassword, name='changePassword'),
    url(r'uploadFilePage', views.uploadFilePage, name='uploadFilePage'),
    url(r'serverAndBrowserInfo', views.serverAndBrowserInfo, name='serverAndBrowserInfo'), 
    url(r'calcDistance', views.calcDistance, name='calcDistance'), 
    url(r'logout', views.logout, name='logout'),
    
]
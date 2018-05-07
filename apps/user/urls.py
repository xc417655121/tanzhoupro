"""tanzhoupro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from user.views import IndexView, LoginView, LogoutView,RegisterView,ActiveUserView,ForgetPwdView,ResetView,ModifyPwdView,UserInfoView,ChangePwdView

urlpatterns = [
    # 主页
    url(r'^index/$', IndexView.as_view(),name='index'),
    # 登录页面
    url(r'^login/$', LoginView.as_view(),name='login'),
    # 退出登录
    url(r'^logout/$', LogoutView.as_view(),name='logout'),
    # 注册页面
    url(r'^register/$', RegisterView.as_view(),name='register'),
    # 激活邮箱
    url(r'^active/(?P<active_code>.*)/$', ActiveUserView.as_view(),name='register'),


    # 忘记密码
    url(r'^forget_pwd/$', ForgetPwdView.as_view(), name='forget_pwd'),

    # 修改密码get
    url(r'^reset/(?P<reset_code>.*)/$', ResetView.as_view(), name='reset_pwd'),

    # 修改密码post
    url(r'^modify_pwd/$', ModifyPwdView.as_view(), name="modify_pwd"),


    # 用户

    # 用户信息
    url(r'info/$', UserInfoView.as_view(), name='info'),

    # 修改密码
    url(r'change_pwd/$', ChangePwdView.as_view(), name='change_pwd'),


]

from django.shortcuts import render
from django.views import View
# Create your views here.
from user.forms import LoginForm,RegisterForm,ForgetPwdForm,ModifyPwdForm,ChangePwdForm
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import HttpResponseRedirect
from django.contrib.auth.hashers import make_password

from django.contrib.auth.backends import ModelBackend
from user.models import UserInfo,EmailVerify
from django.db.models import Q

from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequiredMixin

# 重写authenticate方法
class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserInfo.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None

# 主页
class IndexView(View):
    def get(self,request):
        return render(request, 'index.html')

# 登录
class LoginView(View):
    def get(self,request):
        return render(request,'login.html',{})

    def post(self,request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username","")
            pass_word = request.POST.get("password","")
            user = authenticate(username=user_name,password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return HttpResponseRedirect(reverse("user:index"))
                else:
                    return render(request,'login.html',{'mess':'用户未激活!'})
            else:
                return render(request,'login.html',{'mess':'用户名或密码有误!'})
        else:
            return render(request,'login.html',{'login_form':login_form})

# 退出登录
class LogoutView(View):
    def get(self,request):
        logout(request)
        return render(request,'index.html',{})


# 注册
class RegisterView(View):
    def get(self,request):
        register_form = RegisterForm()
        return render(request,'register.html',{'register_form' : register_form})

    def post(self,request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            email = request.POST.get('email','')
            if UserInfo.objects.filter(email=email):
                return render(request,'register.html',{'register_form':register_form,
                                                       'message':'用户已经存在!'})
            pass_word = request.POST.get('password','')

            user_profile = UserInfo()
            user_profile.username = email
            user_profile.email = email
            user_profile.is_active = False
            user_profile.password = make_password(pass_word)
            user_profile.save()

            # 发送邮箱,这里会生成一个16位随机数并存储到EmailVerify中
            send_register_email(email,'register')
            return HttpResponseRedirect(reverse('user:login'))
        else:
            return render(request,'register.html',{'register_form':register_form})


# 激活邮箱
class ActiveUserView(View):
    def get(self,request,active_code):
        all_records = EmailVerify.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserInfo.objects.get(email=email)
                user.is_active = True
                user.save()
                return render(request,'success_active.html')
            return render(request, 'login.html')


class ForgetPwdView(View):
    def get(self,request):
        forget_form = ForgetPwdForm()
        return render(request,'forgetpwd.html',{'forget_form':forget_form})

    def post(self,request):
        forget_form = ForgetPwdForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email','')
            if UserInfo.objects.filter(email=email):
                send_register_email(email,'forget')
                return render(request,'send_success.html',{'email':email})
            return render(request,'forgetpwd.html',{'forget_form':forget_form,'msg':u'用户不存在!'})
        else:
            return render(request,'forgetpwd.html',{'forget_form':forget_form})

# 修改密码
class ResetView(View):
    def get(self,request,reset_code):
        all_records = EmailVerify.objects.filter(code=reset_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request,'password_reset.html',{'email':email})

# 确认修改密码
class ModifyPwdView(View):
    def post(self,request):
        modify_form = ModifyPwdForm(request.POST)

        if modify_form.is_valid():
            pwd1 = request.POST.get('password1','')
            pwd2 = request.POST.get("password2", "")
            email = request.POST.get("email", "")
            if pwd1 != pwd2:
                return render(request,'password_reset.html',{'email':email,'msg':'密码不一致!'})

            user = UserInfo.objects.get(email=email)
            user.password = make_password(pwd1)
            user.save()
            return render(request,'reset_success.html')
        else:
            email = request.POST.get('email','')
            return render(request,'password_reset.html',{'email':email,'modify_form':modify_form})


# 关于用户信息
class UserInfoView(LoginRequiredMixin,View):
    def get(self,request):
        return render(request,'my_info.html',{})


# 关于用户密码修改
class ChangePwdView(LoginRequiredMixin, View):
    def get(self, request):
        email = request.user.email
        return render(request, 'my_paasword.html', {'email': email})

    def post(self,request):
        change_form = ChangePwdForm(request.POST)
        email = request.user.email
        if change_form.is_valid():
            pwdold = request.POST.get('passwordold','')
            email = request.POST.get('email','')
            user = authenticate(username=email,password=pwdold)
            if user is not None:
                pwd1 = request.POST.get("password1", "")
                pwd2 = request.POST.get("password2", "")
                if pwd1 != pwd2:
                    return render(request, "my_paasword.html", {"email": email, "msg": u"密码不一致"})
                user = UserInfo.objects.get(email=email)
                user.password = make_password(pwd2)
                user.save()

                return render(request,'reset_success.html')
            else:
                return render(request,'my_paasword.html',{'email':email,'msg':'旧密码有误!'})
        return render(request,'my_paasword.html',{'email':email,'change_form':change_form})
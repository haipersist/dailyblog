# -*- coding: utf-8 -*-
"""
the views includes RegisterView, \
                      LoginView,ajaxlogin, \
                      ForgetPasswdView, \
                      ChangePasswdView,\
                      ResetPasswdView,\
                      active_user,\
                      UserprofileView,\
                      ChangeUserprofileView



"""

from __future__ import unicode_literals
from django.http import HttpResponse,HttpResponseRedirect
from django.views.generic import DetailView,FormView
import logging
from dailyblog.settings import SECRET_KEY
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import SetPasswordForm
from django.contrib import auth
from django.core.mail import send_mail
from django.contrib.auth.models import User
from utils.jsonify import jsonify
from utils.token import Token
from django.contrib.auth import get_user_model

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.core.cache import caches
from models import UserProfile
from forms import UserProfileForm,UserChangePasswdForm,UserLoginForm, \
      CustomUserCreationForm,UserPasswordResetForm
from django.forms import ValidationError
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages



logger = logging.getLogger(__name__)




cache = caches['memcache']
token_confirm = Token(SECRET_KEY)



class RegisterView(FormView):
    template_name = 'account/register.html'
    success_url = '/account/login/'
    form_class = CustomUserCreationForm

    def form_valid(self, form):

        username,email = form.create_account_without_active()

        token = token_confirm.generate_validate_token(username)
        global DOMAIN
        DOMAIN = DOMAIN.rstrip('/')
        message = "\n".join([
            '{0},欢迎加入我的博客'.format(username),
            '请访问该链接，完成用户验证:',
            '/'.join([DOMAIN, 'account/activate', token]) + '/'
        ])
        send_mail('注册用户验证信息', message, None, [email])
        try:
            send_mail('有新注册用户啦！', username, None, ['393993705@qq.com', 'hbnnlong@163.com'])
        finally:
            return HttpResponse("请登录到注册邮箱中验证用户，有效期为1个小时。")

    def form_invalid(self, form):
        #form._clean_form()
        #about invalid,I should add some custom program.
        return super(RegisterView,self).form_invalid(form)



def active_user(request,token):
    """
    the view function is used to accomplish the user register confirm,
    only after input the link
    that sent to the register email,user can login the site normally.
    :param request:
    :param activate_key:the paragram is gotten by encrypting username when user register
    :return:
    """
    try:
        username = token_confirm.confirm_validate_token(token,expiration=3600)
    except:
        return HttpResponse('对不起，验证链接已经过期')
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return HttpResponse('对不起，您所验证的用户不存在，请重新注册')
    if not user.is_active:
        user.is_active = True
        user.save()
        confirm = '验证成功，请进行登录操作。'
        return HttpResponseRedirect('/account/login/',{'confirm':confirm})
    else:
        return HttpResponseRedirect('该用户已经激活，可直接登录！')





class LoginView(SuccessMessageMixin,FormView):
    template_name = 'account/login.html'
    form_class = UserLoginForm
    success_url = '/'
    success_message = 'login success,Welcome'

    def get(self, request, *args, **kwargs):
	#self.success_url = request.path
        self.success_url = request.session['login_from'] = request.META.get('HTTP_REFERER', '/')
        return super(LoginView,self).get(request, *args, **kwargs)

    def form_valid(self, form):
        """
        the post method call it auto.

        """
        try:
            form.validate_account(self.request)
        except ValidationError,e:
            form.add_error('password',e)
            form._clean_form()
            return self.render_to_response(self.get_context_data(form=form))
        
	try:
            self.success_url = self.request.session.get('login_from', '/')
        except:
            pass
	
        if '/account/login/' in self.success_url:
            self.success_url ='/'
        return super(LoginView,self).form_valid(form)

    def form_invalid(self, form):
        return super(LoginView,self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(LoginView,self).get_context_data(**kwargs)
        return context





def ajax_login(request):
    """
    In fact,I don't need write this function for ajax login,
    I can complete it in LoginView by adding request.is_ajax.
    I write it seperatly,aims at making it more clear.

    :param request:
    :return:
    """
    username = request.POST.get('username',None)
    password = request.POST.get('password',None)
    user = auth.authenticate(username=username,password=password)
    errors = []
    if user is not None:
        auth.login(request,user)
    else:
        errors.append(u'用户名或密码不正确')

    return HttpResponse(
        jsonify(errors=errors),
        content_type="application/json"
    )


@login_required(login_url='/account/login/')
def Logout(request):
    auth.logout(request)
    messages.success(request,u'You have logged out,Good bye')
    return HttpResponseRedirect('/')



class ChangePasswdView(FormView):

    template_name = 'account/changepassword.html'
    success_url = '/account/login/'
    form_class = UserChangePasswdForm

    #the UserChangePasswdForm must add user parameter,so need reconstruct get_form
    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(self.request.user,**self.get_form_kwargs())

    def form_valid(self, form):
        form.save()
        auth.logout(self.request)
        return super(ChangePasswdView,self).form_valid(form)


class ForgetPasswdView(FormView):
    template_name = 'account/forgetpasswd.html'
    form_class = UserPasswordResetForm
    success_url = '/'

    def form_valid(self, form):
        try:
            form.send()
        except ValidationError,e:
            form.add_error('email', e)
            form._clean_form()
            return self.render_to_response(self.get_context_data(form=form))
        return HttpResponse('check email')

def user_decorator(method):
    def wrapper(instance,request, *args, **kwargs):
        token_generator = default_token_generator
        UserModel = get_user_model()
        uidb64, token = instance.kwargs['uidb64'], instance.kwargs['token']
        assert uidb64 is not None and token is not None
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = UserModel._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            user = None
        if user is not None and token_generator.check_token(user, token):
            instance.request.user = user
            return method(instance,request, *args, **kwargs)
        else:
            return HttpResponse('link expires')
    return wrapper



class ResetPasswdView(FormView):
    template_name = 'account/resetpwd.html'
    form_class = SetPasswordForm
    success_url = '/'

    @user_decorator
    def get(self, request, *args, **kwargs):
        return super(ResetPasswdView,self).get(request, *args, **kwargs)


    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(self.request.user, **self.get_form_kwargs())

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect('/account/login/')

    @user_decorator
    def post(self, request, *args, **kwargs):
        return super(ResetPasswdView,self).post(request,*args,**kwargs)







class ChangeUserprofileView(FormView):
    form_class = UserProfileForm
    success_url = '/account/userprofile/'
    template_name = 'account/changeuserprofile.html'

    def form_valid(self, form):
        if self.request.FILES.has_key('avator'):
            form.instance.avator = self.request.FILES['avator']
        form.save()
        return super(ChangeUserprofileView,self).form_valid(form)

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        profile = UserProfile.objects.get_or_create(user=self.request.user)[0]
        return form_class(instance=profile,**self.get_form_kwargs())



class UserProfileView(DetailView):
    queryset = UserProfile.objects.all()
    context_object_name = 'userprofile'
    template_name = 'account/userprofile.html'

    def get(self, request, *args, **kwargs):
        user = self.request.user
        self.object = UserProfile.objects.get_or_create(user=user)[0]
        context = self.get_context_data(userprofile=self.object)
        context['user'] = self.request.user
        #context['publish_article'] = len(Article.objects.filter(author=user))
        return self.render_to_response(context)

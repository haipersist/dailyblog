# -*- coding: utf-8 -*-

#from __future__ import unicode_literals
from django.forms import ModelForm,Form,CharField,PasswordInput,EmailField, Textarea
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm,PasswordResetForm
from django.contrib.auth.models import User
from models import UserProfile
from django import forms
from django.contrib import auth
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.conf import settings


class UserLoginForm(Form):

   error_messages = {
       'password_incorrect':u'password incorrect'
   }
   username = CharField(max_length=30,
                        error_messages={
                            'required':u"用户名未填写",
                            'invalid':u"用户名不符合标准"},
                        help_text=u'用户名必须为数字，字母或下划线等')
   password = CharField(
        widget=PasswordInput,
        error_messages={
            'required': u"密码未填写"
            }
   )

   def validate_account(self,request):
        cd = self.cleaned_data
        username,password = cd['username'],cd['password']

        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
        else:
            raise forms.ValidationError(
                self.error_messages['password_incorrect'],
                code='password_incorrect'
            )




class CustomUserCreationForm(UserCreationForm):

    error_messages = {
        'password_mismatch': u"两次新密码不匹配",
        'email_incorrect': u'邮箱不正确，请填写正确邮箱，否则收不到激活邮件！'
   }
    email = EmailField(
        error_messages={
            'invalid':  u"email格式错误",
            'required': u'email未填'},
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields

        error_messages = {
            'username': {
                'required':u"用户名未填写",
                'invalid':u'无效，只允许字母，数字，下划线,@等',
                'unique':u'用户名已经注册，请更改用户名'},
        }


    def create_account_without_active(self):
        cd = self.cleaned_data
        username, password, email = cd['username'], cd['password1'], cd['email']
        if not User.objects.filter(username=username):
            user = User.objects.create(username=username, password=password, email=email, is_active=False)
            user.set_password(password)
            user.save()
            return username,email

    def clean_email(self):
        email = self.cleaned_data.get("email")
        #add some logic to validate email further
        if '126' not in email:
            raise forms.ValidationError(
                self.error_messages['email_incorrect'],
                code='email_incorrect',
            )

        return email


class UserChangePasswdForm(PasswordChangeForm):
    error_messages = {'password_mismatch': u"两次新密码不匹配",
                      'password_incorrect':u'旧密码错误!'
                      }

class UserPasswordResetForm(PasswordResetForm):

    def send(self):
        email = self.cleaned_data['email']
        DOMAIN = settings.DOMAIN
        global  DOMAIN
        DOMAIN = DOMAIN.rstrip('/')
        token_generator = default_token_generator
        if len(list(self.get_users(email))) == 0:
            raise forms.ValidationError('user not exists')
        for user in self.get_users(email):
            uid = urlsafe_base64_encode(force_bytes(user.id))
            token = token_generator.make_token(user)
            message = "\n".join([
                '您的用户名是:{0}'.format(user.username),
                '请访问该链接，进行密码重置:',
                '/'.join([DOMAIN, 'account/resetpwd', uid, token]) + '/',
            ])
            send_mail('注册用户密码重置', message, None, [email])



class UserProfileForm(ModelForm):

    class Meta:
        model = UserProfile
        #fields = ['avator','age','school','gender','hobby',
         #         'motto','self_introduction','birthday','user']
        fields = '__all__'
        error_messages = {
            'age': {
                    'required': u"年龄未填写",
                    'invalid': u"必须是整数"},
        }
        help_text = {
            'age':u'年龄必须为数字'
        }
        widgets = {
            'self_introduction':Textarea(attrs={'cols':100,'rows':8})
        }




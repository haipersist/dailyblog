# -*- coding: utf-8 -*-


from django.forms import ModelForm,Form,CharField,PasswordInput,EmailField
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm,UserChangeForm
from django.contrib.auth.models import User
from .models import Article


class UserLoginForm(Form):
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


class CustomUserCreationForm(UserCreationForm):
    email = EmailField(
        error_messages={
            'invalid':  u"email格式错误",
            'required': u'email未填'},
    )
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)


class BlogChangePasswdForm(PasswordChangeForm):
    error_messages = {'password_mismatch': u"两次新密码不匹配",
                      }


class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ['title','alias','content','access','tags','author','category']














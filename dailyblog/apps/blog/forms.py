# -*- coding: utf-8 -*-


from django.forms import ModelForm,Form,CharField,PasswordInput,EmailField, \
    DateField,IntegerField,ImageField,Textarea
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm,UserChangeForm
from django.contrib.auth.models import User
from .models import Article
from ..account.models import UserProfile
from models import Category
from utils.papercode import PaperCode
from utils.extract_from_content import extract_trip

from ..blog.tasks import change_img
from datetime import date


class BlogChangePasswdForm(PasswordChangeForm):
    error_messages = {'password_mismatch': u"两次新密码不匹配",
                      }




class UserProfileForm(ModelForm):

    """
    avator = ImageField(required=False)
    age = IntegerField(error_messages={
                             'required': u"年龄未填写",
                             'invalid': u"必须是整数"},
                       help_text = u'用户名必须为数字，字母或下划线等',
    )
    school = CharField(max_length=48, required=False)
    gender = CharField(error_messages={
        'required': u"性别未填写",
        'invalid': u"必须是男或者女"},
    )
    hobby = CharField(required=False)
    motto = CharField(required=False)
    self_introduction =Textarea()
    birthday = DateField(error_messages={
        'required': u"日期未填写",
        'invalid': u"必须填写正确日期，格式：0000-00-00"},
    )
    """
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





class ArticleForm(ModelForm):

    def form_save(self, request, add=True, object=None):
        """
        the method only return one tuple which is used in trip
        so if the article is not trip,it will return ()
        :param request:
        :param add:if create article add is True ,or else, False
        :param object:if add is False,you must pass one object to modify
        :return:
        """
        cd = self.cleaned_data
        access, title, alias, content, abstract, tags, category = \
            cd['access'], cd['title'], cd['alias'],cd['content'], cd['abstract'], cd['tags'],cd['category']
        qrcode = PaperCode()
        qrcode_url = qrcode.store_qrcode(alias)
        if add:
            article = Article(author=request.user,
                              title=title,
                              alias=alias,
                              content=content,
                              category=category,
                              tags=tags,
                              access=access,
                              abstract=abstract,
                              qrcode=1,
                              qrcode_url=qrcode_url)
            article.ck_save()
            content = change_img(alias)
            #the id is trip id
            if category.id == 28:
                trip_date = request.POST.get('trip_date','')

                trip_date = trip_date if trip_date \
                    else date.today().strftime("%Y-%m-%d")
                    #errors.append(u'填写旅游日期')
                article_url = '/article/' + alias + '.html'
                img = extract_trip(content)
                return article_url, title, img, abstract, trip_date
        else:
            article = object
            article.title,article.alias,article.content,article.category,article.tags,article.access = \
                title,alias,content,category,tags,access
            article.ck_save()
            content = change_img(alias)
        return ()


    class Meta:
        model = Article
        fields = ['title','alias','content','access','tags','category','abstract']
        error_messages = {
            'title':{
                'required':'标题必须填写',
            },
            'alias':{
                 'required':'英文标题必须填写',
            },
             'content':{
                'required':'正文必须填写',
            },
             'tags':{
                'required':'标签必须填写',
                 'invalid':'请用英文逗号分隔'
            },
             'abstract':{
                'required':'摘要必须填写',
            },
        }
        widgets = {
            'abstract': Textarea(attrs={'cols': 100, 'rows': 8})
        }






# -*- coding: utf-8 -*-

#from __future__ import unicode_literals


import datetime
from models import Article,Comment,ReplyComment,Author
from django.views.generic import View,ListView,CreateView,DetailView
from django.http import JsonResponse
from utils.djmodel2dict import djmodel2dict
from utils.token import Token
from utils.get_real_ip import get_real_ip
from utils.validate_email import ValidateEmail
from utils.cache import Cache
import logging


logger = logging.getLogger(__name__)




cache = Cache()



class CommentListView(ListView):

    def get(self,request,*args,**kwargs):
        #the parameter args,kwargs must exists
        self.article_id = kwargs.get('articleid')
        article = Article.objects.get(id=self.article_id)
        comment_list= Comment.objects.filter(article=article)
        comments = []
        if comment_list.exists():
            for comment in comment_list:
                replies = self.get_reply(comment)
                comment = djmodel2dict(comment)
                comment['replies'] = replies
                comments.append(comment)

        return JsonResponse({'comments':comments})


    def get_reply(self,comment):
        replies = ReplyComment.objects.filter(comment=comment)
        if replies.exists():
            replies = map(djmodel2dict,replies)
            return replies
        else:
            return []




class CreateCommentView(CreateView):
    """
    the comment should divide into two categories:
        1. the comment for article.
            Comment
        2.the reply for the comment.
            ReplyComment

    In additions,the author may be guest or logined user
    As for logined user,it's very easy,however the guest may be
    a little complex.
    the request should post several parameters:
       1.content
       2.reply
       3.commentid
       4.toid
       5.username
       6.useremail
    and the kwargs should contains articleid.

    Test:
     curl -X POST -H 'X-CSRFToken:7FzJqhh3EIjYyvRdD0EuJOSrPjcyAn54'
      -d "content=testajaxcsrfpost&username=testpost&useremail=hbnnlong@163.com"
      -b 'csrftoken=7FzJqhh3EIjYyvRdD0EuJOSrPjcyAn54'
       http://localhost/dashboard/comment/article/1/create/



    """
    model = Comment


    #@method_decorator(csrf_exempt)
    def post(self, request, *args, **kwargs):
        content = request.POST.get('content')
        reply = request.POST.get('reply','-1')
        articleid = kwargs.get('articleid')
        self.message = ''
        if reply == '1':
            #if reply is 1,the comment is a reply comment
            comment = ReplyComment()
            commentid = request.POST.get('commentid')
            original_comment = Comment.objects.filter(pk=commentid)
            if not original_comment.exists():
                self.message = 'comment dose not exists'
                return JsonResponse({'msg':self.message})
            comment.comment = original_comment[0]
            toid = request.POST.get('toid')
            comment.reply_to = Author.objects.get(pk=toid)
        else:
            #or else,the comment is first comment
            comment = Comment()
            article = Article.objects.filter(pk=articleid)
            if not article.exists():
                self.message = 'article does not exists'
            comment.article = article[0]
        if not content:
            self.message = 'please input message '
        else:
            comment.content = content

        #the author field,it is a little complex
        user = request.user
        if not user.is_authenticated():
            #return JsonResponse({'user':user})
            confir_token = Token()
            commenttoken = request.session.get('commenttoken',False)
            if commenttoken:
                #the token is in session.
                try:
                    email = confir_token.confirm_validate_token(commenttoken)
                    author = Author.objects.get(email=email)
                except:
                    return JsonResponse({'msg':'tokenexpire'})
            else:
                email = request.POST.get('useremail','')
                name = request.POST.get('username',u'游客')
                if not email:
                    return JsonResponse({'msg':'emailempty'})
                if not ValidateEmail(email):
                    return JsonResponse({'msg':'emailformat'})
                token = confir_token.generate_validate_token(email)
                request.session['commenttoken'] = token
                author = Author.objects.filter(email=email)
                if not author.exists():
                    author = Author()
                    author.name, author.email = name, email
                    author.save()
                    author = Author.objects.get(email=email)
                else:
                    author = author[0]
        else:
            author = Author.objects.filter(name=user.username)
            if author.exists():
                author = author[0]
            else:
                author = Author()
                author.name = user.username
                author.email = user.email
                author.save()

        comment.author = author
        comment.ip = get_real_ip(request)
        comment.save()
        self.message = 'success'

        return JsonResponse({'msg':'success'})




class CommentAuthorView(View):
    queryset = Author.objects.all()
    slug_field = 'authorid'
    from django.core import serializers

    def get(self, request, *args, **kwargs):
        authorid = self.kwargs.get('slug')
        try:
            self.object = self.queryset.get(pk=authorid)
        except Author.DoesNotExist:
            return JsonResponse({'error':'author dose not exist'})
        return JsonResponse({'comment_user':djmodel2dict(self.object)})

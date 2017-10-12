# -*- coding: utf-8 -*-

#from __future__ import unicode_literals
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.views.generic import DetailView,ListView,FormView,View
import logging
from django.http import Http404
from dailyblog.settings import NUM_PER_PAGE,SECRET_KEY
#from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.exceptions import PermissionDenied
from django.core.cache import caches
from django.core.mail import send_mail
from django.contrib.auth.models import User
from utils.permissions import UserPermisson,ArticlePermisson
from .models import Article,Category,OnlineArticle
from ..trip.models import Trip
from utils.token import Token
from django.template.context_processors import csrf
from utils.resources.wechat.Wechat import Wechat
from utils.resources.wechat.music import MusicDict
from django.views.decorators.csrf import csrf_exempt
from utils.resources.wechat.papercode import PaperCode
from utils.resources.wechat.xhj import XHJ
from utils.cache import Cache
from .tasks import incr_readtimes
from utils.logion import get_logion


logger = logging.getLogger(__name__)




cache = Cache()


token_confirm = Token(SECRET_KEY)


class BaseMixin(object):

    def get_context_data(self,*args,**kwargs):
        context = super(BaseMixin, self).get_context_data(**kwargs)
        try:
            context['website_title'] = u'千与千寻'
            context['logion'] = get_logion()
            context['display_page_range'] = range(-3, 4)
            context['carousel_page_list'] = Trip.objects.all()[0:5]
            context['online_ips'] = len(cache.get('onlines'))

        except Exception:
            logger.error('load inital context fails')

        return context


class IndexView(BaseMixin,ListView):
    template_name = 'index.html'
    paginate_by = NUM_PER_PAGE
    context_object_name = 'article_list'

    def get_queryset(self):
        self.keyword = self.request.GET.get('keyword')
        if not self.keyword:
            self.article_list =  []
        else:
            query_sql =( Q(title__icontains=self.keyword) | Q(content__icontains=self.keyword))
            self.article_list = Article.objects.defer('content','content_html').filter(query_sql,status=0)
        return self.article_list

    def get_context_data(self,*args,**kwargs):
        context = super(IndexView,self).get_context_data(**kwargs)
        context['keyword'] = self.keyword
        return context




class ArticleDetailView(BaseMixin,DetailView):
    queryset = Article.objects.filter(status=0)
    slug_field = 'alias'
    context_object_name = 'article'
    template_name = 'article.html'
    object = None

    def get(self, request, *args, **kwargs):
        alias = self.kwargs.get('slug')
        try:
            self.object = self.queryset.get(alias=alias)
        except Article.DoesNotExist:
            logger.error('article does not exsists')
            #I should rewrite the 404 html later
            return Http404
        # add permission,if the article has set permission,the web will raise one exveption
        if not self.object.can_access(request.user):
            raise PermissionDenied
        #Here,it should be set cache,which store the visited IP
        #Article.objects.filter(id=self.object.id).update(read_times=F('read_times')+1)
        incr_readtimes.delay(self.object.id)
        #If the article's qrcode is 0,generate and add qrcode_url into db:blog_article
        if self.object.qrcode == 0:
            qrcode = PaperCode()
            qrcode_url = qrcode.store_qrcode(self.object.alias)
            self.object.qrcode_url = qrcode_url
            Article.objects.filter(id=self.object.id).update(qrcode=1)
            Article.objects.filter(id=self.object.id).update(qrcode_url=qrcode_url)
        context = self.get_context_data(article=self.object)
        #context['visited_ips'] = len(visited_ips)
        return self.render_to_response(context)


    def get_context_data(self,**kwargs):
        context = super(ArticleDetailView,self).get_context_data(**kwargs)
        context['view_article_title'] = 'show detail article'
        return context



class CategoryArticleListView(BaseMixin,ListView):
    template_name = 'category.html'
    paginate_by = NUM_PER_PAGE
    context_object_name = 'article_list'

    def get_queryset(self):
        alias = self.kwargs.get('alias')
        try:
            self.category = Category.objects.get(alias=alias)
        except Category.DoesNotExist:
            logger.error('no this category')
        article_list = self.category.article_set.all()
        return article_list

    def get_context_data(self,*args,**kwargs):
        kwargs['category_name'] = self.category.name
        return super(CategoryArticleListView,self).get_context_data(**kwargs)



class TagArticleListView(BaseMixin,ListView):
    template_name = 'tag.html'
    paginate_by = NUM_PER_PAGE
    context_object_name = 'article_list'

    def get_queryset(self):
        self.tag = self.kwargs.get('article_tag')
        article_list = Article.objects.defer('content','content_html').filter(tags__icontains=self.tag,status=0)
        return article_list

    def get_context_data(self,*args,**kwargs):
        kwargs['tag_name'] = self.tag
        return super(TagArticleListView,self).get_context_data(**kwargs)




class AuthorView(BaseMixin,ListView):

    template_name = 'author_information.html'
    context_object_name = 'categories'

    """
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
         return super(AuthorView, self).dispatch(*args, **kwargs)
    """

    def get_queryset(self):
        categories = Category.available_categories()
        return categories

    def get_context_data(self,*args,**kwargs):
        return super(AuthorView,self).get_context_data(**kwargs)





class WechatView(View):

    def get(self,request,*args,**kwargs):
        chat = Wechat()
        signature = request.GET.get('signature')
        timestamp = request.GET.get('timestamp')
        nonce = request.GET.get('nonce')
        echostr = request.GET.get('echostr')
        return HttpResponse(chat.auth(timestamp,nonce,signature,echostr))

    def post(self,request,*args,**kwargs):
        chat = Wechat()
        mc = cache
        chat.parse_data(request.body)

        if chat.msgtype == 'event':
            if chat.msg.event == 'subscribe':
                reply = u'欢迎关注我的公众号，本公众号可提供与机器人对话，音乐收听，收藏文章等功能。详情可输入"帮助"查询。' \
                        u'如有兴趣，可访问我的个人网站：http://www.hbnnforever.com(Flask开发）；http://dailyblog.applinzi.com(Django开发）'
                return HttpResponse(chat.resp_text(reply))
            elif chat.msg.event == 'SCAN':
                pass
            elif chat.msg.event == 'LOCATION':
                pass
            else:
                return HttpResponse(chat.resp_text(u'其他推送消息'))
        elif chat.msgtype == 'link':
            chat.insert_article(title=chat.msg.title,
                                desc=chat.msg.desc,
                                url=chat.msg.url)
            return HttpResponse(chat.resp_text(u'文章存储成功!\n 若想查看，可输入"查看文章" '))

        elif chat.msgtype == 'text':
            content = chat.msg.content
            if content == u'音乐':
                mc.set(chat.msg.user+'_music','music')
                reply = [u'开始收听，音乐列表:\n\n',
                          u'1.石进-忆\n',
                          u'2.Marry me\n',
                          u'3.羽泉-烛光里的妈妈\n\n',
                          u'请输入序号进行收听。\n',
                          u'若停止收听，请输入"退出"，即可切换到与机器对话。']
                reply = ' '.join(reply)
                return HttpResponse(chat.resp_text(reply))

            elif content == u'退出':
                if mc.get(chat.msg.user+'_music'):
                    mc.delete(chat.msg.user+'_music')
                if mc.get(chat.msg.user+'_article'):
                    mc.delete(chat.msg.user+'_article')
                reply = u'欢迎下次欣赏！'
                return HttpResponse(chat.resp_text(reply))

            elif content == u'帮助':
                reply = [u'本公众号服务列表：\n\n',
                         u'1.本消息支持消息留言，作者会第一时间回复您;\n',
                         u'2.若想收听音乐，请输入"音乐"；输入"退出"可离开音乐播放;\n',
                         u'3.输入"查看文章"可查看现有的文章，输入"退出"可离开文章观看;\n'
                         ]
                reply = ' '.join(reply)
                reply = chat.resp_text(reply)
                return HttpResponse(reply)

            elif content == u'记忆':
                articles = [{'title':u'爱你','desc':u'记忆','picurl':'http://hbnn-hbnnstore.stor.sinaapp.com/boat.jpg',
                     'url':'http://blog.sina.com.cn/s/blog_a2356b8b0102vvq3.html'},
                    {'title':u'老婆我爱你','desc':u'记忆','picurl':'http://hbnn-hbnnstore.stor.sinaapp.com/europ.jpg',
                     'url':'http://finance.ifeng.com/a/20150630/13808481_0.shtml'}]
                return HttpResponse(chat.resp_article(articles))

            elif content == u'查看文章':
                mc.set(chat.msg.user+'_article','article')
                reply = chat.get_all_from_db()
                if reply is None:
                    return HttpResponse(chat.resp_text(u'文章较多，更多精品文章请到我的博客欣赏http://dailyblog.applinzi.com'))
                return HttpResponse(chat.resp_text(reply))
            else:
                article = mc.get(chat.msg.user+'_article')
                music = mc.get(chat.msg.user+'_music')
                if article == 'article':
                    try:
                        reply = chat.get_one_from_db(content)
                        if reply:
                            return HttpResponse(chat.resp_article(reply))
                        else:
                            return HttpResponse(chat.resp_text(u'请输入正确的文章序号;\n 若不查看文章，请输入"退出"\n'))
                    except:
                        return HttpResponse(chat.resp_text(u'请输入正确的文章序号;\n 若不查看文章，请输入"退出"\n'))
                if music == 'music':
                    try:
                        song = MusicDict[content]
                        title, desc, musicurl, hqurl = song['title'],song['desc'],song['url'],song['url']
                        return HttpResponse(chat.resp_music(title, desc, musicurl, hqurl))
                    except KeyError:
                        return HttpResponse(chat.resp_text(u'请输入正确的音乐序号;\n 若不收听，请输入"退出"\n'))
                try:
                    xhj = XHJ()
                    reply = xhj.resp(content)
                    reply = ':'.join(reply) if isinstance(reply,tuple) else reply
                except:
                     try:
                        chat.insert_data('wechat_messages',
                                     user=chat.msg.user,
                                     content=content,
                                     )
                     except Exception:
                        return HttpResponse(chat.resp_text(u'没能正确接收消息！'))
                     reply = u"""机器人暂时不能提供服务，您发送的消息我已收到，我会第一时间给您回复，您也可关注我的博客:http://dailyblog.applinzi.com. Good day!"""
                return HttpResponse(chat.resp_text(reply))


        else:
            return HttpResponse(chat.resp_text(u'待开发'))



def page_not_found(request):
    return render_to_response('errors/404.html')

def permission_forbidden(request):
    return render_to_response('errors/403.html')

def server_broken(request):
    return render_to_response('errors/500.html')




@csrf_exempt
def send_wechat_msg(request):
    chat = Wechat()
    try:
        return HttpResponse(chat.send_text_msg('oL0TOvvfbWBFcA3VgNU8y_LzWD98','test'))
        #return HttpResponse('send success')
    except Exception,e:
        return HttpResponse(str(e))




#@login_required(login_url='/account/login/')
def mail_to_bloger(request):
    user = request.user
    context = {}
    context.update(csrf(request))
    context['user'] = user
    errors = []
    written = False
    if request.method == "POST":
        title = request.POST.get('title')
        title = title if title is not None else u'吐槽你的博客'
        message = request.POST.get('content')
        send_mail(title,message, None,['hbnnlong@163.com','393993705@qq.com'])
        written = True

    context['written'] = written
    context['errors'] = errors
    return render_to_response('advise_to_bloger.html',context)




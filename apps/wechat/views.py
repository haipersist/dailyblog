#encoding:utf-8

import random
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View,ListView
from django.http import HttpResponse,HttpResponseRedirect
from django.utils.decorators import method_decorator

from utils.cache import Cache
from .wechat.Wechat import Wechat
from wechat.music import MusicDict
from .wechat.xhj import XHJ
from ..blog.views import BaseMixin
from utils.permissions import permission_forbidden
from ..blog.models import Article,Category
from .models import WeArticle
from .wechat.WechatArticle import Wechat_Spider
from utils.papercode import PaperCode



cache = Cache()


# Create your views here.



@method_decorator(csrf_exempt,name='dispatch')
class WechatView(View):

    chat = Wechat()

    def get(self,request,*args,**kwargs):
        signature = request.GET.get('signature')
        timestamp = request.GET.get('timestamp')
        nonce = request.GET.get('nonce')
        echostr = request.GET.get('echostr')
        return HttpResponse(self.chat.auth(timestamp,nonce,signature,echostr))

    def post(self,request,*args,**kwargs):
        chat = self.chat
        mc = cache

        chat.parse_data(request.body)

        if chat.msgtype == 'event':
            if chat.msg.event == 'subscribe':
                reply = u'欢迎关注我的公众号，本公众号可提供与机器人对话，音乐收听，收藏文章等功能。详情可输入"帮助"查询。' \
                        u'如有兴趣，可访问我的个人网站：hbnnforever.cn'
                return HttpResponse(chat.resp_text(reply))
            elif chat.msg.event == 'SCAN':
                pass
            elif chat.msg.event == 'LOCATION':
                pass
            else:
                return HttpResponse(chat.resp_text(u'其他推送消息'))
        elif chat.msgtype == 'link':
            article = WeArticle(title=chat.msg.title,
                                desc=chat.msg.desc,
                                url=chat.msg.url)
            article.save()
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



class WeArticleListView(BaseMixin,ListView):
    template_name = 'dashboard/wechat_articles.html'
    context_object_name = 'wechat_article_list'

    def get_queryset(self):
        user_id = self.request.user.id
        self.article_list =  WeArticle.objects.filter(finish=0).order_by('-create_time')
        return self.article_list

    def get_context_data(self,*args,**kwargs):
        context = super(WeArticleListView,self).get_context_data(**kwargs)
        return context



@permission_forbidden(401)
def we_article_2_blog(request,id):
    wechat_article = WeArticle.objects.get(pk=int(id))
    user = request.user
    category = Category.objects.get(pk=int(19))
    access = int(100)
    title = wechat_article.title
    alias = ''.join(['wechat',str(id),str(random.choice(xrange(100)))])
    try:
        wespider = Wechat_Spider('wechat')
        wearticle = wespider.parse(wechat_article.url)
    except Exception,e:
        return HttpResponse(u'文章爬取出现问题:'+str(e))
    try:
        article = Article(author=user,
                      title=title,
                      alias=alias,
                      content=wearticle['content'],
                      content_html=wearticle['content'],
                      category=category,
                      tags=wearticle['postuser'],
                      abstract= wearticle['abstract'],
                      access=access)
        article.ck_save()
        wechat_article.finish = 1
        wechat_article.save()
        return HttpResponseRedirect('/wechat/article/list/')
    except:
        return HttpResponse('save failure')


#!/usr/bin/env python
#encoding:utf8

import random
from BaseSdk import BaiduSDK
from datetime import date


class BaiduApi(object):

    def __init__(self):
        self.api = BaiduSDK()
        #self.url = url
        #self.content = api._get_resp(self.url)


class LifeApi(BaiduApi):
    """
    The api is used to provide some thing about life
    """
    def __init__(self):
        super(LifeApi,self).__init__()

    def get_logion(self):
        """
        :return:
        """
        keywords = ['生活','坚持','宽容','爱','信任','人生','信任','家人']
        page,rows,keyword = random.choice(range(3)),random.choice(range(10)),random.choice(keywords)
        url = 'avatardata/mingrenmingyan/lookup?dtype=JSON&keyword=%s&page=%d&rows=%d' %(keyword,page,rows)
        result = self.api.get_json_content(url)['result']
        index = random.choice(range(len(result)))
        result = result[index]
        return '--'.join([result['famous_saying'],result['famous_name']])


    def HistoryofToday(self,mon=date.today().strftime("%m"),day=date.today().strftime("%d")):

        """
        http://apistore.baidu.com/apiworks/servicedetail/1728.html
        url = ''
        :return:
        """
        if not isinstance(mon,int):
            mon = int(mon)
        if not isinstance(day,int):
            day = int(day)
        url = 'avatardata/historytoday/lookup?yue=%d&ri=%d&type=1&page=1&rows=5&dtype=JOSN&format=false' % (mon,day)
        resp = self.api.get_json_content(url)
        someday = u'%s月%s日' % (mon,day)
        try:
            result = resp['result']
            history = []
            number = 1
            for item in result:
                history.append([str(number)+'.'+item['year']+u'年'+someday,item['title']])
                number += 1
            for item in history:
                item = ' '.join(item)
            return ' '.join(history)
        except:
            return []

    def FamousWord(self):
        """
        url = 'http://apis.baidu.com/txapi/dictum/dictum'
        :return:
        curl  --get --include  'http://apis.baidu.com/txapi/dictum/dictum'  -H 'apikey:您自己的apikey'
        JSON返回示例 :
        {
            "code": 200,  //返回码
            "msg": "success",  //返回状态
            "newslist": [
                {
                    "id": "19139",  //ID
                    "content": "人生一世不就是为了化短暂的事物为永久的吗？要做到这一步，就须懂得如何珍视这短暂和永久。",
                    "mrname": "歌德"  //来源
                }
            ]
        }
        推荐服务
        """
        url = 'txapi/dictum/dictum'
        try:
            resp = self.api.get_json_content(url)
            return resp["newslist"]['content']
        except:
            return None







class ToolApi(BaiduApi):
    """
    The api is used to provide some thing about life
    """
    def __init__(self):
        super(ToolApi,self).__init__()

    def currency_convert(self):
        """
        fromCurrency
        string	是	urlParam
        待转化的币种；具体取值可以通过“支持的币种查询”这个API获取
        展开
        CNY
        toCurrency
        string	是	urlParam
        转化后的币种；具体取值可以通过“支持的币种查询”这个API获取
        展开
        USD
        amount
        string	否	urlParam
        转化金额
        2
        url = 'http://apis.baidu.com/apistore/currencyservice/currency?fromCurrency=CNY&toCurrency=USD&amount=2'
        JSON返回示例 :
        {
           errNum: 0,
           errMsg: "成功",
           retData: {
             date: "2015-08-12",  //日期
             time: "07:10:46",    //时间
             fromCurrency: "CNY", //待转化币种的简称，这里为人民币
             amount: 2,    //转化的金额
             toCurrency: "USD",  //转化后的币种的简称，这里为美元
             currency: 0.1628,   //当前汇率
             convertedamount: 0.3256  //转化后的金额
          }
        }
        :return:
        """

    def get_ip_info(self,ip):
        """
        ​http://apis.baidu.com/apistore/iplookupservice/iplookup
        JSON返回示例 :
        {
            "errNum": 0,
            "errMsg": "success",
            "retData": {
                "ip": "117.89.35.58", //IP地址
                "country": "中国", //国家
                "province": "江苏", //省份 国外的默认值为none
                "city": "南京", //城市  国外的默认值为none
                "district": "鼓楼",// 地区 国外的默认值为none
                "carrier": "中国电信" //运营商  特殊IP显示为未知
            }
        }
        :param ip:the ip that need lookup
        :return:
        """
        url = 'apistore/iplookupservice/iplookup/?ip=%s' % ip
        resp = self.api.get_json_content(url)
        try:
            resp = resp['retData']
            result = ' '.join([resp['country'],resp['province'],resp['city'],resp['district'],resp['carrier']])
        except:
            result = u'对不起，该IP查询不到。'
        return result

    def get_personid(self,personid):
        """
        url = 'http://apis.baidu.com/apistore/idservice/id?id=420984198704207896'
                JSON返回示例 :
        {
            "errNum": 0,
            "retMsg": "success",
            "retData": {
                "sex": "M", //M-男，F-女，N-未知
                "birthday": "1987-04-20", //出生日期
                "address": "湖北省孝感市汉川市" //身份证归属地 市/县
            }
        }
        """
        url = 'apistore/idservice/id?id=%s' % personid
        resp = self.api.get_json_content(url)
        try:
            resp = resp['retData']
            result = ' '.join([resp['sex'],resp['birthday'],resp['address']])
        except:
            result = u'对不起，该身份证查询不到。'
        return result

    def xinzuo_lucky(self):
        """
        请求参数(urlParam) :
        参数名	类型	必填	参数位置	描述	默认值
        consName
        string	是	urlParam
        星座名称,必须为十二星座名称
        双子座
        type
        string	是	urlParam
        运势类型:today,tomorrow,week,nextweek,month,year
        收起
        today
        请求示例 :
        curl示例php示例python示例java示例C#示例ObjectC示例Swift示例

        url = 'http://apis.baidu.com/bbtapi/constellation/constellation_query?consName=%E5%8F%8C%E5%AD%90%E5%BA%A7&type=today'

        1
        # -*- coding: utf-8 -*-
        2
        import sys, urllib, urllib2, json
        3
        ​
        4
        url = 'http://apis.baidu.com/bbtapi/constellation/constellation_query?consName=%E5%8F%8C%E5%AD%90%E5%BA%A7&type=today'
        5
        JSON返回示例 :
        /*今日或明日运势格式*/
        {
            "date":20151214, /*日期数值*/
            "name":"双子座", /*星座名称*/
            "QFriend":"摩羯座", /*速配星座*/
            "all":"40%", /*综合指数*/
            "color":"黄色", /*幸运色*/
            "datetime":"2015年12月14日", /*日期*/
            "health":"55%", /*健康指数*/
            "love":"40%", /*爱情指数*/
            "money":"40%", /*财运指数*/
            "number":4, /*幸运数字*/
            "summary":"依旧是家庭和工作蜡烛二头烧的你，体力真的不堪负荷，超级无敌爆累，已经濒临零界点，一触即发，要好好耐住性子沟通，变得好困难，最后还是吵架了，但也许吵架了吵出彼此的苦，才会换来体谅吧，最终还是家人啊！", /*总结*/
            "work":"40%", /*工作指数*/
            "resultcode":"200", /*返回状态码 200为成功*/
            "error_code":0 /*返回错误码 0为没有错误*/
        }

        /*本周或下周运势格式*/
        {
            "date":"2015年12月13日-2015年12月19日", /*日期*/
            "health":"健康：触发的疾病多和以往享受过度有关。伴侣健康需关注。",
            "job":"求职：运气不错，有望争取到喜欢的职位。 ",
            "love":"恋情：情感中会主动付出，但也在意对方的回应，挑剔、计较多，引发对方反弹。单身的，偏自恋。 ",
            "money":"财运：有合作生财机会，但存在较多变数。正财运旺，多劳多得法则灵验。 ",
            "name":"双子座",
            "weekth":51, /*一年中的第几周*/
            "work":"工作：猜忌、不信任的心态下，展开合作。所幸，当下的工作内容是你喜欢的。 ",
            "resultcode":"200",
            "error_code":0
        }

        /*月份运势格式*/
        {
            "all":"上旬和中旬，合作机会多，或合作关系需要花费较多心力去维护；水星中旬入资源宫后，明显你在合作关系中感受到不愉快，猜测、不信任感增多，但现实中仍需和他人配合才可以应付下去。下旬，太阳入资源宫，合作减少，独立、私下运作的内容增多，善察言观色发现漏洞，并积极利用；天王星逆行结束，人脉圈有变动，可能脱离某个团体或进入一个新团体。\r\n", /*总体介绍*/
            "date":"2015年12月",
            "happyMagic":"",
            "health":"金星转宫，触发的疾病多和以往享受过度有关。上旬和中旬，伴侣健康需关注。下旬，性能量提升，情绪易走极端。\r\n",
            "love":"上旬和中旬，伴侣间有问题必须解决，或伴侣很需要你，但金星月初转宫后，挑剔和计较增多，会主动付出，但也在意对方是否给予自己想要的回应，伴侣间更深刻体会到陪伴和牵制同在，单身的自恋倾向加重。下旬，性能量提升，刺激偏好增强，易被隐秘情缘吸引。火星整月贯穿在恋爱宫，受其能量影响，太过在意对方，无法得到预期回应时，容易触发怒气，引致情感灾难事件。\r\n",
            "money":"上旬和中旬，有合作生财机会，但存在较多变数。下旬，暗财机会多，易涉内幕交易，受冥王能量影响，容易引致钱财的大起大落，需小心谨慎。金星月初转宫后，投机性下降，正财运升，建议争取加薪。\r\n",
            "month":12,
            "name":"双子座",
            "work":"金星月初入工作宫，工作的快乐感增多，接到自己感兴趣的任务。人际充满了妥协和利用。\r\n",
            "resultcode":"200",
            "error_code":0
        }

        /*年份运势格式*/
        {
            "name":"双子座",
            "date":"2015年",
            "year":2015,
            "resultcode":"200",
            "error_code":0,
            "mima":{
                "info":"修剪羽翼的蓄力之年",
                "text":[
                    "过去一年，很多双子座都经历了一段快速提升自我的扩张时期，不论是个人身价还是社会地位都有明显提升，进入了一个不同以往的高位层次。而在2015年，这种扩张速度会开始减慢，反而要静下心来对狼吞虎咽中夺下的“份额”精挑细选，剔除不合适自己的内容，而将有长远发展预期的部分精雕细琢。土星进入合作伴侣宫位将尤其考验现有的合作关系和伴侣关系。工作中的某些合作关系可能遭遇考验，过去独霸一方的个人也有可能突然遭遇强劲对手，必须慎重对待。如果你们在上半年对任何涉及到合作、竞争和伴侣关系的问题过于随意，则在下半年后可能遭遇条款无法兑现状况，或是因对方资金不到位而不得不去填坑，以及被合作方拖下水损害自身声誉等等。婚姻关系也是本年度的关注重点，不论是家庭事务还是外界桃花都可能对现有关系带来影响，必须谨慎处理。"
                ]
            }, /*贴士*/
            "career":[
                "今年对双子座而言会是相对求稳的一年。很多双子座在过去一年已经完成了事业上的提升，自主创业者可能已将公司扩大经营，并购进展顺利，打工者也因为工作出色而获得个人职业级别的提升和认可。而在今年，一切都会慢下脚步，反而应该回顾过去几年所做的工作，将一些对自身已经无益的部分逐渐删减，而那些因为扩张太快而未收拾好的残局也要加以辨别好坏再决定其去留。对公司管理者而言，你要关注手中已有的合同，以及公司内部的管理是否存在监守自盗或是不利公司的行为，及时终止未能履行的合约。对于合作伙伴也需要仔细甄别，留下真正有实力的，剔去那些仅有表面文章的。竞争对手的崛起也会带来职业危机感，让你必须更为勤力。自由职业者要改变过去只要有单就做的辛劳状态，开始选择那些最有利于个人职业发展的工作，减少工作量，重点服务有前景的大客户。打工者则应该将自身稳定下来，而非盲目跳槽，选择合适自身发展的岗位继续深挖。"
            ], /*事业*/
            "love":[
                "过去一年中，很多双子座的感情运波浪起伏，一直游走于风口浪尖之上，也很容易成为众人热议的焦点。而来到2015年，这一趋势还将继续下去。对未婚人士而言，尤其在上半年2月下旬至3月下旬的两次双鱼座满月之间，你们的恋情会经历颇多波折，甚至与个人的名誉事业搅在一起，不受自己控制。感情不算稳定的双子座，在太多外界因素参与之下，尤其容易产生分手的想法，或是干脆淡出不再联系。已婚人士则要小心土星带来的考验，对夫妻共同财务问题谨慎处理，以免最后闹到大家不开心，或是砸钱给对方擦屁股。对另一半的想法和意愿也应更加尊重，而非强制要求两人步调一致。进入下半年，金星逆行会给感情带来考验，尤其容易与旧情人产生交集而对现有感情产生怀疑。整个秋天追求者都是层出不穷，但多数心思不纯，是否值得投入还需考虑。立冬之后，会有赏心悦目的桃花出现，单身者可以享受其中，已婚者内心挣扎面临考验。"
            ], /*感情*/
            "health":[
                "双子座在占星学上掌管着人体的手和肺部，在日常生活当中一定要注意养成良好的卫生习惯，并且在季节变换的时期，主要防护。大部分双子座都能够对卫生和保健方面有个正确的认识。"
            ], /*健康*/
            "finance":[
                "相比往年，今年财运只能算是一般。依然还是有不少小钱入账，但如只是图个小日子滋润也必能如愿。上半年来看，年后的两次双鱼座新月都会给你们带来不少事业机会以及因此获得的经济收益，打工者有望拿到令人满意的红包奖励，而自创业者也会继续得到来源于前一年事业蓬勃发展而交割的现金收益。但在此后，财运开始趋缓，尤其4月间要小心意外破财。立夏之后财运有所好转，也会有机会因为投资而小捞一笔，但想用杠杆做大也并不容易。下半年开始则应收敛心思，老老实实靠勤力赚钱，若想通过投资快速赚钱则反而可能遭遇意外损失，折损本金。立冬之后还有一波财运，但若不能谨慎小心则同样可能偷鸡不成蚀把米。"
            ], /*财务*/
            "luckyStone":"天河石", /*幸运石*/
            "future":[
                ""
            ] /*未来*/
        }
        备注 :
        /** 错误的星座名称 **/
        {
             "error_code" : 205802 ,
             "reason" : "Does not exist in the consName!" ,
             "result" : [

            ] ,
             "resultcode" : "202"
        }

        /** 错误的类型 **/
        {
             "error_code" : 205801 ,
             "reason" : "TYPE ERROR!" ,
             "result" : [

            ] ,
             "resultcode" : "201"
        }
        ​"""
        pass

    def test_xinzuo_match(self):
        """
        url = 'http://apis.baidu.com/txapi/xingzuo/xingzuo?me=%E9%87%91%E7%89%9B&he=%E5%B7%A8%E8%9F%B9&all=1'
        :param:me自己星座，默认去掉“座“下同,he,
        """
        pass

    def WechatHotArticle(self):
        """
        http://apistore.baidu.com/apiworks/servicedetail/632.html
        :return:
        """
        pass


if __name__ =="__main__":
    api = LifeApi()
    print api.FamousWord()
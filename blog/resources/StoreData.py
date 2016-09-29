# !/usr/bin/env python
# encoding:utf-8


import os

import requests
import json
import time
import re
#from fm import standardVerify


def email_to_qq(email):  # 从QQ邮箱中提取QQ号
    qq_epr = ur"^[1-9]\d{4,9}$"
    if email:
        email_parts = email.lower().split("@")
        email_left = email_parts[0]
        email_right = email_parts[1]
        if email_right == "qq.com":
            qq = re.findall(qq_epr, email_left)
            if qq:
                return qq[0]
        else:
            return ""
    else:
        return ""



class EvidencePost(object):

    def __init__(self,filepath):
        self.file_path = filepath
        self.head = []

    def get_head_info(self):
        """
        Get the information of data head,that is ,the first line,
        :return: col_info ,it is used in template
        """
        with  open(self.file_path, 'r') as fr1:
            result1 = fr1.readlines()
            self.data_len = len(result1)  # 获取文件行数
            col_mark = 0
            d = result1[0].strip('\n').split('\t')
            col_info = []
            for each in d:
                #print each + ': ' + str(col_mark)
                col_info.append({'col_name':each,'col_num':col_mark})
                col_mark += 1
                self.head.append(each)
            return col_info

    def parse_and_store(self,data_origin,term_type,col_num1,fraud_type='missContact',environment='test'):
        """
        the method starts from the 2nd line,
        :param data_origin:
        :param term_type:
        :param col_num1:
        :param fraud_type:
        :param environment:
        :return:
        """
        with open(self.file_path, 'r') as fr2:
            result2 = fr2.readlines()
            spl_post = range(10, self.data_len, 10)  # 每50条记录提交一次入库请求
            last_data = self.data_len - 1
            if last_data not in spl_post:
                spl_post.append(self.data_len-1)
            print spl_post
            count = 0
            count_success = 0  # 统计校验通过数据
            count_exist = 0  # 统计数据库中已经存在数据
            count_error = 0  # 统计格式有问题数据
            error_data = []  # 存放格式有问题数据
            black_list = list()
            black_dict = dict()
            fraud_details = []  # 存放数据详情

            print ' Start inserting data into black_list!'

            #term_fm = standardVerify(mode=term_type, logout=True)
            #fm_filter = list()  # 存放被fm包过滤掉的数据
            for line in result2[1::]:
                post_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  # 获取当前系统时间
                count += 1
                d = line.strip('\n').split(' ')  # 默认以TAB分隔
                if len(d) == 1:
                    d = line.strip('\n').split('\t')
                d = [x for x in d if x]
                col_all = len(self.head)  # 获取列数
                if count % 100 == 0:
                    print str(count) + '/' + str(self.data_len)
                if term_type == 'accountEmail':
                    d[col_num1] = d[col_num1].lower()
                if term_type == 'idNumber':
                    d[col_num1] = d[col_num1].upper()
                if term_type == 'accountPhone':
                    d[col_num1] = d[col_num1].replace('-', '')
                d[col_num1] = d[col_num1].strip(' ')
                print d[col_num1]
                res = 1
                #res = term_fm.check(input=d[col_num1], abn_check=True)  # 对字段进行校验
                if not res:
                    fm_filter.append(d[col_num1])
                    print d[col_num1]
                else:
                    count_success += 1
                    black_dict[term_type] = d[col_num1]
                    black_dict['fraudType'] = fraud_type
                    black_dict['evidenceTime'] = post_time
                    for i in range(col_all):
                        fraud_details.append(self.head[i] + ': ' + d[i])
                    # 拼接证据详情信息
                    #black_dict['fraudDetails'] = u'来源: ' + data_origin + '\n' + '\n'.join(fraud_details).strip('\n')
                    black_list.append(black_dict)
                    qq_label = ""
                    if term_type == 'accountEmail':
                        qq_label = email_to_qq(d[col_num1])
                    # 添加QQ邮箱提取出的QQ号
                    if qq_label:
                        black_dict1 = dict()
                        black_dict1['qqNumber'] = qq_label
                        black_dict1['fraudType'] = black_dict['fraudType']
                        black_dict1['evidenceTime'] = black_dict['evidenceTime']
                        black_dict1['fraudDetails'] = black_dict['fraudDetails']
                        black_list.append(black_dict1)
                    fraud_details = []  # 重置列表
                    black_dict = {}
                    if count in spl_post :
                        print count
                        black_list_json = json.dumps(black_list)  # 对数据进行JSON格式化编码
                        if environment == 'online':
                            url = 'https://data-import.tongdun.cn/evidenceService'      # 线上生产环境
                            dump_data = {'secret_key': 'a', 'partner_code': 'tongdun', 'evidence_detail': black_list_json}     # 线上生产环境
                        else:
                            url = 'https://apitest.fraudmetrix.cn/evidenceService'  # 测试环境
                            dump_data = {'secret_key': 'ff3b2994debf40d9ac1d1876f3e7e751', 'partner_code': 'tongdun', 'evidence_detail': black_list_json}  # 测试环境
                        req = requests.post(url, dump_data)  # 生成页面请求的完整数据，每次最多50条记录
                        result = json.loads(req.text)
                        if result["success"]:
                            print ' 成功导入', count_success - count_exist - count_error, '剩余', self.data_len - count, '条待导入  '
                        else:
                            if "exist_datas" in result:
                                count_exist += len(result["exist_datas"])
                            if "error_datas" in result:
                                count_error += len(result["error_datas"])
                                error_data.append(result["error_datas"])
                            #print req.text
                        black_list = []  # 重置列表
            result = {u'导入': count_success - count_exist - count_error}
            result[u'重复数据'] =  count_exist
            result[u'错误数据'] =  count_error
            #result[u"fm包过滤掉的数据"] = list(set(fm_filter))
            fr2.close()
            return result





if __name__ == '__main__':
    file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),'test.txt')
    data_origin = 'a1a测试反馈失联数据'  # 数据来源
    if 'aa' in data_origin:
        # 防止忘了更新data_origin字段
        exit(1)
    term_type1 = 'accountMobile'  # 录入字段
    col_num1 = 2  # 录入字段所在列数，从0开始计数
    # 字段入库
    evip = EvidencePost(file_path)
    head_info = evip.get_head_info()
    result =  evip.parse_and_store(data_origin, term_type1, col_num1)
    for key in result:
        print key,result[key]



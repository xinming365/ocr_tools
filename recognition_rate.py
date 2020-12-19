import os
import json
import re
import numpy as np
import base64

"""
wrr: word recognition rate
srr: sentence recognition rate 
"""


class RecognitionRate:
    def __init__(self, path_label, path_prediction):
        self.path_label = path_label
        self.path_prediction = path_prediction
        self.label = read_file(self.path_label)
        self.prediction = read_file(self.path_prediction)
        self.key_list = global_key_list
        # self.key_list = ['invoice_type', '发票代码', '发票号码', '开票日期', '金额（不含税）', '税额', '金额（含税）', '校验码（后6位）']

    def get_invoice_type_rr(self):
        wrr, match_count, counter = self.ocr_rate(0)
        print('发票类型识别正确率：{:.2%}  ({}/{})'.format(wrr, match_count, counter))
        f.write('发票类型识别正确率：{:.2%}  ({}/{})\n'.format(wrr, match_count, counter))
        return wrr

    def get_invoice_daima_rr(self):
        wrr, match_count, counter = self.ocr_rate(self.key_list.index('发票代码'))
        print('发票代码识别正确率：{:.2%}  ({}/{})'.format(wrr, match_count, counter))
        f.write('发票代码识别正确率：{:.2%}  ({}/{})\n'.format(wrr, match_count, counter))
        return wrr

    def get_huochepiao_date_rr(self):
        wrr, match_count, counter = self.ocr_rate(self.key_list.index('日期'))
        print('日期识别正确率：{:.2%}  ({}/{})'.format(wrr, match_count, counter))
        f.write('日期识别正确率：{:.2%}  ({}/{})\n'.format(wrr, match_count, counter))
        return wrr

    def get_huochepiao_level_rr(self):
        wrr, match_count, counter = self.ocr_rate(self.key_list.index('等级'))
        print('等级识别正确率：{:.2%}  ({}/{})'.format(wrr, match_count, counter))
        f.write('等级识别正确率：{:.2%}  ({}/{})\n'.format(wrr, match_count, counter))
        return wrr

    def get_huochepiao_intital_station_rr(self):
        wrr, match_count, counter = self.ocr_rate(self.key_list.index('出发'))
        print('出发站识别正确率：{:.2%}  ({}/{})'.format(wrr, match_count, counter))
        f.write('出发站识别正确率：{:.2%}  ({}/{})\n'.format(wrr, match_count, counter))
        return wrr

    def get_huochepiao_final_station_rr(self):
        wrr, match_count, counter = self.ocr_rate(self.key_list.index('到达'))
        print('到达站识别正确率：{:.2%}  ({}/{})'.format(wrr, match_count, counter))
        f.write('到达站识别正确率：{:.2%}  ({}/{})\n'.format(wrr, match_count, counter))
        return wrr

    def get_huochepiao_cost_rr(self):
        wrr, match_count, counter = self.ocr_rate(self.key_list.index('价格'))
        print('金额识别正确率：{:.2%}  ({}/{})'.format(wrr, match_count, counter))
        f.write('金额识别正确率：{:.2%}  ({}/{})\n'.format(wrr, match_count, counter))
        return wrr


    def get_invoice_haoma_rr(self):
        wrr, match_count, counter = self.ocr_rate(self.key_list.index('发票号码'))
        print('发票号码识别正确率：{:.2%}  ({}/{})'.format(wrr, match_count, counter))
        f.write('发票号码识别正确率：{:.2%}  ({}/{})\n'.format(wrr, match_count, counter))
        return wrr

    def get_invoice_date_rr(self):
        wrr, match_count, counter = self.ocr_rate(self.key_list.index('开票日期'))
        print('开票日期识别正确率：{:.2%}  ({}/{})'.format(wrr, match_count, counter))
        f.write('开票日期识别正确率：{:.2%}  ({}/{})\n'.format(wrr, match_count, counter))
        return wrr

    def get_money_exclude_tax_rr(self):
        wrr, match_count, counter = self.ocr_rate(4)
        print('金额（不含税）识别正确率：{:.2%}  ({}/{})'.format(wrr, match_count, counter))
        f.write('金额（不含税）识别正确率：{:.2%}  ({}/{})\n'.format(wrr, match_count, counter))
        return wrr

    def get_tax_count_rr(self):
        wrr, match_count, counter = self.ocr_rate(5)
        print('税额识别正确率：{:.2%}  ({}/{})'.format(wrr, match_count, counter))
        f.write('税额识别正确率：{:.2%}  ({}/{})\n'.format(wrr, match_count, counter))
        return wrr

    def get_money_include_tax_rr(self):
        wrr, match_count, counter = self.ocr_rate(self.key_list.index('金额（含税）'))
        print('金额（含税）识别正确率：{:.2%}  ({}/{})'.format(wrr, match_count, counter))
        f.write('金额（含税）识别正确率：{:.2%}  ({}/{})\n'.format(wrr, match_count, counter))
        return wrr

    def get_jiaoyanma_rr(self):
        wrr, match_count, counter = self.ocr_rate(self.key_list.index('校验码（后6位）'))
        print('校验码（后6位）识别正确率：{:.2%}  ({}/{})'.format(wrr, match_count, counter))
        f.write('校验码（后6位）识别正确率：{:.2%}  ({}/{})\n'.format(wrr, match_count, counter))
        return wrr

    def match_count(self, str1, str2):
        """
        预测的字符串与label的字符串不想等时，用*填充
        """
        count = 0
        if not len(str1)==len(str2):
            # print('两个字符串长度不相等, 分别是{}(长度{})和{}(长度{})'.format(str1,len(str1),str2,len(str2)))
            width = max(len(str2), len(str1))
            if len(str1)< len(str2):
                str1 = str1.ljust(width, '*')
            else:
                str2 = str2.ljust(width, '*')
        for index, ch in enumerate(str1):
            if ch == str2[index]:
                count += 1
        return count, count / len(str1)

    def ocr_rate(self, key_number):
        counter = 0
        match_count = 0
        for k, v_prediction in self.prediction.items():
            key_type = self.key_list[key_number]
            v_label = self.label[k]
            if key_type not in v_prediction.keys():
                accuracy = 0
                print(key_type)
                v_prediction.update({key_type: {}})
                if key_type not in v_label.keys():
                    v_label.update({key_type: {}})
            else:
                # mc: 字段数目。accuracy:完全一样为1.
                mc, accuracy = self.match_count(v_prediction[key_type], v_label[key_type])
            # mc, accuracy = self.match_count(v_prediction[key_type], v_label[key_type])
                if accuracy==1:
                    match_count = match_count + 1
            counter = counter+1
            # counter = counter + len(v_prediction[key_type])
        # wrr = match_count / counter
        wrr = match_count/counter
        return wrr, match_count, counter

    def get_total_rr(self):
        count_total_pic = 0
        rr = []
        for k, v_prediction in self.prediction.items():
            print('processing picture name: {}'.format(k))
            total_count = 0
            # print(v_prediction)
            wrong_seg=[]
            for key_number, kye in enumerate(self.key_list):
                wrong_dict={}
                key_type = self.key_list[key_number]
                v_label = self.label[k]
                if key_type not in v_prediction.keys():
                    accuracy=0
                    print(key_type)
                    v_prediction.update({key_type:{}})
                    if key_type not in v_label.keys():
                        v_label.update({key_type:{}})
                else:
                    mc, accuracy = self.match_count(v_prediction[key_type], v_label[key_type])
                if accuracy==1:
                    total_count +=1
                else:
                    wrong_dict[key_type]={'预测结果':v_prediction[key_type],'正确结果':v_label[key_type]}
                if wrong_dict:
                    wrong_seg.append(wrong_dict)
            rr_one_pic = total_count/len(self.key_list)
            rr.append(rr_one_pic)
            if rr_one_pic==1:
                count_total_pic +=1
            else:
                info='{}  图片的识别率是{:.2%};  识别错误字段为:{} \n'.format(k , rr_one_pic, wrong_seg)
                f.write(info)
                print(info)

        rr_total_pic=count_total_pic/len(self.prediction)
        print('识别正确率：{:.2%}'.format(np.mean(rr)))
        f.write('识别正确率：{:.2%}'.format(np.mean(rr)))
        print('整票正确率：{:.2%}  ({}/{})'.format(rr_total_pic, count_total_pic, len(self.prediction)))
        f.write('整票正确率：{:.2%}  ({}/{})'.format(rr_total_pic, count_total_pic, len(self.prediction)))
        return np.mean(rr), rr_total_pic

    def get_seg_rr_invoice(self):
        self.get_invoice_type_rr()
        self.get_invoice_daima_rr()
        self.get_invoice_haoma_rr()
        self.get_invoice_date_rr()
        self.get_jiaoyanma_rr()
        self.get_money_include_tax_rr()

#['invoice_type', '发票代码', '发票号码', '开票日期', '金额（不含税）', '税额','金额（含税）']
    def get_seg_rr_zhuanpiao(self):
        self.get_invoice_type_rr()
        self.get_invoice_daima_rr()
        self.get_invoice_haoma_rr()
        self.get_invoice_date_rr()
        self.get_money_exclude_tax_rr()
        self.get_tax_count_rr()
        self.get_money_include_tax_rr()

    def get_seg_rr_huochepiao(self):
        self.get_invoice_type_rr()
        self.get_huochepiao_date_rr()
        self.get_huochepiao_level_rr()
        self.get_huochepiao_intital_station_rr()
        self.get_huochepiao_final_station_rr()
        self.get_huochepiao_cost_rr()

def read_file(path):
    """
    根据jpg关键字判断该文件的文件名！注意如果是其他格式的文件，需要添加判断条件！
    """
    key_list = []
    val_list = []
    count=0
    with open(path, mode='r', encoding='UTF-8') as f:
        for line in f.readlines():
            # print(line)
            value_dict = {}
            pic_name = ''
            line = line.strip()
            if 'jpg' in line:
                dir, pic_name = os.path.split(line)
                key_list.append(pic_name)
                # count = count+1
                # print('{}'.format(count))
            elif '[' in line:
                name = ''
                value = ''
                structured_dict = {}
                # 注意正则表达式的冒号！！！！
                structure_pattern1 = r'"structured_data"：\[.*?],'
                structure_pattern2 = r'"structured_data": \[.*?],'
                tmp = re.sub(r'"structured_data"：\[.*?],', '', line)
                # print(tmp)
                structured_data = re.compile(structure_pattern1).findall(line)
                if structured_data == []:
                    tmp = re.sub(r'"structured_data": \[.*?],', '', line)
                    structured_data = re.compile(structure_pattern2).findall(line)
                # print(tmp)
                value_dict = json.loads(tmp)[0]
                list_data = structured_data[0].split(',')

                for i in list_data:
                    pair = re.findall(r'".*?"', i)
                    # print(pair)
                    pair = [json.loads(_) for _ in pair]
                    if 'name' in pair:
                        name = pair[-1]
                    elif 'value' in pair:
                        value = pair[-1]
                    structured_dict[name] = value
                value_dict.update(structured_dict)
                val_list.append(value_dict)
    format_list = list(set(key_list))
    format_list.sort(key=key_list.index)
    return dict(zip(format_list, val_list))

# ###---------------------------  普票   ---------------------------------------
# global_key_list = ['invoice_type', '发票代码', '发票号码', '开票日期', '金额（含税）', '校验码（后6位）']
# filename = './information_wrong/D_OCR自测_普票50张_information.txt'
# label_path = 'F:\WORK\实习\E_OCR_自测_results_check\D_OCR自测_普票50张_check.txt'
# prediction_path = 'F:\WORK\实习\E_OCR_自测_results\E_OCR自测_普票50张.txt'

####---------------------------  火车票   ---------------------------------------
global_key_list = ['invoice_type', '日期', '等级', '出发', '到达', '价格']
filename = './information_wrong/D_OCR自测_火车50张_information.txt'
label_path = 'F:\WORK\实习\E_OCR_自测_results_check\D_OCR自测_火车50张_check.txt'
prediction_path = 'F:\WORK\实习\E_OCR_自测_results\E_OCR自测_火车50张.txt'

# ###--------------------------- 电子普票  ---------------------------------------
# global_key_list = ['invoice_type', '发票代码', '发票号码', '开票日期', '金额（含税）', '校验码（后6位）']
# filename = './information_wrong/D_OCR自测_电子普票50张_information.txt'
# label_path = 'F:\WORK\实习\E_OCR_自测_results_check\D_OCR自测_电子普票50张_check.txt'
# prediction_path = 'F:\WORK\实习\E_OCR_自测_results\E_OCR自测_电子普票50张.txt'

###---------------------------  专票   ---------------------------------------
# global_key_list = ['invoice_type', '发票代码', '发票号码', '开票日期', '金额（不含税）', '税额','金额（含税）']
# filename = './information_wrong/D_OCR自测_专票50张_information.txt'
# label_path = 'F:\WORK\实习\E_OCR_自测_results_check\D_OCR自测_专票50张_check.txt'
# prediction_path = 'F:\WORK\实习\E_OCR_自测_results\E_OCR自测_专票50张.txt'





f=open(filename, 'w')

prediction_result = read_file(prediction_path)
label_result = read_file(label_path)

print(len(prediction_result))
print(prediction_result['invoice_direction_2741_0.jpg'])
print(label_result['invoice_direction_2741_0.jpg'])
# print(dd['普3.jpg'])

RecognitionRate(label_path, prediction_path).get_total_rr()
# RecognitionRate(label_path, prediction_path).get_seg_rr_invoice()
# RecognitionRate(label_path, prediction_path).get_seg_rr_zhuanpiao()
RecognitionRate(label_path, prediction_path).get_seg_rr_huochepiao()
# line ='[{"invoice_type": "出租车发票", "id": 0, "bbox": [0, 537, 4032, 2243], "invoice_base64": [], "structured_data": [{"name": "发票代码", "value": "112001960321"},{"name": "发票号码", "value": "21434249"}, {"name": "车费", "value": "18.00"}, {"name": "日期", "value": "2020-08-13"},{"name": "上车时间", "value": "08:07"}, {"name": "下车时间", "value": "08:23"},{"name": "车号", "value": "E-05748"},{"name": "里程", "value": "3.8"}], "error_code": 0, "timeTake": []}]'
# c=re.compile(r'"structured_data": [.*?]').findall(line)
# c=re.compile(r'"structured_data": \[.*?]').findall(line)
# print(c)
# cc =re.compile(r'\[.*?]').findall(c[0])
#
# bb=re.sub(r'"structured_data": \[.*?],', '', line)
#
# bb=json.loads(bb)
# print(bb[0])
# print(cc)
#
# # dd=re.compile(r'\{.*?}').findall(cc[0])
# dd=cc[0].split(',')
# print(dd)
f.close()
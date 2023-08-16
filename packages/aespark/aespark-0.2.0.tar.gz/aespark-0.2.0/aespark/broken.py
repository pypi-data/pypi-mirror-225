import re
import datetime
import pandas as pd
import jionlp
import pkg_resources

dist = pkg_resources.get_distribution("aespark")

class Broken():

    def __init__(self) -> None:
        '''银行卡解析相关文件'''
        self.__df = pd.read_table(f'{dist.location}/aespark/static/bankBIN.txt', keep_default_na='', dtype='str')
        name = pd.read_table(f'{dist.location}/aespark/static/bankSimple.txt', keep_default_na='', dtype='str')
        self.__namedic = dict(zip(name['银行简称'].to_list(), name['银行名称'].to_list()))
        '''IP解析相关文件'''
        self.__ip_info = pd.read_table(f'{dist.location}/aespark/static/ip_info.txt', sep=',', keep_default_na='', dtype='str')
        self.__ip_v4 = self.__ip_info[self.__ip_info['lex'] == 'ipv4']
        self.__ip_v4['ip_start'] = self.__ip_v4['ip_start'].astype(float)
        self.__ip_v6 = self.__ip_info[self.__ip_info['lex'] == 'ipv6']
        '''身份证解析相关文件'''
        self.__idcard_info = pd.read_table(f'{dist.location}/aespark/static/id_card_info.txt', sep=',', keep_default_na='', dtype='str')
        # '''手机号解析相关文件'''
        # self.__phone_info = pd.read_table(f'{dist.location}/aespark/static/phone_number_info.txt', sep=',', keep_default_na='', dtype='str')

    def bank_belong(self, card: str):
        '''
        功能简介：
            银行卡归属行查询；
        return：
            返回一个字典，查询状态statu、卡类型lex、归属行bank；
        '''
        card = re.sub('[^0-9]','',card)
        lins = self.__df[self.__df['长度'].astype(int)==len(card)]
        for i in lins.index:
            if card[:int(lins['BIN长度'][i])] == lins['卡头'][i]:
                return {'lex':lins['卡类型'][i],'bank':lins['银行'][i]}
        return {'lex':'','bank':''}
    
    def bank_simple(self, bank:str):
        '''
        功能简介：
            银行简称转换；
        return：
            返回银行名称；
        '''
        bank1 = re.sub('[^A-Z]', '', bank.upper())
        try:
            return self.__namedic[bank1]
        except:
            return bank
        
    def ip_where(self, ipstr: str):
        '''
        功能简介：
            ip地址解析；
        return：
            一个字典，包含国家country、省province、市city、区area、完整地址address、运营商或网路信息location；
        '''

        def get_information(ind):
            if ind == -1:
                dic = {
                    'country': '',
                    'province': '',
                    'city': '',
                    'area': '',
                    'address': '',
                    'location': '',
                }
            else:
                dic = {
                    'country': self.__ip_info['country'][ind],
                    'province': self.__ip_info['province'][ind],
                    'city': self.__ip_info['city'][ind],
                    'area': self.__ip_info['area'][ind],
                    'address': self.__ip_info['address'][ind],
                    'location': self.__ip_info['location'][ind],
                }
            return dic

        ipstr = re.sub('[^0-9a-f:.]', '', ipstr)
        IIP = lambda x:sum([256 ** i * int(j)for i, j in enumerate(x.split('.')[::-1])])

        if ':' in ipstr:
            try:
                ind = list(self.__ip_v6[self.__ip_v6['ip_start'] <= ipstr].index)[-1]
                result = get_information(ind)
            except:
                result = get_information(-1)
        elif '.' in ipstr:
            try:
                ind = list(self.__ip_v4[self.__ip_v4['ip_start'] <= IIP(ipstr)].index)[-1]
                result = get_information(ind)
            except:
                result = get_information(-1)
        else:
            result = get_information(-1)
        
        return result
    
    def idcard_info(self, idcard:str|int|float):
        '''
        功能简介：
            身份证号码解析；
        所需参数：
            idCard 身份证号码；
        输出信息：
            list. 0.性别、1.年龄、2.省、3.市、4.区；
        调用示例：
            dataframe[['性别', '年龄', '归属省', '归属市', '归属区']] = dataframe['身份证号'].apply(pd.Series(parse_idber))；
        '''
        try:
            idcard = str(idcard).upper()
            idcard = re.sub('[^0-9X]', '', idcard)
            if len(idcard) != 18:
                raise Exception('Error: The id card is wrong.')
            weight = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
            validate = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']
            sum = 0
            for i in range(len(weight)):
                sum += weight[i] * int(idcard[i])
            m = sum % 11
            if validate[m] == idcard[17]:
                if len(self.__idcard_info[self.__idcard_info['code']==idcard[:6]])==0:
                    return ['', '', '', '', '']
                else:
                    ind = self.__idcard_info[self.__idcard_info['code']==idcard[:6]].index[0]
                    return ['男' if int(idcard[16])%2==1 else '女',
                            datetime.datetime.now().year - int(idcard[6:10]),
                            self.__idcard_info['province'][ind],
                            self.__idcard_info['city'][ind],
                            self.__idcard_info['area'][ind]
                            ]
            else:
                raise Exception('Error: The id card is wrong.')
        except Exception as result:
            print(result)
            return ['', '', '', '', '']

    # def phone_info(self, num:str|int|float):
    #     '''
    #     功能简介：
    #         查询手机号码归属地；
    #     参数解释：
    #         传入手机号码即可；
    #     return：
    #         列表，0.归属省 1.归属区
    #     '''
    #     try:
    #         number = str(int(number))
    #         ind = self.__phone_info[self.__phone_info['number']==number[:7]].index[0]
    #         return [self.__phone_info['province'][ind],self.__phone_info['city'][ind]]
    #     except:
    #         return ['', '']

def parse_phoneber(phoneNumber: str):
    '''
    功能简介：
        手机号码解析；
    所需参数：
        phoneNumber 手机号码；
    return：
        Series.  省、市、运营商；
    调用示例：
        dataframe[['省', '市', '运营商']] = dataframe['手机号'].apply(pd.Series(parse_phoneber))；
    '''
    try:
        res = jionlp.cell_phone_location(phoneNumber)
        province = res['province']
        city = res['city']
        operator = res['operator']
    except:
        province = city = operator = ''
    finally:
        return [province, city, operator]
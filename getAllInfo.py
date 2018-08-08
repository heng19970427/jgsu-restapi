# coding=utf-8
import requests
import os
from bs4 import BeautifulSoup
import re
import json
import tempfile
from subprocess import getstatusoutput

from PIL import Image
from numpy import array


# plus : tesseract-ocr 运行附加参数
# clean : 删除tesseract-ocr 产生的结果文件
def img_to_str(img, plus='--psm 7', clean=True):
    if os.path.exists(img) and os.system('tesseract') == 0:
        cmd = 'tesseract ' + img + ' ' + img + ' ' + plus
        status, out = getstatusoutput(cmd)
        if status == 0:
            with open(img + '.txt') as result:
                text = result.read().strip()
            if clean:
                os.remove(img)
                os.remove(img + '.txt')
            return text
        else:
            return 'aaaa'
    else:
        return ''


class Student:
    score = {}
    sess = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729)'
    }
    name = ''
    usermain = ''
    BaseUrl = 'http://xuanke.jgsu.edu.cn/JWXS/'

    def __init__(self, Account, PWD):
        self.Account = Account
        self.PWD = PWD

    def getCheckCode(self):
        AllCODE = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        sess = self.sess
        checkCodeImg = sess.get('http://xuanke.jgsu.edu.cn/other/CheckCode.aspx?datetime=az',
                                headers=self.headers).content
        temp = tempfile.TemporaryFile()
        temp.write(checkCodeImg)
        im = Image.open(temp)
        im = im.convert('L')
        a = array(im)
        for r in range(len(a)):
            for c in range(len(a[r])):
                if a[r][c] > 160:
                    a[r][c] = 1
                else:
                    a[r][c] = 0
        # 去除单独噪点
        for r in range(len(a)):
            for c in range(len(a[r])):
                if a[r][c] == 0 and (a[r][c - 1] == 1 and a[r][c + 1] == 1):
                    a[r][c] = 1
        # 转为灰度照片
        for r in range(len(a)):
            for c in range(len(a[r])):
                # print a[r][c],
                if a[r][c] == 0:
                    a[r][c] = 1
                else:
                    a[r][c] = 255
            # print '\n'
        im = Image.fromarray(a)
        im.save('temp.jpg')
        code = img_to_str('temp.jpg', clean=True)
        temp.close()
        if code == u'':
            return 'cwda'
        else:
            result = ''
            for x in range(0, len(code)):
                if code[x] in AllCODE:
                    result += code[x]
            return result

    def login(self):
        sess = self.sess
        resp = sess.get('http://xuanke.jgsu.edu.cn/Login.aspx', headers=self.headers)
        soup = BeautifulSoup(resp.text, 'lxml')
        VIEWSTATE = soup.find('input', attrs={'id': '__VIEWSTATE'}).get('value')
        VIEWSTATEGENERATOR = soup.find('input', attrs={'id': '__VIEWSTATEGENERATOR'}).get('value')
        EVENTVALIDATION = soup.find('input', attrs={'id': '__EVENTVALIDATION'}).get('value')

        data = {
            '__VIEWSTATE': VIEWSTATE,
            '__VIEWSTATEGENERATOR': VIEWSTATEGENERATOR,
            '__EVENTVALIDATION': EVENTVALIDATION,
            'Account': self.Account,
            'PWD': self.PWD,
            'CheckCode': self.getCheckCode(),
            'cmdok': ''
        }
        r = sess.post('http://xuanke.jgsu.edu.cn/Login.aspx', data=data, headers=self.headers)
        while u'验证码不正确' in r.text:
            data['CheckCode'] = self.getCheckCode()
            r = sess.post('http://xuanke.jgsu.edu.cn/Login.aspx', data=data, headers=self.headers)

        if u'用户名或密码错误' not in r.text:
            p_name = re.compile(r'id="users">(.*?)<')
            self.name = p_name.search(r.text).group(1)
            r = sess.post(self.BaseUrl + 'xsMenu.aspx').text
            p_usermain = re.compile(r'cjcx/jwxs_cjcx_like\.aspx\?usermain=(.*?)"')
            self.usermain = p_usermain.search(r).group(1)
            return True
        else:
            return False

    def getScore(self):
        if self.name != '':
            sess = self.sess
            r = sess.post(self.BaseUrl + 'cjcx/jwxs_cjcx_like.aspx?usermain=' + self.usermain, headers=self.headers)
            p_score = re.compile(
                r"<td>.</td><td>(?P<date>.*?)</td><td>(?P<classid>.*?)</td><td>(?P<classname>.*?)</td><td>(?P<score>.*?)</td><td>(?P<xuefen>.*?)</td><td>(?P<xueshi>.*?)</td><td>(?P<attr>.*?)</td><td>(?P<sort>.*?)</td><td>(?P<xingzhi>.*?)</td><td>(?P<how>.*?)</td><td>(?P<flag>.*?)</td><td>(?P<bukao>.*?)</td>")
            self.score = p_score.findall(r.text)
            scores = []
            for s in self.score:
                temp = {'xq': s[0], 'classid': s[1], 'classname': s[2], 'score': s[3], 'xuefen': s[4], 'keshi': s[5],
                        'bixiu': s[6], 'xianxuan': s[7], 'bukao': s[8], 'kaocha': s[9], 'note': s[10], 'bukaoxq': s[11]}
                scores.append(temp)

            return {'id': self.Account, 'scores': scores}

    def getKeBiao(self):
        if self.name != '':
            sess = self.sess
            r = sess.post(self.BaseUrl + 'pkgl/XsKB_List.aspx?usermain=' + self.usermain, headers=self.headers)
            soup = BeautifulSoup(r.text, 'lxml')
            with open('kebiao.html','w+') as fp:
                fp.write(r.text)
            nowtime = soup.find_all('option', attrs={'selected': 'selected'})
            ddlxnxqh = nowtime[0].get('value')
            nowzc = nowtime[1].get('value')
            __VIEWSTATE = soup.find('input', attrs={'id': '__VIEWSTATE'}).get('value')
            __VIEWSTATEGENERATOR = soup.find('input', attrs={'id': '__VIEWSTATEGENERATOR'}).get('value')
            data = {
                '__EVENTTARGET': 'zc',
                '__EVENTARGUMENT': '',
                '__LASTFOCUS': '',
                '__VIEWSTATE': __VIEWSTATE,
                '__VIEWSTATEGENERATOR': __VIEWSTATEGENERATOR,
                'ddlxnxqh': ddlxnxqh,
                'zc': '',
                'b1': '打印课表',
                'usermain': self.usermain
            }
            html = sess.post(self.BaseUrl + 'pkgl/XsKB_List.aspx?usermain=' + self.usermain, headers=self.headers,
                             data=data).text
            p1 = re.compile(r"title='(.*?)'", re.DOTALL)
            results = p1.findall(html)
            all_class = []
            for result in results:
                temp = {}
                for item in result.split('\n'):
                    item = item.replace('：', ':')
                    kv = item.split(':')
                    temp[kv[0]] = kv[1]
                all_class.append(temp)
            for c in all_class:
                zc = c['上课周次']
                temp = []
                if zc.isnumeric():
                    temp.append(int(zc))
                else:
                    if "," in zc:
                        temp.append(int(zc.split(",")[0]))
                        zc = zc.split(",")[1]
                    if "双周" in zc:
                        zc = zc.replace("双周","")
                        zcr = zc.split("-")
                        temp.extend(list(filter(lambda a: a%2==0, range(int(zcr[0]),int(zcr[1])+1))))
                    elif "单周" in zc:
                        zc = zc.replace("单周","")
                        zcr = zc.split("-")
                        temp.extend(list(filter(lambda a: a%2==1, range(int(zcr[0]),int(zcr[1])+1))))
                    else:
                        zcr = zc.split("-")
                        temp.extend(range(int(zcr[0]),int(zcr[1])+1))
                c['上课周次'] = temp

            return {'id': self.Account, 'classes': all_class},ddlxnxqh,nowzc

    def getBaseinfo(self):
        sess = self.sess
        r = sess.get(self.BaseUrl + 'xskp/jwxs_xskp_like.aspx?usermain=' + self.usermain, headers=self.headers)
        soup = BeautifulSoup(r.text, 'lxml')
        all_info = soup.find_all('input', attrs={'type': 'text'})
        all_info2 = soup.find_all('span')
        baseInfo = {}

        temp = []
        for info in all_info2:
            if info.get('id'):
                temp.append(info.text)

        baseInfo['id'] = self.Account
        baseInfo['name'] = all_info[0].get('value')
        baseInfo['brithday'] = all_info[1].get('value')
        baseInfo['degree'] = all_info[10].get('value')
        baseInfo['when'] = all_info[111].get('value')
        baseInfo['kaohao'] = all_info[113].get('value')
        baseInfo['idnum'] = all_info[114].get('value')
        baseInfo['xueyuan'] = temp[0]
        baseInfo['major'] = temp[1]
        baseInfo['xuezhi'] = temp[2]
        baseInfo['class'] = temp[3]
        baseInfo['img'] = 'http://xuanke.jgsu.edu.cn/upload/XSXX/' + str(self.Account) + '.jpg'
        return baseInfo


if __name__ == '__main__':
    stu = Student(Account=1609103050, PWD='xiaoliu...')
    if stu.login():
        kb = stu.getKeBiao()
        score = stu.getScore()
        baseinfo = stu.getBaseinfo()
        # print(json.dumps(kb, ensure_ascii=False, indent=2))
        # print(json.dumps(score, ensure_ascii=False, indent=2))
        # print(json.dumps(baseinfo, ensure_ascii=False, indent=2))
    else:
        print('登录失败！')

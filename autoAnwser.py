import requests
import random
import re
import json
import time
from threading import Thread


class AutoAnwser:
    url = ''
    sess = requests.session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
    }

    def async(f):
        def wrapper(*args, **kwargs):
            thr = Thread(target=f, args=args, kwargs=kwargs)
            thr.start()

        return wrapper

    def GetQueryString(self, name):
        reg = re.compile("(^|&)" + name + "=([^&]*)(&|$)")
        reg_search = re.compile(r".*?\?(.*)")
        search = reg_search.search(self.url)
        try:
            r = reg.search(search.group(1))
        except AttributeError:
            r = None
        if r is not None:
            return r.group(2)
        else:
            return None

    def GetExercises(self, address, userid):
        exercises_url = 'http://' + address + '/phone/examSystemController/getMockExercises?rnd=' + str(random.random())
        data = {
            'userid': userid
        }
        r = self.sess.post(exercises_url, data=data, headers=self.headers)
        if r.status_code == 200:
            return r.json()
        else:
            return None

    def submit(self, address, userid, testpaperid, stage_questionid, submitanswer, istrue):
        data = {
            "userid": userid,
            "testpaperid": testpaperid,
            "stage_questionid": stage_questionid,
            "submitanswer": submitanswer,
            "istrue": istrue
        }
        submit_url = 'http://' + address + '/phone/examSystemController/submitMockExamAnswer?rnd=' + str(
            random.random())
        resp = self.sess.post(url=submit_url, headers=self.headers, data=data)
        return resp.text

    def finish(self, address, userid, testpaperid, truecount, errorcount, undonecount):
        data = {
            'userid': userid,
            'testpaperid': testpaperid,
            'truecount': truecount,
            'errorcount': errorcount,
            'undonecount': undonecount
        }
        finish_url = 'http://' + address + '/phone/examSystemController/submitMockExamGrade?rnd=' + str(random.random())
        resp = self.sess.post(finish_url, data=data).json()
        if resp['stateType'] == 0:
            return True
        else:
            return False

    @async
    def run(self, score):
        userid = self.GetQueryString('userid')
        address = self.GetQueryString('IP')
        test_text = self.GetExercises(address, userid)
        stateValue = json.loads(test_text['stateValue'])
        testpaperid = stateValue['testpaperid']
        geted_score = 0
        for question in stateValue['stage_questionJson']:
            geted_score += 1
            if geted_score > score:
                stage_questionid = question['id']
                if question['answer'] == 'A':
                    submitanswer = 'B'
                else:
                    submitanswer = 'A'
                istrue = 2
            else:
                stage_questionid = question['id']
                submitanswer = question['answer']
                istrue = 1
            print(stage_questionid, submitanswer)
            self.submit(address, int(userid), testpaperid, stage_questionid, submitanswer, istrue)
            time.sleep(random.randint(1, 3))
        if self.finish(address, userid, testpaperid, score, 100-score, 0):
            print('提交成功')
            return True


if __name__ == '__main__':
    auto = AutoAnwser()
    auto.url = 'http://jdvxexam.jxkth.com/jdwxexam/test_v3/test_v1.html?userid=11&IP=120.78.218.238:8500/jdwxexam'
    # auto.run(想要的分数)
    auto.run(90)

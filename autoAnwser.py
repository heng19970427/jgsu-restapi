import requests
import random
import re
import json
import time
from threading import Thread


class AutoAnwser:
    url = 'http://jdvxexam.jxkth.com/jdwxexam/test_v3/test_v1.html?userid=11&IP=120.78.218.238:8500/jdwxexam'
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
        r = reg.search(search.group(1))
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
        print(data)
        submit_url = 'http://' + address + '/phone/examSystemController/submitMockExamAnswer?rnd=' + str(
            random.random())
        print(submit_url)
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
    def run(self):
        userid = self.GetQueryString('userid')
        address = self.GetQueryString('IP')
        test_text = self.GetExercises(address, userid)
        stateValue = json.loads(test_text['stateValue'])
        testpaperid = stateValue['testpaperid']
        for question in stateValue['stage_questionJson']:
            stage_questionid = question['id']
            submitanswer = question['answer']
            istrue = 1
            print(stage_questionid, submitanswer)
            result = self.submit(address, int(userid), testpaperid, stage_questionid, submitanswer, istrue)
            print(result)
            time.sleep(random.randint(3, 5))
        if self.finish(address, userid, testpaperid, 100, 0, 0):
            print('提交成功')


if __name__ == '__main__':
    auto = AutoAnwser()
    print(0)
    auto.run()
    print(1)



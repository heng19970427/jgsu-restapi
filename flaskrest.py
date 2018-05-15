# -*- coding: utf-8 -*-

from flask import Flask, jsonify, request
from flask_cors import CORS

from getAllInfo import Student
from autoAnwser import AutoAnwser
from db import Dao

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app, supports_credentials=True)

dao = Dao()
confirmed_account = dao.get_all_account()


@app.route('/api_v1/auto_anwser', methods=['POST', 'GET'])
def auto_anwser():
    url = request.form.get('url')
    score = request.form.get('score')
    auto = AutoAnwser()
    userid = auto.GetQueryString('userid')
    if userid is None or auto.GetQueryString('IP') is None or score <= 0 or score > 100:
        return jsonify({'code': 1, 'msg': '请输入合法地址和分数'})
    else:
        auto.url = url
        auto.run(score)
        return jsonify({'code': 0, 'msg': '后台运行中, 请勿重复提交'})


@app.route('/api_v1/get_baseinfo', methods=['POST', 'GET'])
def get_baseinfo():
    str_account = request.form.get('account')
    account = int(str_account)
    passwd = request.form.get('passwd')
    if confirm(account, passwd):
        baseinfo = dao.get_baseinfo(account)
        return jsonify({'code': 0, 'baseinfo': baseinfo})
    else:
        return jsonify({'code': 1, 'msg': 'no info of %s' % account})


@app.route('/api_v1/get_score', methods=['POST', 'GET'])
def get_score():
    str_account = request.form.get('account')
    account = int(str_account)
    passwd = request.form.get('passwd')
    xq = request.form.get('xq')
    if confirm(account, passwd):
        scores = dao.get_scores(account, xq)
        scores['code'] = 0
        return jsonify(scores)
    else:
        return jsonify({'code': 1, 'msg': 'no scores of %s' % account})


@app.route('/api_v1/get_all_class', methods=['POST', 'GET'])
def get_all_class():
    str_account = request.form.get('account')
    account = int(str_account)
    passwd = request.form.get('passwd')
    if confirm(account, passwd):
        classes = dao.get_classes(account)
        xqzc = dao.get_xqzc()
        classes['code'] = 0
        classes['zc'] = xqzc['zc']
        classes['xq'] = xqzc['xq']
        return jsonify(classes)
    else:
        return jsonify({'code': 1, 'msg': 'can not find class of %s'})


@app.route('/api_v1/auth', methods=['POST', 'GET'])
def auth():
    str_account = request.form.get('account')
    account = int(str_account)
    passwd = request.form.get('passwd')
    if confirm(account, passwd):
        return jsonify({'code': 0, 'msg': 'login success'})
    else:
        return jsonify({'code': 1, 'msg': 'account or password wrong'})


@app.route('/api_v1/refresh', methods=['POST', 'GET'])
def refresh():
    str_account = request.form.get('account')
    account = int(str_account)
    passwd = request.form.get('passwd')
    if get_all(account, passwd):
        return jsonify({'code': 0, 'msg': 'update success'})
    else:
        return jsonify({'code': 1, 'msg': 'account or password wrong'})


def confirm(account, passwd, getAllinfo=True):
    if account in confirmed_account and passwd == confirmed_account[account]:
        return True
    else:
        return get_all(account, passwd)


def get_all(account, passwd):
    stu = Student(Account=account, PWD=passwd)
    login_status = stu.login()
    if login_status:
        confirmed_account[account] = passwd
        # 将数据库中没有的用户 加入数据库
        dao.insert_account(account, passwd)
        scores = stu.getScore()
        classes, xq, zc = stu.getKeBiao()
        baseinfo = stu.getBaseinfo()
        dao.update_xqzc(xq, zc)
        dao.insert_scores(scores)
        dao.insert_classes(classes)
        dao.insert_baseinfo(baseinfo)
    return login_status


def main():
    app.run(host='0.0.0.0', port=50080, debug=True)


if __name__ == '__main__':
    main()

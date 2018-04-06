class Dao:
    from pymongo import MongoClient
    client = MongoClient(host='127.0.0.1')
    db = client.JGSU

    def insert_account(self, account, passwd):
        acc_info = {'id': account, 'passwd': passwd}
        col = self.db['account']
        info = col.find_one({'id': account}, {'_id': 0})
        if info is None:
            col.insert(acc_info)
        elif info != acc_info:
            col.update({'id': account}, {'$set': acc_info})

    def insert_baseinfo(self, baseinfo):
        col = self.db['baseinfo']
        info = col.find_one({'id': baseinfo['id']}, {'_id': 0})
        if info is None:
            col.insert(baseinfo)
        elif baseinfo != info:
            col.update({'id': baseinfo['id']}, {'$set': baseinfo})

    def insert_scores(self, scores):
        col = self.db['score']
        info = col.find_one({'id': scores['id']}, {'_id': 0})
        if info is None:
            col.insert(scores)
        elif info != scores:
            col.update({'id': scores['id']}, {'$set': scores})

    def insert_classes(self, classes):
        col = self.db['class']
        info = col.find_one({'id': classes['id']})
        if info is None:
            col.insert(classes)
        else:
            classes['_id'] = info['_id']
            if info != classes:
                # 直接覆盖原来的
                col.save(classes)

    def get_all_account(self):
        col = self.db['account']
        accounts = {}
        for account in col.find({}, {'_id': 0}):
            accounts[account['id']] = account['passwd']
        return accounts

    def get_baseinfo(self, account):
        col = self.db['baseinfo']
        baseinfo = col.find_one({'id': account}, {'_id': 0})
        return baseinfo

    def get_scores(self, account, xq=None):
        col = self.db['score']
        scores = col.find_one({'id': account}, {'_id': 0, 'id': 0})
        if xq is None:
            return scores
        else:
            result = []
            for score in scores.get('scores'):
                if score['xq'] == xq:
                    result.append(score)
            return {'scores': result}

    def get_classes(self, account):
        col = self.db['class']
        all_class = col.find_one({'id': account}, {'_id': 0, 'id': 0})
        return all_class


def main():
    dao = Dao()
    dao.insert_account(1609103050, 'xiaoliu...')
    dao.insert_baseinfo({
        "id": 1609103050,
        "name": "衡玉良",
        "brithday": "1997-04-27",
        "degree": "本科",
        "when": "2016",
        "kaohao": "16411715150867",
        "idnum": "411323199704274472",
        "xueyuan": "电子与信息工程学院",
        "major": "计算机科学与技术",
        "xuezhi": "4.0",
        "class": "计算机16(本3)",
        "img": "http://xuanke.jgsu.edu.cn/upload/XSXX/1609103050.jpg"
    })
    scores = {
        "id": 1609103050,
        "scores": [
            {
                "xq": "2016-2017-1",
                "classid": "1263333",
                "classname": "C语言程序设计",
                "score": "61.0",
                "xuefen": "4.0",
                "keshi": "64",
                "bixiu": "必修",
                "xianxuan": "C1必修",
                "bukao": "正常考试",
                "kaocha": "考试",
                "note": "",
                "bukaoxq": ""
            },
            {
                "xq": "2016-2017-1",
                "classid": "*05020101",
                "classname": "大学英语(1)",
                "score": "60.0",
                "xuefen": "4.0",
                "keshi": "64",
                "bixiu": "必修",
                "xianxuan": "通识课",
                "bukao": "补考1",
                "kaocha": "考试",
                "note": "",
                "bukaoxq": "2016-2017-2"
            },
            {
                "xq": "2016-2017-1",
                "classid": "*05020101",
                "classname": "大学英语(1)",
                "score": "32.0",
                "xuefen": "4.0",
                "keshi": "64",
                "bixiu": "必修",
                "xianxuan": "通识课",
                "bukao": "正常考试",
                "kaocha": "考试",
                "note": "",
                "bukaoxq": ""
            },
            {
                "xq": "2016-2017-1",
                "classid": "07010109",
                "classname": "高等数学A1",
                "score": "19.0",
                "xuefen": "5.0",
                "keshi": "80",
                "bixiu": "必修",
                "xianxuan": "通识课",
                "bukao": "补考1",
                "kaocha": "考试",
                "note": "",
                "bukaoxq": "2016-2017-2"
            },
            {
                "xq": "2016-2017-1",
                "classid": "07010109",
                "classname": "高等数学A1",
                "score": "10.0",
                "xuefen": "5.0",
                "keshi": "80",
                "bixiu": "必修",
                "xianxuan": "通识课",
                "bukao": "正常考试",
                "kaocha": "考试",
                "note": "",
                "bukaoxq": ""
            },
            {
                "xq": "2016-2017-1",
                "classid": "08060505",
                "classname": "计算机导论",
                "score": "74.0",
                "xuefen": "3.0",
                "keshi": "48",
                "bixiu": "必修",
                "xianxuan": "专业基础课",
                "bukao": "正常考试",
                "kaocha": "考查",
                "note": "",
                "bukaoxq": ""
            },
            {
                "xq": "2016-2017-1",
                "classid": "03040407M",
                "classname": "井冈山精神与当代大学生",
                "score": "84.0",
                "xuefen": "1.0",
                "keshi": "16",
                "bixiu": "必修",
                "xianxuan": "通识课",
                "bukao": "正常考试",
                "kaocha": "考查",
                "note": "",
                "bukaoxq": ""
            },
            {
                "xq": "2016-2017-1",
                "classid": "*04020105",
                "classname": "军事理论",
                "score": "88.0",
                "xuefen": "1.0",
                "keshi": "16",
                "bixiu": "必修",
                "xianxuan": "通识课",
                "bukao": "正常考试",
                "kaocha": "考查",
                "note": "",
                "bukaoxq": ""
            },
            {
                "xq": "2016-2017-1",
                "classid": "*00000005",
                "classname": "军训",
                "score": "80.0",
                "xuefen": "1.0",
                "keshi": "0",
                "bixiu": "必修",
                "xianxuan": "实践环节",
                "bukao": "正常考试",
                "kaocha": "考查",
                "note": "",
                "bukaoxq": ""
            },
            {
                "xq": "2016-2017-1",
                "classid": "04020101",
                "classname": "体育1",
                "score": "77.0",
                "xuefen": "1.0",
                "keshi": "32",
                "bixiu": "必修",
                "xianxuan": "通识课",
                "bukao": "正常考试",
                "kaocha": "考查",
                "note": "",
                "bukaoxq": ""
            },
            {
                "xq": "2016-2017-1",
                "classid": "*03040403",
                "classname": "中国近现代史纲要",
                "score": "71.0",
                "xuefen": "2.0",
                "keshi": "24",
                "bixiu": "必修",
                "xianxuan": "通识课",
                "bukao": "正常考试",
                "kaocha": "考试",
                "note": "",
                "bukaoxq": ""
            },
            {
                "xq": "2016-2017-1",
                "classid": "00000031",
                "classname": "准职业人导向训练一",
                "score": "81.0",
                "xuefen": "1.0",
                "keshi": "16",
                "bixiu": "限选",
                "xianxuan": "A2限选",
                "bukao": "正常考试",
                "kaocha": "考查",
                "note": "",
                "bukaoxq": ""
            },
            {
                "xq": "2016-2017-2",
                "classid": "080605061`",
                "classname": "C++程序设计",
                "score": "68.0",
                "xuefen": "4.0",
                "keshi": "64",
                "bixiu": "必修",
                "xianxuan": "专业基础课",
                "bukao": "正常考试",
                "kaocha": "考试",
                "note": "",
                "bukaoxq": ""
            },
            {
                "xq": "2016-2017-2",
                "classid": "*07020101",
                "classname": "大学物理A1",
                "score": "60.0",
                "xuefen": "3.0",
                "keshi": "48",
                "bixiu": "必修",
                "xianxuan": "通识课",
                "bukao": "补考1",
                "kaocha": "考试",
                "note": "",
                "bukaoxq": "2017-2018-1"
            },
            {
                "xq": "2016-2017-2",
                "classid": "*07020101",
                "classname": "大学物理A1",
                "score": "45.0",
                "xuefen": "3.0",
                "keshi": "48",
                "bixiu": "必修",
                "xianxuan": "通识课",
                "bukao": "正常考试",
                "kaocha": "考试",
                "note": "",
                "bukaoxq": ""
            },
            {
                "xq": "2016-2017-2",
                "classid": "66020403S",
                "classname": "大学物理实验1",
                "score": "85.0",
                "xuefen": "1.0",
                "keshi": "32",
                "bixiu": "必修",
                "xianxuan": "B1必修",
                "bukao": "正常考试",
                "kaocha": "考试",
                "note": "",
                "bukaoxq": ""
            },
            {
                "xq": "2016-2017-2",
                "classid": "*05020102",
                "classname": "大学英语(2)",
                "score": "70.0",
                "xuefen": "4.0",
                "keshi": "64",
                "bixiu": "必修",
                "xianxuan": "通识课",
                "bukao": "正常考试",
                "kaocha": "考试",
                "note": "",
                "bukaoxq": ""
            },
            {
                "xq": "2016-2017-2",
                "classid": "05010101",
                "classname": "大学语文",
                "score": "71.0",
                "xuefen": "2.0",
                "keshi": "32",
                "bixiu": "必修",
                "xianxuan": "通识课",
                "bukao": "正常考试",
                "kaocha": "考查",
                "note": "",
                "bukaoxq": ""
            },
            {
                "xq": "2016-2017-2",
                "classid": "08060506a",
                "classname": "电路与电子技术",
                "score": "32.0",
                "xuefen": "4.0",
                "keshi": "64",
                "bixiu": "必修",
                "xianxuan": "C1必修",
                "bukao": "正常考试",
                "kaocha": "考试",
                "note": "",
                "bukaoxq": ""
            },
            {
                "xq": "2016-2017-2",
                "classid": "08060506a",
                "classname": "电路与电子技术",
                "score": "60.0",
                "xuefen": "4.0",
                "keshi": "64",
                "bixiu": "必修",
                "xianxuan": "C1必修",
                "bukao": "补考1",
                "kaocha": "考试",
                "note": "",
                "bukaoxq": "2017-2018-1"
            },
            {
                "xq": "2016-2017-2",
                "classid": "*07010102",
                "classname": "高等数学A2",
                "score": "46.0",
                "xuefen": "5.0",
                "keshi": "80",
                "bixiu": "必修",
                "xianxuan": "通识课",
                "bukao": "正常考试",
                "kaocha": "考试",
                "note": "",
                "bukaoxq": ""
            },
            {
                "xq": "2016-2017-2",
                "classid": "*07010102",
                "classname": "高等数学A2",
                "score": "60.0",
                "xuefen": "5.0",
                "keshi": "80",
                "bixiu": "必修",
                "xianxuan": "通识课",
                "bukao": "补考1",
                "kaocha": "考试",
                "note": "",
                "bukaoxq": "2017-2018-1"
            },
            {
                "xq": "2016-2017-2",
                "classid": "0720111",
                "classname": "基础编程能力培养",
                "score": "86.0",
                "xuefen": "2.0",
                "keshi": "32",
                "bixiu": "公选",
                "xianxuan": "公共选修课",
                "bukao": "正常考试",
                "kaocha": "考查",
                "note": "",
                "bukaoxq": ""
            },
            {
                "xq": "2016-2017-2",
                "classid": "08060507",
                "classname": "离散数学",
                "score": "62.0",
                "xuefen": "4.0",
                "keshi": "64",
                "bixiu": "必修",
                "xianxuan": "专业基础课",
                "bukao": "正常考试",
                "kaocha": "考试",
                "note": "",
                "bukaoxq": ""
            },
            {
                "xq": "2016-2017-2",
                "classid": "*03040402",
                "classname": "思想道德修养与法律基础",
                "score": "75.0",
                "xuefen": "3.0",
                "keshi": "40",
                "bixiu": "必修",
                "xianxuan": "通识课",
                "bukao": "正常考试",
                "kaocha": "考试",
                "note": "",
                "bukaoxq": ""
            },
            {
                "xq": "2016-2017-2",
                "classid": "04020102",
                "classname": "体育(2)",
                "score": "76.0",
                "xuefen": "1.0",
                "keshi": "32",
                "bixiu": "必修",
                "xianxuan": "A1必修",
                "bukao": "正常考试",
                "kaocha": "考试",
                "note": "",
                "bukaoxq": ""
            },
            {
                "xq": "2016-2017-2",
                "classid": "*07010107",
                "classname": "线性代数",
                "score": "42.0",
                "xuefen": "2.0",
                "keshi": "32",
                "bixiu": "必修",
                "xianxuan": "通识课",
                "bukao": "正常考试",
                "kaocha": "考试",
                "note": "",
                "bukaoxq": ""
            },
            {
                "xq": "2016-2017-2",
                "classid": "*07010107",
                "classname": "线性代数",
                "score": "60.0",
                "xuefen": "2.0",
                "keshi": "32",
                "bixiu": "必修",
                "xianxuan": "通识课",
                "bukao": "补考1",
                "kaocha": "考试",
                "note": "",
                "bukaoxq": "2017-2018-1"
            },
            {
                "xq": "2016-2017-2",
                "classid": "0722002",
                "classname": "移动互联网时代的信息安全与防护",
                "score": "99.0",
                "xuefen": "2.0",
                "keshi": "32",
                "bixiu": "任选",
                "xianxuan": "公共选修课",
                "bukao": "正常考试",
                "kaocha": "考查",
                "note": "",
                "bukaoxq": ""
            },
            {
                "xq": "2016-2017-2",
                "classid": "00000032",
                "classname": "准职业人导向训练二",
                "score": "86.0",
                "xuefen": "1.0",
                "keshi": "16",
                "bixiu": "限选",
                "xianxuan": "A2限选",
                "bukao": "正常考试",
                "kaocha": "考查",
                "note": "",
                "bukaoxq": ""
            },
            {
                "xq": "2017-2018-1",
                "classid": "0020102",
                "classname": "大学物理A2",
                "score": "48.0",
                "xuefen": "3.0",
                "keshi": "48",
                "bixiu": "必修",
                "xianxuan": "B1必修",
                "bukao": "正常考试",
                "kaocha": "考试",
                "note": "",
                "bukaoxq": ""
            },
            {
                "xq": "2017-2018-1",
                "classid": "0020102",
                "classname": "大学物理A2",
                "score": "60.0",
                "xuefen": "3.0",
                "keshi": "48",
                "bixiu": "必修",
                "xianxuan": "B1必修",
                "bukao": "补考1",
                "kaocha": "考试",
                "note": "",
                "bukaoxq": "2017-2018-2"
            },
            {
                "xq": "2017-2018-1",
                "classid": "07020146",
                "classname": "大学物理实验B2",
                "score": "90.0",
                "xuefen": "1.0",
                "keshi": "32",
                "bixiu": "必修",
                "xianxuan": "B1必修",
                "bukao": "正常考试",
                "kaocha": "考试",
                "note": "",
                "bukaoxq": ""
            },
            {
                "xq": "2017-2018-1",
                "classid": "*05020103",
                "classname": "大学英语(3)",
                "score": "74.0",
                "xuefen": "4.0",
                "keshi": "64",
                "bixiu": "必修",
                "xianxuan": "通识课",
                "bukao": "正常考试",
                "kaocha": "考试",
                "note": "",
                "bukaoxq": ""
            },
            {
                "xq": "2017-2018-1",
                "classid": "0720113",
                "classname": "电子技术大揭密",
                "score": "75.0",
                "xuefen": "2.0",
                "keshi": "32",
                "bixiu": "公选",
                "xianxuan": "公共选修课",
                "bukao": "正常考试",
                "kaocha": "考查",
                "note": "",
                "bukaoxq": ""
            },
            {
                "xq": "2017-2018-1",
                "classid": "*07010108",
                "classname": "概率与统计",
                "score": "23.0",
                "xuefen": "2.0",
                "keshi": "32",
                "bixiu": "必修",
                "xianxuan": "B1必修",
                "bukao": "正常考试",
                "kaocha": "考试",
                "note": "",
                "bukaoxq": ""
            },
            {
                "xq": "2017-2018-1",
                "classid": "*07010108",
                "classname": "概率与统计",
                "score": "60.0",
                "xuefen": "2.0",
                "keshi": "32",
                "bixiu": "必修",
                "xianxuan": "B1必修",
                "bukao": "补考1",
                "kaocha": "考试",
                "note": "",
                "bukaoxq": "2017-2018-2"
            },
            {
                "xq": "2017-2018-1",
                "classid": "08A3232",
                "classname": "数据结构与算法",
                "score": "88.0",
                "xuefen": "4.0",
                "keshi": "64",
                "bixiu": "必修",
                "xianxuan": "C1必修",
                "bukao": "正常考试",
                "kaocha": "考试",
                "note": "",
                "bukaoxq": ""
            },
            {
                "xq": "2017-2018-1",
                "classid": "08060508",
                "classname": "数字逻辑",
                "score": "27.0",
                "xuefen": "4.0",
                "keshi": "64",
                "bixiu": "必修",
                "xianxuan": "C1必修",
                "bukao": "正常考试",
                "kaocha": "考试",
                "note": "",
                "bukaoxq": ""
            },
            {
                "xq": "2017-2018-1",
                "classid": "08060508",
                "classname": "数字逻辑",
                "score": "60.0",
                "xuefen": "4.0",
                "keshi": "64",
                "bixiu": "必修",
                "xianxuan": "C1必修",
                "bukao": "补考1",
                "kaocha": "考试",
                "note": "",
                "bukaoxq": "2017-2018-2"
            },
            {
                "xq": "2017-2018-1",
                "classid": "04020103",
                "classname": "体育(3)",
                "score": "78.0",
                "xuefen": "1.0",
                "keshi": "32",
                "bixiu": "必修",
                "xianxuan": "A1必修",
                "bukao": "正常考试",
                "kaocha": "考查",
                "note": "",
                "bukaoxq": ""
            },
            {
                "xq": "2017-2018-1",
                "classid": "*08090122",
                "classname": "云计算导论",
                "score": "78.0",
                "xuefen": "2.0",
                "keshi": "32",
                "bixiu": "限选",
                "xianxuan": "C2限选",
                "bukao": "正常考试",
                "kaocha": "考查",
                "note": "",
                "bukaoxq": ""
            },
            {
                "xq": "2017-2018-1",
                "classid": "00000033",
                "classname": "职业定位与发展一",
                "score": "77.0",
                "xuefen": "1.0",
                "keshi": "16",
                "bixiu": "限选",
                "xianxuan": "A2限选",
                "bukao": "正常考试",
                "kaocha": "考查",
                "note": "",
                "bukaoxq": ""
            }
        ]
    }
    classes = {
        "id": 1609103050,
        "classes": [
            {
                "开课编号": "20172000425",
                "课程编码": "05020104",
                "课程名称": "大学英语(4)",
                "授课教师": "刘小英w",
                "开课时间": "10102",
                "上课周次": "1-17",
                "开课地点": "10B105",
                "上课班级": "计算机16(本3)"
            },
            {
                "开课编号": "20172004931",
                "课程编码": "*08070311",
                "课程名称": "IP网络+数据网络构建",
                "授课教师": "朱志超",
                "开课时间": "20102",
                "上课周次": "9-12",
                "开课地点": "",
                "上课班级": "计算机16(本2),计算机16(本3)"
            },
            {
                "开课编号": "20172004117",
                "课程编码": "08060517",
                "课程名称": "操作系统",
                "授课教师": "谭云兰",
                "开课时间": "30102",
                "上课周次": "3-17单周",
                "开课地点": "10B502",
                "上课班级": "计算机16(本3)"
            },
            {
                "开课编号": "20172004114",
                "课程编码": "08060516",
                "课程名称": "计算机组成原理",
                "授课教师": "朱兵",
                "开课时间": "40102",
                "上课周次": "1-17双周",
                "开课地点": "10B507",
                "上课班级": "计算机16(本1),计算机16(本3)"
            },
            {
                "开课编号": "20172004931",
                "课程编码": "*08070311",
                "课程名称": "IP网络+数据网络构建",
                "授课教师": "朱志超",
                "开课时间": "50102",
                "上课周次": "1,5-17",
                "开课地点": "10A002",
                "上课班级": "计算机16(本2),计算机16(本3)"
            },
            {
                "开课编号": "201720000640",
                "课程编码": "04020104",
                "课程名称": "体育(4)",
                "授课教师": "陈万睿",
                "开课时间": "10304",
                "上课周次": "1-17",
                "开课地点": "",
                "上课班级": "电信武术2"
            },
            {
                "开课编号": "20172004934",
                "课程编码": "08090119",
                "课程名称": "Java Web 程序设计",
                "授课教师": "曾劲涛",
                "开课时间": "20304",
                "上课周次": "3-17单周",
                "开课地点": "10B501",
                "上课班级": "计算机16(本3)"
            },
            {
                "开课编号": "20172000425",
                "课程编码": "05020104",
                "课程名称": "大学英语(4)",
                "授课教师": "刘小英w",
                "开课时间": "30304",
                "上课周次": "1-17单周",
                "开课地点": "10C514",
                "上课班级": "计算机16(本3)"
            },
            {
                "开课编号": "20172000425",
                "课程编码": "05020104",
                "课程名称": "大学英语(4)",
                "授课教师": "刘小英w",
                "开课时间": "30304",
                "上课周次": "1-17双周",
                "开课地点": "",
                "上课班级": "计算机16(本3)"
            },
            {
                "开课编号": "20172004929",
                "课程编码": "00000034",
                "课程名称": "职业定位与发展二",
                "授课教师": "陈青霞",
                "开课时间": "40304",
                "上课周次": "1-8",
                "开课地点": "10A006",
                "上课班级": "计算机16(本2),计算机16(本3)"
            },
            {
                "开课编号": "20172004114",
                "课程编码": "08060516",
                "课程名称": "计算机组成原理",
                "授课教师": "朱兵",
                "开课时间": "40304",
                "上课周次": "1-17双周",
                "开课地点": "10B507",
                "上课班级": "计算机16(本1),计算机16(本3)"
            },
            {
                "开课编号": "20172004117",
                "课程编码": "08060517",
                "课程名称": "操作系统",
                "授课教师": "谭云兰",
                "开课时间": "1050607",
                "上课周次": "1-17",
                "开课地点": "10B002",
                "上课班级": "计算机16(本3)"
            },
            {
                "开课编号": "20172004931",
                "课程编码": "*08070311",
                "课程名称": "IP网络+数据网络构建",
                "授课教师": "朱志超",
                "开课时间": "3050607",
                "上课周次": "9-17",
                "开课地点": "",
                "上课班级": "计算机16(本2),计算机16(本3)"
            },
            {
                "开课编号": "20172004114",
                "课程编码": "08060516",
                "课程名称": "计算机组成原理",
                "授课教师": "朱兵",
                "开课时间": "4050607",
                "上课周次": "1-17",
                "开课地点": "10A006",
                "上课班级": "计算机16(本1),计算机16(本3)"
            },
            {
                "开课编号": "20172004934",
                "课程编码": "08090119",
                "课程名称": "Java Web 程序设计",
                "授课教师": "曾劲涛",
                "开课时间": "5050607",
                "上课周次": "1-17",
                "开课地点": "10B104",
                "上课班级": "计算机16(本3)"
            },
            {
                "开课编号": "20172004931",
                "课程编码": "*08070311",
                "课程名称": "IP网络+数据网络构建",
                "授课教师": "朱志超",
                "开课时间": "10809",
                "上课周次": "8-10",
                "开课地点": "10A001",
                "上课班级": "计算机16(本2),计算机16(本3)"
            },
            {
                "开课编号": "20172004182",
                "课程编码": "*03040404",
                "课程名称": "马克思主义基本原理",
                "授课教师": "杨东明",
                "开课时间": "20809",
                "上课周次": "1-17",
                "开课地点": "10A002",
                "上课班级": "计算机16(本3),电信16(本2)"
            },
            {
                "开课编号": "20174000338",
                "课程编码": "*03040401-4",
                "课程名称": "形势与政策",
                "授课教师": "刘怡",
                "开课时间": "60809",
                "上课周次": "9-16",
                "开课地点": "第9教学楼108",
                "上课班级": "计算机16(本1),计算机16(本2),计算机16(本3)"
            }
        ]
    }
    dao.insert_classes(classes)
    dao.insert_scores(scores)
    allscore = dao.get_scores(account=1609103050)
    score_2017 = dao.get_scores(account=1609103050, xq='2017-2018-1')
    all_class = dao.get_classes(account=1609103050)


if __name__ == '__main__':
    main()

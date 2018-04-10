from getAllInfo import Student
from db import Dao

import time

dao = Dao()
stu = Student(Account=1609103050, PWD='xiaoliu...')

while True:
    stu.login()
    classes,xq,zc = stu.getKeBiao()
    dao.update_xqzc(xq,zc)
    time.sleep(86400)
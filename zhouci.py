#!/usr/bin/env python
from getAllInfo import Student
from db import Dao

dao = Dao()
stu = Student(Account=1609103050, PWD='xiaoliu...')

<<<<<<< HEAD
stu.login()
classes,xq,zc = stu.getKeBiao()
dao.update_xqzc(xq,zc)
print(xq,zc)
=======
while True:
    stu.login()
    classes,xq,zc = stu.getKeBiao()
    dao.update_xqzc(xq,zc)
    time.sleep(86400)
    
>>>>>>> 496e281f4f061eb6afc6d3b1fb14cea35518dd4b

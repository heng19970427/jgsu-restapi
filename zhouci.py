#!/usr/bin/env python
from getAllInfo import Student
from db import Dao

dao = Dao()
stu = Student(Account=1609103050, PWD='xiaoliu...')

stu.login()
classes,xq,zc = stu.getKeBiao()
dao.update_xqzc(xq,zc)
print(xq,zc)

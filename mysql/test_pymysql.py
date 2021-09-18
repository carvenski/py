import pymysql
import random

r = int(random.random()*100)
print(r)
#连接数据库
db = pymysql.connect(
    host="21.50.131.33",port=8080, user="finedb",password="finedb",database="db4bi"
)
#使用cursor()方法创建一个游标对象
cursor = db.cursor()
cursor.execute("select id,page_view from BIPlat_PageView;")
data = cursor.fetchall()
# print(data)
for i in data:
    print(i[0])
    r = int(random.random()*100)
    cursor.execute("UPDATE BIPlat_PageView SET page_view=%s where id='%s';" % (r, i[0]) )
    db.commit() # need commit here   
cursor.execute("select id,page_view from BIPlat_PageView;")
data = cursor.fetchall()
for i in data:   
    print(i)
#关闭游标和数据库的连接
cursor.close()
db.close()

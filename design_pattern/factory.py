#!/usr/bin/python
#coding:utf8

'''
Factory Method: use a factory class to create different products,
encapsulate the different production's creation code into one place in factory.
'''
 
class ChinaGetter:
    """A simple localizer a la gettext"""
    def __init__(self):
        self.trans = dict(dog=u"小狗", cat=u"小猫")
 
    def get(self, msgid):
        """We'll punt if we don't have a translation"""
        try:
            return self.trans[msgid]
        except KeyError:
            return str(msgid)
 
 
class EnglishGetter:
    """Simply echoes the msg ids"""
    def get(self, msgid):
        return str(msgid)

 
# this should be a factory here... 
def get_localizer(language="English"):
    """The factory method"""
    languages = dict(English=EnglishGetter, China=ChinaGetter)
    return languages[language]()
 
# Create our localizers
e, g = get_localizer("English"), get_localizer("China")
# Localize some text
for msgid in "dog parrot cat bear".split():
    print(e.get(msgid), g.get(msgid))



''' 
abstract factory:
multi factory + multi product in every factory,
'''

def printInfo(info):  
    print unicode(info, 'utf-8').encode('gbk')  

#抽象产品A：user表  
class IUser():  
    def Insert(self):  
        pass  
    def GetUser(self):  
        pass  
  
#sqlserver实现的User  
class SqlserverUser(IUser):  
    def Insert(self):  
        printInfo("在SQL Server中给User表增加一条记录")  
    def GetUser(self):  
        printInfo("在SQL Server中得到User表的一条记录")  
  
#Access实现的User  
class AccessUser(IUser):  
    def Insert(self):  
        printInfo("在Access中给User表增加一条记录")  
    def GetUser(self):  
        printInfo("在Access中得到User表一条记录")  
  
  
#抽象产品B：部门表  
class IDepartment():  
    def Insert(self):  
        pass  
    def GetUser(self):  
        pass  
  
#sqlserver实现的Department  
class SqlserverDepartment(IUser):  
    def Insert(self):  
        printInfo("在SQL Server中给Department表增加一条记录")  
    def GetUser(self):  
        printInfo("在SQL Server中得到Department表的一条记录")  
  
#Access实现的Department  
class AccessDepartment(IUser):  
    def Insert(self):  
        printInfo("在Access中给Department表增加一条记录")  
    def GetUser(self):  
        printInfo("在Access中得到Department表一条记录")  
  
  
#抽象工厂  
class IFactory():  
    def CreateUser(self):  
        pass  
    def CreateDepartment(self):  
        pass      
  
#sql server工厂  
class SqlServerFactory(IFactory):  
    def CreateUser(self):  
        return SqlserverUser()  
    def CreateDepartment(self):  
        return SqlserverDepartment()  
  
#access工厂  
class AccessFactory(IFactory):  
    def CreateUser(self):  
        return AccessUser()  
    def CreateDepartment(self):  
        return AccessDepartment()  





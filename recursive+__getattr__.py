

# 例子在原来的基础上简化了一下，排除依赖和干扰，详细参见原项目
class UrlGenerator(object):
    def __init__(self, root_url):
        self.url = root_url
 
    def __getattr__(self, item):
        if item == 'get' or item == 'post':
            print self.url
        return UrlGenerator('{}/{}'.format(self.url, item))
 
url_gen = UrlGenerator('http://xxxx')
url_gen.users.show.get
# >>> http://xxxx/users/show


# 同时覆盖掉getattribute和getattr的时候，在getattribute中需要模仿原本的行为抛出AttributeError或者手动调用getattr
class AboutAttr(object):
    def __init__(self, name):
        self.name = name
 
    def __getattribute__(self, item):
        try:
            return super(AboutAttr, self).__getattribute__(item)
        except KeyError:
            return 'default'
        except AttributeError as ex:
            print ex
 
    def __getattr__(self, item):
        return 'default'
 
at = AboutAttr('test')
print at.name
print at.not_exised

# >>>test
# >>>'AboutAttr' object has no attribute 'not_exised'
# >>>None
#上例子里面的getattr方法根本不会被调用，因为原本的AttributeError被我们自行处理并未抛出，也没有手动调用getattr，
#所以访问not_existed的结果是None而不是default.



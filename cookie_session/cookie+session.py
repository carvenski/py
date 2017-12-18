

cookie 存在 浏览器端，为了安全(用户数据应存储在服务器端)，cookie里只记录 sessionID，

session存在 服务器端，每次请求过来，检测cookie中的session_id， 更新或新建，
若有cookie，则用存于其中的sessionID查询出 session，再从session里取出 该用户的某些 信息.

Django的 User Authenticatoin机制就是靠 cookie+session+user来实现的，

Django的cookie+session：
技术细节

如果你还是好奇的话，下面是一些关于session框架内部工作方式的技术细节：

session 字典接受任何支持序列化的Python对象。 参考Python内建模块pickle的文档以获取更多信息。

Session 数据存在数据库表 django_session 中

Session 数据在需要的时候才会读取。 如果你从不使用 request.session ， Django不会动相关数据库表的一根毛。12

Django 只在需要的时候才送出cookie。 如果你压根儿就没有设置任何会话数据，它不会 送出会话cookie
(除非 SESSION_SAVE_EVERY_REQUEST 设置为 True )。

Django session 框架完全而且只能基于cookie。 它不会后退到把会话ID编码在URL中（像某些工具(PHP,JSP)那样）。3

这是一个有意而为之的设计。 把session放在URL中不只是难看，更重要的是这让你的站点 很容易受到攻击——通过 Referer header进行session ID”窃听”
而实施的攻击。

如果你还是好奇，阅读源代码是最直接办法，详见 django.contrib.sessions 。

-------------------------------------------------------------------------------------------------------

Tornado 的 cookie 机制：
Cookie 和安全 Cookie
你可以使用 set_cookie 方法在用户的浏览中设置 cookie：

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        if not self.get_cookie("mycookie"):
            self.set_cookie("mycookie", "myvalue")
            self.write("Your cookie was not set yet!")
        else:
            self.write("Your cookie was set!")
Cookie 很容易被恶意的客户端伪造。加入你想在 cookie 中保存当前登陆用户的 id 之类的信息，你需要对 cookie 作签名以防止伪造。
Tornado 通过 set_secure_cookie 和 get_secure_cookie 方法直接支持了这种功能。 要使用这些方法，你需要在创建应用时提供一个密钥，
名字为 cookie_secret。 你可以把它作为一个关键词参数传入应用的设置中：

application = tornado.web.Application([
    (r"/", MainHandler),
], cookie_secret="61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=")
签名过的 cookie 中包含了编码过的 cookie 值，另外还有一个时间戳和一个 HMAC 签名。如果 cookie 已经过期或者 签名不匹配，
get_secure_cookie 将返回 None，这和没有设置 cookie 时的 返回值是一样的。上面例子的安全 cookie 版本如下：

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        if not self.get_secure_cookie("mycookie"):
            self.set_secure_cookie("mycookie", "myvalue")
            self.write("Your cookie was not set yet!")
        else:
            self.write("Your cookie was set!")

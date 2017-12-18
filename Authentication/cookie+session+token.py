

------------------------------------------------------------------------------------------------------------------------
cookie + session/token登录认证方式总结：(注意：安全问题一般都是指防伪造,而不是防窃取,窃取是没法防范的...)

1.为了解决http无状态/服务端根本不知道是谁在访问它的缺点,当浏览器访问服务端后,服务端可以在http返回中指定set-cookie选项,这样,
浏览器会自动为当前域设置cookie,并存放sessionid,以后再访问该域时,浏览器就会自动带上它的cookie.然后由服务端取出sessionid去数据库查询,
(session一般是存放在服务端数据库里,为了提高速度也会放到redis等内存数据库里),就可以取到当前用户的session里各种认证等信息了.
由于cookie是和域名一一对应存储的,所以cookie+session方式不能支持跨域请求(比如一个项目却分为2个域名子模块,在A域里面认证过的用户只能
继续访问A域,如果访问B域则拿不到A域的cookie信息,因此A域的认证信息不能跨B域使用,当然很少有这种情况)

2.现在换一种做法,服务端不存储session了,当用户第一次使用用户名密码认证过后,服务端会生成一个token(通关令牌)返回给客户端,
然后后面再发请求时都要带上这个token(一般是把token放在Authentication的header里面),服务端每次会验证这个token值,
token里面带有加密的用户的信息等(参考token的生成/验证机制:JWT),一般只需要解密一下就知道该token是不是伪造的了：
(token一般分为xyz三部分,验证token是否是伪造的就是使用xyz三部分互相印证:xy可以生成z,简单来说只要看下decode(x+y)==z即可验证),
当然这种验证只是验证了token不是伪造的,有些应用要求更严格,还是会在服务端数据库存储签发的token,然后比对其值(就是双重验证更安全).
token的生成一般会包含时间戳,有些应用在每次请求都会重新生成/发放新的token,以提高安全性.
一般服务端不存储token,所以一般基于token的验证机制也是无状态的(而cookie+session有状态).
客户端获取token后可以一般使用cookie/localstage来存储token,后面发请求时再取出来放到Authentication header里面去即可.
token与域无关,不像cookie那样和域绑定,所以基于token的验证机制也就可以实现跨域访问(只要它携带的token通过了验证就允许访问,
但为了防范csrf跨域攻击问题,一般应用还是更多的限制跨域访问的吧).
另外:csrf_token是专门为了防止csrf跨域问题而设置的一种token,只有带有本域发放的csrf_token才能证明该请求是从本域发出的,
而没有该csrf_token的请求则被认为是从其他域发来的,就不允许访问.

简单的说,token机制就是：第一次登陆过后,签发token令牌,以后每次请求都要带着该token令牌,然后只要该token被验证时能够自相印证,
不是伪造的token即可,那么就认为这个token是ok的,就相信它(不考虑窃取的情况,没有办法防窃取!),然后取出其中的用户信息使用...
------------------------------------------------------------------------------------------------------------------------

搞了半天，浏览器端cookie存session_id + 服务端存session查询用用户信息的传统验证方式，改为：
    浏览器端cookie/localstage存token（token是由服务端签发的token令牌=用户验证信息+时间戳等加密后字符）,服务端不再存session而已，
    (貌似本质上还一样，也没感觉安全多少,窃取cookie伪造请求还是不安全[不考虑窃取,只谈伪造的情况...],就是cookie+session --> cookie+token)
    浏览器可以用cookie/localstage存储服务器签发的token,下次请求携带token即可验证;
    但代码里用requests库访问服务器的话,返回的token怎么存储(没有cookie,自行存储?)

cookie是和域名一一对应的,所以凡是基于使用cookie的都会有跨域请求问题,那么使用cookie存储token的为什么没有跨域的问题了呢?
(是因为尽管token的存储是使用cookie的,但请求时是把token取出来放在header里面的??)

经常说的安全问题大多是指防范"cookie伪造",而不是防范cookie窃取?如果真的是被截取窃取的情况,无论那种机制都是无法防范的,不是么...
经常想如果token被人截获了怎么办？其实想想如果真有这么一个人，无论是哪种方式都是无法保证安全的。所以https是必须的，不用考虑这种半途打劫的情况。
    
    
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
(意思就是:tom很容易被伪造成mike,但是加密后的"asdf123dffdfwe2fg33"却不容易被伪造,因为名字信息更不好猜了...)
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
用户认证
当前已经认证的用户信息被保存在每一个请求处理器的 self.current_user 当中， 同时在模板的 current_user 中也是。默认情况下，
current_user 为 None。

要在应用程序实现用户认证的功能，你需要复写请求处理中 get_current_user() 这 个方法，在其中判定当前用户的状态，比如通过 cookie。
下面的例子让用户简单地使用一个 nickname 登陆应用，该登陆信息将被保存到 cookie 中：

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

class MainHandler(BaseHandler):
    def get(self):
        if not self.current_user:
            self.redirect("/login")
            return
        name = tornado.escape.xhtml_escape(self.current_user)
        self.write("Hello, " + name)

class LoginHandler(BaseHandler):
    def get(self):
        self.write('<html><body><form action="/login" method="post">'
                   'Name: <input type="text" name="name">'
                   '<input type="submit" value="Sign in">'
                   '</form></body></html>')

    def post(self):
        self.set_secure_cookie("user", self.get_argument("name"))
        self.redirect("/")

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/login", LoginHandler),
], cookie_secret="61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=")
对于那些必须要求用户登陆的操作，可以使用装饰器 tornado.web.authenticated。 如果一个方法套上了这个装饰器，
但是当前用户并没有登陆的话，页面会被重定向到 login_url（应用配置中的一个选项），上面的例子可以被改写成：

class MainHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        name = tornado.escape.xhtml_escape(self.current_user)
        self.write("Hello, " + name)

settings = {
    "cookie_secret": "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
    "login_url": "/login",
}
application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/login", LoginHandler),
], **settings)
如果你使用 authenticated 装饰器来装饰 post() 方法，那么在用户没有登陆的状态下， 服务器会返回 403 错误。

Tornado 内部集成了对第三方认证形式的支持，比如 Google 的 OAuth 。参阅 auth 模块 的代码文档以了解更多信息。 for more details. 
Checkauth 模块以了解更多的细节。在 Tornado 的源码中有一个 Blog 的例子，你也可以从那里看到 用户认证的方法
（以及如何在 MySQL 数据库中保存用户数据）。

跨站伪造请求的防范
跨站伪造请求(Cross-site request forgery)， 简称为 XSRF，是个性化 Web 应用中常见的一个安全问题。
前面的链接也详细讲述了 XSRF 攻击的实现方式。

当前防范 XSRF 的一种通用的方法，是对每一个用户都记录一个无法预知的 cookie 数据，然后要求所有提交的请求中都必须带有这个 cookie 数据。
如果此数据不匹配 ，那么这个请求就可能是被伪造的。

Tornado 有内建的 XSRF 的防范机制，要使用此机制，你需要在应用配置中加上 xsrf_cookies 设定：

settings = {
    "cookie_secret": "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
    "login_url": "/login",
    "xsrf_cookies": True,
}
application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/login", LoginHandler),
], **settings)
如果设置了 xsrf_cookies，那么 Tornado 的 Web 应用将对所有用户设置一个 _xsrf 的 cookie 值，
如果 POST PUT DELET 请求中没有这 个 cookie 值，那么这个请求会被直接拒绝。如果你开启了这个机制，那么在所有 被提交的表单中，
你都需要加上一个域来提供这个值。你可以通过在模板中使用 专门的函数 xsrf_form_html() 来做到这一点：

<form action="/new_message" method="post">
  {{ xsrf_form_html() }}
  <input type="text" name="message"/>
  <input type="submit" value="Post"/>
</form>
如果你提交的是 AJAX 的 POST 请求，你还是需要在每一个请求中通过脚本添加上 _xsrf 这个值。下面是在 FriendFeed 中的 AJAX 的 POST 请求，
使用了 jQuery 函数来为所有请求组东添加 _xsrf 值：

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

jQuery.postJSON = function(url, args, callback) {
    args._xsrf = getCookie("_xsrf");
    $.ajax({url: url, data: $.param(args), dataType: "text", type: "POST",
        success: function(response) {
        callback(eval("(" + response + ")"));
    }});
};
对于 PUT 和 DELETE 请求（以及不使用将 form 内容作为参数的 POST 请求） 来说，你也可以在 HTTP 头中以 X-XSRFToken 这个参数传递 XSRF token。

如果你需要针对每一个请求处理器定制 XSRF 行为，你可以重写 RequestHandler.check_xsrf_cookie()。例如你需要使用一个不支持 cookie 的 API， 
你可以通过将 check_xsrf_cookie() 函数设空来禁用 XSRF 保护机制。然而如果 你需要同时支持 cookie 和非 cookie 认证方式，
那么只要当前请求是通过 cookie 进行认证的，你就应该对其使用 XSRF 保护机制，这一点至关重要。






CSRF(也叫XSRF)介绍:
攻击通过在授权用户访问的页面中包含链接或者脚本的方式工作。例
如：一个网站用户Bob可能正在浏览聊天论坛，而同时另一个用户Alice也在此论坛中，并且后者刚刚发布了一个具有Bob银行链接的图片消息。
设想一下，Alice编写了一个在Bob的银行站点上进行取款的form提交的链接，并将此链接作为图片src。如果Bob的银行在cookie中保存他的授权信息，
并且此cookie没有过期，那么当Bob的浏览器尝试装载图片时将提交这个取款form和他的cookie，这样在没经Bob同意的情况下便授权了这次事务。

是为了防范CSRF,所以只允许本域的请求, 限制跨域的请求,
而CORS正好相反,是因为有些静态资源等的请求就是需要跨域访问的,所以CORS提供了实现跨域访问的方法...

# username + password login in,
# only allow requests from inside the domain,

# only authenticate username + password in login page once.

为了防范"跨域请求伪造(CSRF),需要使用一个csrf_token来证明请求是从本域发出的:
所以在post等重要的请求的时候，服务器需要验证这个请求是不是从网站自身上发出的。
证明这个的办法是，在页面中放上一个自己才有的随机字符串(csrf_token)，然后请求的时候带上这个token，服务器端进行验证。
这样其他网站不能生成这个token所以也就无解了。

csrf_token是专门用来验证是否是本域的请求的,不允许跨域请求.
而普通的token一般是放在一个叫做Authentication的header中的,是专门用来做登录验证的.


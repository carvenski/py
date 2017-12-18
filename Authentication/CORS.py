

CSRF是只允许本域的请求, 限制跨域的请求,
而CORS正好相反,是因为有些静态资源等的请求就是需要跨域访问的,所以CORS提供了实现跨域访问的方法...

# 例: go写的CORS,其实就是打开某些域名,允许它们访问:
e.Use(middleware.CORSWithConfig(middleware.CORSConfig{
		AllowOrigins: []string{"https://labstack.com", "https://labstack.net"},
		AllowMethods: []string{echo.GET, echo.PUT, echo.POST, echo.DELETE},
	}))


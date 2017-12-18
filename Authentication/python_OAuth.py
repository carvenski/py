

OAuth就是使用第三方来做 发放/认证token的事情而已...
# use OAuth module to add third-party authentication mechanism in python web.


# username+password + token :
# many requests act like a transaction:
  # first request using username+password,
  # then, else requests in same transaction using token within expired time.

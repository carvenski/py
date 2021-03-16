## pacman里面设置使用wget使用http代理：
 ```sh
 /usr/bin/wget -k 
 -e "http_proxy=http://10.191.113.100:8002" 
 -e "https_proxy=http://10.191.113.100:8002" 
 --proxy-user=yangxing-007
 --proxy-password=xxx
 -c --passive-ftp -c %u
```


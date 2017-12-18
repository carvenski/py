
cd /root/.shdowsocks 

#download shadowsocks-local-linux64 from crolax.xyz
nohup ./shadowsocks-local-linux64 -c config.json  & 

#set proxy in yandex browser:
nohup yandex-browser-beta --no-sandbox  --proxy-server="socks5://127.0.0.1:1080"  & 

## set proxy in terminal:
#install polipo
#edit /etc/polipo/config 

# logSyslog = true
# logFile = /var/log/polipo/polipo.log
# proxyAddress = "0.0.0.0"
# socksParentProxy = "127.0.0.1:1080"
# socksProxyType = socks5
# chunkHighMark = 50331648
# objectHighMark = 16384
# serverMaxSlots = 64
# serverSlots = 16
# serverSlots1 = 32

nohup polipo -c /etc/polipo/config & 

#set http_proxy/https_proxy
export http_proxy="http://127.0.0.1:8123/"
export https_proxy="http://127.0.0.1:8123/" 

cd -

echo "======set proxy ok======="


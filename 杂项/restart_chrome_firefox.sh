#!/bin/sh

echo '===============restart yandex=================';
ps -ef | grep "yandex-browser-beta --no-sandbox --proxy-server=10.0.125.213:17777" | awk 'NR==1{print $2}' | xargs kill -9;
ps -ef | grep "yandex-browser-beta --no-sandbox --proxy-server=10.0.125.213:17777" | awk 'NR==2{print $2}' | xargs kill -9; sleep 1;
(cd /tmp; nohup yandex-browser  --no-sandbox --proxy-server="10.0.125.213:17777"  & ) 

sleep 5;
echo '===============restart chrome=================';
ps -ef | grep '/opt/google/chrome/chrome --no-sandbox' | awk 'NR==1{print $2}' | xargs kill -9;
ps -ef | grep '/opt/google/chrome/chrome --no-sandbox' | awk 'NR==2{print $2}' | xargs kill -9; sleep 1; 
(cd /tmp; nohup google-chrome --no-sandbox &) 

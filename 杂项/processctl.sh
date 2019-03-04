#!/bin/sh

if [ "$1"x = "start"x ]; then
    nohup  python main.py  >  /dev/null  2>&1  &
    sleep 1
    pid=$(ps -ef | grep 'python main.py' | grep -v 'grep' | awk '{print $2}' | xargs echo)
    echo "starting consumer pid:" $pid
    echo "start ok ..."
elif [ "$1"x = "stop"x ]; then
    pid=$(ps -ef | grep 'python main.py' | grep -v 'grep' | awk '{print $2}' | xargs echo)
    echo "killing consumer pid:" $pid
    ps -ef | grep 'python main.py' | grep -v 'grep' | awk '{print $2}' | xargs kill -9
    echo "stop ok ..."
elif [ "$1"x = "restart"x ]; then
    pid=$(ps -ef | grep 'python main.py' | grep -v 'grep' | awk '{print $2}' | xargs echo)
    echo "killing running consumer pid:" $pid
    ps -ef | grep 'python main.py' | grep -v 'grep' | awk '{print $2}' | xargs kill -9
    nohup  python main.py  >  /dev/null  2>&1  &
    sleep 1
    pid=$(ps -ef | grep 'python main.py' | grep -v 'grep' | awk '{print $2}' | xargs echo)
    echo "restarting new consumer pid:" $pid    
    echo "restart ok ..."
elif [ "$1"x = "check"x ]; then
    pid=$(ps -ef | grep 'python main.py' | grep -v 'grep' | awk '{print $2}' | xargs echo)

    if [ -z "$pid" ]; then 
        echo "consumer not running !"
    elif [ -n "$pid" ]; then 
        echo "found running consumer pid:" $pid
    fi
    
    echo "check ok ..."   
else    
    echo "command must in start|stop|restart|check !!!!"
    echo "your command is: $1"
fi




#!/usr/bin/expect -f

spawn ssh myang@post-processor4.internal.ng.movoto.net
expect "password: "
send "001Company"
interact




#!/usr/bin/expect -f

spawn ssh -p 30022 gs_baoqijian@183.192.161.38

# expect "yes"
# send "yes\r" 

expect "password"
send "3edc#EDC\r" 

expect "SAG"
send "1\r"

expect "login"
send "root\r"

expect "password"
send "1qaz!QAZ\r"

expect "#"
send "ssh 10.200.71.240\r"

expect "password"
send "1qaz!QAZ\r"

expect "root"
send "ssh 10.200.71.170\r"

expect "root"
send "tmux a -t  portal\r"

interact




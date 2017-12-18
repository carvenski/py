#!/usr/bin/expect -f

spawn ssh myang@post-processor4.internal.ng.movoto.net
expect "password: "
send "001Company"
interact



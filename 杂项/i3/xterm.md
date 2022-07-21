## arco linux vm中 xterm需要设置下复制功能
#vim .Xresources       
xterm*selectToClipboard: true       
#xrdb -merge ~/.Xresources       
#现在ctrl-c即可复制了              

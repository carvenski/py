## vbox打开vmdk磁盘文件
```
vbox可以直接打开vmdk格式的磁盘文件,直接打开虚拟机!!
但是要注意,磁盘控制器要选择对应的SCSI控制器/IDE控制器,不能是SATA控制器!!
=> 保证vbox里磁盘控制器要和vmware里使用的一致就行了,因为这个会影响到怎么连接磁盘.
系统+用户的所有文件数据都在磁盘里,vmdk文件才是虚拟机的核心.
```

## vbox安装增强功能
```
1.在vbox里选择安装增强功能,会挂载增强功能的iso到arch虚拟机,
2.mkdir /mnt/cdrom && sudo mount /dev/cdrom /mnt/cdrom
3.sudo /mnt/cdrom/VboxLinuxAddtions.sh (编译增强功能内核模块)
4.umount /mnt/cdrom
5.reboot (之后VBoxService和VBoxClient会自动启动,提供增强功能)
```

## vbox共享目录
```
1.在vbox里面设置一个共享目录
2.arch里面 sudo gpasswd -a michael vboxsf (把用户加入vboxsf组)
```

## vbox键盘独占问题
```
vbox在安装了增强功能之后,分辨率可以自动缩放,鼠标也可以自动切换,
但是: 键盘不能自动切换!! 要么独占要么不占...
键盘快捷键输入不能自动跟随鼠标是否移到虚拟机窗口内外部而自动的切换输入进虚拟机还是外面win10.
(而vmware是可以自动跟随鼠标位置切换键盘的快捷键的输入的)
```

> 目前经验: 还是vmware比vbox更好用...    






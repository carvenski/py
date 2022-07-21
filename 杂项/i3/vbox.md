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

## vbox + arco 搭配
> arcolinux这个发行版开箱即用,推荐vbox + arcolinux虚拟机组合.      
> 目前经验 arcolinux + vbox 很完美!       
*arco开机只占用200M 太强了。居然如此优秀。*


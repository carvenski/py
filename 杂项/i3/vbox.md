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









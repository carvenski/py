## arch pacman 安装旧版本的包/降级安装
```
由于arch系统并不经常更新,而pacman每次却自动安装最新版本的包。。。
导致安装最新版本的包经常会遇到依赖的某个lib库版本过低问题(比如glibc),此时只能安装旧版本的包：
arch有个专门的仓库来存放那些旧版本的包，去这里找就行了：
https://archive.org/download/archlinux_pkg_emacs
https://archive.archlinux.org/packages/l/llvm-libs

arch降级包可以参考wiki:
https://wiki.archlinux.org/index.php/Downgrading_packages_(简体中文)
https://wiki.archlinux.org/index.php/Arch_Linux_Archive#How_to_downgrade_one_package

下载好了旧版本的包后， pacman -U 包  即可安装.
```

## archlinux安装部署各种环境 最佳实践
如果在archlinux上遇到安装各种lib库文件问题时,     
最好的方式应该是直接使用docker容器 - 专门解决这种库文件安装依赖版本问题的           
而不是非得在arch本地安装 - 浪费时间而已 - 坑过多次了 - 使用docker来提高安装效率!!!    



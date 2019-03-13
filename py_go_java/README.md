
# python + go + java
## 记录py/go/java 这3门语言中相通的东西,尽量形成统一的思路和写法

---------

#### 项目目录结构,包结构
```
项目统一使用以下的目录结构组织代码:
ProjectRootDir/
    src/
        rootpackage/
             ...(目录,文件对应包结构的导入路径)
        main文件(main.py/main.go/main.java,其中import的根包就是rootpackage)
    README.md
    .gitignore
    ...

    之所以这么组织项目代码结构的原因就是:
    go和java都有个src目录专门放代码,
    java的gradle项目结构默认就是带有src目录的.
    go编译时会搜索GOPATH路径下的src目录里的包(import的包的根路径都是从这里入口的),
    所以需要把ProjectRootDir目录加入GOPATH并且它里面要有个src目录,这样编译main时就能搜索到导入路径中的rootpackage包.
    那么py也统一加个src目录.
    
    统一py/go/java的包声明写法(以java的为准,OOP写法):
    一个文件夹对应一个包,该文件夹里的所有文件均声明为这个包,
    然后文件夹里面的每个文件里放一个Class/Struct/public Class(当然也可以放包级别的变量,函数),
    然后使用的地方都是import 包名.类名
```


#### py/go/java的代码都用OOP思路来写
```
统一采用OOP面向对象的思路来设计/编写代码,先拆分系统成功能模块,再在各个模块中拆分出各个功能对象,
采用面向对象的思路,设计出各个对象/组件!最后再组合这些组件/对象来实现整体的功能.
原因也很简单: 遵照OOP面向对象的写法能够轻松把py/go/java的代码风格统一起来 => 代码里一眼望去全是类-_-

go中的结构体/py和java中的class, 面向对象写法很重要!它是统一py/go/java这3门语言的代码风格的关键 !!
```

####

####









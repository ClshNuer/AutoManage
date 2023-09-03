# Python Flask

<!--last modify: 20230814-->



```
# flask 依赖两个外部库，jinja2 模板引擎和werkzeug WSGI工具集
# python 沙盒环境逃逸绕过注册方式，进而调用python 内置对象

# http://$ip:5000/?name={{1+1}}

# __bases__ 以元组返回一个类的所有父类构成的元组
# __mro__ 以元组的形式返回类的继承关系
# __class__ 返回实例所属的类
# __globals__ 以字典的形式返回当前位置的全部全局变量
# __subclasses__ 以列表的形式返回类的所有子类
# __builtins__ 内建函数，可直接运行一些内建函数，如int(),list()
```


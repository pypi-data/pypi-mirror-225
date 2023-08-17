#-*- coding:utf-8 -*-
__all__ = ['utils'] #针对模块公开接口的一种约定，以提供了”白名单“的形式暴露接口。
                    #如果定义了__all__，
                    #使用from xxx import *导入该文件时，只会导入 __all__ 列出的成员，可以其他成员都被排除在外。

__version_info = (0, 0, 3, 230817)
__version__ = ".".join([str(x) for x in __version_info])

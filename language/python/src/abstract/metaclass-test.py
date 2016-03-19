#!/usr/bin/python
#coding:utf8


class _DefaultMetaClass(type):
    """_DefaultMetaClass:用于创建Man类
        主要用途：创建API，按照我的意图构建类的主体框架
    """
    tellSomething = "wa ha ha."
    def __init__(cls, name, base, attrd):
        """__init__

        :param name:
        :param base:
        :param attrd:
        """
        super(_DefaultMetaClass, cls).__init__(name, base, attrd)
        if "getName" not in attrd:
            raise TypeError("Not found getName functions.")

        if "getAge" not in attrd:
            raise TypeError("Not found getAge functions.")


class Man(object):
    __metaclass__ = _DefaultMetaClass
    authorName = "unlessbamboo@gmail.com"
    age = 26
    def __init__(self, dct):
        """__init__

        :param dct:
        """
        if "name" in dct:
            self.authorName = dct['name']

        if 'age' in dct:
            self.age = dct['age']

        if 'desc' not in dct:
            raise Exception("Not found desc.")
        else:
            self.desc = dct['desc']

    def getName(self):
        """getName"""
        return self.authorName

    def getAge(self):
        """getAge"""
        return self.age

    def display(self):
        """display"""
        print 'Name:', self.authorName
        print 'Age:', self.age
        print 'Description:', self.desc
        # 用于验证元类和其他类并非继承关系
        # 但是可以通过__new__来创建新的属性
        if hasattr(self, 'tellSomething'):
            print 'Tell:', self.tellSomething


if __name__ == '__main__':
    mobj = Man({'desc': 'I am a cool children.'})
    mobj.display()

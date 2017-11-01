#
# def foo(x):
#     return x*x
#
# r=map(foo,[1,2,3,4,5])
# print(list(r))
# def test_lamdba2(x=0):
#     return lambda y: x + y
# obj=test_lamdba2(3)
# print(obj())
# f=lambda x,y,z:x+y+z
# print(f(1,2,3))

from functools import reduce

# def add(x,y):
#     return x+y
# k=reduce(add,[1,3,5,7,9])
# print(k)
# class Singleton(object):
#     def __new__(cls, *args, **kwargs):
#         print(cls)
#         if not hasattr(cls,'_inst'):
#             cls._inst = super(Singleton,cls).__new__(cls)
#             print(cls._inst)
#         return cls._inst
#
# if __name__ == '__main__':
#     class A(Singleton):
#         def __init__(self,s):
#             self.s=s
#
#
#     a=A('apple')
#     # b=A('banana')
#     print(a.s)
#     # print(b.s)



# class Borg(object):
#     stared={}
#     def __new__(cls, *args, **kwargs):
#         obj=super(Borg,cls).__new__(cls)
#         obj.__dict__=cls.stared
#         return obj
# if __name__ == '__main__':
#     class Example(Borg):
#         pass
#     a=Example()
#     print(a)
#
#
#
# class Singleton(type):
#     def __init__(self,name,bases,class_dict):
#         super(Singleton,self).__init__(name,bases,class_dict)
#         self._instance=None
#     def __call__(self, *args, **kwargs):
#         if self._instance is None:
#             self._instance=super(Singleton,self).__call__(*args, **kwargs)
#             print('===',self._instance)
#         return self._instance
#
# if __name__ == '__main__':
#     class A(object):
#         __metaclass=Singleton
#
#     a=A()
#     print(a)



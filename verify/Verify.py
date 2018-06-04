import re
from unittest import TestCase


def assertEqual(a, b):
    print("-------------------待验证的值-------------------")
    print(a)
    print("-------------------期望的值-------------------")
    print(b)
    tc = TestCase()
    tc.assertEqual(a, b)
    print("-------------------验证结束-------------------")


def assertIsDigit(a):
    print("-------------------待验证的值-------------------")
    print(a)
    print("-------------------验证结果-------------------")
    pattern = r'[0-9]+'
    if (re.match(pattern, a)):
        print(a + " 是数字，符合期望")
    else:
        raise ValueError(a + "不是数字，不符合预期")
    print("-------------------验证结束-------------------")


def assertEqualInt(a, b):
    print("-------------------待验证的值-------------------")
    print(a)
    print("-------------------期望的值-------------------")
    print(b)
    tc = TestCase()
    a = int(a)
    b = int(b)
    tc.assertEqual(a, b)
    print("-------------------验证结束-------------------")


def assertContain(a, b):
    print("-------------------待验证的值-------------------")
    print(a)
    print("-------------------期望的值-------------------")
    print(b)
    if b in a:
        print("[%s] 包含 [%s]" % (a, b))
    else:
        raise ValueError("[%s] 不包含 [%s]" % (a, b))
    print("-------------------验证结束-------------------")

def assertMatchReg(a,b):
    print("-------------------待验证的值-------------------")
    a=str(a)
    print(a)
    print("-------------------验证结果-------------------")
    b= r'%s'%(b)
    if (re.match(b, a)):
        print(a+" 匹配正则表达式 "+b)
    else:
        raise ValueError(a+" 不匹配正则表达式 "+b)
    print("-------------------验证结束-------------------")
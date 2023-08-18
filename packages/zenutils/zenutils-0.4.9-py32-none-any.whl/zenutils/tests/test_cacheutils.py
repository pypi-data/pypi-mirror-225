#!/usr/bin/env python
# -*- coding: utf8 -*-
from __future__ import (
    absolute_import,
    division,
    generators,
    nested_scopes,
    print_function,
    unicode_literals,
    with_statement,
)
from zenutils.sixutils import *
from zenutils import cacheutils

import random
import unittest

_test_cacheutils_counter = 0


class Object(object):
    pass


class TestCacheUtils(unittest.TestCase):
    def test01(self):
        a = Object()

        def hi():
            return "hi"

        assert cacheutils.get_cached_value(a, "hi", hi) == "hi"

    def test02(self):
        global _test_cacheutils_counter
        _test_cacheutils_counter = 0
        a = Object()

        def counter():
            global _test_cacheutils_counter
            _test_cacheutils_counter += 1
            return _test_cacheutils_counter

        assert cacheutils.get_cached_value(a, "counter", counter) == 1
        assert cacheutils.get_cached_value(a, "counter", counter) == 1

    def test03(self):
        a = Object()

        @cacheutils.cache(a, "_num")
        def getNum():
            return random.randint(1, 10)

        v1 = getNum()
        v2 = getNum()
        v3 = getNum()
        assert v1
        assert v1 == v2 == v3

    def test04(self):
        @cacheutils.cache(None, "_num")
        def getNum():
            return random.randint(1, 10)

        a = Object()
        v1 = getNum(a)
        v2 = getNum(a)
        v3 = getNum(a)
        assert v1
        assert v1 == v2 == v3

    def test5(self):
        @cacheutils.cache()
        def getNum():
            return random.randint(1, 10)

        a = Object()
        v1 = getNum(a, "_num")
        v2 = getNum(a, "_num")
        v3 = getNum(a, "_num")
        assert v1
        assert v1 == v2 == v3

    def test6(self):
        """ReqIdCache重复性检验的测试。"""
        cachedb = cacheutils.ReqIdCache(10)
        assert cachedb.exists(1) is False
        assert cachedb.exists("2") is False
        # 插入1后
        cachedb.add("1")
        # 判断1存在
        assert cachedb.exists("1")
        # 插入1000个值，将已插入的1溢出
        for inum in range(100):
            cachedb.add(inum)
        # 重新判断发现1已经不存在
        assert cachedb.exists("1") is False

    def test7(self):
        """simple_cache注解函数的测试。"""

        @cacheutils.simple_cache
        def say_hi(name):
            """say hi to someone."""
            return "hi, {0}.".format(name)

        res1 = say_hi("n1")
        res2 = say_hi("n2")
        res3 = say_hi("n3")
        assert res1 == "hi, n1."
        assert res1 == res2
        assert res1 == res3
        assert say_hi.__doc__ == "say hi to someone."

    def test8(self):
        """simple_cache注解类方法的测试。"""

        class A:
            @cacheutils.simple_cache
            def say_hi(self, name):
                """just say_hi."""
                return "hello, {0}.".format(name)

        a = A()
        res1 = a.say_hi("n1")
        res2 = a.say_hi("n2")
        res3 = a.say_hi("n3")
        assert res1 == "hello, n1."
        assert res1 == res2
        assert res1 == res3
        assert a.say_hi.__doc__ == "just say_hi."

    def test9(self):
        """simple_cache无参数的测试"""

        @cacheutils.simple_cache
        def say_hi():
            return "hi"

        res1 = say_hi()
        res2 = say_hi()
        res3 = say_hi()
        assert res1 == "hi"
        assert res1 == res2
        assert res1 == res3

    def test10(self):
        """同一个函数，使用别名或引用后，仍然视为同一个函数。使用相同的缓存键。"""

        def hi():
            return "hi"

        hia = hi
        hib = hi

        hiaa = cacheutils.simple_cache(hia)
        hibb = cacheutils.simple_cache(hib)

        res1 = hiaa()
        res2 = hibb()
        assert res1 == res2

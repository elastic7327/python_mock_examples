#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import unittest

import mock
import pytest

from fots import abc_urandom, my_random


def simple_urandom(length):
    return 'f' * length


"""
The side_effect keyword argument simply allows you to
replace an entire function with another. Please also notice that the decorator
now adds an additional argument to the function that it wraps which
I’ve called urandom_function.
We’ll discuss some of the things you can do with this later on.
The code above also works if we were importing a
function that used os.urandom too.
"""


class TestRandomPartOne(unittest.TestCase):
    # 이런식으로 사이드 이팩트로 가져온다는것은
    # 함수를 위에 있는 것으로 가져오겠다는 뜻 입니다^^
    @mock.patch('os.urandom', side_effect=simple_urandom)
    def test_urandom(self, urandom_function):
        assert os.urandom(5) == 'fffff'


"""
OK, but what if we imported the urandom function using a from statement?
Well this is a special case where you can use __main__ to mock the function:
"""


class TestRandomPartTwo(unittest.TestCase):
    @pytest.mark.skip(reason="skip it for a moment")
    @mock.patch('__main__.urandom', side_effect=simple_urandom)
    def test_urandom(self, urandom_function):
        assert os.urandom(5) == 'fffff'


# 이런식으로도 가능합니다.
class TestRandomPartThree(unittest.TestCase):
    """
    At this point, we know how to mock the various
    types of function calls that may occur.
    If you would like to perform a much simpler mock and
    just replace the return
    value of the function with a simple expression, you may do this:
    """
    # 이런식으로도 가능합니다.
    @mock.patch('fots.urandom', side_effect=simple_urandom)
    def test_abc_urandom(self, abc_urandom_function):
        assert abc_urandom(5) == 'abcfffff'


class TestRandomPartFour(unittest.TestCase):
    """
    If you would like to perform a much simpler mock and just replace
    the return value of the function with a simple expression, you may do this:
    """
    # 그러니까 urandom 이라는 모듈은 무조건  HelloWOrldHolaHola를
    # 리턴한다. fots urandom 이란애는 그 값을 리턴한다.
    # 파라미터 오타 정말 조심해야한다.b 예를 들어서
    # return_value ( o )  / return_values ( x )
    @mock.patch('fots.urandom', return_value='HelloWorldHola')
    def test_abc_urandom(self, abc_urandom_function):
        # abc_urandom 쪽에서는 abcHelloWorld 가 나옵니다.
        assert abc_urandom(5) == 'abcHelloWorldHola'


class TestRandomPartFive(unittest.TestCase):
    """
    For more granular control over when mocking should
    take place within a test case,
    you may use a with statement instead of a decorator as shown below.
    """
    @pytest.mark.skip(reason="skip it for a moment")
    def test_mocking_without_decoration(self):
        # 인코딩에러 발생함 . . .
        # encofing error occcured
        with mock.patch('os.urandom', return_value='pumpkins') as abc_urandom_function:
            assert abc_urandom(5) == 'abcpumpkins'


class TestRandomPartSix(unittest.TestCase):
    @pytest.mark.skip(reason="skip it for a moment")
    @mock.patch('fots.urandom')
    def test_abc_urandom(self, urandom_function):
        urandom_function.return_value == 'awesome'
        assert my_random(5) == 'awesome'
        # 아래와 같은 식으로 리턴값을 조작 할 수있습니다.
        urandom_function.return_value == 'baddass daniel'
        assert my_random(5) == 'baddass daniel'
        urandom_function.side_effect = (
                lambda l: 'f' * l
        )
        assert my_random(5) == 'fffff'


class TestRandomPartSeven(unittest.TestCase):
    """
    사실 가장 필요한 방법은 이 방법 인 것 같습니다.
    그냥 리턴값 따로 명시를 해놓고...
    """
    @mock.patch('os.urandom', return_value='pumpkins')
    def test_abc_urandom(self, urandom_function):
        # The mock function hasn't been called yet
        assert not urandom_function.called
        # Here we call the mock function twice and assert that it has been
        # called and the number of times called is 2
        assert os.urandom(5) == 'pumpkins'
        assert os.urandom(5) == 'pumpkins'
        assert urandom_function.called
        assert urandom_function.call_count == 2

        # Finally, we can reset all function call statistics as though the
        # mock function had never been used
        urandom_function.reset_mock()
        assert not urandom_function.called
        assert urandom_function.call_count == 0

"""
    This is tutorial for pytest
    Default recognization rules for pytest:
        test files: all files with names started with "test_" or "_test"
        cases: class name started with "Test" in test files
        testcases:测试类中每个test开头的方法就是一条测试用例，测试文件中每个test开头的函数也是一条测试用例，

    Key notes:
        pytest.main执行的参数传递
            pytest.main(['-v','-s'])
        指定执行的测试目录
            pytest testcase/
        指定执行的测试文件
            pytest testcase/test_demo1.py
        指定执行的测试类
            pytest testcase/test_demo1.py::TestClass::test_method

    Args:
        -v : display the detailed params
        -s : display output of test files
"""


# Test cases in function
def test_demo():
    assert 100 == 100


# Test cases in class
class TestDemo:
    def test_demo1(self):
        assert 11 == 11

    def test_demo2(self):
        assert 11 == 22


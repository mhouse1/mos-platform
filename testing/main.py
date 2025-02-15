'''

@requirements
    # install pytest and optional plugins
    pip install pytest
    pip install pytest-html
    pip install pytest-order
    pip install pytest junit-xml
'''
import pytest
import test_parameters

@pytest.mark.order(1)
@pytest.mark.isTestFixtureOk
@pytest.mark.timeout(60) #timeout in seconds
def test_isTestFixtureOk():
    '''
    implement a pretest to check if system is ok before running tests

    usage: pytest .\main.py -s -vv -m isTestFixtureOk --html=..\test_output\report.html
    '''
    # import pre_test
    # pre_test.pre_test_sequence()
    pass

@pytest.mark.order(2)
@pytest.mark.systemUpdate
def test_system_update(sys_update_file):
    '''
    it may be more useful to run this as a separate script, see pre_test.py

    example: pytest main.py --vv --html=..\test_output\report.html --enable_system_update --sys_update_file

        you can setup fixture items such as sys_update_file then pass it to the test but i'd recommend
    using test_parameters.py instead and in the conftest.py file update the test_parameter during pytest_sessionstart
    this makes it easier to maintain and use test_parameters
    '''
    # import pre_test
    # pre_test.pre_test_sequence()
    pass


@pytest.mark.xfail(reason=" forced fail via pytest.xfail")
def test_fail_example():
    '''Mark as an expected fail, and also include a message visible intest report'''
    pytest.xfail(" this is an expected fail because we havent installed our new hardware")


def test_unordered_test():
    '''
    Since we did not specify a @pytest.mark.order this test will run after all the tests with
    test orders specified
    '''
    pass

@pytest.mark.my_super_special_test
def test_specific_test():
    '''
    running pytest with -m my_super_special_test means only tests marked 
    with my_super_special_test will run
    '''
    print('$$$$$$$$$$$$$$$$ running my_super_special_test $$$$$$$$$$$$$$$$$$$ ')
    pass


@pytest.mark.order(6)
@pytest.mark.my_special_test_that_fail
def test_example_fail():
    '''
    use assert to fail and write a message visible in report
    '''

    assert False, "this is what a test failure looks like when using assert false"

@pytest.mark.order(7)
@pytest.mark.my_special_test_that_pass
def test_example_pass():
    '''
    use assert to pass a test and write a message visible in report
    '''

    assert True, "this is what a test pass looks like when using assert True"

@pytest.fixture
def test_example_pytest():
    '''
    indicate something wrong with fixture
    '''
    pytest.fail('something is wrong with the fixture')


@pytest.mark.order(3)
def test_example_order():
    '''
    force this test to run as test number3, the order the test, because we use order()
    it bypasses the order this function was added to this file.
    '''
    print('############# this test should run as the third test')

@pytest.fixture
def test_raise_exception():
    '''
    raise an exception to indicate something wrong with the fixture
    '''
    raise Exception('Ooops something worng with fixture?')

@pytest.mark.skip(reason=" skipping this test while an issue is being investigated")
def test_demo_test_skip_with_reason():
    '''
    Demo pytest skip test feature
    '''
    print(' if you are seeing this, this test is not being skipped')
    assert False, "pytest should skip this test"

@pytest.mark.skipif(test_parameters.is_windows_host, reason="this test can only run on linunx systems")
def test_demo_skipif_feature():
    '''
    demo the skipif feature while also testing if the test is running in windows
    '''
    if test_parameters.is_windows_host:
        assert False, "this test should have been skipped becauase skipif is configure to skipif is_windows_host"

def test_print_test_name():
    '''
    Demo's how to get the test name while test is running
    '''
    import inspect
    test_name = inspect.currentframe.f_code.co_name
    print(f'Running test: {test_name}')


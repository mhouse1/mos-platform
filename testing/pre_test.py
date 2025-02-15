'''
@date 1/1/25
'''
import pytest

import test_parameters

@pytest.mark.isTestFixtureOk
def test_pre_test():
    '''
    make sure the host is setup correctly
    dont bother running tests if this test fails
    
    example: python -m pytest pre_test.py -s -vv -m isTestFixtureOk
    '''

    print(f'Automated Test Version: {test_parameters.automated_test_version}')

    # test if these libraries are available
    import paramiko, serial, subprocess

    # test tool versions
    import sys
    # check python version
    if not sys.version_info[0] == 3:
        assert False, "python3 required but not detected"
    




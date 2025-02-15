'''
This test is required by pytest, it defines some pytest settings, start, end and configuration
'''
import pytest, warnings
import test_parameters

def pytest_sessionstart(session):
    ''' This function runs at the start of pytest session'''
    print(f'========== Pytest starting ===========')

    # take the command line args and update the test_parameters
    test_parameters.my_serial_port = session.config.getoption("myserialport")

    test_parameters.test_marker_used = session.config.getoption('-m')

    # for now we ignore the previous line and overwrite the serial port if it has a known serial number
    try:
        import usb_test
        known_hardware = usb_test.assign_known_hardware()
        if 'MYHARDWAREENAME' in known_hardware.keys():
            test_parameters.my_serial_port = known_hardware['MYHARDWARENAME']
    except Exception as e:
        warnings.warn('unable to auto assign serial port using serialnumbers')
        warnings.warn(str(e))

def pytest_collection_modifyingitems(config, items):
    '''
    This runs before any tests, it adjusts markers based on commandline options,
    this function runs after pytest_sessionstart
    '''

    if config.getoption('--ignore_test_blockers') == 'true':
        test_parameters.ignore_blockers = True

    # Demo: modifying test suite by adding a marker
    # skip_update = pytest.mark.skip(reason = "you did not specify --enable_sys_update in commandline when invoking test")
    # for item in items:
    #     if "systemUpdate" in item.keywards:
    #         item.add_marker(skip_update)


def pytest_addoption(parser):
    '''
    Define custom pytest commandline parameters
    '''
    print('='*30, f'Running Automated Test Version: {test_parameters.automated_test_version}')

    parser.addoption(
        "--myserialport", action="store", default=test_parameters.my_serial_port, help= "serial port name to use"
    )

    parser.addoption(
        "--ignore_test_blockers", action="store", default=False, help= "allows ignoring test blockers"
    )


############## test fixtures
@pytest.fixture(scope="module")
def my_serial_port(pytestconfig):
    test_parameters.my_serial_port = pytestconfig.getoption("my_serial_port")
    return test_parameters.my_serial_port

##################################

@pytest.fixture(autouse=True)
def setup_test():
    '''
    This runs at the beginning of any tests
    '''

    # exit early if a test blocker failed
    if test_parameters.blocker_failed:
        pytest.exit("A blocker failed, exiting early")

def increment_attempts(attempts_made):
    '''
    Used to track tests that we run in multiple attempts
    '''
    if attempts_made == None:
        attemps_made =1
    else: 
        attempts_made += 1
    return attempts_made

def pytest_sessionfinish(session):
    '''Runs once at the end of a pytest session'''
    import test_parameters
    print('\n pytest session finished ... cleaning up')
    # if test_parameters.some_process_is_running:
    #   quit_process()

    pytest_status = 'PASS' if session.testsfailed == 0 else 'FAILED'
    print(f'---------------- pytest session info ------------------')
    print(f'Pytest current session: {pytest_status}')
    print(f'Pytest marker {test_parameters.test_marker_used}')

    # check test marker used and update the attempts made so we can report
    # on how many attempts it took for a test to pass
    # if test_parameters.test_marker_used == 'systemupdate':
    #     attempts = metrics_get_value('sysupdateAttempts')
    #     attempts = increment_attempts(attempts)
    #     new_metrics = {'updateattempts': attempts}
    #     metrics_add_to(new_metrics)

    # try:
    #     metrics_print()
    #     import shutil, os
    #     shutil.copy(test_parameters.test_metrics_json, test_parameters.test_metrics_to_be_published)
    # except Exception as e:
    #     warnings.warn("metrics not supported did you run pre-test marker to initialize metrics file?")
    #     warnings.warn(str(e)

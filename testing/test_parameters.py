'''
I like to use a test_parameters file so all test parameters are in one place
it also allows us to easily use it during tests

'''
import os,sys,datetime, socket, time
this_script_location = os.path.dirname(os.path.realpath(__file__))
parent_folder = os.path.dirname(os.path.dirname(this_script_location))

# dont forget to also update the CHANGELOG.md file so we can track chages to the test suite
automated_test_version = '0.0.1'
test_marker_used = ''
time_date = datetime.date.today()
time_now = f"{datetime.datetime.now()}"

################ define test fixture default parameters
# for serial ports linux and windows have different syntax
# for linux to show serial ports: ls /dev/ttyUSB*
# for windows use device manager
# or just run the python usb_test.py script
if sys.platform == 'win32':
    # see https://github.com/mhouse1/mechsoftronic/commit/cc25d871a605fe6b890826714d7e0c88f4d31062
    is_windows_host = True
    my_serial_port = 'COM3'
else:
    is_windows_host = False
    my_serial_port = '/dev/ttyUSB0'

# it may be useful to know the hostname to determine which machine this test is running on
hostname = socket.gethostname()

# rather than keep using time.sleep I recommend defining our own.
def wait(seconds = 60, why =""):
    '''
    wait and print status so we know something is happening
    '''
    timeout = time.time() + seconds
    while time.time() < timeout:
        print(why,f"; waited {round(abs(timeout - seconds - time.time()),2) } of {seconds} seconds")
        time.sleep(5)

############## Automated test runtime parameters
# in some tests we might want to exit test suite if a test blocker is present
# i.e. maybe the test needs internet but it detected no internet, exit early so we dont waste time
# running tests we know will fail.
ignore_blockers = False
active_ssh_connections = 0

if __name__ == '__main__':
    print(f'is_windows_host {is_windows_host}')
    print(f'parent folder holding this script: {parent_folder}')
    print(f'time today: {time_date}')
    print(f'time now: {time_now}')
    wait(10, "testing wait function")
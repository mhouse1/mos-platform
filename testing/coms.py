'''
@date 1/1/25

@brief      tools for communication via ssh, etc
'''
import paramiko, sys, os, time
from scp import SCPClient
import serial
import test_parameters

def sshCreate(hostname, port, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.MissingHostKeyPolicy())
    client.connect(hostname,port,username,password, timeout = 60.0)

    # keep track of how many clients are active, TODO warn if more than 1?
    test_parameters.active_ssh_connections += 1
    print(f'total active ssh clients = {test_parameters.active_ssh_connections}')
    return client


def sshFree(ssh = None):
    if ssh:
        if test_parameters.active_ssh_connections >0:
            ssh.close()
            test_parameters.active_ssh_connections -= 1
        # else: warnings.warn('more than 1 ssh connection is active')

def sshProgress(filename,size,sent):
    '''callback function used by sshUPload to show ssh scp progress'''
    percent = (float(sent)/float(size))*100
    if percent.is_integer():
        sys.stdout.write("%s\'s progress: %.2f%%  \r" % (filename,percent))

def sshUpload(ssh, file_location, file_destination):
    '''Uploads a file using the ssh connection using SCP
    where file_location and file_destination is full file path /filepath/file.txt'''
    try:
        scp = SCPClient(ssh.get_transport(), progress = sshProgress, socket_timeout = 30.0)
        scp.put(file_location, file_destination)
        scp.close()
    except:
        print(f'ssh upload filed to upload: {file_location} to {file_destination}')
    else:
        print(f' ssh upload successful to: {file_destination}')

def sshCommand(ssh,cmd,timeout= 60):
    stdin, _stdout, _stderr = ssh.exec_command(cmd,timeout=timeout) #Non-blocking call
    output = _stdout.read().decode()
    #print(f'SSH COMMAND OUTPUT: {output}')
    return output

def sshCommandWait(ssh,cmd,timeout=60):
    '''
    execute ssh command and wait until command finishes
    this may be useful for a command that takes more time to finish
    '''
    stdin, _stdout, _stderr = ssh.exec_command(cmd,timeout=timeout) #Non-blocking call
    exit_code = _stdout.channel.recv_exit_status()
    if exit_code == 0:
        print(f'finished ssh command: {cmd}')
    else:
        assert False, f'ssh command finished with error {exit_code} while running command: {cmd}'

def check_ping(address):
    response = os.system("ping -c 1 "+ address)
    if response == 0:
        assert True, 'Ping successful'
        return True
    else:
        assert False, 'Ping Failed'

def check_ping_until_timeout(address, timeout=20):
    timeout = time.time() + timeout
    while time.time() < timeout:
        response = os.system('ping -c 1 ' + address)
        print(f'{test_parameters.time_now} checking ping at: {address} ')
        if response == 0:
            print(f'{test_parameters.time_now} Ping Successful')
            return True
        else:
            print('Ping failed, trying again')
            time.sleep(5)
    assert False, 'Ping failed, timed-out while trying'

def serial_read(serial, timeout):
    if serial.inWaiting() > 0:
        data = serial.readline().decode('utf-8', errors='ignore')
        print(data[:-2]) # ignore last two chars which is likely \r\n

def serial_monitor(serial_port = 'undefined', serial_text_scan_timeout = 30):
    try:
        ser = serial.Serial(port = serial_port, baudrate=115200,bytesize=8,partity='N',stopbits=1,timeout=1)
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        print(f'connected to : {serial_port}')
        data = ser.readlines()

        scantimeout = time.time() + serial_text_scan_timeout
        while time.time() < scantimeout:
            if 'hello world' in str(data):
                return True
            #ser.write(b'\r')# hit return key in serial
        
        data = ser.readlines()
        for value in data:
            print('serial data',value)
    except:
        raise
    finally:
        print('serial_monitor() closing...')
        ser.close()

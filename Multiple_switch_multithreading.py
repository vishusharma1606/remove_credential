from concurrent.futures import thread
from decimal import DecimalException
from distutils.cmd import Command
from distutils.util import execute
from ensurepip import version
import threading
from netmiko import ConnectHandler
from getpass import getpass

# Opening a file 
file = open('myfile.txt', 'w')

#First create the device object using a dictionary

device1 = {
    'password': 'Innovium123',    #ssh password  
    'device_type': 'linux',       #device type
    'ip':   '10.4.4.76',          #IP Address
    'username': 'admin',          #ssh username
}

device2 = {
    'password': 'Innovium123',    #ssh password
    'device_type': 'linux',       #DEVICE_TYPE
    'ip':   '10.4.4.76',          #IP address
    'username': 'admin'           #ssh username
}

device3 = {
    'password': 'Innovium123',    #ssh password
    'device_type': 'linux',       #DEVICE_TYPE
    'ip':   '10.4.4.76',          #IP address
    'username': 'admin'           #ssh username
}

Device_list = [device1,device2,device3]



def device_info(device):
    print('connecting to the device ' + device['ip'])

    try:
       # Next establish the SSH connection
       net_connect = ConnectHandler(**device)
       print('connecting succesfully to the device ' + device['ip'])
   
       #execute show version on router and save output to output object 
       output = net_connect.send_command('show version' ,read_timeout = 120)
       print(output)
       file.write(f"\n{output}\n")
   
       #execute show ip interface on router and save output to output object 
       output = net_connect.send_command('show ip interface' ,read_timeout = 120)
       print(output)
       file.write(f"\n{output}\n")
    
    except:
        print("authentication failed")




#_multithreading 
thread_list = list()
for device in Device_list:
    thread = threading.Thread(target=device_info, args=(device,))
    thread.start()
    thread_list.append(thread)
for thread in thread_list:
    thread.join()
print("## finished execution of the script ####")

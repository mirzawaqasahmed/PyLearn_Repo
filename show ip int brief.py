import netmiko
import time
import csv

cmd = 'show ip int brief'

clients = []
with open('routers.csv') as devicesFile:
    devicesDict = csv.DictReader(devicesFile, dialect='excel')
    for row in devicesDict:
        clients.append(row)


def split_interfaces(interface):

    info = {}
    interface = interface.split()
    info['Interface'] = interface[0]
    info['IP'] = interface[1]
    if len(interface) > 6:
        info['Status'] = interface[4] + ' ' + interface[5]
        info['Protocol'] = interface[6]
    else:
        info['Status'] = interface[4]
        info['Protocol'] = interface[5]
    return info

def display_show_ip_int_brief(output):

    output = str(output)
    line = output.split('\n')
    line = line[1::]
    for l in line:
        info = split_interfaces(l)
        print "Interface = %s" % info['Interface']
        print "IP = %s" % info['IP']
        print "Status = %s" % info['Status']
        print "Protocol is = %s" % info['Protocol']

def connect_and_send():

    for client in clients:
        client.pop('hostname')
        connection = netmiko.ConnectHandler(**client)
        output = connection.send_command(cmd)
        display_show_ip_int_brief(output)


connect_and_send()

'''
Interface             IP-Address      OK?    Method Status     	            Protocol
GigabitEthernet0/1    unassigned      YES    unset  up         	            up
GigabitEthernet0/2    192.168.190.235 YES    unset  up         	            up
GigabitEthernet0/3    unassigned      YES    unset  up         	            up
GigabitEthernet0/4    192.168.191.2   YES    unset  up         	            up
TenGigabitEthernet2/1 unassigned      YES    unset  up         	            up
TenGigabitEthernet2/2 unassigned      YES    unset  up         	            up
TenGigabitEthernet2/3 unassigned      YES    unset  up         	            up
TenGigabitEthernet2/4 unassigned      YES    unset  down       	            down
GigabitEthernet36/1   unassigned      YES    unset  down                    down
GigabitEthernet36/2   unassigned      YES    unset  down                    down
GigabitEthernet36/11  unassigned      YES    unset  down       	            down
GigabitEthernet36/25  unassigned      YES    unset  down       	            down
Te36/45               unassigned      YES    unset  down       	            down
Te36/46               unassigned      YES    unset  down       	            down
Te36/47               unassigned      YES    unset  administratively down   down
Te36/48               unassigned      YES    unset  down       	            down
Virtual36             unassigned      YES    unset  up         	            up

show ip interface brief Field Descriptions:

Interface    ---> Type of interface.
IP-Address   ---> IP address assigned to the interface
OK?          ---> "Yes" means that the IP Address is valid. "No" means that the IP Address is not valid.
Method       ---> The Method field has the following possible values:

                    RARP or SLARP--Reverse Address Resolution Protocol (RARP) or Serial Line Address Resolution Protocol (SLARP) request.

                    BOOTP--Bootstrap protocol.

                    TFTP--Configuration file obtained from the TFTP server.

                    manual--Manually changed by the command-line interface.

                    NVRAM--Configuration file in NVRAM.

                    IPCP--ip address negotiated command.

                    DHCP--ip address dhcp command.

                    unset--Unset.

                    other--Unknown.

Status       ---> Shows the status of the interface. Valid values and their meanings are:

                    up--Interface is up.

                    down--Interface is down.

                    administratively down--Interface is administratively down.

Protocol     ---> Shows the operational status of the routing protocol on this interface.

'''

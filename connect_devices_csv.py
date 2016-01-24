# coding=utf-8
# Author: Mirza Waqas Ahmed (m.w.ahmed@gmail.com)
# (Copyright 2016 Mirza Waqas Ahmed”)
# This code is free software and is distributed under the terms of the GNU General Public License.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
######################################################
# This a script to connect Cisco routers defined in routers.csv file using Netmiko and then send
# show and config commands.
######################################################

import csv
from netmiko import ConnectHandler
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
import yaml
# import sys
#
#
# arg1 = sys.argv[1]

# http://www.saidvandeklundert.nl/network-automation-netmiko.php
# The logic of these below two functions were inspired from the blog post mentioned in the above URL.
def push_show_commands(username, password, ip_address, vendor_class, secret, commands):
    try:
        net_connect = ConnectHandler(device_type=vendor_class, ip=ip_address, username=username, password=password, secret=secret)
        print '#' * 80 + '\n'
        for command in commands:
            output = net_connect.send_command(command)
            print output + '\n' + '#' * 80
    except:
        print 'Error in either connecting or executing show command @ ' + ip_address
def push_config_commands(username, password, ip_address, vendor_class, secret, commands):
    try:
        net_connect = ConnectHandler(device_type=vendor_class, ip=ip_address, username=username, password=password, secret=secret)
        net_connect.enable()
        output = net_connect.send_config_set(commands)
        print output
    except:
        print 'Error in either connecting or executing configuration command @ ' + ip_address
# Devices in the CSV file
devices = []
def load_csv_files():
    with open('routers.csv') as devicesFile:
        devicesdict = csv.DictReader(devicesFile, dialect='excel')
        for row in devicesdict:
            devices.append(row)
load_csv_files()
# Setting up environment for Jinja2
env = Environment(loader=FileSystemLoader('./templates'),trim_blocks=True)

# Loading variables from YAML file.
with open('./YAML/configuration.yml') as _:
   config_commands_var = yaml.load(_)

template = env.get_template('add_description_ospf.j2')
show_commands = ['show ip inter brief', 'show ip route', 'show cdp neighbors', 'show ip ospf nei']

for device in range(len(devices)):
    print "\nStart time: " + str(datetime.now())
    username = devices[device]['username']
    password = devices[device]['password']
    ip = devices[device]['ip']
    device_type = devices[device]['device_type']
    secret = devices[device]['secret']
    hostname = devices[device]['hostname']
    config_commands_list = ''
#   Pushing show commands:
    push_show_commands(username, password, ip, device_type, secret, show_commands)

#   Rendering YAML Dictionary in Jinja2
    config_commands_list += template.render(interface=config_commands_var['routers']['interfaces'][hostname])
    config_commands_list += template.render(routing=config_commands_var['routers']['routing_protocol'][hostname])
    # print config_commands
    rendered_config = str(config_commands_list)
    rendered_config = rendered_config.splitlines()
    push_config_commands(username, password, ip, device_type, secret, rendered_config)

print "\nEnd time: " + str(datetime.now())

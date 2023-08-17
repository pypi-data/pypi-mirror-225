#!/usr/bin/env python3
import argparse
import subprocess
import os
import sys
import magic
import shutil
from typing import Sequence
from textwrap import dedent
from magic.proto.remote_config_pb2 import RemoteDeviceConfig, RemoteDevice
from google.protobuf import text_format
import getpass

def dals(string):
    """dedent and left-strip"""
    return dedent(string).lstrip()

def parse_args():
    help_docs="""
        command:
           list: list all remote devices in config file
           info: get details about specific device
        usage:
            magic-ssh {info, list}
    """
    if any([x in ['-h', '--help'] for x in sys.argv[1:]]):
        print(dals(help_docs))
    p = argparse.ArgumentParser()     
    p.add_argument('-p', '--password', default=None, help='password')
    p.add_argument('-o', '--port', type=int, default=None, help='port')
    p.add_argument('argv', nargs="*", help='command or options')
 
    return p.parse_args()

class Device:
    def __init__(self, name, ip, username, password, port, description):
        self.name = name
        self.ip = ip
        self.username = username
        self.password = password
        self.port = port
        self.description = description

    @property
    def host(self):
        return self.username + '@' + self.ip

    def __repr__(self):
        string = str(self.host) + '\n'
        string += '  name: {}\n'.format(self.name)
        string += '  ip: {}\n'.format(self.ip)
        string += '  username: {}\n'.format(self.username)
        string += '  password: {}\n'.format(self.password)
        string += '  port: {}\n'.format(self.port)
        string += '  description: {}\n'.format(self.description)
        return string

class DeviceManager:
    def __init__(self, devices: Sequence[Device], default_password=None, default_port=None):
        self.devices = devices
        self.default_password = default_password
        self.default_port = default_port

    def list(self):
        msg_fmt = '{:<4} {:<20} {:<35} {}'
        print(msg_fmt.format('id', 'name', 'host', 'description'))
        for index, device in enumerate(self.devices):
            msg = msg_fmt.format(index, device.name[:20], device.host, device.description)
            print(msg)

    def ssh_connect(self, remote):
        host = None
        password = None
        port = 22
        if remote.isdecimal():
            # index in device list
            idx = int(remote)
            if idx >= len(self.devices):
                raise RuntimeError('target idx error: %s' % idx)
            host, password, port = self.devices[idx].host, self.devices[idx].password, self.devices[idx].port
        else:
            host = remote
            assert '@' in host, 'valid host is username@ip_address'   
            for d in self.devices:
                if d.host == host:
                    print("[WARN] remote is in device list")
                    password, port = d.password, d.port
                    break

        # check/update password and port
        password =  self.default_password or password 
        password = password or getpass.getpass("{}'s password: ".format(host))
        port = self.default_port or port 
        cmd = 'sshpass -p {} ssh -p {} -o StrictHostKeyChecking=no {}'.format(password, port, host)
        print("connecting: ssh -p {} {}".format(port, host))
        subprocess.run(cmd, shell=True)


    def display_info(self, argv):
        if argv.isdecimal() and int(argv) < len(self.devices):
            print(self.devices[int(argv)])
        else:   
            for device in self.devices:
                if argv in [device.name, device.ip, device.host]:
                    print(device)

def main():
    args = parse_args()

    remote_config_file = os.path.join(magic.config_root, 'remote_device.pt')
    if not os.path.exists(remote_config_file):
        os.makedirs(magic.config_root, exist_ok=True)
        # create a template of config file
        remote_conf = RemoteDeviceConfig()
        remote_device = RemoteDevice()
        remote_device.name = 'name'
        remote_device.ip = '0.0.0.0'
        remote_device.username = 'username'
        remote_device.password = 'password'
        remote_device.port = 22
        remote_device.description = 'description'
        remote_conf.device.append(remote_device)
        with open(remote_config_file, 'w') as f:
            text_format.PrintMessage(remote_conf, f)
    remote_conf = RemoteDeviceConfig()
    with open(remote_config_file, 'r') as f:
        text_format.Parse(f.read(), remote_conf)
    # print(remote_conf)help

    remote_devices = []
    for device_conf in remote_conf.device:
        device = Device(
            name=device_conf.name,
            ip=device_conf.ip,
            username=device_conf.username,
            password=device_conf.password,
            port=device_conf.port,
            description=device_conf.description
            )
        assert len(device.name), 'device name is empty'
        assert len(device.ip),  'device ip is empty'
        assert len(device.username),  'device username is empty'
        device.port = device.port or 22  # default port is 22
        remote_devices.append(device)

    if not remote_devices:
        print('[WARN] remote device has not been added to remote_device.pt')
    remote_devices = sorted(remote_devices, key=lambda x: x.name, reverse=False)
    device_manager = DeviceManager(
        devices=remote_devices, 
        default_password=args.password, 
        default_port=args.port)

    # 参数解析
    
    argv = args.argv
    if len(argv) == 0 or argv[0] == 'list':
        device_manager.list()
    elif len(argv) == 2 and argv[0] == 'info':
        device_manager.display_info(argv[1])
    elif len(argv) == 1:
        device_manager.ssh_connect(argv[0])

if __name__ == "__main__":
    main()

import paramiko
import os
import getpass
import yaml

class SftpClient:
    def __init__(self, local_path, remote_path, host, password=None, port=22, timeout=5,
                 exclude=None, include=None):
        assert os.path.exists(local_path), "local path error: %s" % local_path
        self.local_path = os.path.abspath(local_path)
        self.remote_path = remote_path
        if '@' not in host:
            raise RuntimeError("host error: %s" % host)
        self.username, self.ip_address = host.split('@')
        self.password = password or getpass.getpass("{}'s password: ".format(host))
        self.port = port

        # include hints
        self.enable_include_hint = True if include else False
        self.include_file_list = []  # 绝对路径
        self.include_paths = []
        if self.enable_include_hint:
            for hint in include:
                assert len(hint) >= 2, 'too short hint'
                if os.path.isfile(hint):
                    self.include_file_list.append(os.path.abspath(hint))
                else:
                    self.include_paths.append(hint)
            # info_str = "include:"
            # for p in self.include_file_list:
            #     info_str += "\n  " + p
            # for p in self.include_paths:
            #     info_str += "\n  " + p
            # print(info_str)
        # exclude hints
        self.enable_exclude_hint = True if exclude else False
        self.exclude_file_list = []  # 绝对路径
        self.exclude_paths = []
        if self.enable_exclude_hint:
            for hint in exclude:
                assert len(hint) >= 2, 'too short hint'
                if os.path.isfile(hint):
                    self.exclude_file_list.append(os.path.abspath(hint))
                else:
                    self.exclude_paths.append(hint)
            info_str = "exclude:"
            for p in self.exclude_file_list:
                info_str += "\n  " + p
            for p in self.exclude_paths:
                info_str += "\n  " + p
            print(info_str)

        # 创建 SSHClient 对象并建立连接
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(hostname=self.ip_address, port=self.port, username=self.username,
                         password=self.password, look_for_keys=False, timeout=timeout)
        # 创建 SFTPClient 对象
        self.sftp = self.ssh.open_sftp()

    def exclude_file(self, local_file_path, file):
        """priority is file list > path > extension """
        if not self.enable_exclude_hint:
            return 0
        if local_file_path in self.exclude_file_list:
            return 1
        for path_regex in self.exclude_paths:
            key, ext = path_regex, None
            if "*" in path_regex:
                key, ext = path_regex.split("*")
                # print(key, ext, local_file_path)
            if key in local_file_path:
                if ext:
                    _, extension = os.path.splitext(file)
                    if extension == ext:
                        return 1
                else:
                    return 1
        return 0

    def include_file(self, local_file_path, file):
        """priority is file > path > extension, must provide path when specify extension
        Return:
            0 - not subject to exclude filtering rules
            1 - include by regex. subject to exclude filtering rules
            2 - not included
        """
        if not self.enable_include_hint:
            return 1
        if local_file_path in self.include_file_list:
            return 0
        for path_regex in self.include_paths:
            key, ext = path_regex, None
            if "*" in path_regex:
                key, ext = path_regex.split("*")
            # print(key, ext, local_file_path)
            if key in local_file_path:
                if ext:
                    _, extension = os.path.splitext(file)
                    if extension == ext:
                        return 1
                else:
                    return 1
        return 2

    def send(self):
        try:
            self.sftp.stat(self.remote_path)
        except Exception as err:
            self.sftp.close()
            self.ssh.close()
            print("remote path not exists: %s" % self.remote_path)
            exit(0)

        # 根据过滤条件进行文件传输
        for root, dirs, files in os.walk(self.local_path):
            for file in files:
                local_file_path = os.path.join(root, file)
                include_state = self.include_file(local_file_path, file)
                if include_state == 2:
                    continue
                elif include_state == 1:
                    if self.exclude_file(local_file_path, file):
                        continue
                remote_file_path = os.path.join(self.remote_path, os.path.relpath(local_file_path, self.local_path))
                self.create_remote_directory(os.path.dirname(remote_file_path))
                print(f"upload: {local_file_path} -> {remote_file_path}")
                self.sftp.put(local_file_path, remote_file_path)

        # 关闭连接
        self.sftp.close()
        self.ssh.close()

    def create_remote_directory(self, remote_dir):
        try:
            self.sftp.stat(remote_dir)
        except Exception as err:
            path, folder = os.path.split(remote_dir)
            self.create_remote_directory(path)
            self.sftp.mkdir(remote_dir)

def deploy_configure_parser(sub_parsers):
    p = sub_parsers.add_parser("deploy", help="deploy project to remote")
    p.add_argument("config_file", help='config file for deployment rules')
    p.set_defaults(func=sftp_deploy)

def sftp_deploy(args):
    """api for terminal command"""
    with open(args.config_file, 'r') as file:
        config = yaml.safe_load(file)
    client = SftpClient(
        local_path=config.get('local_path', ''),
        remote_path=config('remote_path', ''),
        host=config.get('host', ''),
        password=config.get('password', None),
        port=config.get('port', 22),
        exclude=config.get('exclude', []),
        include=config.get('include', [])
    )
    client.send()

def deployment(
        host, local_path, remote_path, password=None,
        port=22, include=None, exclude=None):
    """api for python scripts"""
    client = SftpClient(
        host=host,
        local_path=local_path,
        remote_path=remote_path,
        password=password,
        port=port,
        exclude=exclude,
        include=include
    )
    client.send()

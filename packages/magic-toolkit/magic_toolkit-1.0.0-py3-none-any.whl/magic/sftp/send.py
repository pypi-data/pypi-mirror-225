import paramiko
import os
import getpass

class SftpClient:
    def __init__(self, local_paths, remote_path, host, password=None, port=22, timeout=5,
                 exclude=None):
        self.local_paths = local_paths
        self.remote_path = remote_path
        if '@' not in host:
            raise RuntimeError("correct host is user@ip")
        self.username, self.ip_address = host.split('@')
        self.password = password or getpass.getpass("{}'s password: ".format(host))
        self.port = port

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

    def check_exclude_file(self, local_file_path, file):
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

    def send(self):
        try:
            self.sftp.stat(self.remote_path)
        except Exception as err:
            self.sftp.close()
            self.ssh.close()
            print("[Error] remote path not exists:", self.remote_path)
            exit(1)  # Did not exit as expected
        for path in self.local_paths:
            # path is a file
            if os.path.isfile(path):
                root, file = os.path.split(path)
                # print(root, file)
                remote_file_path = os.path.join(self.remote_path, file)
                print(f"upload: {path} -> {remote_file_path}")
                self.sftp.put(path, remote_file_path)
            elif os.path.isdir(path):
                path = os.path.abspath(path)
                for root, dirs, files in os.walk(path):
                    for file in files:
                        local_file_path = os.path.join(root, file)
                        if self.check_exclude_file(local_file_path, file):
                            continue
                        remote_file_path = os.path.join(self.remote_path,
                                                        os.path.relpath(local_file_path, os.path.dirname(path)))
                        self.create_remote_directory(os.path.dirname(remote_file_path))
                        print(f"upload: {local_file_path} -> {remote_file_path}")
                        self.sftp.put(local_file_path, remote_file_path)
            else:
                print('[Error] not exist:', path)
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

def send_config_parser(sub_parsers):
    p = sub_parsers.add_parser("send", help="send to remote")
    p.add_argument('host', type=str, help='usrname@ip_address')
    p.add_argument('paths', nargs='+', help='path1 path2 ..., the last is remote_path')
    p.add_argument('-p', '--password', type=str, help='sftp password to login')
    p.add_argument('-o', '--port', type=int, help='remote port', default=22)
    p.add_argument('--exclude', nargs='+', type=str, default=None, help='paths, files or extensions to filter')
    p.set_defaults(func=sftp_send)

def sftp_send(args):
    """api for send files by sftp transformer"""
    assert len(args.paths) >= 2, 'need at least one local path and  one remote path separately'
    local_paths = args.paths[:-1]
    remote_path = args.paths[-1]
    # print(local_paths)
    client = SftpClient(
        local_paths=local_paths,
        remote_path=remote_path,
        host=args.host,
        password=args.password,
        port=args.port,
        timeout=5,
        exclude=args.exclude
    )
    client.send()

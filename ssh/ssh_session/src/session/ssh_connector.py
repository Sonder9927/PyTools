from pathlib import Path
import paramiko
import shutil


class SSHConnector(object):

    def __init__(self, host=None, port=None, username=None, pwd=None):
        """
        :param host: ip
        :param port: port
        :param username: username
        :param pwd: password
        """
        self.host = host
        self.port = port
        self.username = username
        self.pwd = pwd
        self.__k = None

    def connect(self):
        transport = paramiko.Transport((self.host, self.port))
        transport.connect(username=self.username, password=self.pwd)
        self.__transport = transport

    def close(self):
        self.__transport.close()

    def listdir(self, remote_path) -> list[str]:
        sftp = paramiko.SFTPClient.from_transport(self.__transport)
        return sftp.listdir(remote_path)

    def upload(self, local_path, target_path):
        sftp = paramiko.SFTPClient.from_transport(self.__transport)
        sftp.put(local_path, target_path)

    def download(self, remote_path, local_path):
        sftp = paramiko.SFTPClient.from_transport(self.__transport)
        lp = Path(local_path)
        if lp.exists():
            lp.unlink()
        sftp.get(remote_path, local_path)

    def download_slowly(self, remote_path, local_path):
        # for vary large file
        sftp = paramiko.SFTPClient.from_transport(self.__transport)
        with sftp.open(remote_path, "rb") as fp:
            shutil.copyfileobj(fp, open(local_path, 'wb'))

    def cmd(self, command):
        ssh = paramiko.SSHClient()
        ssh._transport = self.__transport

        # execute command
        stdin, stdout, stderr = ssh.exec_command(command)

        # get result
        result = stdout.read()
        result = str(result, encoding='utf-8')
        return result


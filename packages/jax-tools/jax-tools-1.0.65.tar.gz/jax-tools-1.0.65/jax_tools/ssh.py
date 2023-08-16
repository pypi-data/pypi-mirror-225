# -*- coding: utf-8 -*-
"""
ssh operations
"""
import paramiko
from jax_tools.logger import logger


class SSHClient(object):
    """
    SSH Connector
    """
    SSH_CONNECTION_FAILED = 'SSH connection failed'

    def __init__(self, host, port, username, password) -> None:
        """
        SSH Connector
        Args:
            host (str): host for ssh connection
            port (int): port for ssh connection
            username (str): username for ssh connection
            password (str): password for ssh connection
        """
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.ssh_client = self.__get_ssh_client()

    def __get_ssh_client(self):
        """
        Get ssh client
        Args:

        Returns:
            ssh client or None

        """
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        response = True
        try:
            client.connect(
                self.host,
                self.port,
                username=str(self.username),
                password=str(self.password),
                timeout=10)
        except paramiko.ssh_exception.AuthenticationException:
            logger.error('authentication failed')
            response = None
        except paramiko.ssh_exception.NoValidConnectionsError:
            logger.error('can not connect to host')
            response = None
        except Exception as e:
            logger.error(e)
            response = None
        if response:
            return client
        else:
            return response

    def run_cmd(self, cmd, read_line=False, time_out=300):
        """
        Run command on remote host
        Args:
            cmd (str): command to run
            read_line (bool): True if read line by line, False if read all
            time_out (int): timeout in seconds

        Returns:
            String if read_line is False

        """
        result = None
        if self.ssh_client is None:
            logger.warning(self.SSH_CONNECTION_FAILED)
            return result
        try:
            _std_in, std_out, _std_err = self.ssh_client.exec_command(cmd, timeout=time_out)
            if read_line:
                result = std_out.readlines()
            else:
                result = std_out.read().decode('utf-8').rstrip()
        except Exception as e:
            logger.error('Connection exception, User login info may be wrong, or connection has been closed, '
                         ' msg: %s' % e)
        return result

    def put_file(self, local_file, remote_file):
        """
        Put file to remote host
        Args:
            local_file (str): local file path
            remote_file (str): remote file path

        Returns:

        """
        if self.ssh_client is None:
            logger.warning(self.SSH_CONNECTION_FAILED)
            return
        try:
            sftp_client = self.ssh_client.open_sftp()
            sftp_client.put(local_file, remote_file)
        except Exception as e:
            logger.error('Connection exception, User login info may be wrong, or connection has been closed, '
                         ' msg: %s' % e)

    def get_file(self, remote_file, local_file):
        """
        Get file from remote host
        Args:
            remote_file (str): remote file path
            local_file (str): local file path

        Returns:

        """
        if self.ssh_client is None:
            logger.warning(self.SSH_CONNECTION_FAILED)
            return
        try:
            sftp_client = self.ssh_client.open_sftp()
            sftp_client.get(remote_file, local_file)
        except Exception as e:
            logger.error('Connection exception, User login info may be wrong,  msg: %s' % e)

    def close(self) -> None:
        """
        Close ssh connection
        Returns:

        """
        self.ssh_client.close()

    def __del__(self):
        if self.ssh_client:
            self.close()


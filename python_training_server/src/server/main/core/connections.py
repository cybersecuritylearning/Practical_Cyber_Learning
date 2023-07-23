import paramiko
from main.core.utils import log_data
from random import randrange

class Connection:
    def __init__(self,ssh_key,url,user,port=22):
        self.url = url
        self.port = port
        self.ssh_key = ssh_key
        self.user = user
        self.ssh = paramiko.SSHClient()

    def make_connection(self):
        """Function which generates connection"""
        try:
            private_key = paramiko.RSAKey.from_private_key_file(self.ssh_key)
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect(hostname=self.url,username=self.user,pkey=private_key)
            return True

        except Exception as e:
            log_data.log_debug(e)
            return False

    def exec_command(self,command):
        """Function which executes a ssh command
        params:
            (str)command: command to exec
        return:
            (tupple)stds: paramiko std's pipes
        """
        try:
            ssh_stdin, ssh_stdout, ssh_stderr=self.ssh.exec_command(command)
            return (ssh_stdin,ssh_stdout,ssh_stderr)
        except Exception as exp:
            log_data.log_debug(exp)
            return False

    def get_available_port(self)->str:
        """Function which checks and generate port
        return:
                (str)port: port number as string
        """
        try:
            
            used_ports = self.exec_command("netstat -ant |grep LISTEN |  awk '{print $4}'|awk -F \":\" '{print $NF}' | sort -u ")   
            used_ports = used_ports[1].read().decode().split("\n")
            
            port = str(randrange(1000,10000))
            while port in used_ports:
                port = str(randrange(1000,10000))
            
            return port
        except Exception as e:
            log_data.log_debug(e)
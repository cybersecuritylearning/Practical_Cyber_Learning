import paramiko
from main.core.utils import log_data

class Connection:
    def __init__(self,ssh_key,url,user,port=22):
        self.url = url
        self.port = port
        self.ssh_key = ssh_key
        self.user = user
        self.ssh = paramiko.SSHClient()

    def make_connection(self):
        try:
            
            private_key = paramiko.RSAKey.from_private_key_file(self.ssh_key)
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect(hostname=self.url,username=self.user,pkey=private_key)
            return True

        except Exception as e:
            log_data.log_debug(e)
            return False

    def exec_command(self,command):
        try:
            ssh_stdin, ssh_stdout, ssh_stderr=self.ssh.exec_command(command)
            return (ssh_stdin,ssh_stdout,ssh_stderr)
        except Exception as exp:
            log_data.log_debug(exp)
            return False

    def check_available_port(self,port):
        try:
            breakpoint()
            used_ports = self.exec_command("netstat -tulnp | awk -F \" \" '{printf(\"%s\n\",$4)}' | awk -F \":\" '{printf(\"%s\n\",$2)}'| sort -u")[1].read()   
            print(used_ports)
            return True
        except Exception as e:
            log_data.log_debug(e)
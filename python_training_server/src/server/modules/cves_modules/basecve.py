from main.core.connections import Connection
import logging


class BaseCVE:
    RESULT = {"Data":"Try Harder"}

    def __init__(self,ssh_key:str,ip_addr:str):
        self.ssh_key = ssh_key
        self.ip_addr = ip_addr
        self.logger = logging.getLogger(__name__)
        self.__conn = Connection(self.ssh_key,self.ip_addr,"root",22)
        self.__conn.make_connection()

    def _exec_docker_command(self,docker_name:str, command:str):
        """
        Executes a command inside a Docker container.

        params:
            docker_name (str): The name of the Docker container.
            command (str): The command to execute.
        
        return:
            str: The command output.
        """
        try:
            output = self.__conn.exec_command(f"docker exec {docker_name} {command}")
            result = output[1].read().decode().strip()
        except Exception as e:
            self.logger.error(str(e))
            result = None        
        
        return result
    
    def process(self, user):
        """
        This method should be implemented in the derived class.

        params:
            user (object): Represents the object of a user (from SQL).
        
        return:
            dict: Result of the process.
        """
        return True
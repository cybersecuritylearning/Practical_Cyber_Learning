from modules.cves_modules.basecve import BaseCVE

class CVE_2021_41773(BaseCVE):
    TRAIN_ID = "TRAIN-01-08"
    DOCKER_NAME = "cve-2021-41773C"
    SSH_KEY = "/run/secrets/host_ssh_key"
    IP_ADDR = "192.168.0.104"

    def __init__(self,request):
        super().__init__(self.SSH_KEY,self.IP_ADDR)
        self.request = request
  
    def __gets_flag(self,command):
        """
        It gets the flag from the docker and sets to user for checks
        params:
            command(str):represents a command run on docker for flag
        return:
            True/False(Boolean):it says if it's up or not
        """
        return self._exec_docker_command(self.DOCKER_NAME,command)
 
    def process(self,user):
        
        __docker_flag = self.__gets_flag("cat /tmp/flag.txt")
        if __docker_flag:
            user.Hash_check = __docker_flag
            user.save()
            return {"Status":"Up"}
        
        return self.RESULT
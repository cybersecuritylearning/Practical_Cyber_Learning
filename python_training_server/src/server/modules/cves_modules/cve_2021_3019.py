from modules.cves_modules.basecve import BaseCVE

class CVE_2021_3019(BaseCVE):
    TRAIN_ID = "TRAIN-01-09"
    DOCKER_NAME = "cve-2021-3019C"
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
        
        __docker_flag = self.__gets_flag("tail -n 1 /lanproxy-server/distribution/proxy-server-0.1/conf/config.properties")
        if __docker_flag:
            __docker_flag = __docker_flag[6:]
            user.Hash_check = __docker_flag
            user.Current_Level = self.TRAIN_ID
            user.save()
            return {"Status":"Up"}
        
        return self.RESULT
    
import paramiko

ssh = paramiko.SSHClient()
k = paramiko.RSAKey.from_private_key_file("/Users/catalinfilip/.ssh/linode")
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname="23.92.24.245",username="root",pkey=k)

print(dir(ssh))


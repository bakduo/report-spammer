import time
import paramiko
import io

import logging

logger = logging.getLogger(__name__)

class SSHService(object):
    
    def __init__(self):
        super()
        
    def execute_ssh_command(self,host, port, username, password, keyfilepath, keyfiletype, command):
        """
        execute_ssh_command(host, port, username, password, keyfilepath, keyfiletype, command) -> tuple
        Executes the supplied command by opening a SSH connection to the supplied host
        on the supplied port authenticating as the user with supplied username and supplied password or with
        the private key in a file with the supplied path.
        If a private key is used for authentication, the type of the keyfile needs to be specified as DSA or RSA.
        :rtype: tuple consisting of the output to standard out and the output to standard err as produced by the command
        """
        ssh = None
        key = None
        #Patch para poder leer la key por medio de file
        try:
            keyfileBytes = open(keyfilepath,'r')
            linesKeys = keyfileBytes.read()
            keyfile = io.StringIO(linesKeys)
        except Exception as e:
            logger.error("{}".format(e))
            raise Exception("No es posible leer el KeyFile")
        
        try:
            if keyfilepath is not None:
                # Get private key used to authenticate user.
                if keyfiletype == 'DSA':
                    # The private key is a DSA type key.
                    key = paramiko.DSSKey.from_private_key_file(keyfile)
                else:
                    # The private key is a RSA type key.
                    key = paramiko.RSAKey.from_private_key(keyfile)

            # Create the SSH client.
            ssh = paramiko.SSHClient()

            # Setting the missing host key policy to AutoAddPolicy will silently add any missing host keys.
            # Using WarningPolicy, a warning message will be logged if the host key is not previously known
            # but all host keys will still be accepted.
            # Finally, RejectPolicy will reject all hosts which key is not previously known.
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            # Connect to the host.
            if key is not None:
                # Authenticate with a username and a private key located in a file.
                ssh.connect(host, port, username, None, key)
            else:
                # Authenticate with a username and a password.
                ssh.connect(host, port, username, password)

            # Send the command (non-blocking)
            stdin, stdout, stderr = ssh.exec_command(command)

            # Wait for the command to terminate
            while not stdout.channel.exit_status_ready() and not stdout.channel.recv_ready():
                time.sleep(1)

            stdoutstring = stdout.readlines()
            stderrstring = stderr.readlines()
            return stdoutstring, stderrstring
        finally:
            if ssh is not None:
                # Close client connection.
                ssh.close()
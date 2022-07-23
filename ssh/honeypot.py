from honeypot import configuration

import socket
import threading
import paramiko
import time


LOGFILE_LOCK = threading.Lock()


class SSHServer(paramiko.ServerInterface):
    def __init__(self, addr):
        self.event = threading.Event()
        self.addr = addr

    def check_auth_password(self, username, password):
        LOGFILE_LOCK.acquire()
        try:
            # Listen to all conenctions to the SSHServer
            # We get all users information but only log it to the file.
            with open(configuration.settings.ssh_log, "a") as f:
                # Log ssh data to the file
                print(str(time.time()) + ";" + "Login: " + self.addr[0] + ";" + username + ";" + password)
                f.write(str(time.time()) + ";" +self.addr[0]+";"+username + ";" + password + "\n")
        finally:
            LOGFILE_LOCK.release()
        return paramiko.AUTH_FAILED


def handle_ssh_connection(client, addr):
    transport = paramiko.Transport(client)
    # Set created RSA key to the paramiko server
    host_key = paramiko.RSAKey(filename=configuration.settings.ssh_key)
    transport.add_server_key(host_key)
    server = SSHServer(addr)
    try:
        transport.start_server(server=server)
        channel = transport.accept(1)
        if channel is not None:
            channel.close()
    except ConnectionResetError:
        print('Closed ssh connection from: ' + addr[0])


def start_ssh_honeypot(ip='0.0.0.0'):
    # Similarly as in http and https we create socket which listens on specific port.
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((ip, configuration.settings.ssh_port))
        server_socket.listen(100)
        # The log file for the library which we use to the ssh connection
        paramiko.util.log_to_file(configuration.settings.paramiko_log)

        while True:
            try:
                conn, remote_addr = server_socket.accept()
                # For each ssh connection we create another thread so multiple users can connect to the honeypot.
                t = threading.Thread(target=handle_ssh_connection, args=(conn, remote_addr, ))
                t.deamon = True
                t.start()
            except Exception as e:
                print(e)

    except Exception as e:
        print(e)

if __name__ == "__main__":
    configuration.init('dev')
    start_ssh_honeypot()

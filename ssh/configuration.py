import os

def init(mode='dev'):
    global settings

    settings = Config(mode)

class Config(object):
    def __init__(self, mode='dev'):
        # This is configruation for hte whole project
        # in multiple places we can say if we want to run the prod/dev
        # mode and this sets the proper paths/variables.
        self.prod_log_prefix = "/var/log/python-honeypot"
        self.MODES = {
            "prod": {
                "ssh_key": "/root/.ssh/honeypot.key",
                "ssl_key": "/etc/pki/tls/private/key.pem",
                "ssl_cert": "/etc/pki/tls/certs/cert.pem",
                "https_log": os.path.join(self.prod_log_prefix,"https.log"),
                "http_log": os.path.join(self.prod_log_prefix,"http.log"),
                "ssh_log": os.path.join(self.prod_log_prefix,"ssh.log"),
                "paramiko_log": os.path.join(self.prod_log_prefix,"paramiko.log"),
                "ssh_port": 22,
                "http_port": 80,
                "https_port": 433,
                "crontab_time": "* * * * *",
            },
            "dev": {
                "ssh_key": os.path.abspath("keys/honeypot.key"),
                "ssl_key": os.path.abspath("keys/key.pem"),
                "ssl_cert": os.path.abspath("keys/cert.pem"),
                "https_log": os.path.abspath("logs/https.log"),
                "http_log": os.path.abspath("logs/http.log"),
                "ssh_log": os.path.abspath("logs/ssh.log"),
                "paramiko_log": os.path.abspath("logs/paramiko.log"),
                "ssh_port": 8022,
                "http_port": 8080,
                "https_port": 8043,
                "crontab_time": "0 * * * *",
            }
        }
        self.mode = mode
        for key, value in self.MODES[self.mode].items():
            setattr(self, key, value)

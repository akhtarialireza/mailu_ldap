#!/usr/bin/python3

import os
import time
import subprocess


command = [
    "certbot",
    "-n", "--agree-tos", # non-interactive
    "-d", os.environ["HOSTNAMES"],
    "-m", "{}@{}".format(os.environ["POSTMASTER"], os.environ["DOMAIN"]),
    "certonly", "--standalone",
    "--cert-name", "mailu",
    "--preferred-challenges", "http", "--http-01-port", "8008",
    "--keep-until-expiring",
    "--config-dir", "/certs/letsencrypt",
    "--renew-with-new-domains",
    "--post-hook", "/config.py"
]

# Wait for nginx to start
time.sleep(5)

# Run certbot every hour
while True:
    subprocess.call(command)
    time.sleep(3600)


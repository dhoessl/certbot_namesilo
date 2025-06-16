#!/usr/bin/env python3

from subprocess import check_output, DEVNULL, CalledProcessError
from datetime import datetime
from os import environ, path, remove
import logging


def check_domains():
    logging.info("Checking for Domain renewal")
    renew_certs = []
    wildcard_certs = check_output(
        ['certbot', 'certificates'],
        stderr=DEVNULL
    )
    logging.info(wildcard_certs.decode())
    for line in wildcard_certs.decode().split('\n'):
        if '*.' not in line:
            continue
        cert_data = check_output(
            ['certbot', 'certificates', '-d', line.split()[1]],
            stderr=DEVNULL
        ).decode().split('\n')
        for line2 in cert_data:
            if 'Expiry Date: ' not in line2:
                continue
            if (datetime.fromisoformat(line2.split()[2]) - datetime.today()).days < 7:
                renew_certs.append(line.split()[1])
    return renew_certs


def renew_domains(domain_list):
    for domain in domain_list:
        logging.info("Renew Domain: " + domain)
        try:
            output = check_output(
                [
                    'certbot', 'certonly', '--manual',
                    '--email', environ['CERTBOT_EMAIL'],
                    '--agree-tos', '--preferred-challenges=dns',
                    '--manual-auth-hook', './authenticator.py',
                    '--manual-cleanup-hook', './cleanup.py',
                    '--manual-public-ip-logging-ok', '-d', domain
                ]
            )
        except CalledProcessError:
            logging.error(output.stderr.decode())
            exit(1)
        logging.info(output.decode())


def main():
    logging.info("Start renew")
    # Fetch domains to renew
    domains_to_renew = check_domains()
    # Renew previously fetched Domains
    renew_domains(domains_to_renew)


if __name__ == '__main__':
    # Comment next 3 lines if you want to keep all logs
    # This is just to look at logs if some error occurs
    logfile = "/etc/letsencrypt/certbot_run.log"
    if path.exists(logfile):
        remove(logfile)
    # Create logger
    logging.basicConfig(
        filename=logfile,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    # Start the main function
    main()

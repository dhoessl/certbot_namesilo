#!/usr/bin/env python3

from subprocess import check_output, DEVNULL
from datetime import datetime
from os import environ


def check_domains():
    renew_certs = []
    wildcard_certs = check_output(
        ['certbot', 'certificates'],
        stderr=DEVNULL
    ).decode().split('\n')
    for line in wildcard_certs:
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
        check_output(
            [
                'certbot', 'certonly', '--manual',
                '--email', environ['CERTBOT_EMAIL'],
                '--agree-tos', '--preferred-challenges=dns',
                '--manual-auth-hook', './authenticator.py',
                '--manual-cleanup-hook', './cleanup.py',
                '--manual-public-ip-logging-ok', '-d', domain
            ],
            stderr=DEVNULL
        )


def main():
    domains_to_renew = check_domains()
    renew_domains(domains_to_renew)


if __name__ == '__main__':
    main()

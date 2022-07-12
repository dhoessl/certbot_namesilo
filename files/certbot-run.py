#!/usr/bin/env python3

from subprocess import check_output, DEVNULL
from datetime import datetime
from os import environ


def check_domains():
    wildcard_certificates = {}
    return_certificates = []
    certbot_cert_output = check_output(
            ['certbot', 'certificates'],
            stderr=DEVNULL
    )
    for line in certbot_cert_output.decode().split('\n'):
        if '*.' in line:
            certificate_data = check_output(
                    ['certbot', 'certificates', '-d', line.split()[1]],
                    stderr=DEVNULL
            ).decode().split('\n')
            for cert_data_line in certificate_data:
                if 'Expiry Date: ' in cert_data_line:
                    wildcard_certificates[line.split()[1]] = cert_data_line.split()[2]  # noqa: E501
    for certificate in wildcard_certificates:
        if (datetime.fromisoformat(wildcard_certificates[certificate]) - datetime.today()).days < 7:  # noqa: E501
            return_certificates.append(certificate)
    return return_certificates


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

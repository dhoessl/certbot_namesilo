#!/usr/bin/env python3
from namesiloapi import NamesiloApiWrapper as naw
from subprocess import check_output, DEVNULL
from os import environ
from time import sleep


def set_record():
    record_id = None
    API = naw(environ['CERTBOT_NAMESILO_API_KEY'])
    api_result = API.listRecords(environ['CERTBOT_DOMAIN'])
    if 'NO DNS ' in api_result['namesilo']['reply']['detail']:
        pass
    elif api_result['namesilo']['reply']['detail'] != 'success':
        exit(1)
    if api_result['namesilo']['reply']['resource_record']:
        for record in api_result['namesilo']['reply']['resource_record']:
            if record_id is not None:
                break
            if isinstance(record, str):
                continue
            for subdomain_field in record:
                if (subdomain_field == 'host'
                        and record['host'] == '_acme-challenge.' + environ['CERTBOT_DOMAIN']):  # noqa: E501
                    record_id = record['record_id']
    if record_id:
        change_record(record_id)
    else:
        create_record()


def change_record(rrid):
    API = naw(environ['CERTBOT_NAMESILO_API_KEY'])
    API.updateRecord(
            environ['CERTBOT_DOMAIN'],
            rrid,
            '_acme-challenge',
            environ['CERTBOT_VALIDATION']
    )


def create_record():
    API = naw(environ['CERTBOT_NAMESILO_API_KEY'])
    API.addRecord(
            environ['CERTBOT_DOMAIN'],
            'TXT',
            '_acme-challenge',
            environ['CERTBOT_VALIDATION']
    )


def check_if_record_exists():
    record_exists = False
    tries = 0
    while record_exists is False and tries < 10:
        domain_data = check_output(
                [
                    'dig', 'TXT',
                    '_acme-challenge.' + environ['CERTBOT_DOMAIN'],
                    '+short'
                ],
                stderr=DEVNULL
        )
        if (domain_data.decode().split('\n')[0].strip('"')
                == environ['CERTBOT_VALIDATION']):
            record_exists = True
        else:
            tries += 1
            sleep(600)


if __name__ == '__main__':
    set_record()
    check_if_record_exists()

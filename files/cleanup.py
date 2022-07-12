#!/usr/bin/env python3

from namesiloapi import NamesiloApiWrapper as naw
from os import environ


def cleanup_record():
    record_id = None
    API = naw(environ['CERTBOT_NAMESILO_API_KEY'])
    api_result = API.listRecords(environ['CERTBOT_DOMAIN'])
    if 'NO DNS ' in api_result['namesilo']['reply']['detail']:
        exit(0)
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
        delete_record(record_id)
    else:
        exit(0)


def delete_record(record_id):
    API = naw(environ['CERTBOT_NAMESILO_API_KEY'])
    API.deleteRecord(
            environ['CERTBOT_DOMAIN'],
            record_id
    )


if __name__ == '__main__':
    cleanup_record()

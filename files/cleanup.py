#!/usr/bin/env python3

from namesiloapi import NamesiloApiWrapper as naw
from os import environ


def cleanup_record():
    API = naw(environ['CERTBOT_NAMESILO_API_KEY'])
    api_result = API.listRecords(environ['CERTBOT_DOMAIN'])
    if 'NO DNS ' in api_result['reply']['detail']:
        exit(0)
    elif api_result['reply']['detail'] != 'success':
        exit(1)
    rr_set = api_result["reply"]["resource_record"]
    if isinstance(rr_set, dict):
        rr_set = [rr_set]
    for record in rr_set:
        if record["host"] == "_acme-challenge." + environ["CERTBOT_DOMAIN"]:
            delete_record(API, record["record_id"])
    exit(0)


def delete_record(API, record_id):
    API.deleteRecord(
            environ['CERTBOT_DOMAIN'],
            record_id
    )


if __name__ == '__main__':
    cleanup_record()

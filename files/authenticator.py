#!/usr/bin/env python3
from namesiloapi import NamesiloApiWrapper as naw
from dns.resolver import resolve
from os import environ
from time import sleep


def set_record(API) -> bool:
    api_result = API.listRecords(environ['CERTBOT_DOMAIN'])
    if api_result['reply']['detail'] != 'success':
        exit(1)
    if 'NO DNS ' in api_result['reply']['detail']:
        create_record(API)
        return True
    rr_set = api_result["reply"]["resource_record"]
    # If its a singel RR set then it must be changed from dict to list
    if isinstance(rr_set, dict):
        rr_set = [rr_set]
    if not rr_set:
        create_record(API)
        return True
    for record in rr_set:
        if record["host"] == "_acme-challenge." + environ["CERTBOT_DOMAIN"]:
            change_record(API, record["record_id"])
            return True


def change_record(API, rrid):
    API.updateRecord(
        environ['CERTBOT_DOMAIN'],
        rrid,
        '_acme-challenge',
        environ['CERTBOT_VALIDATION']
    )


def create_record(API):
    API.addRecord(
        environ['CERTBOT_DOMAIN'],
        'TXT',
        '_acme-challenge',
        environ['CERTBOT_VALIDATION']
    )


def check_if_record_exists():
    record_exists = False
    tries = 0
    while record_exists is False and tries < 15:
        answer = resolve("_acme-challenge." + environ["CERTBOT_DOMAIN"], "TXT")
        for entry in answer:
            if environ["CERTBOT_VALIDATION"] in answer.to_text():
                record_exists = True
        if not record_exists:
            tries += 1
            sleep(600)


if __name__ == '__main__':
    API = naw(environ['CERTBOT_NAMESILO_API_KEY'])
    set_record(API)
    check_if_record_exists()

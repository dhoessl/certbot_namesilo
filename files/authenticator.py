#!/usr/bin/env python3
from namesiloapi import NamesiloApiWrapper as naw
from dns.resolver import resolve, NXDOMAIN
from os import environ
from time import sleep
import logging


def set_record(API) -> bool:
    logging.info("Set Record")
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
    logging.info("UPDATE Record")
    API.updateRecord(
        environ['CERTBOT_DOMAIN'],
        rrid,
        '_acme-challenge',
        environ['CERTBOT_VALIDATION']
    )


def create_record(API):
    logging.info("CREATE Record")
    API.addRecord(
        environ['CERTBOT_DOMAIN'],
        'TXT',
        '_acme-challenge',
        environ['CERTBOT_VALIDATION']
    )


def check_if_record_exists():
    logging.info("Check for Record")
    record_exists = False
    tries = 0
    while record_exists is False and tries < 15:
        try:
            answer = resolve("_acme-challenge." + environ["CERTBOT_DOMAIN"], "TXT")
            for entry in answer:
                if environ["CERTBOT_VALIDATION"] in answer.to_text():
                    logging.info("Record found")
                    record_exists = True
        except NXDOMAIN:
            logging.info(
                "Record not yet found ... waiting 600 sec ... "
                f"checked {tries + 1} times"
            )
            tries += 1
            sleep(600)


def check_env_vars() -> None:
    logging.info("======\nChecking Env Vars\n======")
    if "CERTBOT_NAMESILO_API_KEY" in environ:
        logging.info("CERTBOT_NAMESILO_API_KEY: (redacted and found)")
    else:
        logging.info("CERTBOT_NAMESILO_API_KEY: (not found)")
    logging.info("CERBOT_EMAIL: " + environ["CERTBOT_EMAIL"])
    logging.info("CERBOT_DOMAIN: " + environ["CERBOT_DOMAIN"])
    logging.info("CERTBOT_VALIDATION: " + environ["CERTBOT_VALIDATION"])


if __name__ == '__main__':
    logging.info("Starting Authenticator")
    if "CERTBOT_CUSTOM_DEBUG" in environ and environ["CERTBOT_CUSTOM_DEBUG"]:
        check_env_vars()
    API = naw(environ['CERTBOT_NAMESILO_API_KEY'])
    set_record(API)
    check_if_record_exists()

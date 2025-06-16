#!/usr/bin/env python3

from namesiloapi import NamesiloApiWrapper as naw
from os import environ
import logging


def cleanup_record():
    logging.info("Cleanup Record")
    API = naw(environ['CERTBOT_NAMESILO_API_KEY'])
    api_result = API.listRecords(environ['CERTBOT_DOMAIN'])
    if 'NO DNS ' in api_result['reply']['detail']:
        logging.info("No Records")
        exit(0)
    elif api_result['reply']['detail'] != 'success':
        logging.warning("API call failed!")
        exit(1)
    rr_set = api_result["reply"]["resource_record"]
    if isinstance(rr_set, dict):
        rr_set = [rr_set]
    for record in rr_set:
        if record["host"] == "_acme-challenge." + environ["CERTBOT_DOMAIN"]:
            delete_record(API, record["record_id"])


def delete_record(API, record_id):
    logging.info("Deleting Record...")
    API.deleteRecord(
        environ['CERTBOT_DOMAIN'],
        record_id
    )


if __name__ == '__main__':
    logfile = "/etc/letsencrypt/certbot_run.log"
    # Create logger
    logging.basicConfig(
        filename=logfile,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    cleanup_record()

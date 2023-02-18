import click
import sys
import socket
import re
import logging

from bigrest.bigip import BIGIP
from urllib.parse import urlparse


def connect_to_bigip(hostname: str, username: str, password: str, no_ssl_verify: bool):
    """
    Connects to BIG-IP device and returns the connection object.
    """

    try:
        bigip = BIGIP(hostname, username, password, request_token=True, session_verify=no_ssl_verify)
    except Exception as e:
        click.secho(f"Error: {e}")
        sys.exit()

    return bigip


def get_bigip_object(bigip, full_url):
    """
    Retrieves object information from BIG-IP device.
    full_url is the full URL to the object
    """

    object_url_path = urlparse(full_url).path

    # check if variable has a value
    if bool(object_url_path):
        # get object
        object = bigip.load(object_url_path)

    logging.debug(f"input: {full_url}")
    logging.debug(f"return:\r\n{object}")
    return object


def get_pm_ips(bigip, vs):
    """
    Get all the pool member ip addresses
    """

    pm_ips = []

    try:
        # Check if we have a default pool
        if "pool" in vs.properties:

            # get pool object
            pool_fullpath = vs.properties["pool"]
            pool_url = urlparse(vs.properties["poolReference"]["link"]).path
            click.secho(f"default_pool: {pool_fullpath}", fg="yellow")

            pool = get_bigip_object(bigip, pool_url)
            pm_url = urlparse(pool.properties["membersReference"]["link"]).path
            pms = get_bigip_object(bigip, pm_url)

            logging.debug(f"pool:\r\n{pool}")
            logging.debug(f"pms:\r\n{pms}")

            for pm in pms:
                # add pool member ip to list
                pm_ips.append(pm.properties["address"])

                logging.debug(f"pm:\r\n{pm}")
                logging.debug(f"pm_ips: {pm_ips}")

            # DO DNS lookup of ip
            pm_hostname = [ip_lookup(ip) for ip in pm_ips]
            logging.debug(f"pm_hostname: {pm_hostname}")
        else:
            pm_ips = None
    except Exception as e:
        logging.info(f"Error: {e}")

    logging.debug(f"return: {pm_ips}")
    return pm_ips


def ip_lookup(addr):
    """
    Convert an IP address to a host name, returning shortname and fqdn to the
    caller
    """

    try:
        fqdn = socket.gethostbyaddr(addr)[0]
        shortname = fqdn.split(".")[0]
        if fqdn == shortname:
            fqdn = ""

    except Exception as e:

        logging.debug(f"Exception: {e}")

        # can't resolve it, so default to the address given
        shortname = addr
        fqdn = "None"

    logging.debug(f"input: {addr}, hostname: {shortname}, fqdn: {fqdn}")
    return shortname, fqdn


def extract_virtual_ip(data):
    """
    Extracts the IPv4 or IPv6 address and returns ip and port
    """

    try:
        ip, port = re.search(r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|[0-9a-fA-F:]+):(\d+)", data).groups()
    except Exception as e:
        logging.error(f"extract_virtual_ip, Error: {e}")

    logging.debug(f"input: {data}, ip: {ip}, port: {port}")
    return ip, port

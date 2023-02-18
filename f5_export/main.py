import click
import logging
import os
import json

from importlib.metadata import distribution
from dotenv import load_dotenv
from f5_export.utils.bigip import connect_to_bigip, get_bigip_object, extract_virtual_ip, get_pm_ips, ip_lookup
from f5_export.utils.export import init_csv, append_csv


# Get distribution info
dist = distribution("f5_export")

# CSV Filename
csv_filename = "virtual_servers.csv"

# load .env file
load_dotenv()

# Disable proxy, do direct connection
os.environ["NO_PROXY"] = "*"

__author__ = dist.metadata["Author"]
__version__ = dist.metadata["Version"]


def setup_logger(log_file, log_level):
    """
    Configures loglevel and logfile
    """
    logging.basicConfig(
        filename=log_file,
        level=log_level,
        force=True,
        format="%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s",
        datefmt="%d-%b-%y %H:%M:%S",
    )


@click.command()
@click.option("-h", "--hostname", help="BIG-IP hostname or address", envvar="F5EXPORT_HOSTNAME", required=True)
@click.option("-u", "--username", help="BIG-IP username", envvar="F5EXPORT_USERNAME", required=True)
@click.password_option(
    confirmation_prompt=False,
    prompt_required=True,
    envvar="F5EXPORT_PASSWORD",
    default="admin",
    help=("BIG-IP password [prompted when not specified]"),
)
@click.option("-v", "--verbose", is_flag=True, default=False, help=("Enables VERBOSE mode."))
@click.option("-d", "--debug", is_flag=True, default=False, help=("Enables DEBUG mode."))
@click.option(
    "--no-ssl-verify",
    is_flag=True,
    envvar="F5EXPORT_SSLVERIFY",
    default=True,
    help=(
        "f5export uses SSL when communicating with the F5 BIG-IP."
        "This option overrides the default behavior of verifying SSL certificates."
    ),
)
@click.option(
    "--timeout",
    default=15,
    help=("Specifies the number of seconds to wait for a response from the device. (default: 15s)"),
)
@click.version_option(__version__)
def main(hostname: str, username: str, password: str, verbose: bool, debug: bool, no_ssl_verify: bool, timeout: str):
    """
    F5 export tool (f5export) is a for exporting config data to a file.
    It will export the config of a F5 BIG-IP via the REST API interface.

    You need to specifiy the hostname, username and the password
    of the F5 device for the tool to work.

    For detailed help, try this: f5export --help

    Environment variables can be used instead of passing some common global options:

        F5EXPORT_HOSTNAME - f5export hostname to connect to. ex. host:8443 to use another port.

        F5EXPORT_USERNAME - f5export username. Requires F5EXPORT_PASSWORD to be set.

        F5EXPORT_PASSWORD - Password. Requires F5EXPORT_USERNAME to be set.

        F5EXPORT_SSLVERIFY - This option overrides the default behavior of verifying SSL certificates.
    """

    vs_ip = None
    loglevel = None

    if verbose:
        loglevel = logging.INFO
    if debug:
        loglevel = logging.DEBUG

    # REST-API URLs
    vss_url = "/mgmt/tm/ltm/virtual"

    # initialize logging
    setup_logger(None, loglevel)

    # Connect to BIG-IP
    bigip = connect_to_bigip(hostname, username, password, no_ssl_verify)

    # Retrieve virtual servers information
    vss = get_bigip_object(bigip, vss_url)

    # Write header to csv
    init_csv(csv_filename)

    # Loop through virtual servers
    for vs in vss:
        vs_fullpath = vs.properties["fullPath"]

        click.secho(f"Virtual Server: {vs_fullpath}", fg="green")
        logging.debug(f"VS:\r\n{json.dumps(vs.properties, indent=4)}")

        # Extract the IPv4 or IPv6 destination address
        # if "trafficMatchingCriteriaReference" in virtual_server.properties:
        #     click.secho("Address List in use, destination unknown...", fg="red")
        #     virtual_server_ip_fullpath = (f'255.255.255.255{virtual_server.properties["destination"]}')
        # else:

        vs_ip, vs_port = extract_virtual_ip(vs.properties["destination"])

        # Use dummy ip if None
        if vs_ip is None:
            vs_ip = "0.0.0.0"

        vs_hostname, vs_fqdn = ip_lookup(vs_ip)

        pm_ips = get_pm_ips(bigip, vs)

        if pm_ips is not None:
            pm_ips_txt = ", ".join([str(elem) for elem in pm_ips])
        else:
            pm_ips_txt = "None"

        logging.debug(f"VS_Hostname: {vs_ip}, member_ips: {pm_ips}")
        append_csv(csv_filename, [vs_fullpath, vs_fqdn, pm_ips_txt])


if __name__ == "__main__":
    main()

import csv
import socket
import click
import logging

from dotenv import load_dotenv
from bigrest.bigip import BIGIP


# Get distribution info
dist = distribution("f5_export")

# load .env file
load_dotenv()

__author__ = dist.metadata["Author"]
__version__ = dist.metadata["Version"]

@click.command()
@click.option("-h", "--hostname", help="BIG-IP hostname or address", required=True)
@click.option("-u", "--username", help="BIG-IP username", required=True)
@click.password_option(
    confirmation_prompt=False,
    prompt_required=True,
    envvar="F5CMD_PASSWORD",
    default="admin",
    help=("BIG-IP password [prompted when not specified]"),
)
def main(hostname, username, password):
    # Connect to BIG-IP
    bigip = BIGIP(hostname, username, password)

    # Retrieve virtual servers information
    virtual_servers = bigip.ltm.virtuals.get_collection()

    # Open a CSV file for writing
    with open("virtual_servers.csv", "w") as csvfile:
        writer = csv.writer(csvfile)

        # Write header row
        writer.writerow(["Virtual Server IP", "Pool Member IP(s)"])

        # Loop through virtual servers
        for virtual_server in virtual_servers:
            virtual_server_ip = virtual_server.destination.split(":")[0]
            pool_name = virtual_server.pool
            pool = bigip.ltm.pools.load(name=pool_name)
            pool_members = pool.members_s.get_collection()
            member_ips = [member.address for member in pool_members]
            try:
                virtual_server_ip = socket.gethostbyaddr(virtual_server_ip)[0]
                member_ips = [socket.gethostbyaddr(ip)[0] for ip in member_ips]
            except:
                pass
            writer.writerow([virtual_server_ip] + member_ips)

if __name__ == "__main__":
    main()

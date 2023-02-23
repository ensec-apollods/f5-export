import csv
import logging


def init_csv(file_name):
    """
    Writes header to csv
    """
    header = ["VS Name", "VS FQDN", "Pool Member Hosts"]

    with open(file_name, "w", newline="") as file:
        writer = csv.writer(file)

        # Write header row
        writer.writerow(header)

    file.close()


def append_csv(file_name, data):
    """
    Writes data to a CSV file.
    """

    logging.debug(f"input: {data}")

    with open(file_name, "a", newline="") as file:
        writer = csv.writer(file)

        # Write rows
        writer.writerow(data)

    file.close()

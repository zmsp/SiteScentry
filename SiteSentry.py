import csv
import json
import shutil
import ssl
from datetime import datetime
from urllib.parse import urlparse

import OpenSSL.crypto
import gspread
import requests
import yaml


# configure logging
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger()

# read the configuration file
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)


# extract google sheets information
use_google_sheet = config['use_google_sheet']
google_sheets_config = config['google_sheets']
spreadsheet_id = google_sheets_config['spreadsheet_id']
worksheet_name = google_sheets_config['worksheet_name']

service_account_json_path = google_sheets_config['service_account_json_path']

# extract slack information
use_slack = config['use_slack']
slack_config = config['slack']
slack_username = slack_config['username']
slack_icon_emoji = slack_config['emoji']
slack_channel = slack_config["channel"]
slack_webhook_url = slack_config["webhook"]
proxyDict = config["proxyDict"]

# load file config
files_config = config['files']

current_file = files_config['current_file']
last_file = files_config['last_file']

certificate_config = config['certificate']
warning_days = certificate_config['warning_days']


def check_certificate_expiry(list_file, warn_days):
    n_time = datetime.now()
    with open(list_file, 'r') as f:
        for line in f:
            logger.info(f"checking {line}" )
            url_parts = urlparse(line.strip())
            try:
                cert = ssl.get_server_certificate((url_parts.hostname, url_parts.port or 443))
            except (TimeoutError, OSError) as e:
                logger.error(e)
                send_to_slack(
                    f"ERROR: {url_parts.hostname} {'timeout' if isinstance(e, TimeoutError) else 'network unreachable'}!")
                continue
            except Exception as e:
                logger.error(e)
                send_to_slack(f"ERROR: with {url_parts.hostname}")
                continue

            x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
            e_time = datetime.strptime(x509.get_notAfter().decode('ascii'), '%Y%m%d%H%M%SZ')
            delta = e_time - n_time
            if x509.has_expired():
                send_to_slack(f"DANGER: {url_parts.hostname} has expired {delta.days} day(s) ago!!")
            elif delta.days < warn_days:
                send_to_slack(f"WARNING: {url_parts.hostname} is expiring in {delta.days} day(s) on {e_time.date()}")


def download_csv_from_google_sheets(service_account_json_path, spreadsheet_id, worksheet_name, filename):
    # authenticate with the Google Sheets API using a service account
    gc = gspread.service_account(filename=service_account_json_path)

    # open the specified worksheet by name
    worksheet = gc.open_by_key(spreadsheet_id).worksheet(worksheet_name)

    # get all the rows of data from the worksheet
    rows = worksheet.get_all_values()

    # write the rows to a CSV file

    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(rows)

    logger.info(f"Downloaded {len(rows)} rows of data from worksheet '{worksheet_name}' to file '{filename}'")


def diff_files(file1="old.csv", file2="latest.csv"):
    with open(file1, 'r') as f1:
        with open(file2, 'r') as f2:
            # read the contents of the files into memory
            file1_contents = f1.readlines()
            file2_contents = f2.readlines()

            # compare the contents line by line
            diff_log = []
            for i, line in enumerate(file1_contents):
                if line != file2_contents[i]:
                    diff_log.append(f'Difference found on line {i + 1}:')
                    diff_log.append(f'{file1}: {line.strip()}')
                    diff_log.append(f'{file2}: {file2_contents[i].strip()}')
            return diff_log


def send_to_slack(message):
    """
    Sends message to slack
    :param message:
    """



    if not use_slack:
        logger.info(message)
        return True
    else:
        slack_data = {'text': message, 'channel': slack_channel, "username": slack_username,
                      "icon_emoji": slack_icon_emoji}
        logger.info(slack_data)

        response = requests.post(
            slack_webhook_url, data=json.dumps(slack_data),
            headers={'Content-Type': 'application/json'},
            proxies=proxyDict
        )
        if response.status_code != 200:
            raise ValueError(
                'Request to slack returned an error %s, the response is:\n%s'
                % (response.status_code, response.text)
            )


def send_diff_log_to_slack(diff_log):
    if len(diff_log) > 0:
        message = '\n'.join(diff_log)
        send_to_slack(message)


def main():
    ### ID can be found in the URL,
    try:
        if use_google_sheet:
            download_csv_from_google_sheets(service_account_json_path=service_account_json_path,
                                            spreadsheet_id=spreadsheet_id, worksheet_name=worksheet_name,
                                            filename=current_file)
            send_diff_log_to_slack(diff_files(last_file, current_file))
            shutil.copy(current_file, last_file)

        check_certificate_expiry(current_file, warning_days)
    except Exception as E:
        logger.error(E)
        send_to_slack(f"ERROR: Failed loading cert checker")


if __name__ == '__main__':
    main()

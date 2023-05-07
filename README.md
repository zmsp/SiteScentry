## About this tool
This script is a Python script that checks the expiration date of SSL/TLS certificates for a list of URLs. It can also download a list of URLs from a Google Sheet and compare it with the previous version to notify if any changes were made.



# Setup Guide for config.yaml

This guide explains how to set up the variables in the `config.yaml` file for the SiteSentry tool. 

### Files

The `files` section of the configuration file contains information about the sites to be checked

- `current_file`: The path to the CSV file containing the current state of the monitored websites.
- `last_file`: The path to the CSV file containing the last state of the monitored websites.

You can change the file paths to match the location of your files. 

### Google Sheets

If you want to use Google Sheets to store the monitored websites instead of CSV files, you can set `use_google_sheet` to `true` in the `config.yaml` file. 

To use this feature, you'll need to provide the following details in the `config.yaml` file:

- `spreadsheet_id`: The ID of the Google Sheets document. You can find this in the URL of the document. The ID is the long string of characters between "/d/" and "/edit" in the URL. For example, in the URL "https://docs.google.com/spreadsheets/d/1AbCdEfGhIjKlMnOpQrStUvWxYz/edit", the ID is "1AbCdEfGhIjKlMnOpQrStUvWxYz".
- `worksheet_name`: The name of the worksheet containing the monitored websites. This should match the name of the worksheet in the Google Sheets document.
- `service_account_json_path`: The path to the JSON file containing the credentials for accessing the Google Sheets API. This file contains the service account key that you can generate from the Google Developers Console. 

To generate a service account key, follow these steps:

1. Go to the [Google Developers Console](https://console.developers.google.com/).
2. Create a new project and enable the Google Sheets API.
3. Go to the "Credentials" section and click "Create credentials".
4. Select "Service account key" and create a new service account.
5. Download the JSON file containing the service account key and save it to a secure location.
6. Add the path to the JSON file to the `config.yaml` file as the `service_account_json_path`.

Once you have the service account key, you'll need to share the Google Sheets document with the service account email address. To do this, open the Google Sheets document and click "Share" in the top-right corner. In the "Share with others" dialog box, enter the email address associated with the service account and give it edit access.

### Slack

The `slack` section of the configuration file contains information about the Slack channel to send notifications to. 

In your Slack obtain the webhook URL for your Slack channel, you need to create a new incoming webhook integration in Slack. 
- `username`: The username to use when posting messages to Slack.
- `emoji`: The emoji to use for the username.
- `channel`: The name of the Slack channel to post messages to.
- `webhook`: The URL of the Slack webhook to use for posting messages.

### Certificate

The `certificate` section of the configuration file contains information about how many days in advance to issue warnings for expiring SSL certificates.

- `warning_days`: The number of days in advance to issue warnings for expiring SSL certificates.

You can change the number of days to match your preferences.

### Proxy

The `proxyDict` section of the configuration file contains information about a proxy server to use for connecting to the internet. 

If you need to connect to the internet through a proxy server, uncomment the section and fill in the details for the server. If you don't need to use a proxy server, leave this section commented out. 

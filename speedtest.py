#!/usr/bin/env python

from __future__ import print_function
import os
import json
import subprocess
import re
import time

import gdata
import gdata.spreadsheets.client
import gdata.spreadsheets.data
import gdata.gauth

import oauth2client
import oauth2client.client
import oauth2client.tools
import oauth2client.file

from json import load
from urllib2 import urlopen

my_ip = load(urlopen('http://jsonip.com'))['ip']

# Set constants
DIRECTORY = os.path.dirname(os.path.realpath(__file__))
SCOPES = "https://spreadsheets.google.com/feeds/"
APPLICATION_NAME = "google-speedtest-chart"

#DOWNLOAD_RE = re.compile(r"Download: ([\d.]+) .bit")
#UPLOAD_RE = re.compile(r"Upload: ([\d.]+) .bit")
#PING_RE = re.compile(r"([\d.]+) ms")
DOWNLOAD_RE = re.compile(r"Download: ([\d.]+) .bit")
UPLOAD_RE = re.compile(r"Upload: ([\d.]+) .bit")
PING_RE = re.compile(r"Ping: ([\d.]+) ms")

# Parse possible args (--noauth_local_webserver)
try:
    import argparse
    flags = argparse.ArgumentParser(
        parents=[oauth2client.tools.argparser]).parse_args()
except ImportError:
    flags = None

# Load config file
with open(os.path.join(DIRECTORY, "config.json"), "r") as configfile:
    config = json.load(configfile)

# Function to check for valid OAuth access tokens
def get_credentials():
    home_dir = os.path.expanduser("~")
    credential_dir = os.path.join(home_dir, ".credentials")
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, "drive-python-quickstart.json")

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        print("--------")
        flow = oauth2client.client.flow_from_clientsecrets(
            os.path.join(DIRECTORY, config["client_secret_file"]), SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = oauth2client.tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = oauth2client.tools.run(flow, store)
        print("Storing credentials to " + credential_path)
        print("--------")
    return credentials

# Function to submit speedtest result
def submit_into_spreadsheet(pingvthn,downloadvthn,uploadvthn,pingvthcm,downloadvthcm,uploadvthcm,pingvnpthn,
                            downloadvnpthn,uploadvnpthn,pingnetnamhn,downloadnetnamhn,uploadnetnamhn,pingcmchn,
                            downloadcmchn,uploadcmchn,pingvtchn,downloadvtchn,uploadvtchn,pingmobihn,downloadmobihn,
                            uploadmobihn,pingsgphn,downloadsgphn,uploadsgphn,pingvnptdn,downloadvnptdn,uploadvnptdn,
                            pingvtdn,downloadvtdn,uploadvtdn,pingvsgpdn,downloadsgpdn,uploadsgpdn,pingfpthcm,
                            downloadfpthcm,uploadfpthcm,pingnetnamhcm,downloadnetnamhcm,uploadnetnamhcm,pingsgphcm,
                            downloadsgphcm,uploadsgphcm,pingmobihcm,downloadmobihcm,uploadmobihcm,pingvtchcm,
                            downloadvtchcm,uploadvtchcm,pingsctvhcm,downloadsctvhcm,uploadsctvhcm):
    credentials = get_credentials()

    # create the spreadsheet client and authenticate
    spr_client = gdata.spreadsheets.client.SpreadsheetsClient()
    auth2token = gdata.gauth.OAuth2TokenFromCredentials(credentials)
    spr_client = auth2token.authorize(spr_client)

    # Prepare dictionary
    data = {
        "date": time.strftime("%m/%d/%Y %H:%M:%S"),
        "ipaddress":my_ip,
        "pingvthn": pingvthn,
        "downloadvthn": downloadvthn,
        "uploadvthn": uploadvthn,
        "pingvthcm": pingvthcm,
        "downloadvthcm": downloadvthcm,
        "uploadvthcm": uploadvthcm,
        "pingvnpthn": pingvnpthn,
        "downloadvnpthn": downloadvnpthn,
        "uploadvnpthn": uploadvnpthn,
        "pingnetnamhn": pingnetnamhn,
        "downloadnetnamhn":downloadnetnamhn,
        "uploadnetnamhn":uploadnetnamhn,
        "pingcmchn": pingcmchn,
        "downloadcmchn":downloadcmchn,
        "uploadcmchn":uploadcmchn,
        "pingvtchn":pingvtchn ,
        "downloadvtchn":downloadvtchn,
        "uploadvtchn": uploadvtchn,
        "pingmobihn":pingmobihn,
        "downloadmobihn":downloadmobihn,
        "uploadmobihn":uploadmobihn,
        "pingsgphn":pingsgphn,
        "downloadsgphn":downloadsgphn,
        "uploadsgphn":uploadsgphn,
        "pingvnptdn":pingvnptdn,
        "downloadvnptdn":downloadvnptdn,
        "uploadvnptdn":uploadvnptdn,
        "pingvtdn":pingvtdn,
        "downloadvtdn":downloadvtdn,
        "uploadvtdn":uploadvtdn,
        "pingvsgpdn":pingvsgpdn,
        "downloadsgpdn":downloadsgpdn,
        "uploadsgpdn":uploadsgpdn,
        "pingfpthcm":pingfpthcm,
        "downloadfpthcm":downloadfpthcm,
        "uploadfpthcm":uploadfpthcm,
        "pingnetnamhcm":pingnetnamhcm,
        "downloadnetnamhcm":downloadnetnamhcm,
        "uploadnetnamhcm":uploadnetnamhcm,
        "pingsgphcm":pingsgphcm,
        "downloadsgphcm":downloadsgphcm,
        "uploadsgphcm":uploadsgphcm,
        "pingmobihcm":pingmobihcm,
        "downloadmobihcm":downloadmobihcm,
        "uploadmobihcm":uploadmobihcm,
        "pingvtchcm":pingvtchcm,
        "downloadvtchcm":downloadvtchcm,
        "uploadvtchcm":uploadvtchcm,
        "pingsctvhcm":pingsctvhcm,
        "downloadsctvhcm":downloadsctvhcm,
        "uploadsctvhcm":uploadsctvhcm,
    }

    print(data)
    with open('/var/log/vccloudnet.log', 'a') as outfile:
	json.dump(data, outfile)
        outfile.write('\n')

    entry = gdata.spreadsheets.data.ListEntry()
    entry.from_dict(data)

    # add the ListEntry you just made
    spr_client.add_list_entry(entry, config["spreadsheet_id"], config["worksheet_id"])

# Main function to run speedtest
def main():
    # Check for proper credentials
    print("Checking OAuth validity ... ")

    credentials = get_credentials()

    # Run speedtest and store output

    print("Starting speed test VIETTEL HN... ")
    try:
        speedtest_result_vthn = subprocess.check_output(["speedtest-cli", "--server", "9903", "--simple"],
                                                     stderr=subprocess.STDOUT)
        # Find download bandwidth
        downloadvthn = DOWNLOAD_RE.search(speedtest_result_vthn).group(1)
        # Find upload bandwidth
        uploadvthn = UPLOAD_RE.search(speedtest_result_vthn).group(1)
        # Find ping latency
        pingvthn = PING_RE.search(speedtest_result_vthn).group(1)
    except Exception:
        downloadvthn = 0.0
        # Find upload bandwidth
        uploadvthn = 0.0
        # Find ping latency
        pingvthn = 0.0
    print("Starting VTHN speed finished!")



    print("Starting speed test VIETTEL HCM... ")
    try:
        speedtest_result_vthcm = subprocess.check_output(["speedtest-cli", "--server", "2427", "--simple"], stderr=subprocess.STDOUT)
        # Find download bandwidth
        downloadvthcm = DOWNLOAD_RE.search(speedtest_result_vthcm).group(1)
        # Find upload bandwidth
        uploadvthcm = UPLOAD_RE.search(speedtest_result_vthcm).group(1)
        # Find ping latency
        pingvthcm = PING_RE.search(speedtest_result_vthcm).group(1)
    except Exception:
        downloadvthcm = 0.0
        # Find upload bandwidth
        uploadvthcm = 0.0
        # Find ping latency
        pingvthcm = 0.0
    print("Starting VTHCM speed finished!")



    print("Starting speed test VNPT-NET HANOI... ")
    try:
        speedtest_result_vnpthn = subprocess.check_output(["speedtest-cli", "--server", "6085", "--simple"], stderr=subprocess.STDOUT)
        # Find download bandwidth
        downloadvnpthn = DOWNLOAD_RE.search(speedtest_result_vnpthn).group(1)
        # Find upload bandwidth
        uploadvnpthn = UPLOAD_RE.search(speedtest_result_vnpthn).group(1)
        # Find ping latency
        pingvnpthn = PING_RE.search(speedtest_result_vnpthn).group(1)
    except Exception:
        downloadvnpthn = 0.0
        # Find upload bandwidth
        uploadvnpthn = 0.0
        # Find ping latency
        pingvnpthn = 0.0
    print("Starting VNPTHN speed finished!")

    print("Starting speed test VNPT-NET HCM... ")
    try:
        speedtest_result_vnpthcm = subprocess.check_output(["speedtest-cli", "--server", "6106", "--simple"], stderr=subprocess.STDOUT)
        # Find download bandwidth
        downloadvnpthcm = DOWNLOAD_RE.search(speedtest_result_vnpthcm).group(1)
        # Find upload bandwidth
        uploadvnpthcm = UPLOAD_RE.search(speedtest_result_vnpthcm).group(1)
        # Find ping latency
        pingvnpthcm = PING_RE.search(speedtest_result_vnpthcm).group(1)
    except Exception:
        downloadvnpthcm = 0.0
        # Find upload bandwidth
        uploadvnpthcm = 0.0
        # Find ping latency
        pingvnpthcm = 0.0
    print("Starting VNPT-NET HCM speed finished!")



    print("Starting speed test NetNam Corp HANOI... ")
    try:
        speedtest_result_netnamhn = subprocess.check_output(["speedtest-cli", "--server", "5774", "--simple"], stderr=subprocess.STDOUT)
        # Find download bandwidth
        downloadnetnamhn = DOWNLOAD_RE.search(speedtest_result_netnamhn).group(1)
        # Find upload bandwidth
        uploadnetnamhn = UPLOAD_RE.search(speedtest_result_netnamhn).group(1)
        # Find ping latency
        pingnetnamhn = PING_RE.search(speedtest_result_netnamhn).group(1)
    except Exception:
        downloadnetnamhn = 0.0
        # Find upload bandwidth
        uploadnetnamhn = 0.0
        # Find ping latency
        pingnetnamhn = 0.0
    print("Starting NetNam Corp HANOI speed finished!")



    print("Starting speed test  CMC HANOI... ")
    try:
        speedtest_result_cmchn = subprocess.check_output(["speedtest-cli", "--server", "6342", "--simple"], stderr=subprocess.STDOUT)
        # Find download bandwidth
        downloadcmchn = DOWNLOAD_RE.search(speedtest_result_cmchn).group(1)
        # Find upload bandwidth
        uploadcmchn = UPLOAD_RE.search(speedtest_result_cmchn).group(1)
        # Find ping latency
        pingcmchn = PING_RE.search(speedtest_result_cmchn).group(1)
    except Exception:
        downloadcmchn = 0.0
        # Find upload bandwidth
        uploadcmchn = 0.0
        # Find ping latency
        pingcmchn = 0.0
    print("Starting CMC HANOI speed finished!")

    print("Starting speed test VTC HANOI... ")
    try:
        speedtest_result_vtchn = subprocess.check_output(["speedtest-cli", "--server", "8156", "--simple"], stderr=subprocess.STDOUT)
        # Find download bandwidth
        downloadvtchn = DOWNLOAD_RE.search(speedtest_result_vtchn).group(1)
        # Find upload bandwidth
        uploadvtchn = UPLOAD_RE.search(speedtest_result_vtchn).group(1)
        # Find ping latency
        pingvtchn = PING_RE.search(speedtest_result_vtchn).group(1)

    except Exception:
        downloadvtchn = 0.0
        uploadvtchn = 0.0
        pingvtchn = 0.0
    print("Starting VTC HANOI speed finished!")

    print("Starting speed test MOBIFONE HANOI... ")
    try:
        speedtest_result_mobihn = subprocess.check_output(["speedtest-cli", "--server", "9174", "--simple"], stderr=subprocess.STDOUT)
        # Find download bandwidth
        downloadmobihn = DOWNLOAD_RE.search(speedtest_result_mobihn).group(1)
        # Find upload bandwidth
        uploadmobihn = UPLOAD_RE.search(speedtest_result_mobihn).group(1)
        # Find ping latency
        pingmobihn = PING_RE.search(speedtest_result_mobihn).group(1)
    except Exception:
        downloadmobihn = 0.0
        uploadmobihn = 0.0
        pingmobihn = 0.0
    print("Starting VNPTHN speed finished!")

    print("Starting speed test SAIGON POSTEL CORP HANOI... ")
    try:
        speedtest_result_sgphn = subprocess.check_output(["speedtest-cli", "--server", "7215", "--simple"], stderr=subprocess.STDOUT)
        # Find download bandwidth
        downloadsgphn = DOWNLOAD_RE.search(speedtest_result_sgphn).group(1)
        # Find upload bandwidth
        uploadsgphn = UPLOAD_RE.search(speedtest_result_sgphn).group(1)
        # Find ping latency
        pingsgphn = PING_RE.search(speedtest_result_sgphn).group(1)
    except Exception:
        downloadsgphn = 0.0
        uploadsgphn = 0.0
        pingsgphn = 0.0
    print("Starting VNPTHN speed finished!")

    print("Starting speed test VNPT-NET Da Nang... ")
    try:
        speedtest_result_vnptdn = subprocess.check_output(["speedtest-cli", "--server", "6102", "--simple"], stderr=subprocess.STDOUT)
        # Find download bandwidth
        downloadvnptdn = DOWNLOAD_RE.search(speedtest_result_vnptdn).group(1)
        # Find upload bandwidth
        uploadvnptdn = UPLOAD_RE.search(speedtest_result_vnptdn).group(1)
        # Find ping latency
        pingvnptdn = PING_RE.search(speedtest_result_vnptdn).group(1)
    except Exception:
        downloadvnptdn = 0.0
        uploadvnptdn = 0.0
        pingvnptdn = 0.0
    print("Starting VNPTHN speed finished!")

    print("Starting speed test VIETTEL Da Nang... ")
    try:
        speedtest_result_vtdn = subprocess.check_output(["speedtest-cli", "--server", "10040", "--simple"], stderr=subprocess.STDOUT)
        # Find download bandwidth
        downloadvtdn = DOWNLOAD_RE.search(speedtest_result_vtdn).group(1)
        # Find upload bandwidth
        uploadvtdn = UPLOAD_RE.search(speedtest_result_vtdn).group(1)
        # Find ping latency
        pingvtdn = PING_RE.search(speedtest_result_vtdn).group(1)
    except Exception:
        downloadvtdn = 0.0
        # Find upload bandwidth
        uploadvtdn = 0.0
        # Find ping latency
        pingvtdn = 0.0
    print("Starting VIETTEL Da Nang speed finished!")

    print("Starting speed test SAIGON POSTEL CORP. Da Nang... ")
    try:
        speedtest_result_sgpdn = subprocess.check_output(["speedtest-cli", "--server", "6758", "--simple"], stderr=subprocess.STDOUT)
        # Find download bandwidth
        downloadsgpdn = DOWNLOAD_RE.search(speedtest_result_sgpdn).group(1)
        # Find upload bandwidth
        uploadsgpdn = UPLOAD_RE.search(speedtest_result_sgpdn).group(1)
        # Find ping latency
        pingvsgpdn= PING_RE.search(speedtest_result_sgpdn).group(1)
    except Exception:
        downloadsgpdn = 0.0
        # Find upload bandwidth
        uploadsgpdn = 0.0
        # Find ping latency
        pingvsgpdn = 0.0
    print("Starting SAIGON POSTEL CORP. Da Nang speed finished!")



    print("Starting speed test FPT Telecom (Ho Chi Minh... ")
    try:
        speedtest_result_fpthcm = subprocess.check_output(["speedtest-cli", "--server", "2515", "--simple"], stderr=subprocess.STDOUT)
        # Find download bandwidth
        downloadfpthcm = DOWNLOAD_RE.search(speedtest_result_fpthcm).group(1)
        # Find upload bandwidth
        uploadfpthcm = UPLOAD_RE.search(speedtest_result_fpthcm).group(1)
        # Find ping latency
        pingfpthcm = PING_RE.search(speedtest_result_fpthcm).group(1)
    except Exception:
        downloadfpthcm = 0.0
        # Find upload bandwidth
        uploadfpthcm = 0.0
        # Find ping latency
        pingfpthcm = 0.0
    print("Starting FPT Telecom (Ho Chi Minh speed finished!")


    print("Starting speed test NetNam (Ho Chi Minh... ")
    try:
        speedtest_result_netnamhcm = subprocess.check_output(["speedtest-cli", "--server", "3381", "--simple"], stderr=subprocess.STDOUT)
        # Find download bandwidth
        downloadnetnamhcm = DOWNLOAD_RE.search(speedtest_result_netnamhcm).group(1)
        # Find upload bandwidth
        uploadnetnamhcm = UPLOAD_RE.search(speedtest_result_netnamhcm).group(1)
        # Find ping latency
        pingnetnamhcm = PING_RE.search(speedtest_result_netnamhcm).group(1)
    except Exception:
        downloadnetnamhcm = 0.0
        # Find upload bandwidth
        uploadnetnamhcm = 0.0
        # Find ping latency
        pingnetnamhcm = 0.0
    print("Starting NetNam (Ho Chi Minh speed finished!")

    print("Starting speed test SAIGON POSTEL CORP. (Ho Chi Minh ... ")
    try:
        speedtest_result_sgphcm = subprocess.check_output(["speedtest-cli", "--server", "6378", "--simple"], stderr=subprocess.STDOUT)
        # Find download bandwidth
        downloadsgphcm = DOWNLOAD_RE.search(speedtest_result_sgphcm).group(1)
        # Find upload bandwidth
        uploadsgphcm = UPLOAD_RE.search(speedtest_result_sgphcm).group(1)
        # Find ping latency
        pingsgphcm = PING_RE.search(speedtest_result_sgphcm).group(1)
    except Exception:
        downloadsgphcm = 0.0
        # Find upload bandwidth
        uploadsgphcm = 0.0
        # Find ping latency
        pingsgphcm = 0.0
    print("Starting SAIGON POSTEL CORP. (Ho Chi Minh speed finished!")

    print("Starting speed test MOBIFONE (Ho Chi Minh ... ")
    try:
        speedtest_result_mobihcm = subprocess.check_output(["speedtest-cli", "--server", "9331", "--simple"], stderr=subprocess.STDOUT)
        # Find download bandwidth
        downloadmobihcm = DOWNLOAD_RE.search(speedtest_result_mobihcm).group(1)
        # Find upload bandwidth
        uploadmobihcm = UPLOAD_RE.search(speedtest_result_mobihcm).group(1)
        # Find ping latency
        pingmobihcm = PING_RE.search(speedtest_result_mobihcm).group(1)
    except Exception:
        downloadmobihcm = 0.0
        # Find upload bandwidth
        uploadmobihcm = 0.0
        # Find ping latency
        pingmobihcm = 0.0
    print("Starting MOBIFONE (Ho Chi Minh speed finished!")

    print("Starting speed test VTC DIGICOM Ho Chi Minh City ... ")
    try:
        speedtest_result_vtchcm = subprocess.check_output(["speedtest-cli", "--server", "8158", "--simple"], stderr=subprocess.STDOUT)
        # Find download bandwidth
        downloadvtchcm = DOWNLOAD_RE.search(speedtest_result_vtchcm).group(1)
        # Find upload bandwidth
        uploadvtchcm = UPLOAD_RE.search(speedtest_result_vtchcm).group(1)
        # Find ping latency
        pingvtchcm = PING_RE.search(speedtest_result_vtchcm).group(1)
    except Exception:
        downloadvtchcm = 0.0
        # Find upload bandwidth
        uploadvtchcm = 0.0
        # Find ping latency
        pingvtchcm = 0.0
    print("Starting VTC DIGICOM Ho Chi Minh City speed finished!")

    print("Starting speed test SCTV Co.Ltd (Ho Chi Minh City ... ")
    try:
        speedtest_result_sctvhcm = subprocess.check_output(["speedtest-cli", "--server", "8491", "--simple"], stderr=subprocess.STDOUT)
        # Find download bandwidth
        downloadsctvhcm = DOWNLOAD_RE.search(speedtest_result_sctvhcm).group(1)
        # Find upload bandwidth
        uploadsctvhcm = UPLOAD_RE.search(speedtest_result_sctvhcm).group(1)
        # Find ping latency
        pingsctvhcm = PING_RE.search(speedtest_result_sctvhcm).group(1)
    except Exception:
        downloadsctvhcm = 0.0
        # Find upload bandwidth
        uploadsctvhcm = 0.0
        # Find ping latency
        pingsctvhcm = 0.0
    print("Starting SCTV Co.Ltd (Ho Chi Minh City speed finished!")



    # Write to spreadsheet
    print("Writing to spreadsheet ...")
    submit_into_spreadsheet(pingvthn,downloadvthn,uploadvthn,pingvthcm,downloadvthcm,uploadvthcm,pingvnpthn,
                            downloadvnpthn,uploadvnpthn,pingnetnamhn,downloadnetnamhn,uploadnetnamhn,pingcmchn,
                            downloadcmchn,uploadcmchn,pingvtchn,downloadvtchn,uploadvtchn,pingmobihn,downloadmobihn,
                            uploadmobihn,pingsgphn,downloadsgphn,uploadsgphn,pingvnptdn,downloadvnptdn,uploadvnptdn,
                            pingvtdn,downloadvtdn,uploadvtdn,pingvsgpdn,downloadsgpdn,uploadsgpdn,pingfpthcm,
                            downloadfpthcm,uploadfpthcm,pingnetnamhcm,downloadnetnamhcm,uploadnetnamhcm,pingsgphcm,
                            downloadsgphcm,uploadsgphcm,pingmobihcm,downloadmobihcm,uploadmobihcm,pingvtchcm,
                            downloadvtchcm,uploadvtchcm,pingsctvhcm,downloadsctvhcm,uploadsctvhcm)
    print("Successfuly written to spreadsheet!")

if __name__ == "__main__":
    main()

import sys
import logging
import os
import re

#progressie bar
def printProgress(times, total, prefix='', suffix='', decimals=2, barLength=50):
    fraction = times / float(total)
    filledLength = int(round(barLength * fraction))
    bar = '#' * filledLength + '-' * (barLength - filledLength)
    percent = round(100.00 * fraction, decimals)
    sys.stdout.write(f"{prefix} [{bar}] {percent}% {suffix}\r")
    sys.stdout.flush()
    if times == total:
        print("\n")

#string functies
def strings(filename, directory, min_length=4):
    strings_file = os.path.join(directory, "strings.txt")
    path = os.path.join(directory, filename)
    try:
        with open(path, 'rb') as infile:
            content = infile.read().decode('Latin-1', errors='ignore')
            str_list = re.findall(r"[ -~]{%d,}" % min_length, content)  # regex
            with open(strings_file, "a", encoding='utf-8') as st:
                for string in str_list:
                    logging.debug(f"String found: {string}")
                    st.write(f"{string}\n")
    except Exception as e:
        logging.error(f"Error processing file {filename}: {e}")

#dit is nog een test
def on_message(message, data):
    if message['type'] == 'send':
        print("[*] {0}".format(message['payload']))
    elif message['type'] == 'error':
        print("[!] {0}".format(message['stack']))

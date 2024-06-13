import textwrap
import frida
import os
import sys
import dumper
import utils
import argparse
import logging
import psutil 
from dumper import merge_dumps

logo = """
  ______ _               _                                                                                    
 / _____) |             | |                                                                                   
( (____ | |__  _____  __| |_____ ____                                                                         
 \____ \|  _ \(____ |/ _  | ___ |    \                                                                        
 _____) ) | | / ___ ( (_| | ____| | | |                                                                      
(______/|_| |_\_____|\____|_____)_|_|_|                                                                      
                                                                                                             
  ______                                       _______                                           _             
(_____ \                                     (_______)                                         (_)            
 _____) )_____ _   _ _____  ____ ___ _____    _____   ____   ____ _____ ____  _____ _____  ____ _ ____   ____ 
|  __  /| ___ | | | | ___ |/ ___)___) ___ |  |  ___) |  _ \ / _  | ___ |  _ \| ___ | ___ |/ ___) |  _ \ / _  |
| |  \ \| ____|\ V /| ____| |  |___ | ____|  | |_____| | | ( (_| | ____| | | | ____| ____| |   | | | | ( (_| |
|_|   |_|_____) \_/ |_____)_|  (___/|_____)  |_______)_| |_|\___ |_____)_| |_|_____)_____)_|   |_|_| |_|\___ |
                                                           (_____|                                     (_____| 
"""

def get_process_list():
    """Haalt de lijst van lopende processen op en retourneert deze."""
    process_list = []
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            process_list.append((proc.info['pid'], proc.info['name']))
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return process_list

def choose_process():
    """Presenteert de gebruiker een lijst van processen om uit te kiezen."""
    process_list = get_process_list()
    print("Beschikbare processen:")
    for idx, (pid, name) in enumerate(process_list):
        print(f"[{idx}] {name} (PID: {pid})")

    choice = int(input("Kies het nummer van het proces dat je wilt injecteren: "))
    return process_list[choice]  

def MENU():
    parser = argparse.ArgumentParser(
        prog='fridump',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent("""
        Fridump: Een tool voor het injecteren en dumpen van geheugendumps van een proces.

        Commands:
        process            De naam van het proces dat je wilt injecteren.
        
        Opties:
        -o, --out          Specificeer de uitvoermap. Standaard is 'dump' in de huidige map.
        -U, --usb          Verbind met een apparaat via USB.
        -v, --verbose      Zet het log-niveau op debug voor gedetailleerde logs.
        -r, --read-only    Dump alleen de read-only gedeeltes van het geheugen.
        -s, --strings      Voer een strings-analyse uit op alle dump bestanden.
        --max-size         Stel de maximale grootte in van een dump bestand in bytes (standaard: 20971520).
        """))

    parser.add_argument('-o', '--out', type=str, metavar="dir",
                        help='Specificeer de uitvoermap. Standaard is \'dump\' in de huidige map.')
    parser.add_argument('-U', '--usb', action='store_true',
                        help='Verbind met een apparaat via USB.')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Zet het log-niveau op debug voor gedetailleerde logs.')
    parser.add_argument('-r', '--read-only', action='store_true',
                        help='Dump alleen de read-only gedeeltes van het geheugen.')
    parser.add_argument('-s', '--strings', action='store_true',
                        help='Voer een strings-analyse uit op alle dump bestanden.')
    parser.add_argument('--max-size', type=int, metavar="bytes",
                        help='Stel de maximale grootte in van een dump bestand in bytes (standaard: 20971520).')
    args = parser.parse_args()
    return args

print(logo)
arguments = MENU()

#laat de gebruiker een proces kiezen
if len(sys.argv) == 1:
    pid, APP_NAME = choose_process()
else:
    APP_NAME = sys.argv[1]
    pid = None  #user heeft een naam opgegeven, PID is niet nodig

DIRECTORY = ""
USB = arguments.usb
DEBUG_LEVEL = logging.INFO
STRINGS = arguments.strings
MAX_SIZE = 20971520
PERMS = 'rw-'

if arguments.read_only:
    PERMS = 'r--'

if arguments.verbose:
    DEBUG_LEVEL = logging.DEBUG
logging.basicConfig(format='%(levelname)s:%(message)s', level=DEBUG_LEVEL)

#start een nieuwe sessie
session = None
try:
    if USB:
        if pid:
            session = frida.get_usb_device().attach(pid)
        else:
            session = frida.get_usb_device().attach(APP_NAME)
    else:
        if pid:
            session = frida.attach(pid)
        else:
            session = frida.attach(APP_NAME)
except frida.ProcessNotFoundError:
    print(f"Process '{APP_NAME}' not found. Please make sure the process name or PID is correct.")
    logging.debug(f"Process '{APP_NAME}' not found.")
    sys.exit(1)
except frida.PermissionDeniedError:
    print(f"Permission denied when trying to attach to '{APP_NAME}'. Try running as administrator.")
    logging.debug(f"Permission denied for process '{APP_NAME}'.")
    sys.exit(1)
except Exception as e:
    print(f"Can't connect to App. Have you connected the device? Error: {str(e)}")
    logging.debug(str(e))
    sys.exit(1)

#directory waar de output komt
if arguments.out is not None:
    DIRECTORY = arguments.out
    if os.path.isdir(DIRECTORY):
        print("Output directory is set to: " + DIRECTORY)
    else:
        print("The selected output directory does not exist!")
        sys.exit(1)
else:
    print("Current Directory: " + str(os.getcwd()))
    DIRECTORY = os.path.join(os.getcwd(), "dump")
    print("Output directory is set to: " + DIRECTORY)
    if not os.path.exists(DIRECTORY):
        print("Creating directory...")
        os.makedirs(DIRECTORY)

mem_access_viol = ""
print("Starting Memory dump...")

script = session.create_script(
    """'use strict';
    rpc.exports = {
      enumerateRanges: function (prot) {
        return Process.enumerateRangesSync(prot);
      },
      readMemory: function (address, size) {
        return Memory.readByteArray(ptr(address), size);
      }
    };
    """)
script.on("message", utils.on_message)
script.load()

agent = script.exports_sync
ranges = agent.enumerate_ranges(PERMS)

if arguments.max_size is not None:
    MAX_SIZE = arguments.max_size

i = 0
l = len(ranges)

for range in ranges:
    base = range["base"]
    size = range["size"]

    logging.debug("Base Address: " + str(base))
    logging.debug("Size: " + str(size))

    if size > MAX_SIZE:
        logging.debug("Too big, splitting the dump into chunks")
        mem_access_viol = dumper.splitter(agent, base, size, MAX_SIZE, mem_access_viol, DIRECTORY)
        continue
    mem_access_viol = dumper.dump_to_file(agent, base, size, mem_access_viol, DIRECTORY)
    i += 1
    utils.printProgress(i, l, prefix='Progress:', suffix='Complete', barLength=50)
print("")

if STRINGS:
    files = os.listdir(DIRECTORY)
    i = 0
    l = len(files)
    print("Running strings on all files:")
    for f1 in files:
        utils.strings(f1, DIRECTORY)
        i += 1
        utils.printProgress(i, l, prefix='Progress:', suffix='Complete', barLength=50)
print("Finished!")

#samenvoegen van dumps
output_file_path = os.path.join(DIRECTORY, "merged_dump.data")
merge_dumps(DIRECTORY, output_file_path)
print(f"All dumps have been merged into {output_file_path}")

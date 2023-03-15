#!/usr/bin/ python

import re
import subprocess
import optparse
from pwn import *

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")
    (options, arguments) = parser.parse_args()

    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info")
    # elif not options.new_mac:
    #     parser.error("[-] Please specify new MAC address, use --help for more info")
    return options


def change_mac(interface, new_mac):
    log.info(f"Changing MAC address for {interface} to {new_mac}")

    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])


def get_current_mac(interface):
    ifconfig_results = subprocess.check_output(["ifconfig", interface])
    new_mac_address = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_results))
    if new_mac_address:
        return new_mac_address.group(0)
    else:
        log.warning("Could not read MAC address.")


options = get_arguments()

interface = options.interface
org_mac = "00:0c:29:7f:05:7d"
new_mac = "00:1b:18:6e:04:6c"

current_mac = get_current_mac(interface)
log.success(str("Current MAC address: " + current_mac))

change_mac(interface, new_mac)

current_mac = get_current_mac(interface)
if current_mac == new_mac:
    log.success(str("MAC address was successfully changed to " + current_mac))
else:
    log.warning("MAC address did not get changed")

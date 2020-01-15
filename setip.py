import sys
import os
from os.path import expanduser
import re

IP_REGEX = 'http://(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\:[0-9]+'

def modify_server_address(path, address):
    if not address.startswith('http://'):
        address = 'http://' + address
    if address.count(':') < 2:
        address = address + ':80'

    pattern = re.compile(IP_REGEX)
    if (not pattern.match(address)):
        sys.exit("Server address is not valid. Type -h for help.")

    for dirName, subDirList, fileList in os.walk(path):
        for fname in fileList:
            if (not fname.endswith('.js')) and (not fname.endswith('.map')):
                continue
            with open("%s/%s" % (dirName, fname), 'r+') as f:
                content = f.read()
                replaced_content = re.sub(IP_REGEX, address, content)
                f.seek(0)
                f.write(replaced_content)
                f.truncate()
                
    print ('Server address is modified to', address)

def help():
    print("Usage: python3 setip.py --src [path to index.html directory] --address [address]")
    print("Example: python3 setip.py --src ./website/frontend/build --address 127.0.0.1:8000")

def run():
    if '-h' in sys.argv or '--help' in sys.argv:
        help()
        return

    path = './website/frontend/build'
    if '-s' in sys.argv:
        index = sys.argv.index('-s')
        path = sys.argv[index + 1]

    elif '--src' in sys.argv:
        index = sys.argv.index('--src')
        path = sys.argv[index + 1]

    address = ''
    if '-a' in sys.argv:
        index = sys.argv.index('-a')
        address = sys.argv[index + 1]

    elif '--address' in sys.argv:
        index = sys.argv.index('--address')
        address = sys.argv[index + 1]

    else:
        sys.exit("Please specify server address. Type -h for help.")

    modify_server_address(path, address)

if __name__ == "__main__":
    run()
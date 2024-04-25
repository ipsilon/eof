#!/usr/bin/env python

# Filters geth snapshot dump...
#
#    geth snapshot dump --nostorage | malicious_bytes_spanscan.py

import fileinput
import json

from .malicious_bytes_analysis import get_offsets_of_malicious_bytes

for line in fileinput.input():
    account = json.loads(line)
    try:
        code = bytes.fromhex(account['code'][2:])
        offsets = get_offsets_of_malicious_bytes(code)
        print(" ".join(map(str, offsets)))
    except KeyError as e:
        if e.args[0] == 'code':
            pass



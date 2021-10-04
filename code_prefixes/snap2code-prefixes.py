#!/usr/bin/env python

# Filters geth snapshot dump and collects 4-byte code prefixes of all accounts.
#
#    geth snapshot dump --nostorage | snap2code-prefixes.py > code-prefixes.txt

import collections
import fileinput
import json

prefixes = collections.defaultdict(int)

for line in fileinput.input():
    account = json.loads(line)
    try:
        code = account['code']
        prefix = code[2:10]
        prefixes[prefix] += 1
    except KeyError as e:
        if e.args[0] == 'code':
            pass

for prefix, count in prefixes.items():
    print(f"{prefix:8}: {count}")

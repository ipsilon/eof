import sys
import os
import json

sys.path.insert(0, os.getcwd())

import eips_code.eip3540 as eip3540
import eips_code.eip4750 as eip4750

USAGE = """
eof_dasm <eof_bytecode> - where <eof_bytecode> is a hex string
"""

def consume(code, ln, number=False):
    value = code[:ln]
    code = code[ln:]

    if number:
        value = int.from_bytes(value, 'big')

    return value, code

def getIO(code):
    ios = []
    while len(code) > 0:
        i, code = consume(code, 1, True)
        o, code = consume(code, 1, True)
        ios.append((i,o))
    return ios

def disect_eof(code):
    # Get version
    _ , code = consume(code, 1)
    version, code = consume(code, 2, True)

    # Get section header
    section_names = { 0x01: "Code", 0x02: "Data", 0x03: "Types" }

    section, code = consume(code, 1, True)
    section_defs = []
    while section != 0x00:
        length, code = consume(code, 2, True)
        section_defs.append({ section_names[section] : { "length": length }})
        section, code = consume(code, 1, True)

    # Get sections contents
    sections = []
    for section in section_defs:
        section_id = list(section.keys())[0]
        section_len = section[section_id]['length']
        content, code = consume(code, section_len )

        if section_id == "Code":
            sections.append({section_id: {'length': section_len, 'code': content.hex()}})
        if section_id == "Data":
            sections.append({section_id: {'length': section_len, 'content': content.hex()}})
        if section_id == "Types":
            ios = getIO(content)
            sections.append({ section_id: {'length': section_len, 'io': ios }})

    return json.dumps({ 'version': version, 'sections': sections})

def is_valid_eof(code):
    result = False
    message = ""
    if eip3540.is_eof(code):
        try:
            eip4750.validate_eof(code)
            return True, message
        except eip4750.ValidationException as ve:
            message=ve
    else:
        message = "Invalid EOF"
    return result,message

def main():
    if len(sys.argv) != 2:
        print(USAGE)
        exit()
    eof_code = sys.argv[1]
    if eof_code[0:2] == "0x": eof_code = eof_code[2:]

    try:
        eof_code = bytes.fromhex(eof_code)
    except ValueError as ve:
        print("Error:", ve)
        exit(1)

    valid, msg = is_valid_eof(eof_code)
    if valid:
        result = disect_eof(eof_code)
        print(result)
    else:
        print("Error:", msg)


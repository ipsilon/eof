from eip4750 import *
from eip5450 import validate_function, FunctionType


# EOF code validation, including container format validation, code section validation and function stack validation.
# Raises ValidationException on invalid code
def validate_eof1(container: bytes):
    validate_eof(container)

    section_sizes, header_size = read_eof1_header(container)

    if len(section_sizes[S_TYPE]) != 0:
        type_section_size = section_sizes[S_TYPE][0]
        types = read_eof1_types(container, header_size, type_section_size)
        pos = header_size + type_section_size
    else:
        types = [FunctionType(0, 0)]  # implicit code section 0 type
        pos = header_size

    for func_idx in range(0, len(section_sizes[S_CODE])):
        code_section_size = section_sizes[S_CODE][func_idx]
        validate_function(func_idx, container[pos:pos + code_section_size], types)
        pos += code_section_size


def read_eof1_header(container: bytes) -> (dict[int, list[int]], int):
    section_sizes = {S_TYPE: [], S_CODE: [], S_DATA: []}
    pos = len(MAGIC) + 1
    while True:
        section_id = container[pos]
        pos += 1
        if section_id == S_TERMINATOR:
            break

        section_sizes[section_id].append((container[pos] << 8) | container[pos + 1])
        pos += 2

    return section_sizes, pos


def read_eof1_types(container: bytes, header_size: int, type_section_size: int) -> list[FunctionType]:
    pos = header_size
    types = []
    while pos < header_size + type_section_size:
        types.append(FunctionType(container[pos], container[pos + 1]))
        pos += 2

    return types

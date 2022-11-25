#!/usr/bin/python

import atheris
import sys

with atheris.instrument_imports():
    import eip5450


def TestOneInput(data):
    if len(data) == 0:
        return

    a = -1
    try:
        a = eip5450.validate_function_2pass(0, data)
    except eip5450.ValidationException:
        pass

    b = -1
    try:
        b = eip5450.validate_function_1pass(0, data)
    except eip5450.ValidationException:
        pass

    assert b == a, "mismatched results"


atheris.Setup(sys.argv, TestOneInput)
atheris.Fuzz()

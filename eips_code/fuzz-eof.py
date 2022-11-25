#!/usr/bin/python

import atheris
import sys

with atheris.instrument_imports():
    import eof1_validation_test


def TestOneInput(data):
    eof1_validation_test.wrapped_validate_eof1(data)


atheris.Setup(sys.argv, TestOneInput)
atheris.Fuzz()

"""Shared utilities for tests."""

from subprocess import check_call
from tempfile import mkdtemp
import os
import sys

import cbor2

from pycddl import Schema

BSTR_SCHEMA = Schema("object = bstr")

BSTR_1K = cbor2.dumps(b"A" * 1_000)
BSTR_1M = cbor2.dumps(b"A" * 1_000_000)


# Generate the largest bstr in a subprocess, so that we don't increase maxrss
# in this process unnecessarily:
def _make_bstr_100m():
    path = os.path.join(mkdtemp(), "out.cbor")
    check_call(
        [
            sys.executable,
            "-c",
            """\
import cbor2
with open({}, 'wb') as f:
    cbor2.dump(b"A" * 100_000_000, f)
""".format(
                repr(path)
            ),
        ]
    )
    with open(path, "rb") as f:
        return f.read()


BSTR_100M = _make_bstr_100m()
assert len(BSTR_100M) == 100_000_005

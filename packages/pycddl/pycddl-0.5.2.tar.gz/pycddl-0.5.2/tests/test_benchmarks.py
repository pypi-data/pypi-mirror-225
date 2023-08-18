"""
Benchmarks for parsing.

Run with pytest:

    $ pytest benchmarks.py
"""

import pytest

from .utils import BSTR_1K, BSTR_1M, BSTR_100M, BSTR_SCHEMA


@pytest.mark.parametrize("document_length", [1000, 1_000_000])
def test_validate_bytestring(benchmark, document_length, tmp_path):
    """
    Measure how long it takes to validate a bytestring of a given size.

    The hope is that validation time is still fast for large byte strings.
    """
    document = {1000: BSTR_1K, 1_000_000: BSTR_1M, 100_000_000: BSTR_100M}[
        document_length
    ]
    benchmark(lambda: BSTR_SCHEMA.validate_cbor(document))

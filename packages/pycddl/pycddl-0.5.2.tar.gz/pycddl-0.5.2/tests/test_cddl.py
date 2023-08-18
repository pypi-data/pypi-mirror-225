"""Tests for pycddl."""

import platform
import resource
import mmap

from psutil import Process
import pytest
import cbor2

from pycddl import Schema, ValidationError

from .utils import BSTR_SCHEMA, BSTR_100M, BSTR_1K


def assert_invalid_caught(schema, data):
    """
    The schema correctly identifies that data as invalid.
    """
    with pytest.raises(ValidationError):
        schema.validate_cbor(cbor2.dumps(data))


def test_invalid_schema_errors_out():
    """
    Attempting to create a new ``CDDLSchema`` with an invalid CDDL schema
    results in a ValueError.
    """
    with pytest.raises(ValueError):
        Schema(
            """
    reputation-object = {
        application: text
        reputons: [* reputon]

    """
        )


REPUTON_SCHEMA = """\
reputation-object = {
  application: text
  reputons: [* reputon]
}

reputon = {
  rater: text
  assertion: text
  rated: text
  rating: float16
  ? confidence: float16
  ? normal-rating: float16
  ? sample-size: uint
  ? generated: uint
  ? expires: uint
  * text => any
}
"""


def test_schema_validates_good_document():
    """
    A valid schema will validate a valid document (i.e. no exception is
    raised).
    """
    schema = Schema(REPUTON_SCHEMA)
    for document in [
        {"application": "blah", "reputons": []},
        {
            "application": "conchometry",
            "reputons": [
                {
                    "rater": "Ephthianura",
                    "assertion": "codding",
                    "rated": "sphaerolitic",
                    "rating": 0.34133473256800795,
                    "confidence": 0.9481983064298332,
                    "expires": 1568,
                    "unplaster": "grassy",
                },
                {
                    "rater": "nonchargeable",
                    "assertion": "raglan",
                    "rated": "alienage",
                    "rating": 0.5724646875815566,
                    "sample-size": 3514,
                    "Aldebaran": "unchurched",
                    "puruloid": "impersonable",
                    "uninfracted": "pericarpoidal",
                    "schorl": "Caro",
                },
            ],
        },
    ]:
        schema.validate_cbor(cbor2.dumps(document))


def test_schema_fails_bad_documents():
    """
    Bad documents cause ``validate_cbor()`` to raise a ``ValidationError``.
    """
    schema = Schema(REPUTON_SCHEMA)
    for bad_document in [
        b"",
        cbor2.dumps({"application": "blah"}),  # missing reputons key
        cbor2.dumps({"application": "blah", "reputons": "NOT A LIST"}),
    ]:
        with pytest.raises(ValidationError):
            schema.validate_cbor(bad_document)


def test_integer_value_enforcement():
    """
    Schemas that limit minimum integer value are enforced.  This is important
    for security, for example.
    """
    uint_schema = Schema(
        """
    object = {
        xint: uint
    }
    """
    )
    for i in [0, 1, 4, 5, 500, 1000000]:
        uint_schema.validate_cbor(cbor2.dumps({"xint": i}))
    for i in [-1, -10000, "x", 0.3]:
        assert_invalid_caught(uint_schema, i)

    more_than_3_schema = Schema(
        """
    object = {
        xint: int .gt 3
    }
    """
    )
    for i in [4, 5, 500, 1000000]:
        more_than_3_schema.validate_cbor(cbor2.dumps({"xint": i}))
    for i in [-1, -10000, "x", 0.3, 0, 1, 2, 3]:
        assert_invalid_caught(more_than_3_schema, {"xint": i})


def test_schema_repr():
    """``repr(Schema)`` reflects the schema string."""
    schema_text = """
    object = {
        xint: int .gt 3
        "value": uint
    }
    """
    schema = Schema(schema_text)
    assert repr(schema) == f'Schema("""{schema_text}""")'


def get_max_rss_mb():
    # ru_maxrss is kilobytes on Linux, bytes on macOS
    result = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024
    if platform.system() == "Darwin":
        result /= 1024
    return result


@pytest.mark.skipif(platform.system() == "Windows", reason="Need POSIX to check maxrss")
def test_memory_usage():
    """
    Validating a large document doesn't significantly increase memory usage.
    """
    process = Process()
    # This returns units of bytes, so divide appropriately:
    before_rss_mb = process.memory_info().rss / (1024 * 1024)
    before_max_rss_mb = get_max_rss_mb()

    # If this fails, this test won't be meaningful because new allocation won't
    # budge max RSS. So if this fails, to fix it you should try to adjust
    # runtime to ensure we don't have extra high max RSS. E.g. in utils.py we
    # try to generate large CBOR docs in a subprocess.
    #
    # TODO Fil should really expose an API for "current in-use memory and
    # current peak memory", it has the info...
    assert (
        before_max_rss_mb - before_rss_mb < 105
    ), "This is an environmental check; see code"

    BSTR_SCHEMA.validate_cbor(BSTR_100M)
    new_max_rss_mb = get_max_rss_mb()

    # We're validating a 100MB document. The underlying parser used by the Rust
    # library allocates memory linearly based on input (see
    # https://github.com/anweiss/cddl/issues/167), but we at least should not
    # be copying memory much beyond that. Ideally this should be more like < 10.
    assert new_max_rss_mb - before_rss_mb < 120


def test_buffer_interface(tmp_path):
    """
    It's possible to pass in read-only buffers, e.g. ``memoryview``.
    """
    # memoryview() of bytes works fine: it's read-only.
    BSTR_SCHEMA.validate_cbor(memoryview(BSTR_1K))

    # But if we mmap() an existing file in read-only way, that's fine:
    path = tmp_path / "out.cbor"
    with path.open("wb") as f:
        f.write(BSTR_1K)
    with path.open("rb") as f2:
        mapping = mmap.mmap(f2.fileno(), len(BSTR_1K), access=mmap.ACCESS_READ)
        BSTR_SCHEMA.validate_cbor(mapping)


@pytest.mark.skipif(
    platform.python_implementation() == "PyPy",
    reason="PyPy is buggy, it thinks bytearray() is read-only...",
)
def test_buffer_interface_refuses_writeable():
    """
    Writeable buffers won't get validated.
    """
    # bytearray won't work because it's mutable:
    arr = bytearray(BSTR_1K)
    with pytest.raises(ValueError):
        BSTR_SCHEMA.validate_cbor(arr)

    # Likewise for writeable mmap():
    mapping = mmap.mmap(-1, len(BSTR_1K))
    mapping[:] = BSTR_1K
    with pytest.raises(ValueError):
        BSTR_SCHEMA.validate_cbor(mapping)

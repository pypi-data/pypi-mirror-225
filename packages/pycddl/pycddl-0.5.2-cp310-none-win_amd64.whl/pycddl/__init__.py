__all__ = ["Schema", "ValidationError"]

import platform
from .pycddl import Schema, ValidationError

if platform.python_implementation() == "PyPy":
    _Schema = Schema

    class Schema:
        def __init__(self, schema_string):
            self._schema = _Schema(schema_string)

        def validate_cbor(self, cbor):
            # On PyPy, not wrapping with memoryview() results in bytes being
            # copied, which is very memory inefficient for large documents.
            return self._schema.validate_cbor(memoryview(cbor))

        def __repr__(self):
            return repr(self._schema)

        def __str__(self):
            return str(self._schema)

    Schema.__doc__ = _Schema.__doc__
    Schema.validate_cbor.__doc__ = Schema.validate_cbor.__doc__

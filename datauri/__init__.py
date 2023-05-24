import mimetypes
import re
import textwrap
from base64 import b64decode as decode64
from base64 import b64encode as encode64
from urllib.parse import quote, unquote

from .exceptions import InvalidCharset, InvalidDataURI, InvalidMimeType

MIMETYPE_REGEX = r"[\w]+\/[\w\-\+\.]+"
_MIMETYPE_RE = re.compile("^{}$".format(MIMETYPE_REGEX))

CHARSET_REGEX = r"[\w\-\+\.]+"
_CHARSET_RE = re.compile("^{}$".format(CHARSET_REGEX))

DATA_URI_REGEX = (
    r"data:"
    + r"(?P<mimetype>{})?".format(MIMETYPE_REGEX)
    + r"(?:\;name\=(?P<name>[\w\.\-%!*'~\(\)]+))?"
    + r"(?:\;charset\=(?P<charset>{}))?".format(CHARSET_REGEX)
    + r"(?P<base64>\;base64)?"
    + r",(?P<data>.*)"
)
_DATA_URI_RE = re.compile(r"^{}$".format(DATA_URI_REGEX), re.DOTALL)


class DataURI(str):
    @classmethod
    def make(cls, mimetype, charset, base64, data):
        parts = ["data:"]
        if mimetype is not None:
            if not _MIMETYPE_RE.match(mimetype):
                raise InvalidMimeType("Invalid mimetype: %r" % mimetype)
            parts.append(mimetype)
        if charset is not None:
            if not _CHARSET_RE.match(charset):
                raise InvalidCharset("Invalid charset: %r" % charset)
            parts.extend([";charset=", charset])
        if base64:
            parts.append(";base64")
            _charset = charset or "utf-8"
            if isinstance(data, bytes):
                _data = data
            else:
                _data = bytes(data, _charset)
            encoded_data = encode64(_data).decode(_charset).strip()
        else:
            encoded_data = quote(data)
        parts.extend([",", encoded_data])
        return cls("".join(parts))

    @classmethod
    def from_file(cls, filename, charset=None, base64=True):
        mimetype, _ = mimetypes.guess_type(filename, strict=False)
        with open(filename, "rb") as fp:
            data = fp.read()

        return cls.make(mimetype, charset, base64, data)

    def __new__(cls, *args, **kwargs):
        uri = super(DataURI, cls).__new__(cls, *args, **kwargs)
        uri._parse  # Trigger any ValueErrors on instantiation.
        return uri

    def __repr__(self):
        truncated = str(self)
        if len(truncated) > 80:
            truncated = truncated[:79] + "…"
        return "DataURI(%s)" % (truncated,)

    def wrap(self, width=76):
        return "\n".join(textwrap.wrap(self, width, break_on_hyphens=False))

    @property
    def mimetype(self):
        return self._parse[0]

    @property
    def name(self):
        name = self._parse[1]
        if name is not None:
            return unquote(name)
        return name

    @property
    def charset(self):
        return self._parse[2]

    @property
    def is_base64(self):
        return self._parse[3]

    @property
    def data(self):
        return self._parse[4]

    @property
    def text(self):
        if self.charset is None:
            raise InvalidCharset("DataURI has no encoding set.")

        return self.data.decode(self.charset)

    @property
    def is_valid(self):
        match = _DATA_URI_RE.match(self)
        if not match:
            return False
        return True

    @property
    def _parse(self):
        if self.is_valid is False:
            raise InvalidDataURI("Not a valid data URI: %r" % self)
        match = _DATA_URI_RE.match(self)
        mimetype = match.group("mimetype") or None
        name = match.group("name") or None
        charset = match.group("charset") or None

        if match.group("base64"):
            _charset = charset or "utf-8"
            _data = bytes(match.group("data"), _charset)
            data = decode64(_data)
        else:
            data = unquote(match.group("data"))

        return mimetype, name, charset, bool(match.group("base64")), data

    # Pydantic methods
    @classmethod
    def __get_validators__(cls):
        # one or more validators may be yielded which will be called in the
        # order to validate the input, each validator will receive as an input
        # the value returned from the previous validator
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError("string required")

        m = cls(v)
        if not m.is_valid:
            raise ValueError("invalid data-uri format")
        return m

    @classmethod
    def __modify_schema__(cls, field_schema):
        # __modify_schema__ should mutate the dict it receives in place,
        # the returned value will be ignored
        field_schema.update(
            pattern=DATA_URI_REGEX,
            examples=[
                "data:text/plain;charset=utf-8;base64,VGhlIHF1aWNrIGJyb3duIGZveCBqdW1wZWQgb3ZlciB0aGUgbGF6eSBkb2cu"
            ],
        )

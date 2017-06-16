import mimetypes
import re
import textwrap
import urllib


MIMETYPE_REGEX = r'[\w]+\/[\w\-\+\.]+'
_MIMETYPE_RE = re.compile('^{}$'.format(MIMETYPE_REGEX))

CHARSET_REGEX = r'[\w\-\+\.]+'
_CHARSET_RE = re.compile('^{}$'.format(CHARSET_REGEX))

DATA_URI_REGEX = (
    r'data:' +
    r'(?P<mimetype>{})?'.format(MIMETYPE_REGEX) +
    r'(?:\;charset\=(?P<charset>{}))?'.format(CHARSET_REGEX) +
    r'(?P<base64>\;base64)?' +
    r',(?P<data>.*)')
_DATA_URI_RE = re.compile(r'^{}$'.format(DATA_URI_REGEX), re.DOTALL)


class DataURI(str):

    @classmethod
    def make(cls, mimetype, charset, base64, data):
        parts = ['data:']
        if mimetype is not None:
            if not _MIMETYPE_RE.match(mimetype):
                raise ValueError("Invalid mimetype: %r" % mimetype)
            parts.append(mimetype)
        if charset is not None:
            if not _CHARSET_RE.match(charset):
                raise ValueError("Invalid charset: %r" % charset)
            parts.extend([';charset=', charset])
        if base64:
            parts.append(';base64')
            encoded_data = data.encode('base64').replace('\n', '')
        else:
            encoded_data = urllib.quote(data)
        parts.extend([',', encoded_data])
        return cls(''.join(parts))

    @classmethod
    def from_file(cls, filename, charset=None, base64=True):
        mimetype, _ = mimetypes.guess_type(filename, strict=False)
        with open(filename) as fp:
            data = fp.read()
        return cls.make(mimetype, charset, base64, data)

    def __new__(cls, *args, **kwargs):
        uri = super(DataURI, cls).__new__(cls, *args, **kwargs)
        uri._parse  # Trigger any ValueErrors on instantiation.
        return uri

    def __repr__(self):
        return 'DataURI(%s)' % (super(DataURI, self).__repr__(),)

    def wrap(self, width=76):
        return type(self)('\n'.join(textwrap.wrap(self, width)))

    @property
    def mimetype(self):
        return self._parse[0]

    @property
    def charset(self):
        return self._parse[1]

    @property
    def is_base64(self):
        return self._parse[2]

    @property
    def data(self):
        return self._parse[3]

    @property
    def _parse(self):
        match = _DATA_URI_RE.match(self)
        if not match:
            raise ValueError("Not a valid data URI: %r" % self)
        mimetype = match.group('mimetype') or None
        charset = match.group('charset') or None
        if match.group('base64'):
            data = match.group('data').decode('base64')
        else:
            data = urllib.unquote(match.group('data'))
        return mimetype, charset, bool(match.group('base64')), data

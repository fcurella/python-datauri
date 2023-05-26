import os
from pathlib import Path

import pytest

from datauri import DataURI, exceptions

TEST_DIR = os.path.dirname(__file__)
ASSETS_DIR = Path(TEST_DIR) / "assets"


def test_parse():
    t = "data:text/plain;charset=utf-8,VGhlIHF1aWNrIGJyb3duIGZveCBqdW1wZWQgb3ZlciB0aGUgbGF6eSBkb2cu"
    DataURI(t)


def test_parse_base64():
    t = "data:text/plain;charset=utf-8;base64,VGhlIHF1aWNrIGJyb3duIGZveCBqdW1wZWQgb3ZlciB0aGUgbGF6eSBkb2cu"
    DataURI(t)


def test_parse_invalid_datauri():
    t = "data:*garbled*;charset=utf-8;base64,VGhlIHF1aWNrIGJyb3duIGZveCBqdW1wZWQgb3ZlciB0aGUgbGF6eSBkb2cu"
    with pytest.raises(exceptions.InvalidDataURI):
        DataURI(t)

    t = "data:text/plain;charset=*garbled*;base64,VGhlIHF1aWNrIGJyb3duIGZveCBqdW1wZWQgb3ZlciB0aGUgbGF6eSBkb2cu"
    with pytest.raises(exceptions.InvalidDataURI):
        DataURI(t)


def test_parse_invalid_mimetype():
    with pytest.raises(exceptions.InvalidMimeType):
        DataURI.make(
            mimetype="*garbled*",
            charset="utf-8",
            base64=True,
            data="VGhlIHF1aWNrIGJyb3duIGZveCBqdW1wZWQgb3ZlciB0aGUgbGF6eSBkb2cu",
        )


def test_parse_invalid_charset():
    with pytest.raises(exceptions.InvalidCharset):
        DataURI.make(
            mimetype="text/plain",
            charset="*garbled*",
            base64=True,
            data="VGhlIHF1aWNrIGJyb3duIGZveCBqdW1wZWQgb3ZlciB0aGUgbGF6eSBkb2cu",
        )


def test_from_file():
    filename = ASSETS_DIR / "test_file.txt"
    parsed = DataURI.from_file(filename)
    assert parsed.data == b"This is a message.\n"
    assert parsed.charset is None


def test_from_file_charset():
    filename = ASSETS_DIR / "test_file.txt"
    parsed = DataURI.from_file(filename, charset="us-ascii")
    assert parsed.data == b"This is a message.\n"
    assert parsed.text == "This is a message.\n"
    assert parsed.charset == "us-ascii"

    filename = ASSETS_DIR / "test_file_ebcdic.txt"
    parsed = DataURI.from_file(filename, charset="cp500")
    assert (
        parsed.data == b"\xe3\x88\x89\xa2@\x89\xa2@\x81@\x94\x85\xa2\xa2\x81\x87\x85K%"
    )

    assert parsed.text == "This is a message.\n"
    assert parsed.charset == "cp500"


def test_no_wrap():
    filename = ASSETS_DIR / "test_long_file.txt"
    parsed = DataURI.from_file(filename)
    assert "\n" not in str(parsed)


def test_parse_name():
    t = (
        "data:text/plain;name=file-1_final.txt;charset=utf-8;base64,VGhlIHF1aWNrIGJyb3duIGZveCBqdW1wZWQgb3ZlciB0aGUgb"
        "GF6eSBkb2cu"
    )
    parsed = DataURI(t)
    assert parsed.name == "file-1_final.txt"


def test_emptyname():
    t = "data:text/plain;charset=utf-8;base64,VGhlIHF1aWNrIGJyb3duIGZveCBqdW1wZWQgb3ZlciB0aGUgbGF6eSBkb2cu"
    parsed = DataURI(t)
    assert parsed.name is None


def test_urlencoded():
    t = (
        "data:text/plain;name=file%201%20('final'!)%20*~.txt;charset=utf-8;base64,VGhlIHF1aWNrIGJyb3duIGZveCBqdW1wZWQ"
        "gb3ZlciB0aGUgbGF6eSBkb2cu"
    )
    parsed = DataURI(t)
    assert parsed.name == "file 1 ('final'!) *~.txt"


def test_parse_name_no_charset():
    t = "data:text/plain;name=file.txt;base64,VGhlIHF1aWNrIGJyb3duIGZveCBqdW1wZWQgb3ZlciB0aGUgbGF6eSBkb2cu"
    parsed = DataURI(t)
    assert parsed.name == "file.txt"


def test_mimetype():
    t = "data:text/plain;charset=utf-8;base64,VGhlIHF1aWNrIGJyb3duIGZveCBqdW1wZWQgb3ZlciB0aGUgbGF6eSBkb2cu"
    parsed = DataURI(t)
    assert parsed.mimetype == "text/plain"


def test_is_base64():
    t = "data:text/plain;charset=utf-8;base64,VGhlIHF1aWNrIGJyb3duIGZveCBqdW1wZWQgb3ZlciB0aGUgbGF6eSBkb2cu"
    parsed = DataURI(t)
    assert parsed.is_base64 is True


def test_text():
    t = (
        "data:text/plain;name=file-1_final.txt;charset=utf-8;base64,VGhlIHF1aWNrIGJyb3duIGZveCBqdW1wZWQgb3ZlciB0aGUgb"
        "GF6eSBkb2cu"
    )
    parsed = DataURI(t)
    assert isinstance(parsed.data, bytes)
    assert isinstance(parsed.text, str)


def test_wrap():
    t = "data:text/plain;charset=utf-8;base64,VGhlIHF1aWNrIGJyb3duIGZveCBqdW1wZWQgb3ZlciB0aGUgbGF6eSBkb2cu"
    parsed = DataURI(t)
    assert (
        parsed.wrap()
        == """data:text/plain;charset=utf-8;base64,VGhlIHF1aWNrIGJyb3duIGZveCBqdW1wZWQgb3Z
lciB0aGUgbGF6eSBkb2cu"""
    )


def test_text_no_charset():
    t = "data:text/plain;name=file.txt;base64,VGhlIHF1aWNrIGJyb3duIGZveCBqdW1wZWQgb3ZlciB0aGUgbGF6eSBkb2cu"
    parsed = DataURI(t)
    assert isinstance(parsed.data, bytes)
    with pytest.raises(exceptions.InvalidCharset):
        assert isinstance(parsed.text, str)


def test_make():
    made = DataURI.make(
        "text/plain", charset="us-ascii", base64=False, data="This is a message."
    )
    assert made.data == b"This is a message."
    assert made.text == "This is a message."


def test_make_base64():
    made = DataURI.make(
        "text/plain", charset="us-ascii", base64=True, data="This is a message."
    )
    assert made.data == b"This is a message."
    assert made.text == "This is a message."


def test_make_no_charset():
    made = DataURI.make(
        "text/plain", charset=None, base64=True, data="This is a message."
    )
    assert made.data == b"This is a message."
    with pytest.raises(exceptions.InvalidCharset):
        made.text  # NOQA


def test_repr():
    t = "data:text/plain;charset=utf-8;base64,VGhlIHF1aWNrIGJyb3duIGZveCBqdW1wZWQgb3ZlciB0aGUgbGF6eSBkb2cu"
    uri = DataURI(t)
    assert (
        repr(uri)
        == "DataURI(data:text/plain;charset=utf-8;base64,VGhlIHF1aWNrIGJyb3duIGZveCBqdW1wZWQgb3Zlci…)"
    )

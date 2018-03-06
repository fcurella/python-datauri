import os
import unittest

import six
from datauri import DataURI


TEST_DIR = os.path.dirname(__file__)


class ParseTestCase(unittest.TestCase):

    def test_parse(self):
        t = 'data:text/plain;charset=utf-8,VGhlIHF1aWNrIGJyb3duIGZveCBqdW1wZWQgb3ZlciB0aGUgbGF6eSBkb2cu'
        DataURI(t)

    def test_parse_base64(self):
        t = 'data:text/plain;charset=utf-8;base64,VGhlIHF1aWNrIGJyb3duIGZveCBqdW1wZWQgb3ZlciB0aGUgbGF6eSBkb2cu'
        DataURI(t)

    def test_parse_invalid_mimetype(self):
        t = 'data:*garbled*;charset=utf-8;base64,VGhlIHF1aWNrIGJyb3duIGZveCBqdW1wZWQgb3ZlciB0aGUgbGF6eSBkb2cu'
        with self.assertRaises(ValueError):
            DataURI(t)

    def test_parse_invalid_charset(self):
        t = 'data:text/plain;charset=*garbled*;base64,VGhlIHF1aWNrIGJyb3duIGZveCBqdW1wZWQgb3ZlciB0aGUgbGF6eSBkb2cu'
        with self.assertRaises(ValueError):
            DataURI(t)

    def test_from_file(self):
        filename = os.path.join(TEST_DIR, 'test_file.txt')
        parsed = DataURI.from_file(filename)
        self.assertEqual(parsed.data, b'This is a message.\n')
        self.assertEqual(parsed.charset, None)

    def test_from_file_charset(self):
        filename = os.path.join(TEST_DIR, 'test_file.txt')
        parsed = DataURI.from_file(filename, charset='us-ascii')
        self.assertEqual(parsed.data, b'This is a message.\n')
        self.assertEqual(parsed.text, 'This is a message.\n')
        self.assertEqual(parsed.charset, 'us-ascii')

        filename = os.path.join(TEST_DIR, 'test_file_ebcdic.txt')
        parsed = DataURI.from_file(filename, charset='cp500')
        self.assertEqual(parsed.data, b'\xe3\x88\x89\xa2@\x89\xa2@\x81@\x94\x85\xa2\xa2\x81\x87\x85K%')
        self.assertEqual(parsed.text, 'This is a message.\n')
        self.assertEqual(parsed.charset, 'cp500')

    def test_parse_name(self):
        t = 'data:text/plain;name=file-1_final.txt;charset=utf-8;base64,VGhlIHF1aWNrIGJyb3duIGZveCBqdW1wZWQgb3ZlciB0aGUgbGF6eSBkb2cu'
        parsed = DataURI(t)
        self.assertEqual(parsed.name, 'file-1_final.txt')

    def test_emptyname(self):
        t = 'data:text/plain;charset=utf-8;base64,VGhlIHF1aWNrIGJyb3duIGZveCBqdW1wZWQgb3ZlciB0aGUgbGF6eSBkb2cu'
        parsed = DataURI(t)
        self.assertEqual(parsed.name, None)

    def test_urlencoded(self):
        t = "data:text/plain;name=file%201%20('final'!)%20*~.txt;charset=utf-8;base64,VGhlIHF1aWNrIGJyb3duIGZveCBqdW1wZWQgb3ZlciB0aGUgbGF6eSBkb2cu"
        parsed = DataURI(t)
        self.assertEqual(parsed.name, "file 1 ('final'!) *~.txt")

    def test_parse_name_no_charset(self):
        t = 'data:text/plain;name=file.txt;base64,VGhlIHF1aWNrIGJyb3duIGZveCBqdW1wZWQgb3ZlciB0aGUgbGF6eSBkb2cu'
        parsed = DataURI(t)
        self.assertEqual(parsed.name, 'file.txt')

    def test_mimetype(self):
        t = 'data:text/plain;charset=utf-8;base64,VGhlIHF1aWNrIGJyb3duIGZveCBqdW1wZWQgb3ZlciB0aGUgbGF6eSBkb2cu'
        parsed = DataURI(t)
        self.assertEqual(parsed.mimetype, 'text/plain')

    def test_is_base64(self):
        t = 'data:text/plain;charset=utf-8;base64,VGhlIHF1aWNrIGJyb3duIGZveCBqdW1wZWQgb3ZlciB0aGUgbGF6eSBkb2cu'
        parsed = DataURI(t)
        self.assertEqual(parsed.is_base64, True)

    def test_text(self):
        t = 'data:text/plain;name=file-1_final.txt;charset=utf-8;base64,VGhlIHF1aWNrIGJyb3duIGZveCBqdW1wZWQgb3ZlciB0aGUgbGF6eSBkb2cu'
        parsed = DataURI(t)
        self.assertTrue(isinstance(parsed.data, six.binary_type))
        self.assertTrue(isinstance(parsed.text, six.text_type))

    def test_wrap(self):
        t = 'data:text/plain;charset=utf-8;base64,VGhlIHF1aWNrIGJyb3duIGZveCBqdW1wZWQgb3ZlciB0aGUgbGF6eSBkb2cu'
        parsed = DataURI(t)
        self.assertEqual(parsed.wrap(), """data:text/plain;charset=utf-8;base64,VGhlIHF1aWNrIGJyb3duIGZveCBqdW1wZWQgb3Z
lciB0aGUgbGF6eSBkb2cu""")

    def test_text_no_charset(self):
        t = 'data:text/plain;name=file.txt;base64,VGhlIHF1aWNrIGJyb3duIGZveCBqdW1wZWQgb3ZlciB0aGUgbGF6eSBkb2cu'
        parsed = DataURI(t)
        self.assertTrue(isinstance(parsed.data, six.binary_type))
        with self.assertRaises(ValueError):
            self.assertTrue(isinstance(parsed.text, six.text_type))

    def test_make(self):
        made = DataURI.make('text/plain', charset='us-ascii', base64=False, data='This is a message.')
        self.assertEqual(made.data, 'This is a message.')

    def test_make_base64(self):
        made = DataURI.make('text/plain', charset='us-ascii', base64=True, data='This is a message.')
        self.assertEqual(made.text, u'This is a message.')

    def test_make_no_charset(self):
        made = DataURI.make('text/plain', charset=None, base64=True, data='This is a message.')
        self.assertEqual(made.data, b'This is a message.')

    def test_repr(self):
        t = 'data:text/plain;charset=utf-8;base64,VGhlIHF1aWNrIGJyb3duIGZveCBqdW1wZWQgb3ZlciB0aGUgbGF6eSBkb2cu'
        uri = DataURI(t)
        self.assertEqual(repr(uri), "DataURI('data:text/plain;charset=utf-8;base64,VGhlIHF1aWNrIGJyb3duIGZveCBqdW1wZWQgb3ZlciB0aGUgbGF6eSBkb2cu')")

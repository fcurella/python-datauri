import unittest

import six
from datauri import DataURI


class ParseTestCase(unittest.TestCase):

    def test_parse(self):
        t = 'data:text/plain;charset=utf-8;base64,VGhlIHF1aWNrIGJyb3duIGZveCBqdW1wZWQgb3ZlciB0aGUgbGF6eSBkb2cu'
        DataURI(t)

    def test_parse_name(self):
        t = 'data:text/plain;name=file-1_final.txt;charset=utf-8;base64,VGhlIHF1aWNrIGJyb3duIGZveCBqdW1wZWQgb3ZlciB0aGUgbGF6eSBkb2cu'
        parsed = DataURI(t)
        self.assertEqual(parsed.name, 'file-1_final.txt')

    def test_urlencoded(self):
        t = 'data:text/plain;name=file%201.txt;charset=utf-8;base64,VGhlIHF1aWNrIGJyb3duIGZveCBqdW1wZWQgb3ZlciB0aGUgbGF6eSBkb2cu'
        parsed = DataURI(t)
        self.assertEqual(parsed.name, 'file 1.txt')

    def test_parse_name_no_charset(self):
        t = 'data:text/plain;name=file.txt;base64,VGhlIHF1aWNrIGJyb3duIGZveCBqdW1wZWQgb3ZlciB0aGUgbGF6eSBkb2cu'
        parsed = DataURI(t)
        self.assertEqual(parsed.name, 'file.txt')

    def test_text(self):
        t = 'data:text/plain;name=file-1_final.txt;charset=utf-8;base64,VGhlIHF1aWNrIGJyb3duIGZveCBqdW1wZWQgb3ZlciB0aGUgbGF6eSBkb2cu'
        parsed = DataURI(t)
        self.assertTrue(isinstance(parsed.data, six.binary_type))
        self.assertTrue(isinstance(parsed.text, six.text_type))

    def test_text_no_charset(self):
        t = 'data:text/plain;name=file.txt;base64,VGhlIHF1aWNrIGJyb3duIGZveCBqdW1wZWQgb3ZlciB0aGUgbGF6eSBkb2cu'
        parsed = DataURI(t)
        self.assertTrue(isinstance(parsed.data, six.binary_type))
        with self.assertRaises(ValueError):
            self.assertTrue(isinstance(parsed.text, six.text_type))

    def test_make(self):
        made = DataURI.make('text/plain', charset='us-ascii', base64=True, data='This is a message.')
        self.assertEqual(made.text, u'This is a message.')

    def test_make_no_charset(self):
        made = DataURI.make('text/plain', charset=None, base64=True, data='This is a message.')
        self.assertEqual(made.data, b'This is a message.')

from snippetysnip import *
import unittest

class Test_get_snippet(unittest.TestCase):
    def test_gets_snippet(self):
        self.assertEqual(
            "void bar() {\n    foo();\n}\n",
            get_snippet("example.cpp", "bar"))

    def test_missing_snippet_returns_errormessage(self):
        self.assertEqual(
            "ERROR: Didn't find snippetysnip_begin:platypus\n",
            get_snippet("example.cpp", "platypus"))

    def test_missing_snippet_end_returns_errormessage(self):
        self.assertEqual(
            "ERROR: Didn't find snippetysnip_end after snippetysnip_begin:error\n",
            get_snippet("example.cpp", "error"))

    def test_missing_file_returns_errormessage(self):
        self.assertEqual(
            "ERROR: Couldn't open file: [Errno 2] No such file or directory: 'missing_file.cpp'\n",
            get_snippet("missing_file.cpp", "tag"))

class Test_find_end_line(unittest.TestCase):
    def test_returns_correct_line_when_found(self):
        self.assertEqual(1, find_end_line(['a','snippetysnip_end:foo:bar', 'b'], 'foo', 'bar'))

    def test_returns_minus_one_when_not_found(self):
        self.assertEqual(-1, find_end_line([], 'foo', 'bar'))


def fake_get_snippet(file_name, snippet_name):
    return "line1\nline2\n"

class Test_insert_snippets(unittest.TestCase):
    def test_inserts_snippet(self):
        buffer = [
            "foo",
            "<!-- snippetysnip:snippy.cpp:snippet -->",
            "bar"
        ]
        expected = [
            "foo",
            "<!-- snippetysnip:snippy.cpp:snippet -->",
            "line1",
            "line2",
            "<!-- snippetysnip_end:snippy.cpp:snippet -->",
            "bar"
        ]
        self.assertEqual(expected, insert_snippets(buffer, fake_get_snippet))

    def test_replaces_snippet(self):
        buffer = [
            "foo",
            "<!-- snippetysnip:snippy.cpp:snippet -->",
            "line1",
            "<!-- snippetysnip_end:snippy.cpp:snippet -->",
            "bar"
        ]
        expected = [
            "foo",
            "<!-- snippetysnip:snippy.cpp:snippet -->",
            "line1",
            "line2",
            "<!-- snippetysnip_end:snippy.cpp:snippet -->",
            "bar"
        ]
        self.assertEqual(expected, insert_snippets(buffer, fake_get_snippet))

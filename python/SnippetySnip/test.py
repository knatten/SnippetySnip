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


def mock_get_snippet(file_name, snippet_name):
    mock_get_snippet.last_file_name = file_name
    return "line1\nline2\n"

class Test_insert_snippets(unittest.TestCase):
    def test_inserts_simple_snippet(self):
        buffer = [
            "foo",
            "<!-- snippetysnip:snippy.cpp:snippet -->",
            "bar"
        ]
        expected = [
            "foo",
            "<!-- snippetysnip:snippy.cpp:snippet -->",
            "",
            "line1",
            "line2",
            "",
            "<!-- snippetysnip_end:snippy.cpp:snippet -->",
            "bar"
        ]
        self.assertEqual(expected, insert_snippets(buffer, mock_get_snippet))
        self.assertEqual("snippy.cpp", mock_get_snippet.last_file_name)

    def test_replaces_simple_snippet(self):
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
            "",
            "line1",
            "line2",
            "",
            "<!-- snippetysnip_end:snippy.cpp:snippet -->",
            "bar"
        ]
        self.assertEqual(expected, insert_snippets(buffer, mock_get_snippet))
        self.assertEqual("snippy.cpp", mock_get_snippet.last_file_name)

    def test_inserts_before(self):
        buffer = [
            "foo",
            "<!-- snippetysnip:snippy.cpp:snippet:(before=\"[sourcecode language='cpp']\") -->",
            "bar"
        ]
        expected = [
            "foo",
            "<!-- snippetysnip:snippy.cpp:snippet:(before=\"[sourcecode language='cpp']\") -->",
            "",
            "[sourcecode language='cpp']",
            "line1",
            "line2",
            "",
            "<!-- snippetysnip_end:snippy.cpp:snippet -->",
            "bar"
        ]
        actual = insert_snippets(buffer, mock_get_snippet)
        self.assertEqual(expected, actual)
        self.assertEqual("snippy.cpp", mock_get_snippet.last_file_name)

    def test_inserts_before_and_after(self):
        return
        buffer = [
            "foo",
            "<!-- snippetysnip:snippy.cpp:snippet:(before=\"[sourcecode language='cpp']\", after=\"[/sourcecode]\") -->",
            "bar"
        ]
        expected = [
            "foo",
            "<!-- snippetysnip:snippy.cpp:snippet:(before=\"[sourcecode language='cpp']\", after=\"[/sourcecode]\") -->",
            "[sourcecode language='cpp']",
            "line1",
            "line2",
            "[/sourcecode]",
            "<!-- snippetysnip_end:snippy.cpp:snippet -->",
            "bar"
        ]
        actual = insert_snippets(buffer, mock_get_snippet)
        self.assertEqual(expected, actual)
        self.assertEqual("snippy.cpp", mock_get_snippet.last_file_name)


class Test_get_arguments(unittest.TestCase):
    def test_if_no_arguments_returns_empty(self):
        self.assertEqual({}, get_arguments("snippetysnip:file:snippet"))

    def test_if_one_argument_returns_that(self):
        self.assertEqual({'before':'foo'}, get_arguments("snippetysnip:file:snippet:(before=\"foo\")"))

    def test_if_two_arguments_returns_both(self):
        self.assertEqual({'before':'foo', 'after':'bar'}, get_arguments('snippetysnip:file:snippet:(before="foo",after="bar")'))

    def test_spaces_are_allowed_but_optional(self):
        self.assertEqual({'before':'foo', 'after':'bar'}, get_arguments('snippetysnip:file:snippet:(before =  "foo",   after="bar")'))

    def test_single_quotes_also_work(self):
        self.assertEqual({'before':'foo', 'after':'bar'}, get_arguments("snippetysnip:file:snippet:(before='foo',after='bar')"))


class Test_remove_arguments(unittest.TestCase):
    def test_leaves_string_without_arguments_alone(self):
        actual =  "<!-- snippetysnip:snippy.cpp:snippet -->"
        self.assertEqual(actual, remove_arguments(actual))

    def test_removes_arguments(self):
        actual = "<!-- snippetysnip:snippy.cpp:snippet:(before=\"[sourcecode]\") -->"
        expected =  "<!-- snippetysnip:snippy.cpp:snippet -->"
        self.assertEqual(expected, remove_arguments(actual))

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

    def test_illegal_snippet_name_returns_errormessage(self):
        self.assertEqual(
            "'!' is not a legal character for a snippet name! Legal characters are'%s'." % LEGAL_SNIPPET_CHARS,
            get_snippet("example.cpp", "!"))

class Test_matches_snippet_begin(unittest.TestCase):

    def test_matches_whole_line(self):
        self.assertTrue(matches_snippet_begin('snippetysnip_begin:foo', 'foo'))

    def test_does_not_match_similar_snippet(self):
        self.assertFalse(matches_snippet_begin('snippetysnip_begin:foo2', 'foo'))
        self.assertFalse(matches_snippet_begin('snippetysnip_begin:fooooo', 'foo'))
        self.assertFalse(matches_snippet_begin('snippetysnip_begin:fooO', 'foo'))
        self.assertFalse(matches_snippet_begin('snippetysnip_begin:foo-', 'foo'))
        self.assertFalse(matches_snippet_begin('snippetysnip_begin:foo_', 'foo'))
        self.assertFalse(matches_snippet_begin('snippetysnip_begin:foo.', 'foo'))

    def test_all_characters_are_allowed(self):
        self.assertTrue(matches_snippet_begin('snippetysnip_begin:09azAZ-_.', '09azAZ-_.'))

class Test_assert_legal_snippet_name(unittest.TestCase):
    def test_legal_name_does_not_raise(self):
        assert_legal_snippet_name('09azAZ-_.')

    def test_illegal_character_in_name_raises(self):
        with self.assertRaises(ValueError):
            assert_legal_snippet_name('!')

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

class Test_get_current_snippet_name(unittest.TestCase):
    buf = ['what', 'ever', 'snippetysnip_begin:foo', 'here', 'snippetysnip_end',
        'snippetysnip_begin:bar', 'more', 'snippetysnip_end', 'jubajuba']

    def test_when_in_foo__returns_foo(self):
        self.assertEqual("foo", get_current_snippet_name(self.buf, self.buf.index('snippetysnip_begin:foo')))

    def test_when_in_bar__returns_bar(self):
        self.assertEqual("bar", get_current_snippet_name(self.buf, self.buf.index('snippetysnip_begin:bar')))

    def test_when_not_in_snippet__raises_exception(self):
        with self.assertRaises(ValueError) as error:
            get_current_snippet_name(self.buf, 0)
        self.assertEqual('Not in a snippet', error.exception.message)

    def test_when_not_in_snippet__doesnt_accidentally_pick_the_previous_one(self):
        with self.assertRaises(ValueError) as error:
            get_current_snippet_name(self.buf, self.buf.index('jubajuba'))
        self.assertEqual('Not in a snippet', error.exception.message)


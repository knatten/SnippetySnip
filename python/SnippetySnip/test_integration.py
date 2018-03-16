import unittest
from snippetysnip import insert_snippets

class Test_IntegrationTest(unittest.TestCase):
    def test_integration_test(self):
        self.maxDiff = None
        with open('integration_tests/example.html', 'r') as example:
            buf = [line[:-1] for line in example.readlines()]
            with open('integration_tests/expected.html', 'r') as expected:
                expected = [line[:-1] for line in expected.readlines()]
                actual = insert_snippets(buf)
                self.assertEqual(expected, actual)

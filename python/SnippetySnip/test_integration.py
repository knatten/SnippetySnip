import unittest
from snippetysnip import insert_snippets

class Test_IntegrationTest(unittest.TestCase):
    def test_integration_test(self):
        self.maxDiff = None
        buf = open('integration_tests/example.html', 'r').readlines()
        buf = [line[:-1] for line in buf]
        expected = open('integration_tests/expected.html', 'r').readlines()
        expected = [line[:-1] for line in expected]
        actual = insert_snippets(buf)
        self.assertEqual(expected, actual)

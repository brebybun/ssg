import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_has_tag(self):
        node = HTMLNode("p")
        self.assertIsNotNone(node.tag)
    def test_has_value(self):
        node = HTMLNode(None, "test value")
        self.assertIsNotNone(node.value)
    def test_has_children(self):
        node = HTMLNode(None, None, ["child1", "child2"])
        self.assertIsNotNone(node.children)
    def test_has_props(self):
        node = HTMLNode(None, None, None, {"href": "https://google.com"})
        self.assertIsNotNone(node.props)
    def test_props_to_html(self):
        node = HTMLNode("a", "google.com", None, {"href": "https://google.com", "target": "_blank"})
        properties_string = node.props_to_html()
        expected_string = ' href="https://google.com" target="_blank"'
        self.assertEqual(properties_string, expected_string)
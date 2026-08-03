import unittest
from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        node2 = TextNode("This is a bold text node", TextType.BOLD)
        self.assertEqual(node, node2)
    def test_not_eq(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        node2 = TextNode("This is an italic node text", TextType.ITALIC)
        self.assertNotEqual(node, node2)
    def test_is_link(self):
        node = TextNode("This is link text", TextType.LINK, "https://google.com.au")
        self.assertIsNotNone(node.url)
    def test_is_not_link(self):
        node = TextNode("This is bold text", TextType.BOLD)
        self.assertIsNone(node.url)
    def test_different_text(self):
        node = TextNode("This bold text", TextType.BOLD)
        node2 = TextNode("This is different bold text", TextType.BOLD)
        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()
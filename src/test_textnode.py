import unittest
from textnode import TextNode, TextType, text_node_to_html_node

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

class TestTextNodeToHTML(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    def test_bold(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")
    def test_italic(self):
        node = TextNode("This is an italic text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic text node")
    def test_code(self):
        node = TextNode("This is a code text node", TextType.CODE_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code text node")
    def test_link(self):
        node = TextNode("Test Link", TextType.LINK, "test.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Test Link")
        self.assertEqual(html_node.props["href"], "test.com")
    def test_image(self):
        node = TextNode("Test Image", TextType.IMAGE, "test/image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.props["src"], "test/image.png")
        self.assertEqual(html_node.props["alt"], "Test Image")

if __name__ == "__main__":
    unittest.main()
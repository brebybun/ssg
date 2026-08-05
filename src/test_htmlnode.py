import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

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

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    def test_leaf_to_html_a(self):
        node = LeafNode("a", "google", {"href": "https://google.com", "target": "_blank"})
        self.assertEqual(node.to_html(), '<a href="https://google.com" target="_blank">google</a>')
    def test_leaf_has_no_children(self):
        node = LeafNode("a", "test link", {"href": "testlink.com"})
        self.assertIsNone(node.children)

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_nested_parent_nodes(self):
        grandchild_node = LeafNode("a", "some text as a link", {"href": "testlink.com", "target": "_blank"})
        great_grandchild_node = LeafNode(None, "some text", {"test": "property"})
        grandchild_node2 = ParentNode("div", [great_grandchild_node])
        child_node = ParentNode("p", [grandchild_node, grandchild_node2], {"test": "test property"})
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(),
            '<div><p test="test property"><a href="testlink.com" target="_blank">some text as a link</a><div>some text</div></p></div>'
        )

    def test_multiple_leaf_nodes(self):
        leaf1 = LeafNode("p", "test")
        leaf2 = LeafNode("p", "another test")
        leaf3 = LeafNode("a", "link", {"href": "test.com"})
        leaf4 = LeafNode("b", "bold text")
        leaf5 = LeafNode(None, "untagged text")
        parent_node = ParentNode("div", [leaf1, leaf2, leaf3, leaf4, leaf5])
        self.assertEqual(parent_node.to_html(), '<div><p>test</p><p>another test</p><a href="test.com">link</a><b>bold text</b>untagged text</div>')
if __name__ == "__main__":
    unittest.main()
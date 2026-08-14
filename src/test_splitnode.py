import unittest
from inline import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes
from textnode import TextNode, TextType

class TestSplitNode(unittest.TestCase):
    def test_mid_string_split(self):
        node1 = TextNode("This text has **bold** text", TextType.TEXT)
        split_list = split_nodes_delimiter([node1], "**", TextType.BOLD)
        self.assertEqual(len(split_list), 3)
        self.assertEqual(split_list[0].text, "This text has ")
        self.assertEqual(split_list[1].text, "bold")
        self.assertEqual(split_list[2].text, " text")
        self.assertEqual(split_list[0].text_type, TextType.TEXT)
        self.assertEqual(split_list[1].text_type, TextType.BOLD)
        self.assertEqual(split_list[2].text_type, TextType.TEXT)

    def test_start_string_split(self): # tests if the delimiter pair is at the start of the node
        node1 = TextNode("**bold** text at the start", TextType.TEXT)
        split_list = split_nodes_delimiter([node1], "**", TextType.BOLD)
        self.assertEqual(len(split_list), 2)
        self.assertEqual(split_list[0].text, "bold")
        self.assertEqual(split_list[1].text, " text at the start")
        self.assertEqual(split_list[0].text_type, TextType.BOLD)
        self.assertEqual(split_list[1].text_type, TextType.TEXT)

    def test_multiple_pairs(self):
        node1 = TextNode("There's **two** bolds **mid** way", TextType.TEXT)
        split_list = split_nodes_delimiter([node1], "**", TextType.BOLD)
        self.assertEqual(len(split_list), 5)
        self.assertEqual(split_list[0].text, "There's ")
        self.assertEqual(split_list[1].text, "two")
        self.assertEqual(split_list[2].text, " bolds ")
        self.assertEqual(split_list[3].text, "mid")
        self.assertEqual(split_list[4].text, " way")
        self.assertEqual(split_list[0].text_type, TextType.TEXT)
        self.assertEqual(split_list[1].text_type, TextType.BOLD)
        self.assertEqual(split_list[2].text_type, TextType.TEXT)
        self.assertEqual(split_list[3].text_type, TextType.BOLD)
        self.assertEqual(split_list[4].text_type, TextType.TEXT)

    def test_split_at_start_end(self):
        node1 = TextNode("**start** and **end**", TextType.TEXT)
        split_list = split_nodes_delimiter([node1], "**", TextType.BOLD)
        self.assertEqual(len(split_list), 3)
        self.assertEqual(split_list[0].text, "start")
        self.assertEqual(split_list[1].text, " and ")
        self.assertEqual(split_list[2].text, "end")
        self.assertEqual(split_list[0].text_type, TextType.BOLD)
        self.assertEqual(split_list[1].text_type, TextType.TEXT)
        self.assertEqual(split_list[2].text_type, TextType.BOLD)

    def test_blank_markdown(self):
        node1 = TextNode("This has **** blank markdown", TextType.TEXT)
        split_list = split_nodes_delimiter([node1], "**", TextType.BOLD)
        self.assertEqual(len(split_list), 2)
        self.assertEqual(split_list[0].text, "This has ")
        self.assertEqual(split_list[1].text, " blank markdown")
        self.assertEqual(split_list[0].text_type, TextType.TEXT)
        self.assertEqual(split_list[1].text_type, TextType.TEXT)

    def test_blank_markdown_start(self):
        node1 = TextNode("****Blank markdown at start", TextType.TEXT)
        split_list = split_nodes_delimiter([node1], "**", TextType.BOLD)
        self.assertEqual(len(split_list), 1)
        self.assertEqual(split_list[0].text, "Blank markdown at start")
        self.assertEqual(split_list[0].text_type, TextType.TEXT)

    def test_multiple_items_in_list(self):
        node1 = TextNode("**Node** one", TextType.TEXT)
        node2 = TextNode("**Node** two", TextType.TEXT)
        split_list = split_nodes_delimiter([node1, node2], "**", TextType.BOLD)
        self.assertEqual(len(split_list), 4)
        self.assertEqual(split_list[0].text, "Node")
        self.assertEqual(split_list[1].text, " one")
        self.assertEqual(split_list[2].text, "Node")
        self.assertEqual(split_list[3].text, " two")
        self.assertEqual(split_list[0].text_type, TextType.BOLD)
        self.assertEqual(split_list[1].text_type, TextType.TEXT)
        self.assertEqual(split_list[2].text_type, TextType.BOLD)
        self.assertEqual(split_list[3].text_type, TextType.TEXT)

    def test_different_delimiter(self):
        node1 = TextNode("This text is _italic_", TextType.TEXT)
        split_list = split_nodes_delimiter([node1], "_", TextType.ITALIC)
        self.assertEqual(len(split_list), 2)
        self.assertEqual(split_list[0].text, "This text is ")
        self.assertEqual(split_list[1].text, "italic")
        self.assertEqual(split_list[0].text_type, TextType.TEXT)
        self.assertEqual(split_list[1].text_type, TextType.ITALIC)

    def test_no_markdown(self):
        node1 = TextNode("This is text", TextType.TEXT)
        split_list = split_nodes_delimiter([node1], "**", TextType.BOLD)
        self.assertEqual(len(split_list), 1)
        self.assertEqual(split_list[0].text, "This is text")
        self.assertEqual(split_list[0].text_type, TextType.TEXT)

    def test_mismatched(self):
        node1 = TextNode("This **is** **text", TextType.TEXT)
        self.assertRaises(ValueError, split_nodes_delimiter, [node1], "**", TextType.BOLD)

    def test_single_delimiter(self):
        node1 = TextNode("**Text", TextType.TEXT)
        self.assertRaises(ValueError, split_nodes_delimiter, [node1], "**", TextType.BOLD)

    def test_blank_string(self):
        node1 = TextNode("", TextType.TEXT)
        split_list = split_nodes_delimiter([node1], "**", TextType.BOLD)
        self.assertEqual(len(split_list), 0)



class TestMarkdownImagesAndLinks(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links("This is text with a [link](link.com)")
        self.assertListEqual([("link", "link.com")], matches)

    def test_multiple_links(self):
        matches = extract_markdown_links("This text has [multiple](link 1.com) [links](link 2.com)")
        self.assertListEqual([("multiple", "link 1.com"), ("links", "link 2.com")], matches)

    def test_multiple_images(self):
        matches = extract_markdown_images("This text has ![multiple](folder/image.png) ![images](img.png)")
        self.assertListEqual([("multiple", "folder/image.png"), ("images", "img.png")], matches)

    def test_no_link(self):
        matches = extract_markdown_links("This text has no links.")
        self.assertListEqual([], matches)

    def test_no_image(self):
        matches = extract_markdown_images("This text has no image.")
        self.assertListEqual([], matches)

    def test_single_set_brackets(self):
        matches = extract_markdown_links("This text has [brackets] but no link.")
        self.assertListEqual([], matches)



class TestSplitImages(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual([
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
        ], new_nodes,)

    def test_single_image(self):
        node = TextNode("This is text with an ![image](img.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "img.png")
        ], new_nodes)

    def test_no_image(self):
        node = TextNode("This is text with no image.", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode("This is text with no image.", TextType.TEXT)], new_nodes)

    def test_only_image(self):
        node = TextNode("![This is only an image.](image.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode("This is only an image.", TextType.IMAGE, "image.png")], new_nodes)

    def test_no_image_with_brackets(self):
        node = TextNode("This is not an ![image]", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode("This is not an ![image]", TextType.TEXT)], new_nodes)

    def test_empty_string(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode("", TextType.TEXT)], new_nodes)

    def test_multiple_nodes(self):
        node1 = TextNode("This is an ![image](url)", TextType.TEXT)
        node2 = TextNode("Another ![image](url) - and another one ![image2](url2)", TextType.TEXT)
        new_nodes = split_nodes_image([node1, node2])
        expected = [
            TextNode("This is an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "url"),
            TextNode("Another ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "url"),
            TextNode(" - and another one ", TextType.TEXT),
            TextNode("image2", TextType.IMAGE, "url2")]
        self.assertListEqual(expected, new_nodes)



class TestSplitLinks(unittest.TestCase):
    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](link.com) and another [link2](link2.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual([
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "link.com"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("link2", TextType.LINK, "link2.com")
        ], new_nodes)

    def test_single_link(self):
        node = TextNode("This is text with a [link](url.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "url.com")
        ], new_nodes)

    def test_no_link(self):
        node = TextNode("This is text with no link.", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([TextNode("This is text with no link.", TextType.TEXT)], new_nodes)

    def test_only_link(self):
        node = TextNode("[This is only a link.](link.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([TextNode("This is only a link.", TextType.LINK, "link.com")], new_nodes)

    def test_no_link_with_brackets(self):
        node = TextNode("This is not a [link]", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([TextNode("This is not a [link]", TextType.TEXT)], new_nodes)

    def test_empty_string(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([TextNode("", TextType.TEXT)], new_nodes)

    def test_multiple_nodes(self):
        node1 = TextNode("This is a [link](url)", TextType.TEXT)
        node2 = TextNode("Another [link2](url2) - and another one [link3](url3)", TextType.TEXT)
        new_nodes = split_nodes_link([node1, node2])
        expected = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "url"),
            TextNode("Another ", TextType.TEXT),
            TextNode("link2", TextType.LINK, "url2"),
            TextNode(" - and another one ", TextType.TEXT),
            TextNode("link3", TextType.LINK, "url3")]
        self.assertListEqual(expected, new_nodes)


class TestTextToTextNodes(unittest.TestCase):
    def test_five_types(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev")]
        self.assertListEqual(expected, new_nodes)

    def test_multiple_links_and_images(self):
        text = "[link1](link1.com) ![image1](image1.png) [link2](link2.com) ![image2](image2.com)"
        expected = [
            TextNode("link1", TextType.LINK, "link1.com"),
            TextNode(" ", TextType.TEXT),
            TextNode("image1", TextType.IMAGE, "image1.png"),
            TextNode(" ", TextType.TEXT),
            TextNode("link2", TextType.LINK, "link2.com"),
            TextNode(" ", TextType.TEXT),
            TextNode("image2", TextType.IMAGE, "image2.com")
        ]
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(expected, new_nodes)

    def test_multiple_formatting(self):
        text = "This text has **bold text** and _italic text_ and more **bold text**. And some `code` as well."
        expected = [
            TextNode("This text has ", TextType.TEXT),
            TextNode("bold text", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic text", TextType.ITALIC),
            TextNode(" and more ", TextType.TEXT),
            TextNode("bold text", TextType.BOLD),
            TextNode(". And some ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" as well.", TextType.TEXT)
        ]
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(expected, new_nodes)

    def test_no_spaces(self):
        text = "ThisTextHas**Bold**TextButNo_Spaces_![image](img.png)[link](url.com)"
        expected = [
            TextNode("ThisTextHas", TextType.TEXT),
            TextNode("Bold", TextType.BOLD),
            TextNode("TextButNo", TextType.TEXT),
            TextNode("Spaces", TextType.ITALIC),
            TextNode("image", TextType.IMAGE, "img.png"),
            TextNode("link", TextType.LINK, "url.com"),
        ]
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(expected, new_nodes)

    def test_empty(self):
        text = ""
        expected = []
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(expected, new_nodes)

    def test_mismatched(self):
        text = "**Bold text** with stray ** tag"
        self.assertRaises(ValueError, text_to_textnodes, text)
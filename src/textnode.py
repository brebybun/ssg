from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str | None = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other) -> bool:
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    if text_node.text_type.value == "text":
        return LeafNode(None, text_node.text, None) # return text LeafNode
    elif text_node.text_type.value == "bold":
        return LeafNode("b", text_node.text, None) # return bold LeafNode
    elif text_node.text_type.value == "italic":
        return LeafNode("i", text_node.text, None) # return italic LeafNode
    elif text_node.text_type.value == "code":
        return LeafNode("code", text_node.text, None) # return link LeafNode
    elif text_node.text_type.value == "link":
        return LeafNode("a", text_node.text, {"href": text_node.url}) # return image LeafNode
    elif text_node.text_type.value == "image":
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text}) # error if not valid type
    raise ValueError("Error: text_node must be of type TEXT, BOLD, ITALIC, CODE, LINK, IMAGE")
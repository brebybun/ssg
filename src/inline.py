import re
from textnode import TextType, TextNode

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes: # TODO: can redo this more elegantly with regex i think
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
        elif node.text.count(delimiter) % 2 != 0:
            raise ValueError("Error: mismatched delimiters in text node")
        else:
            split_node_list = node.text.split(delimiter)
            for i in range(len(split_node_list)):
                if split_node_list[i] != "":
                    if i % 2 == 0:
                        new_nodes.append(TextNode(split_node_list[i], TextType.TEXT))
                    else:
                        new_nodes.append(TextNode(split_node_list[i], text_type))
    return new_nodes

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        #print(f"Node: '{node.text}'")
        #print(f"Node Type: '{node.text_type}'")
        if node.text_type is not TextType.TEXT:
            #print(f"Node is already formatted, appending: '{node}'")
            new_nodes.append(node)
        else:
            remaining_text = node.text
            #print(f"Declared remaining text as: '{remaining_text}'")
            images = extract_markdown_images(node.text)
            #print(f"Images found: '{images}'")
            for image in images:
                split_node = remaining_text.split(f"![{image[0]}]({image[1]})", 1)
                #print(f"Split node: '{split_node}'")
                if split_node[0] != "":
                    #print(f"Split node[0] exists, appending as text type: '{split_node[0]}'")
                    new_nodes.append(TextNode(split_node[0], TextType.TEXT))
                #print(f"Appending image node: '{TextNode(image[0], TextType.IMAGE, image[1])}'")
                new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
                remaining_text = split_node[1]
                #print(f"remaining_text is now: '{remaining_text}'")
            if not images:
                #print(f"No links found - appending node: '{node}'")
                new_nodes.append(node)
            elif remaining_text != "":
                #print(f"Adding remaining_text: '{remaining_text}'")
                new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        #print(f"Node: '{node.text}'")
        #print(f"Node Type: '{node.text_type}'")
        if node.text_type is not TextType.TEXT:
            #print(f"Node is already formatted, appending: '{node}'")
            new_nodes.append(node)
        else:
            remaining_text = node.text
            #print(f"Declared remaining_text as: '{remaining_text}'")
            links = extract_markdown_links(node.text)
            #print(f"Links found: '{links}'")
            for link in links:
                split_node = remaining_text.split(f"[{link[0]}]({link[1]})", 1)
                #print(f"Split node: '{split_node}'")
                if split_node[0] != "":
                    #print(f"Split node[0] exists, appending as text type: '{split_node[0]}'")
                    new_nodes.append(TextNode(split_node[0], TextType.TEXT))
                #print(f"Appending link node: '{TextNode(link[0], TextType.LINK, link[1])}'")
                new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
                remaining_text = split_node[1]
                #print(f"remaining_text is now: '{remaining_text}'")
            if not links:
                #print(f"No links found - appending node: '{node}'")
                new_nodes.append(node)
            elif remaining_text != "":
                #print(f"Adding remaining_text: '{remaining_text}'")
                new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes

def extract_markdown_images(text) -> list[tuple]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text) -> list[tuple]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def text_to_textnodes(text):
    new_nodes = [TextNode(text, TextType.TEXT)]
    new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    new_nodes = split_nodes_image(new_nodes)
    #print("Nodes after images:")
    #for node in new_nodes:
    #    print(node.text)
    #    print(node.text_type)
    new_nodes = split_nodes_link(new_nodes)
    #print("Nodes after links:")
    #for node in new_nodes:
    #    print(f'"{node.text}"')
    #    print(f'"{node.text_type}"')
    return new_nodes

if __name__ == "__main__":
    text_to_textnodes("[link1](link1.com) ![image1](image1.png) [link2](link2.com) ![image2](image2.com)")
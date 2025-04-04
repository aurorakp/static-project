import re

from leafnode import LeafNode
from textnode import TextNode, TextType

def text_node_to_html_node(text_node):
    match(text_node.text_type):
        case TextType.NORMAL:
            return LeafNode(tag=None, value=text_node.text)

        case TextType.BOLD:
            return LeafNode(tag='b', value=text_node.text)

        case TextType.ITALIC:
            return LeafNode(tag='i', value=text_node.text)

        case TextType.CODE:
            return LeafNode(tag='code', value=text_node.text)

        case TextType.LINK:
            return LeafNode(tag='a', value=text_node.text, props={'href': text_node.url})

        case TextType.IMAGE:
            return LeafNode(tag='img', value='', props={'src': text_node.url, 'alt': text_node.text})

        case _:
            raise ValueError('invalid text type')


def split_node_delimiter(node, delimiter, text_type, url=None):
    new_nodes = []
    if node.text.count(delimiter) % 2 != 0:
        raise ValueError(f'invalid Markdown syntax, closing delimiter {delimiter} not found')

    if node.text == '':
        return [TextNode(node.text, TextType.NORMAL)]

    text_parts = node.text.split(sep=delimiter)
    if text_parts[0] != '':
        new_nodes.append(TextNode(text_parts[0], TextType.NORMAL))
    for i in range(1, len(text_parts)):
        if i % 2 != 0:
            new_nodes.append(TextNode(text_parts[i], text_type, url=url))
        else:
            if text_parts[i] != '':
                new_nodes.append(TextNode(text_parts[i], TextType.NORMAL))

    return new_nodes

def split_nodes_delimiter(old_nodes, delimiter, text_type, url=None):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
        else:
            new_nodes.extend(split_node_delimiter(node, delimiter, text_type, url=url))
    return new_nodes        
                                  
def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.NORMAL))
            new_nodes.append(
                TextNode(
                    image[0],
                    TextType.IMAGE,
                    image[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.NORMAL))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.NORMAL))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.NORMAL))
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.NORMAL)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
            
def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks


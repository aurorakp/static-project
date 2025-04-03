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
    matches = re.findall(r'!\[(.*?)\]\((.*?)\)', text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r'\[(.*?)\]\((.*?)\)', text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
        else:
            matches = re.finditer(r'!\[(.*?)\]\((.*?)\)', node.text)
            match_indexes = []

            for m in matches:
                match_indexes.append([m.start(), m.end()])

            if len(match_indexes) == 0:
                new_nodes.append(node)
            else:
                if match_indexes[0][0] != 0:
                    new_nodes.append(TextNode(node.text[0:match_indexes[0][0]], TextType.NORMAL))

                for i in range(len(match_indexes)):
                    index_pair = match_indexes[i]
                    image_text, image_url = extract_markdown_images(node.text[index_pair[0]:index_pair[1]+1])[0]
                    new_nodes.append(TextNode(image_text, TextType.IMAGE, image_url))

                    if i != len(match_indexes) - 1:
                        if index_pair[1] < match_indexes[i+1][0] - 1:
                            new_nodes.append(TextNode(node.text[index_pair[1]:match_indexes[i+1][0]], TextType.NORMAL))
                    elif i == len(match_indexes) - 1:
                        if index_pair[1] != len(node.text):
                            new_nodes.append(TextNode(node.text[index_pair[1]:], TextType.NORMAL))
                
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
        else:
            matches = re.finditer(r'\[(.*?)\]\((.*?)\)', node.text)
            match_indexes = []

            for m in matches:
                match_indexes.append([m.start(), m.end()])

            if len(match_indexes) == 0:
                new_nodes.append(node)
            else:
                if match_indexes[0][0] != 0:
                    new_nodes.append(TextNode(node.text[0:match_indexes[0][0]], TextType.NORMAL))           

                for i in range(len(match_indexes)):
                    index_pair = match_indexes[i]
                    link_text, link_url = extract_markdown_links(node.text[index_pair[0]:index_pair[1]+1])[0]
                    new_nodes.append(TextNode(link_text, TextType.LINK, link_url))

                    if i != len(match_indexes) - 1:
                        if index_pair[1] < match_indexes[i+1][0] - 1:
                            new_nodes.append(TextNode(node.text[index_pair[1]:match_indexes[i+1][0]], TextType.NORMAL))
                    elif i == len(match_indexes) - 1:
                        if index_pair[1] != len(node.text):
                            new_nodes.append(TextNode(node.text[index_pair[1]+1:], TextType.NORMAL))
            
    return new_nodes


def text_to_textnodes(text):
    text_node = TextNode(text, TextType.NORMAL)
    return split_nodes_delimiter(split_nodes_delimiter(split_nodes_delimiter(split_nodes_link(split_nodes_image([text_node])), '`', TextType.CODE, ), '_', TextType.ITALIC), '**', TextType.BOLD)
            

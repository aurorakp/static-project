from textnode import TextNode, TextType
from parentnode import ParentNode
from blocks import BlockType, block_to_block_type
from converters import markdown_to_blocks, text_node_to_html_node, text_to_textnodes

def markdown_to_html_node(markdown):
    markdown_blocks = markdown_to_blocks(markdown)
    all_blocks = [markdown_block_to_html_node(b) for b in markdown_blocks]
    page_node = ParentNode(tag='div', children=all_blocks)
    return page_node
    
def markdown_block_to_html_node(block):
    block_type = block_to_block_type(block)
    match (block_type):
        case BlockType.CODE:
            return extract_html_children_from_code(block)

        case BlockType.PARAGRAPH:
            return extract_html_children_from_paragraph(block)

        case BlockType.HEADING:
            return extract_html_children_from_heading(block)

        case BlockType.QUOTE:
            return extract_html_children_from_quote(block)

        case BlockType.UNORDERED_LIST:
            return extract_html_children_from_ul(block)

        case BlockType.ORDERED_LIST:
            return extract_html_chlidren_from_ol(block)

        case _:
            raise ValueError("Invalid block type")

def extract_children_from_plain_text(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for node in text_nodes:
        html_node = text_node_to_html_node(node)
        html_nodes.append(html_node)
    return html_nodes
        
def extract_html_children_from_ul(text):
    split_lines = text.split('\n')
    line_nodes = []
    for line in split_lines:
        content = line[2:]
        line_children = extract_children_from_plain_text(content)
        line_nodes.append(ParentNode(tag='li', children=line_children))
    return ParentNode(tag='ul', children=line_nodes)

def extract_html_chlidren_from_ol(block):
    split_lines = block.split('\n')
    line_nodes = []
    for line in split_lines:
        content = line[3:]
        line_children = extract_children_from_plain_text(content)
        line_nodes.append(ParentNode(tag='li', children=line_children))
    return ParentNode(tag='ol', children=line_nodes)

def extract_html_children_from_quote(block):
    split_lines = block.split('\n')
    quote_lines = []
    for quote_line in split_lines:
        if not quote_line.startswith(">"):
            raise ValueError("invalid quote block")
        quote_lines.append(quote_line.lstrip(">").strip())
    quote_text = " ".join(quote_lines)
    quote_children = extract_children_from_plain_text(quote_text)
    return ParentNode(tag="blockquote", children=quote_children)

def extract_html_children_from_heading(block):
    hash_level = 0
    for ch in block:
        if ch == "#":
            hash_level += 1
        else:
            break
    tag = f'h{hash_level}'
    if hash_level + 1 > len(block):
        raise ValueError('invalid heading level for block size')
    text = block[hash_level + 1 :]
    heading_nodes = extract_children_from_plain_text(text)
    return ParentNode(tag=tag, children=heading_nodes)

def extract_html_children_from_paragraph(block):
    lines = block.split('\n')
    block_paragraph = " ".join(lines)
    paragraph_nodes = extract_children_from_plain_text(block_paragraph)
    return ParentNode(tag='p', children=paragraph_nodes)

def extract_html_children_from_code(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid markings for code block")
    code_block = block.lstrip('```\n').rstrip('```')
    code_text_node = text_node_to_html_node(TextNode(text=code_block, text_type=TextType.NORMAL))
    code_node = ParentNode(tag="code", children=[code_text_node])
    return ParentNode(tag='pre', children=[code_node])
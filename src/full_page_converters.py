from pathlib import Path
import os
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

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    header_line = None
    for block in blocks:
        print(f'block: {block}')
        lines = block.split('\n')
        for line in lines:
            if line.startswith('# '):
                header_line = line
                break
    if header_line is None:
        raise ValueError('No title line!')
    return header_line.lstrip('# ').rstrip()

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    if not os.path.exists(from_path):
        raise ValueError("'from_path' directory does not exist'")
    if not os.path.exists(template_path):
        raise ValueError("'template_path' file does not exist")
    markdown = None
    template = None
    try:
        with open(from_path, 'r')as f:
            markdown = f.read()
    except Exception as e:
        raise Exception(f'Error while trying to parse {from_path}: {str(e)}'
                        )
    try:
        with open(template_path, 'r') as f:
            template = f.read()
    except Exception as e:
        raise Exception(f'Error while trying to parse {template_path}: {str(e)}'
                        )
    markdown_node = markdown_to_html_node(markdown)
    html_string = markdown_node.to_html()
    print(f'html_string: {html_string}')
    title = extract_title(markdown)
    template = template.replace('href="', 'href="' + basepath.rstrip('/'))
    formatted_template = template.replace('{{ Title }}', title).replace('{{ Content }}', html_string)
    print(f'formatted template: {formatted_template}')
    formatted_template = formatted_template.replace('href=/', 'href=' + basepath)
    formatted_template = formatted_template.replace('src=/', 'src=' + basepath)

    dest_file = Path(dest_path)
    dest_file.parent.mkdir(exist_ok=True, parents=True)
    try:
        with open(dest_path, 'w+') as f:
            f.write(formatted_template)
    except Exception as e:
        raise Exception(f'Error while trying to write {dest_path}: {str(e)}')


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for filename in os.listdir(dir_path_content):
        start = os.path.join(dir_path_content, filename)
        end = os.path.join(dest_dir_path, filename)
        if os.path.isfile(start):
            end = Path(end).with_suffix('.html')
            generate_page(start, template_path, end, basepath)
        else:
            generate_pages_recursive(start, template_path, end, basepath)
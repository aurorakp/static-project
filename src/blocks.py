from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
    if re.match('#{1,6}\s.+', block) is not None:
        return BlockType.HEADING

    if re.match('`.+`', block, re.DOTALL) is not None:
        return BlockType.CODE

    block_lines = block.split('\n')

    if all([l[0] == '>' for l in block_lines]):
        return BlockType.QUOTE
    
    if all([l[:2] == '- ' for l in block_lines]):
        return BlockType.UNORDERED_LIST

    for i in range(len(block_lines)):
        if len(block_lines[i]) < 3:
            return BlockType.PARAGRAPH
            
        if block_lines[i][:3] != f'{i+1}. ': 
            return BlockType.PARAGRAPH

    return BlockType.ORDERED_LIST
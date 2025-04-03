import unittest
from blocks import BlockType, block_to_block_type

class BlocksTest(unittest.TestCase):

    def test_heading(self):
        block_str = '### asdf'
        self.assertEqual(block_to_block_type(block_str), BlockType.HEADING)

    def test_code(self):
        block_str = '``` some code here ```'
        self.assertEqual(block_to_block_type(block_str), BlockType.CODE)

    def test_quote(self):
        block_str = ">this is a quote\n> with some extra lines\n>that should still work "
        self.assertEqual(block_to_block_type(block_str), BlockType.QUOTE)

    def test_unordered_list(self):
        block_str = '- an item\n- another item  \n- still another one'
        self.assertEqual(block_to_block_type(block_str), BlockType.UNORDERED_LIST)

    def test_ordered_list(self):
        block_str = '1. item one\n2.  item two  \n3. item three'
        self.assertEqual(block_to_block_type(block_str), BlockType.ORDERED_LIST)

    def test_paragraph(self):
        block_str_1 = 'asdf'
        block_str_2 = '<not a complete quote block\nnopethislinefails'
        block_str_3 = '- this is not an unordered list\nbecausethis line fails'
        block_str_4 = '1. this list is out of order\n3. yes \n4. yup'
        block_str_5 = '` not a code block due to missing backticks '
        block_str_6 = '##not a heading as no whitespace between'
        self.assertEqual(block_to_block_type(block_str_1), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(block_str_2), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(block_str_3), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(block_str_4), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(block_str_5), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(block_str_6), BlockType.PARAGRAPH)
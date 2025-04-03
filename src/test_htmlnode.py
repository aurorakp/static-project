import unittest
from htmlnode import HTMLNode

class TestHtmlNode(unittest.TestCase):

    def test_html_nyi(self):
        node = HTMLNode()
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_props_to_html(self):
        node = HTMLNode(props={'href': 'https://www.google.com', 'target': '_blank'})
        self.assertEqual(node.props_to_html(), ' href=https://www.google.com target=_blank')

    def test_repr_empty(self):
        node = HTMLNode()
        self.assertEqual(str(node), 'Tag: None Value: None Children: None Props: None')

    def test_repr(self):
        child1 = HTMLNode()
        child2 = HTMLNode()
        node = HTMLNode(tag='p', value='asdf', children=[child1, child2], props={'a': 'b'})
        result = str(node)

        self.assertIn("Tag: p", result)
        self.assertIn("Value: asdf", result)
        self.assertIn("Props: {'a': 'b'}", result)
        
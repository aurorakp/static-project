import unittest
from leafnode import LeafNode
from parentnode import ParentNode


class TestParentNode(unittest.TestCase):

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_multiple_children(self):
        child1_node = LeafNode("span", "child1")
        child2_node = LeafNode("span", "child2")
        parent_node = ParentNode("div", [child1_node, child2_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child1</span><span>child2</span></div>")

    def test_to_html_with_no_tag(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(None, [child_node])
        with self.assertRaisesRegex(ValueError, 'no tag'):
            parent_node.to_html()

    def test_to_html_with_no_children(self):
        parent_node = ParentNode('p', None)
        with self.assertRaisesRegex(ValueError, 'no children'):
            parent_node.to_html()

    def test_to_html_with_props(self):
        child_node = LeafNode("a", "child", {'href': 'https://boot.dev'})
        parent_node = ParentNode("div", [child_node], {'a': 'b'})  
        self.assertEqual(parent_node.to_html(), "<div a=b><a href=https://boot.dev>child</a></div>")
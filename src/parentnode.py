import functools

from htmlnode import HTMLNode
from leafnode import LeafNode



class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError('no tag')

        if self.children is None or len(self.children) == 0:
            raise ValueError('no children')
        
        props_html = self.props_to_html()

        child_html = ""
        for child in self.children:
            child_html = child_html + child.to_html()

        html = f'<{self.tag}{props_html}>{child_html}</{self.tag}>'
        return html

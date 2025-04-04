

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props is None or len(self.props) == 0:
            return ""
            
        return ''.join(map(lambda x: f' {x[0]}={x[1]}', self.props.items()))

    def __repr__(self):
        return f'HTML Node properties: Tag: {self.tag} Value: {self.value} Children: {self.children} Props: {self.props}'


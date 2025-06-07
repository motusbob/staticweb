from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, children=None, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError
        if self.tag is None:
            return str(self.value)
        else:
            html_tag = ""
            html_tag += f"<{self.tag}"
            if self.props is not None:
                html_tag += self.props_to_html()
            html_tag += f">{self.value}</{self.tag}>"
            return html_tag

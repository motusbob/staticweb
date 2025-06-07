from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError
        if self.children is None:
            return ValueError("Must have a children node")
        else:
            html_tag = ""
            html_tag += f"<{self.tag}>"
            for child in self.children:
                html_tag += child.to_html()
            html_tag += f"</{self.tag}>"
            return html_tag

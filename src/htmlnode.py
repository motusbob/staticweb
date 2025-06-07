
class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        str = ""
        for k,v in self.props.items():
            str += f" {k}={v}"
        return str

    def __repr__(self):
        str = ""
        if self.tag is not None:
            str += f"Tag: {self.tag}\n"
        if self.value is not None:
            str += f"Value: {self.value}\n"
        if self.children is not None:
            str += f"Children: {self.children}\n"
        if self.props is not None:
            str += f"Props: {self.props_to_html()}\n"
        return str


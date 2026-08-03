class HTMLNode:
    def __init__(self,
            tag: str | None = None,
            value: str | None = None,
            children: list | None = None,
            props: dict | None = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        return_string = ""
        if self.props is not None:
            for prop in self.props:
                return_string += f' {prop}="{self.props[prop]}"'
        return return_string

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
class HTMLNode: # basic class structure for HTML node, input variables are all optional and default to None
    def __init__(self,
            tag: str | None = None,
            value: str | None = None,
            children: list | None = None,
            props: dict | None = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self): # will be overwritten by children classes
        raise NotImplementedError

    def props_to_html(self) -> str: # converts the given "props" value to actual HTML format
        props_html = ""
        if self.props is not None:
            for prop in self.props:
                props_html += f' {prop}="{self.props[prop]}"'
        return props_html

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HTMLNode): # child class for nodes that have no children
    def __init__(self, tag: str | None, value: str, props: dict | None = None): # tag and value is required
        super().__init__(tag, value, None, props) # initiates parent variables, sets children to None

    def to_html(self) -> str: # converts to a valid HTML string
        if self.value is None:
            raise ValueError("Value error: value must not be None")
        if self.tag is None:
            return self.value
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'

    def __repr__(self): # doesn't include the children value unlike the parent class
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
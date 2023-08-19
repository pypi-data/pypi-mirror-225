from .yaml_item import YamlItem


class PageInput:
    root_item: YamlItem = None
    name: str = ""

    def __init__(self, name, root_item=None) -> None:
        self.root_item = root_item
        self.name = name

    @property
    def comments(self):
        if self.root_item:
            return self.root_item.comments
        return []

    @property
    def line_comment(self):
        if self.root_item:
            return self.root_item.line_comment
        return ""

    @property
    def values(self):
        if self.root_item:
            return self.root_item.value
        return []

    @property
    def object_type(self):
        return self.root_item.object_type()

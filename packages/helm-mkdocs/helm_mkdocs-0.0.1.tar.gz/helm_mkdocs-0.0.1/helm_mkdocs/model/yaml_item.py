from typing import Optional, Union


class YamlItem:
    name: str
    value: Union[str, bool, int, float, dict[str, "YamlItem"], list["YamlItem"]]
    type: str
    line_comment: str
    comments: [str]
    examples: [str]
    parent: Optional["YamlItem"]

    def __init__(self, name=None, value=None):
        self.name = name
        self.examples = []
        self.comments = []
        self.line_comment = ""
        self.value = value
        self.parent = None
        self.type = ""
        self._depth = None

    def __repr__(self) -> str:
        return "%s: %s" % (self.name, self.value)

    def add_value(self, current_item):
        if not isinstance(self.value, dict) and not isinstance(self.value, list):
            raise "Cannot append to non collection type"
        current_item.parent = self
        if isinstance(self.value, list):
            current_item.name = len(self.value)
            self.value.append(current_item)
        if isinstance(self.value, dict):
            self.value[current_item.name] = current_item

    @property
    def object_type(self):
        if not self.type:
            self.type = self._guess_type()
        return self.type

    def _guess_type(self):
        if isinstance(self.value, dict):
            return 'object'
        if isinstance(self.value, list):
            return 'list'
        if self.value is None:
            return "null"
        try:
            int(self.value)
            return 'number'
        except ValueError:
            pass
        if self.value.lower() in ["true", "false"]:
            return 'boolean'
        if self.value in ["[]", "[ ]"]:
            return "list"
        if self.value in ["{}}", "{ }"]:
            return "object"

        return "string"

    @property
    def depth(self):
        if self._depth is None:
            self._depth = -2
            item = self
            while item is not None:
                self._depth += 2
                item = item.parent
        return self._depth
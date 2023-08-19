from enum import Enum

TokenType = Enum('TokenType',
                 ['comment', 'line_comment', 'name', 'value', 'pipe', 'pipe_start', 'pipe_end', 'list_start',
                  'list_item', 'list_end', 'object_start', 'object_end', 'line', 'value_start', 'value_end',
                  'depth_up', 'depth_down', 'object_list_start', 'object_list_end', 'start_new_value',
                  'end_new_value'])


class YamlTokenException(Exception):

    def __init__(self, token, expected) -> None:
        super().__init__(
            "Unexpected token %s, expected %s. (line: %s - %s)" % (
                str(token.type), ", ".join([str(exp) for exp in expected]), token.line, token.value))


class Token:
    type: TokenType
    value: str
    depth: int
    line: int

    def __init__(self, type, value, depth, line):
        self.type = type
        self.value = value
        self.depth = depth
        self.line = line

    def __repr__(self):
        return "%d: %s %s %s %d" % (self.line, " " * self.depth, self.value, self.type, self.depth)

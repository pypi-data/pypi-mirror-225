import os
import re
from typing import Tuple

from helm_mkdocs.model import TokenType, Token
from helm_mkdocs.model import YamlItem


def count_depth(line):
    count = 0
    for char in line:
        if char == ' ':
            count += 1
            continue
        return count


def split_comment(value) -> Tuple[str, str]:
    # the line has quotes and a comment
    if "'" in value or '"' in value:
        split = re.compile('("[^"]*" #|\'[^\']*\' #)').split(value)
        return "".join(split[0:-1])[0:-1], "# " + split[-1]
    # line is a simple comment on unquoted line
    else:
        value_split = value.split("#")
        return value_split[0], "# " + "#".join(value_split[1:])  # comments can have # in them so rejoin the #


def tokenize_objects(lines):
    class State:
        is_pipe = -1

    class Open:
        def __init__(self, depth, type):
            self.depth = depth
            self.type = type

        def end_token_type(self):
            match self.type:
                case 'object':
                    return TokenType.object_end
                case 'list':
                    return TokenType.list_end
                case 'value':
                    return TokenType.value_end
                case 'pipe':
                    return TokenType.pipe_end
                case 'object_list':
                    return TokenType.object_list_end

    def object_start(_opens, depth, line):
        _token = Token(TokenType.object_start, None, depth, line)
        _opens.append(Open(depth, 'object'))
        return _opens, _token

    def pipe_start(_opens, depth, line):
        _token = Token(TokenType.pipe_start, None, depth, line)
        _opens.append(Open(depth, 'pipe'))
        state.is_pipe = depth
        return _opens, _token

    def list_start(_opens, depth, line):
        _token = Token(TokenType.list_start, None, depth, line)
        _opens.append(Open(depth, 'list'))
        return _opens, _token

    def object_list_start(_opens, depth):
        _opens.append(Open(depth, 'object_list'))
        return _opens

    def close_to_depth(_opens, depth, line):
        if len(_opens) == 0:
            return
        current = _opens[-1]
        while current.depth > depth:
            yield Token(current.end_token_type(), None, current.depth, line)
            if current.end_token_type() == TokenType.pipe_end:
                state.is_pipe = -1
            _opens.pop()
            if len(_opens) == 0:
                return
            current = _opens[-1]

    opens: [Open] = []

    await_start = False
    state = State()

    for token in tokenize_lines(lines, state):
        if token.type == TokenType.line:
            yield token
            continue

        # the depth has changed, so we need to check the type
        if await_start and token.type != TokenType.comment:
            if token.type == TokenType.name or token.type == TokenType.value_start:
                opens, start_token = object_start(opens, token.depth, token.line)
                yield start_token
            if token.type == TokenType.list_item:
                opens, start_token = list_start(opens, token.depth, token.line)
                yield start_token
            if token.type == TokenType.pipe:
                opens, start_token = pipe_start(opens, token.depth, token.line)
                yield start_token
                await_start = False
                continue
            await_start = False

        if token.type == TokenType.object_list_start:
            object_list_start(opens, token.depth)
        # if the depth is going up then we should await the next token to decide if it is a list or object
        if token.type == TokenType.depth_up:
            await_start = True

        if token.type == TokenType.depth_down:
            yield from close_to_depth(opens, token.depth, token.line)

        yield token

    opens.reverse()

    for _open in opens:
        match _open.type:
            case 'object':
                yield Token(TokenType.object_end, None, _open.depth, len(lines))
            case 'list':
                yield Token(TokenType.list_end, None, _open.depth, len(lines))
            case 'value':
                yield Token(TokenType.value_end, None, _open.depth, len(lines))
            case 'pipe':
                yield Token(TokenType.pipe_end, None, _open.depth, len(lines))
            case 'object_list':
                yield Token(TokenType.object_list_end, None, _open.depth, len(lines))


def tokenize_lines(lines, state):
    current_depth = 0
    for line_token in tokenize(lines):
        # yield the line token to next level, can be ignored by users
        yield line_token

        # if we are consuming a pipe then do not tokenize the lines
        if state.is_pipe != -1 and line_token.depth >= state.is_pipe:
            yield Token(TokenType.value, "%s\n" % line_token.value, line_token.depth, line_token.line)
            continue

        if line_token.value == "":
            continue

        # if the depth has changed then yield a change
        if line_token.depth > current_depth:
            yield Token(TokenType.depth_up, line_token.depth - current_depth, line_token.depth, line_token.line)
        if line_token.depth < current_depth:
            yield Token(TokenType.depth_down, line_token.depth - current_depth, line_token.depth, line_token.line)
        current_depth = line_token.depth

        # line is a comment line so yield and continue
        if line_token.value.startswith("#"):
            yield Token(TokenType.comment, line_token.value, line_token.depth, line_token.line)
            continue

        # now we have to deal with the possible options for the line e.g:
        # Value statement `name: value`
        # List or Object statement `name:`
        # List item statement ` - value` or ` - some: value`
        # Pipe statement `name: |` or `name: |-`

        # all the above statements can have a line comment so lets first strip that off
        name_value = line_token.value
        line_comment = None
        if "#" in name_value:
            name_value, line_comment = split_comment(line_token.value)

        # name_value should now be one of the above statements,
        # with line_comment being any line comment that is on the line

        # let's start with lists
        is_list = False
        if name_value.startswith("- "):
            # at this point we do not track list start/end we just deal with the line data,
            # so we need to yield a list item at the current depth
            yield Token(TokenType.list_item, None, line_token.depth, line_token.line)
            # remove the list marker from the name_value
            name_value = name_value[2:]
            is_list = True

        # if we have a colon then we are not a value list, so we can remove that option
        if ":" not in name_value:
            yield Token(TokenType.value_start, None, current_depth, line_token.line)
            yield Token(TokenType.name, 'list_item', line_token.depth, line_token.line)
            yield Token(TokenType.value, name_value, line_token.depth, line_token.line)
            if line_comment:
                yield Token(TokenType.line_comment, line_comment, line_token.depth, line_token.line)
            yield Token(TokenType.value_end, None, current_depth, line_token.line)
            continue

        # now we are left with the move complex options.
        split = name_value.split(":")
        name = split[0].strip()
        value = split[1].strip()

        # let's deal with pipes
        if value in ["|", "|-", "|+", ">", ">-", ">+"]:
            yield Token(TokenType.name, name, line_token.depth, line_token.line)
            current_depth += 2
            yield Token(TokenType.depth_up, +2, current_depth, line_token.line)
            yield Token(TokenType.pipe, value, current_depth, line_token.line)
            if line_comment:
                yield Token(TokenType.line_comment, line_comment, current_depth, line_token.line)
            continue

        # we could also be just a list or object statement
        if value == "":
            yield Token(TokenType.name, name, line_token.depth, line_token.line)
            if line_comment:
                yield Token(TokenType.line_comment, line_comment, line_token.depth, line_token.line)
            continue

        # now we have to be either a list of objects or a value statement
        if is_list:
            current_depth += 2
            # as we know that we are a new object in a list, send a depth up to indicated we are at a new level
            yield Token(TokenType.depth_up, +2, current_depth, line_token.line)
        # now yield the name and value
        yield Token(TokenType.value_start, None, current_depth, line_token.line)
        yield Token(TokenType.name, name, current_depth, line_token.line)
        yield Token(TokenType.value, value, current_depth, line_token.line)
        if line_comment:
            yield Token(TokenType.line_comment, line_comment, current_depth, line_token.line)
        yield Token(TokenType.value_end, None, current_depth, line_token.line)


def tokenize(lines):
    iterator = iter(lines)
    line_number = 1
    line = next(iterator, None)
    while line is not None:
        depth = count_depth(line)
        yield Token(TokenType.line, line.strip(), depth, line_number)
        line_number += 1
        line = next(iterator, None)


def read_yaml_raw(file, log_tokens=False):
    with open(file) as f:
        readlines = f.readlines()
        for token in tokenize_objects(readlines):
            print(token)


def check_examples(comments, examples, parent):
    if len(examples) == 0:
        return examples, comments
    optional = YamlItem()
    optional.examples = examples
    optional.comments = comments
    parent.add_value(optional)
    return [], []


def read_yaml(file, log_tokens=False) -> YamlItem:
    dirname = os.path.basename(os.path.dirname(file))

    item = YamlItem(name=dirname, value={})
    current_parent = item
    current_item = None
    comments = []
    with open(file) as f:
        readlines = f.readlines()
        for token in tokenize_objects(readlines):
            if log_tokens:
                print(token)
            match token.type:
                # object start will come before the name of the object
                case TokenType.object_start:
                    if current_item is None:
                        current_item = YamlItem()
                        if isinstance(current_parent.value, list):
                            current_parent.add_value(current_item)
                            if len(comments) > 0:
                                current_item.comments = comments
                                comments = []
                    # then create a new object - name will be set on next token
                    current_item.value = {}
                    current_parent = current_item
                    current_item = None
                # object end will come when there are not more tokens for the current
                # object, so we should move up the hierarchy
                case TokenType.object_end:
                    current_item = None
                    current_parent = current_parent.parent
                # value start means a new simple value is coming
                case TokenType.value_start:
                    current_item = YamlItem(value="")
                # value start means a simple value is complete
                case TokenType.value_end:
                    current_item = None
                # name will come to name a new object or new value
                case TokenType.name:
                    if current_item is None:
                        current_item = YamlItem()
                    current_item.name = token.value
                    if len(comments) > 0:
                        current_item.comments = comments
                        comments = []
                    current_parent.add_value(current_item)
                case TokenType.value:
                    current_item.value += str(token.value)
                case TokenType.line_comment:
                    current_item.line_comment = token.value
                case TokenType.comment:
                    # comments can come before the object start or value
                    comments.append(token.value)
                case TokenType.list_start:
                    if current_item is None:
                        current_item = YamlItem()
                    # then create a new object - name will be set on next token
                    current_item.value = []
                    current_parent = current_item
                    current_item = None
                case TokenType.list_end:
                    current_item = None
                    current_parent = current_parent.parent
                case TokenType.pipe_start:
                    current_item.value = ""
                case TokenType.pipe_end:
                    current_item = None
    return item

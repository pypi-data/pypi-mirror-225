"""
Utilities for working with transforms in the CLI.
"""
import json
import yaml
import sys


def load_transform(file):
    if file.endswith('.yaml') or file.endswith('.yml'):
        loader = _yaml_load
    elif file.endswith('.json'):
        loader = json.load
    elif file.endswith('.md'):
        loader = load_from_markdown
    elif file.endswith('.lua'):
        loader = load_from_lua
    else:
        print("Only YAML, JSON, Lua, and Markdown files may be uploaded.")
        sys.exit(1)

    with open(file, 'r', encoding='utf-8') as fd:
        pages = loader(fd)
    return pages


def _yaml_load(fd):
    return list(yaml.load_all(fd, Loader=yaml.Loader))


def load_from_lua(source):  # noqa: C901
    import lupa.lua53

    info = {'description': '', 'configurationSchema': None}
    content = list(source)

    lua = lupa.lua53.LuaRuntime()
    try:
        lua.execute("".join(content))
    except lupa.lua53.LuaSyntaxError as e:
        print(e)
        return

    # find top comment in file
    first = None
    last = None
    for i in range(0, len(content)-1):
        if first is None and content[i].startswith('--[['):
            first = i
        elif first is not None and last is None and (
                content[i].startswith(']]') or content[i].startswith('--]]')):
            last = i
            break
    if first is None or last is None:
        print("No top-level comment found in file.")
        return

    lines = content[first+1:last-1]
    name, lines = _get_name(lines)
    info['name'] = name

    for line in lines:
        line = line.strip()
        if line.startswith('@'):
            parts = line[1:].split(' ', maxsplit=1)
            if len(parts) == 2:
                if parts[0] in ['input', 'output']:
                    bits = parts[1].split(' ', maxsplit=1)
                    try:
                        info[parts[0] + 's'][bits[0]] = bits[1]
                    except KeyError:
                        info[parts[0] + 's'] = {bits[0]: bits[1]}
                else:
                    info[parts[0]] = parts[1]
        else:
            info['description'] += line + '\n'

    if lua.globals().configurationSchema is not None:
        info['configurationSchema'] = _table_to_dict(lua.globals().configurationSchema)

    info['implementation'] = ''.join(content)
    return info


def _table_to_dict(lua_value):
    if lua_value is None:
        return None
    if isinstance(lua_value, (str, bool, int, float)):
        return lua_value
    d = {k: _table_to_dict(v) for k, v in lua_value.items()}
    if all([isinstance(n, int) for n in d.keys()]):
        return [v for _, v in sorted(d.items())]
    else:
        return d


def load_from_markdown(source):
    info = {}
    content = list(source)
    if content[0] == "---\n":
        split_at = len(content)
        # get metadata from header
        for i in range(1, len(content)-1):
            if content[i] == "---\n":
                split_at = i
                break
        raw_yaml = "".join(content[1:split_at])
        content = content[split_at+1:]
        info = yaml.load(raw_yaml, Loader=yaml.Loader)

    info['configurationSchema'] = None
    info['description'] = ''

    name, content = _get_name(content)
    chunks = _split_into_chunks(content)

    # first chunk is the description if it doesn't have a '##' at the start
    if not chunks[0][0].startswith('## '):
        info['description'] = "".join(chunks[0])
        chunks = chunks[1:]

    info['name'] = name

    for chunk in chunks:
        _update_info_from_chunk(info, chunk)

    info['kind'] = 'transform'

    return info


def _update_info_from_chunk(info, chunk):
    if chunk[0].startswith('## Metadata'):
        info.update(yaml.load("".join(chunk[1:]), Loader=yaml.Loader))
    if chunk[0].startswith('## Configuration Schema'):
        # we need the ```yaml ... ``` parts (or json)
        source = _find_fenced_block(chunk[1:], "yaml")
        if source is not None:
            info['configurationSchema'] = yaml.load("".join(source), Loader=yaml.Loader)
        else:
            source = _find_fenced_block(chunk[1:], "json")
            if source is not None:
                info['configurationSchema'] = json.loads("".join(source))
    if chunk[0].startswith('## Implementation'):
        # we need the ```lua ... ``` parts
        lua = _find_fenced_block(chunk[1:], "lua")
        if lua is not None:
            info['implementation'] = "".join(lua)


def _get_name(content):
    name = None
    # the first top-level header is the name of the transform
    for i in range(0, len(content)-1):
        if content[i].startswith('# '):
            name = content[i][2:].strip()
            content = content[i+1:]
            break
    return name, content


def _split_into_chunks(content):
    chunks = []
    chunk = []
    for line in content:
        if line.startswith('## '):
            if len(chunk) > 0:
                chunks.append(chunk)
            chunk = []
        chunk.append(line)
    if len(chunk) > 0:
        chunks.append(chunk)
    return chunks


def _find_fenced_block(chunk, tag):
    buffer = []
    started = False
    for line in chunk:
        if not started and line == f'```{tag}\n':
            started = True
            continue
        if started and line == '```\n':
            return buffer
        if started:
            buffer.append(line)
    return None

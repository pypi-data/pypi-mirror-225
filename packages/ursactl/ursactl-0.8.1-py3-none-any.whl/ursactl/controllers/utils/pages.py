"""
Utilities for loading pages and getting metadata from the header.
"""
import yaml
import sys


def load_page(file):
    if file.endswith('.md'):
        loader = load_from_markdown
    else:
        print("Only Markdown files may be uploaded.")
        sys.exit(1)

    with open(file, 'r', encoding='utf-8') as fd:
        pages = loader(fd)
    return pages


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

    title, content = _get_title(content)

    if title is not None:
        info['title'] = title
    info['content'] = "".join(content)
    info['kind'] = 'page'

    return info


def _get_title(content):
    title = None
    # the first top-level header is the name of the transform
    for i in range(0, len(content)-1):
        if content[i].startswith('# '):
            title = content[i][2:].strip()
            content = content[i+1:]
            break
    return title, content

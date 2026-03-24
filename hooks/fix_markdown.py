import re


def on_page_markdown(markdown, **kwargs):
    """Add blank line before list items that follow non-list, non-blank lines.

    Fixes Python-Markdown treating list items as part of preceding paragraphs
    when there's no blank line separator (e.g. after *참고: URL* lines).
    """
    lines = markdown.split('\n')
    result = []
    for i, line in enumerate(lines):
        if i > 0 and re.match(r'^[-*+] ', line):
            prev = lines[i - 1].strip()
            if prev and not re.match(r'^[-*+] |^\d+\. ', prev):
                result.append('')
        result.append(line)
    return '\n'.join(result)

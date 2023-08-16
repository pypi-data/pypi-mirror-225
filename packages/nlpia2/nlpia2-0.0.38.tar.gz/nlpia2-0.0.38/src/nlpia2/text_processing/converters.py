""" Utilities for manipulating asccidoc (asciidoctor) documents

Typical DocTestParser Expression objects:
{'source': 'import spacy\n', 
 'want': '',
 'lineno': 64,
 'indent': 0,
 'options': {},
 'exc_msg': None},
{'source': 'nlp = spacy.load("en_core_web_sm")\n',
 'want': '',
 'lineno': 65,
 'indent': 0,
 'options': {},
 'exc_msg': None},
{'source': 'sentence = \"\"\"The faster Harry got to the store, the faster Harry,\n    the ...',
 'want': '',
 'lineno': 67,
 'indent': 0,
 'options': {},
 'exc_msg': None}
"""
from doctest import DocTestParser
from pathlib import Path
import re
import nbformat as nbf
from nlpia2.text_processing.extractors import parse_args
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell

HEADER_TEXT = f"""\
### Imports and Settings

>>> import pandas as pd
>>> pd.options.display.max_columns = 3000
"""
HEADER_BLOCKS = [
    dict(source='### Imports and Settings', typ='markdown'),
    dict(source='''\
        >>> import pandas as pd
        >>> pd.options.display.max_columns = 3000
        ''', typ='python')
]

TEST_TEXT = f"""\
### A dataframe

>>> pd.DataFrame([[1,2],[3,4]])
   0  1
0  1  2
1  2  3
"""
TEST_BLOCKS = [
    dict(source='### A dataframe', typ='markdown'),
    dict(source='''\
        >>> pd.DataFrame([[1,2],[3,4]])
        ''', typ='python',
         want='''\
           0  1
        0  1  2
        1  2  3
        ''')
]


ADOC_CODEBLOCK_HEADER = [
    r'[.][-\w\s\(\)\[\]\|!@#{}&^%$+=<,>.?/]+'  # '.Problem setup'
    r'\[source,python\]\s*',
    r'----[-]*\s*',
]

ADOC_CODEBLOCK_HEADER_REVERSED = reversed(ADOC_CODEBLOCK_HEADER)


def get_examples(text, with_headings=True):
    dtparser = DocTestParser()
    expressions = dtparser.get_examples(text)
    lines = text.splitlines()

    # FIXME: need function to convert arrays of lines and expressions into blocks
    blocks = []
    for i, exp in enumerate(expressions):
        for k in range(expressions['lineno'] - 1, -1, -1):
            lineno = k
            line = lines[lineno]
            if line.strip() and re.match(r'----[-]*\s*', line):
                lineno -= 1
                line = lines[lineno]
            if line.strip() and re.match(r'\[source,python\]\s*', line):
                lineno -= 1
                line = lines[lineno]
                if line.strip() and re.match(r'[.][-\w\s\(\)\[\]\|!@#{}&^%$+=<,>.?/]+', line):
                    exp[i]['markdown'] = exp[i].get('markdown', '') + f'#### {line[1:]}'
    return expressions


def adoc2ipynb(filepath=None, dest_filepath=None, **kwargs):
    text = kwargs.pop('text', None) or ''
    dest_filepath = dest_filepath if not dest_filepath else Path(dest_filepath)
    if filepath:
        expressions = get_examples(filepath.read())
    else:
        expressions = get_examples(text)

    nb = new_notebook()
    cells = []
    cells.append(new_markdown_cell(f"#### {filepath}"))

    for exp in expressions:
        # need to run the doctest parser on a lot of text to get attr names right
        if isinstance(exp, str):
            cells.append(new_markdown_cell(exp))
        if hasattr(exp, 'text'):
            cells.append(new_markdown_cell(exp.text))
        if hasattr(exp, 'code'):
            new_code_cell(exp.code)

    nb['cells'] = cells
    if dest_filepath:
        with dest_filepath.open('w') as f:
            nbf.write(nb, f)
    return nb


def test(**kwargs):
    filepath = kwargs.pop('input')
    if filepath:
        print(filepath)
        text = Path(filepath).open().read()
        print(len(text))
    else:
        text = TEST_TEXT
    text = HEADER_TEXT + '\n\n' + text
    return dict(nb=adoc2ipynb(text=text), text=text, filepath=filepath)


if __name__ == '__main__':
    kwargs = parse_args(
        description='Convert adoc code blocks and preceding heading text to a jupyter notebook',
        input_help='File path to input adoc file',
        output_help='File path to output ipynb file')
    format = kwargs.pop('format')
    results = test(**kwargs)
    # print(results)

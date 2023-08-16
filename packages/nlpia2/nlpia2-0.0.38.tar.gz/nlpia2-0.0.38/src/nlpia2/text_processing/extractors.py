import argparse
import doctest
from doctest import DocTestParser
from parsimonious import Grammar
from pathlib import Path
import pandas as pd
import re
import tempfile
from types import MappingProxyType
import nbformat as nbf

from nlpia2.text_processing.re_patterns import RE_URL_WITH_SCHEME, RE_URL_SIMPLE  # noqa
from nlpia2.constants import SRC_DATA_DIR, MANUSCRIPT_DIR, BASE_DIR

RE_TEXT_LINE = r"^[A-Z_\*][-A-Za-z\ 0-9 :\";',!@#$%^&*()_+-={}<>?,.\/]+"
RE_TITLE_LINE = r"^[=]+[A-Za-z0-9\ \-?!,]+"
RE_MARKUP_LINE = r"^[\[][A-Za-z0-9,\ ]+[\]]"
RE_CODE_OR_OUTPUT = r"^(>>>|\.\.\.|[a-z0-9\-\+]+|\(|[\ ]+).*"
RE_CODE_COMMENT=r"^[<].*"
RE_METADATA = r"^[:].*"
RE_EMPTY_LINE = r"^[ \t]*$"
RE_FIGURE_NAME=r"^[\.].*"
RE_SEPARATOR=r"^(\-\-\-\-|====)[\-=]*\s*"
RE_COMMENT=r"^(\\\\|\/\/).*"

ADOC_DIR = MANUSCRIPT_DIR / 'adoc'
LINES_FILENAME = 'nlpia_lines.csv'
LINES_FILEPATH = SRC_DATA_DIR / LINES_FILENAME  # src/nlpia2/data/nlpia_lines.csv

# ch10 haystack section: 'https://gitlab.com/tangibleai/nlpia2/-/raw/main/src/nlpia2/data/nlpia_lines.csv'
DEFAULT_ADOC_FILENAME = 'Chapter-09_Stackable-deep-learning-Transformers.adoc'
DEFAULT_ADOC_FILEPATH = ADOC_DIR / DEFAULT_ADOC_FILENAME
DEFAULT_OPTIONFLAGS = doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE


def extract_blocks_with_grammar(
        filepath=Path('data/tests/test.adoc'),
        grammarpath=Path(SRC_DATA_DIR / 'grammars' / 'adoc_basic.ppeg')):
    filepath, grammarpath = Path(filepath), Path(grammarpath)
    g = Grammar(grammarpath.open().read())
    ast = g.parse(filepath.open().read())
    return ast


def extract_lines(text=DEFAULT_ADOC_FILEPATH, with_meta=True):
    filepath, filename = '', ''
    if (isinstance(text, Path) or len(text) < 1024) and Path(text).is_file():
        filepath = Path(text)
        filename = filepath.name
        text = filepath.read_text(encoding='utf-8')

    lines = []
    for i, line in enumerate(text.splitlines()):
        lines.append(dict(
            line_text=line,
            line_number=i,
            filename=filename,
            is_text=bool(re.match(RE_TEXT_LINE, line)),
            is_empty=bool(re.match(RE_EMPTY_LINE, line)),
            is_code_or_output=bool(re.match(RE_CODE_OR_OUTPUT, line)),
            is_title=bool(re.match(RE_TITLE_LINE, line)),
            is_metadata=bool(re.match(RE_METADATA, line)),
            is_code_comment=bool(re.match(RE_CODE_COMMENT, line)),
            is_markup=bool(re.match(RE_MARKUP_LINE, line)),
            is_figure_name=bool(re.match(RE_FIGURE_NAME, line)),
            is_separator=bool(re.match(RE_SEPARATOR, line)),
            is_comment=bool(re.match(RE_COMMENT, line))
            )
        )
    return lines


def extract_code_sections(filepath=DEFAULT_ADOC_FILEPATH, with_metadata=True, section_break=None):
    """ Extract lines of Python using DocTestParser, return list of strs """
    text = Path(filepath).open('rt').read()
    sections = extract_expression_sections(text=text, section_break=section_break)
    # assert len(sections) > 0
    if not isinstance(sections, list):
        sections = [sections]

    if with_metadata:
        return [[vars(expr) for expr in sect] for sect in sections] 
    return [[ex.source for ex in sect] for sect in sections]


def extract_doctest_examples(filepath=DEFAULT_ADOC_FILEPATH, with_metadata=True, section_break=None):
    """ Extract lines of Python using DocTestParser, return list of strs """
    sections = extract_code_sections(
        filepath=filepath,
        with_metadata=with_metadata,
        section_break=section_break)

    # flatten the list of lists
    flat = []
    for sect in sections:
        flat.extend(sect)
    return flat


def extract_expressions(filepath=DEFAULT_ADOC_FILEPATH):
    """ Use doctest.DocTestParser to find lines of Python code in doctest format """
    text = Path(filepath).open('rt').read()
    dtparser = DocTestParser()
    return dtparser.get_examples(text)


def extract_code_lines(filepath=DEFAULT_ADOC_FILEPATH, with_metadata=True):
    """ Extract lines of Python using DocTestParser, return list of strs """
    expressions = extract_expressions(filepath=filepath)
    if with_metadata:
        return [vars(ex) for ex in expressions]
    return [ex.source for ex in expressions]


# see nonworking duplicate `extract_code_sections_with_grammar`
def extract_code_blocks(filepath=DEFAULT_ADOC_FILEPATH, with_output=False):
    meta = extract_code_lines(filepath=filepath, with_metadata=True)
    df = pd.DataFrame(meta)
    df['num_lines'] = df['source'].str.split('\n').str.len()
    df['next_lineno'] = df['num_lines'] + df['lineno']
    # df['stop_block'] = df['want'].str[:4].str.startswith('----')
    df['stop_block'] = df['want'].str.strip().str.len() > 0

    blocks = ['']
    for line, stop_block, want in zip(df['source'], df['stop_block'], df['want']):
        blocks[-1] += line + '\n'
        if stop_block:
            if with_output:
                blocks[-1].append('\n'.join(['# ' + x for x in want.splitlines()]))
            blocks.append('')
    return blocks


def extract_code_file(filepath=DEFAULT_ADOC_FILEPATH, destfile=None, with_output=True):
    """ Extract the lines of code from code blocks in an adoc file """
    filepath = Path(filepath or DEFAULT_ADOC_FILEPATH)
    lines = extract_code_blocks(filepath=filepath, with_output=with_output)
    
    if destfile is True:
        destfile = filepath.with_suffix('.adoc.ipy')
    if destfile:
        destfile = Path(destfile)
        if destfile.is_dir():
            destfile = destfile / filepath.with_suffix('.adoc.py').name
        with Path(destfile).open('wt') as fout:
            fout.writelines(lines)
    return '\n'.join(lines)


def create_notebook(code_lines, destfile):
    """ extract code from adoc files and export them to Jupyter Notebook files """
    destfile = Path(destfile)
    nb = nbf.v4.new_notebook()
    nb['cells'] = []
    text = code = ''
    if not isinstance(code_lines[0], str):  # must be dicts with meta from doctest
        df = pd.DataFrame(code_lines)
        code_lines = list(df['source'])
    for line in code_lines:
        if line.lstrip()[:2] == '# ':  # comments assumed to be markdown
            text += line.lstrip()[2:].rstrip() + '\n'
            if code:
                nb['cells'].append(nbf.v4.new_code_cell(code))
                code = ''
        elif line.strip():  
            code += line.rstrip() + '\n'
            if text:
                nb['cells'].append(nbf.v4.new_markdown_cell(text))
                text = ''
    # finish up with last line:
    if text:
        nb['cells'].append(nbf.v4.new_markdown_cell(text))
    if code:
        nb['cells'].append(nbf.v4.new_code_cell(code))

    if nb.cells:
        print(destfile)
        with destfile.open('w') as f:
            nbf.write(nb, f)
    return nb


def extract_notebooks(input_dir=MANUSCRIPT_DIR, glob='*.adoc'):
    """ Convert adoc file code blocks into cells within jupyter notebooks """
    notebooks = []
    for p in input_dir.glob(glob):
        blocks = extract_code_blocks(filepath=p, with_meta=with_meta)
        create_notebook
    return outputs
    for p in files:
        code_lines = p.open().readlines()
        if code_lines:
            destfile = p.with_suffix(p.suffix + '.ipynb')
            print(destfile)
            create_notebook(
                code_lines=code_lines,
                destfile=destfile)


def extract_doctest_examples_file(filepath=DEFAULT_ADOC_FILEPATH, destfile=None):
    """ Extract the lines of code from code blocks in an adoc file """
    filepath = Path(filepath)
    if destfile is True:
        destfile = filepath.with_suffix('.adoc.ipy')
    if destfile.is_dir():
        destfile = destfile / filepath.with_suffix('.adoc.py').name
    lines = extract_doctest_examples(filepath=filepath, with_metadata=False)
    if destfile:
        with Path(destfile).open('wt') as fout:
            fout.writelines(lines)
    return '\n'.join(lines)


def extract_image_paths(filepath=DEFAULT_ADOC_FILEPATH):
    filepath = Path(filepath)
    text = filepath.open('rt').read()
    parent = filepath.parent
    image_paths = []
    for line in text.splitlines():
        match = re.match(r'image::([^\[]+)', line)
        if match:
            path = Path(match.groups()[0])
            if path.is_file():
                image_paths.append((path.resolve(), 'exists'))
                continue
            path = (parent / path)
            if path.is_file():
                image_paths.append((path.resolve(), 'exists'))
                continue
            image_paths.append((path, ''))
    return image_paths


def extract_tagged_code_lines(filepath=DEFAULT_ADOC_FILEPATH, with_metadata=True):
    if not with_metadata:
        print('WARNING: Must extract metadata for extract_tagged_code... with_metadata=True')
    if not isinstance(filepath, list) or isinstance(filepath, (str, Path)):
        doctests = extract_code_lines(filepath=filepath, with_metadata=True)
    tagged_lines = [] 
    for k, doc in enumerate(doctests):
        doc['docnum'] = k
        doc['source_lines'] = doc['source'].split('\n')
        for i, line in enumerate(doc['source_lines']):
            tagged = doc.copy()
            tagged['line'] = line
            tagged['doc_lineno'] = i
            tagged['file_lineno'] = len(tagged_lines)
            tagged['prompted_line'] = '>>> ' + line
            if line.startswith(' ') or tagged['indent']:
                tagged['prompted_line'] = '... ' + line
            if "#" in line:
                # TODO: check for quoted "#"
                comments = re.findall(r'\s*#\s*<\d+>[ \t]*\n', line)
                if comments:
                    tagged['annotation'] = comments[-1]
                comments = re.findall(r'#[^#]*', line)
                if comments:
                    tagged['comment'] = comments[-1]
                    if len(comments) > 1:
                        tagged['fixme'] = 'multiple hashes'
            tagged_lines.append(tagged)
    return tagged_lines


def extract_expression_sections(text, section_break='// SECTIONBREAK'):
    """ Use doctest.DocTestParser to find lines of Python code in doctest format """
    if len(text) < 128 and Path(text).is_file():
        text = Path(text).open('rt').read()
    dtparser = DocTestParser()
    
    if not section_break:
        return [dtparser.get_examples(text)]

    text_sections = ['']
    for line in text.splitlines():
        print(line)
        if line.strip() == section_break:
            text_sections[-1] = text_sections[-1] + '>>> #' + section_break + '\n'
            text_sections.append('')
        else:
            text_sections[-1] = text_sections[-1] + line + '\n'
    return [dtparser.get_examples(text) for text in text_sections]
    

def extract_urls_from_text(text=DEFAULT_ADOC_FILEPATH, with_meta=True):
    """ Find all URLs in the file at filepath, return a list of dicts with urls """
    filepath, filename = '', ''
    if (isinstance(text, Path) or len(text) < 1024) and Path(text).is_file():
        text = Path(text).open('rt').read()
    urls = []
    for i, line in enumerate(text.splitlines()):
        for k, match in enumerate(re.finditer(RE_URL_SIMPLE, line)):
            urls.append(dict(
                scheme=match.group('scheme_type') or '',
                url=match.group('url') or '',
                url_path=match.group('path') or '',
                tld=match.group('tld') or '',
                line_number=i,
                url_number=k,
                line_text=line,
                filepath=str(filepath),
                filename=filename
            ))
    return urls


def extract_lists_from_files(input_dir=MANUSCRIPT_DIR, glob='*.adoc',
                             extractor=extract_urls_from_text, with_meta=True):
    """ Run specified extractor (default: extract_urls) on each file input_dir, return a list of dicts with urls """
    outputs = []
    for p in input_dir.glob(glob):
        df = extractor(filepath=p, with_meta=with_meta)
        outputs.append(df)
    return outputs


extract_lists = extract_lists_from_files


def extract_url_lists_from_files(input_dir=MANUSCRIPT_DIR, glob='*.adoc',
                                 extractor=extract_urls_from_text, with_meta=True):
    """ Find all URLs in files at input_dir, return a list of dicts with urls """
    return extract_lists(input_dir=input_dir, extractor=extract_urls_from_text, glob=glob, with_meta=with_meta)


extact_url_lists = extract_url_lists_from_files


def extract_urls(texts=MANUSCRIPT_DIR, glob='*.adoc', with_meta=True):
    if (isinstance(texts, Path) or len(texts) < 1024):
        if Path(texts).is_file():
            return extract_urls_from_text(text=texts, with_meta=with_meta)
        elif Path(texts).is_dir():
            glob = glob or '*'
            return extract_url_lists_from_files(
                input_dir=texts, glob='*.adoc', with_meta=with_meta)
    return extract_urls_from_text(text=texts, with_meta=with_meta)


def extract_urls_df(filepath=DEFAULT_ADOC_FILEPATH, with_meta=True):
    """ Use regex to extract URLs from text file, return DataFrame with url column """
    urls = extract_urls_from_text(filepath=filepath, with_meta=with_meta)
    df = pd.DataFrame(urls, index=[
        f"{u['line_number']}-{u['url_number']}" for u in urls])
    df['filename'] = filepath.name
    df['filepath'] = str(filepath)
    return df


def extract_lines_df(filepath=DEFAULT_ADOC_FILEPATH, with_meta=True):
    lines = extract_lines(text=filepath, with_meta=with_meta)
    df = pd.DataFrame(lines)
    return df


def expressions_to_doctests(expressions, prompt='>>> ', ellipsis='... ', comment=''):
    # expressions = extract_expressions(filepath=filepath)

    prompt = prompt or ''
    if prompt and prompt[-1] != ' ':
        prompt += ' '
    if not isinstance(prompt, str):
        prompt = '>>> '

    ellipsis = ellipsis or ''
    if ellipsis and ellipsis[-1] != ' ':
        ellipsis += ' '
    if not isinstance(ellipsis, str):
        ellipsis = '... '

    comment = comment or ''
    if not isinstance(comment, str):
        comment = '# '
    if comment and comment[-1] != ' ':
        comment += ' '
    blocks = ['']

    for exp in expressions:
        lines = exp.source.splitlines()
        if exp.source.strip() and len(lines) == 1:
            blocks[-1] += prompt + exp.source
        else:
            blocks[-1] += prompt + lines[0] + '\n'
            for line in lines[1:]:
                blocks[-1] += ellipsis + lines[0] + '\n'

        if exp.want:
            blocks[-1] += comment + exp.want
            blocks.append('')


def extract_goodreads_quotes(text):
    """ Regexes used in Sublime to turn goodreads copypasta text into yaml entries in quotes.yml

    Example output:
      https://gitlab.com/tangibleai/nlpia2/-/tree/main/src/nlpia2/data/quotes.yml
    Example input (copy text in browser):
      https://www.goodreads.com/author/quotes/5780686.Liu_Cixin
    Crawler can start with search for author/keyword quotes:
      https://www.goodreads.com/quotes/search?q=Chiang
    """
    resub_pairs = dict(
        unicode_quotes=[r'[“”]', r'"'],
        unicode_appostrophes=[r'[‘’]', r"'"],
        quote_text=[r'― ([^,]+),([-!?\w\d ]+)',
            r'''
  author: \1
  source: Good Reads
  book: \2
'''],
        likes=[
            r'''

(\d*) likes
Like
(".*)
''',
            r'''

-
  text: \2
  likes: \1
'''],

    )
    for name, (pattern, replacement) in resub_pairs.items():
        text = re.sub(pattern, replacement, text)
    return text


re_codeblock_source = r'[ ]*\[[ ]*source\s*,[ ]*python[ ]*\][ ]*'
re_ipython_shabang = r'([>]{2,3}|[.]{2,3})?[ ]*[!].*'
re_codeblock_horizontal_line = r'[ ]*[-]{2,80}[ ]*'


def test_file(filepath=DEFAULT_ADOC_FILEPATH, skip=0, adoc=True,
              cleanup=True,  # whether to remove the temporary adoc file containing preprocessed code blocks
              optionflags=DEFAULT_OPTIONFLAGS,
              name=None,
              verbose=False,
              package=None,
              module_relative=False,
              **kwargs):
    if name is None:
        name = filepath.name
    if package:
        module_relative = True
    if not module_relative:
        assert filepath.is_file()
    if adoc:
        # Insert blank line before '----' at end of adoc code block for doctests
        with filepath.open() as fin:
            lines = fin.readlines()
            newlines = []
            # blocks the command line and the running of doctests
            ignore_line_prefixes = [
                '>>> !firefox',
                '>>> displacy.serve(',
                '>>> spacy.cli.download(',
            ]
            ignore_linepair_prefixes = [
                '>>> %timeit',
            ]
            ignore_nextline = False
            for i, (line, nextline) in enumerate(zip(lines[:-1], lines[1:])):
                if i < skip:
                    continue
                # skip ignore_prefixes lines:
                if any((line.lower().lstrip().startswith(p) for p in ignore_line_prefixes)):
                    line = '\n'

                if ignore_nextline:
                    line = '\n'
                    ignore_nextline = False
                if any((line.lower().lstrip().startswith(p) for p in ignore_linepair_prefixes)):
                    line = '\n'
                    ignore_nextline = True
                # remove nonpython shell commands (shabangs) !
                # line = re.match(r'(>[2,3]|[.]{3})?\s*!.*', '', line)

                # remove comment hash at begging of return value (e.g. '# 42')
                # line = re.sub(r'^#\s+', '', line)

                # rstrip EOL footnotes/comments (e.g. '  # <1>')
                line = re.sub(r'[ ]+#[ ]+<\d+>[ ]*', '', line)

                newlines.append(line)

                # insert newline before '----' at end of code block
                if nextline.startswith('----'):
                    # print(f'line: {len(newlines)}')
                    # print(repr(line))
                    # print(f'nextline: {len(newlines)+1}')
                    # print(repr(nextline))
                    if not re.match(re_codeblock_source, line):
                        newlines.append('\n')
                    # check for inline adoc code block comments (callout bubbles)
            # for loop finishes one early, so append the last line of text
            newlines.append(lines[-1])
        fp, filepath = tempfile.mkstemp(text=True, suffix='.adoc')
        filepath = Path(filepath)
        print(f"Testing: {filepath}")
        with filepath.open('wt') as fout:
            fout.writelines(newlines)
    results = doctest.testfile(str(filepath),
                               name=name,
                               module_relative=module_relative, package=package,
                               optionflags=optionflags, verbose=verbose,
                               **kwargs)
    if results.failed > 0:
        fp, pyfilepath = tempfile.mkstemp(text=True, suffix='.py')
        extract_code_file(filepath=filepath, destfile=pyfilepath)
        print(f"You can find the doctests in {pyfilepath}")
    if cleanup:
        filepath.unlink()
    else:
        print(f"You can find the preprocessed adoc text in {filepath}")
    return results


def extract_doctest_files(filepath=DEFAULT_ADOC_FILEPATH, destfile=None, save_sections=False):
    filepath = Path(filepath)
    if not destfile:
        destfile = filepath.parent.parent / 'py'
        destfile.mkdir(exist_ok=True)
    destfile = Path(destfile)
    if destfile.is_dir():
        destfile = destfile / filepath.with_suffix('.adoc.py').name
    sections_lines = extract_tagged_code_lines(
        filepath=filepath, with_metadata=False)
    
    if destfile:
        destfile = Path(destfile)
    if not sections_lines:
        return ''
    all_lines = []
    all_meta = []
    for i, lines in enumerate(sections_lines):
        all_meta.extend(lines)
        all_lines.extend(lines['source_lines'])
        if destfile and save_sections:
            sfx = f'.sect{i:02d}' if len(sections_lines) > 1 else ''
            sect_destfile = destfile.with_suffix(sfx + destfile.suffix)
            print(f'{sect_destfile} ({len(lines["source_lines"])})')
            # FIXME: only outputs a single line now that using extract_tagged_code_lines
            # FIXME: tagged code lines should include section_num
            with sect_destfile.open('wt') as fout:
                fout.writelines('\n'.join(lines['source_lines']))
    return ''.join(all_lines)


def extract_lists_from_files(input_dir=MANUSCRIPT_DIR, glob='*.adoc',
                             extractor=extract_urls_from_text, with_meta=True):
    outputs = []
    for p in input_dir.glob(glob):
        df = extractor(filepath=p, with_meta=with_meta)
        outputs.append(df)
    return outputs


def extract_files(
        adocdir=MANUSCRIPT_DIR, destdir=None, glob='*.adoc',
        extractor=extract_code_file, suffix='.adoc.py'):
    """ Run an extractor on all the text (default=adoc) files in a directory returning the extracted file paths """
    output_paths = []
    adocdir = Path(adocdir)
    
    assert adocdir.is_dir()
    paths = list(adocdir.glob(glob))
    if not len(paths) and (adocdir / 'adoc').is_dir():
        adocdir = adocdir / 'adoc'
        paths = list(adocdir.glob(glob))

    destdir = Path(destdir or adocdir)
    destdir.mkdir(exist_ok=True)
    assert destdir.is_dir()
    

    for p in paths:
        destfile = (destdir / p.name).with_suffix(suffix)
        print(f"{p} => {destfile}")
        code = extractor(filepath=p)
        with destfile.open('wt') as fout:
            fout.write(code)
        output_paths.append(destfile)
    return output_paths


def extract_code_files(adocdir=ADOC_DIR, **kwargs):
    kwargs['destdir'] = kwargs.get('destdir') or adocdir.parent / 'py'
    return extract_files(extractor=extract_code_file, **kwargs)


def extract_url_dfs_from_files(
        adocdir=MANUSCRIPT_DIR, destdir=None,
        glob='*.adoc', suffix='.adoc.py'):
    adocdir = Path(adocdir)
    dfs = extract_dfs_from_files(
        extractor=extract_urls_df,
        adocdir=adocdir, destdir=destdir, glob=glob,
        suffix=suffix)
    return dfs


def extract_big_line_df_from_files(
        adocdir=MANUSCRIPT_DIR, destdir=None,
        glob='*.adoc', suffix='.adoc.py'):
    adocdir = Path(adocdir)
    output = []
    for p in adocdir.glob(glob):
        lines = extract_lines(text=p)
        output.extend(lines)
    df = pd.DataFrame(output)

    # for each line, see if we know what its type is
    one_hot_columns = [col for col in df.columns if col.startswith('is_')]
    df['num_types'] = df[one_hot_columns].sum(axis=1)
    df['is_type_defined'] = df[one_hot_columns].sum(axis=1) > 0

    return df


def extract_dfs_from_files(
        adocdir=MANUSCRIPT_DIR, output_dir=None, glob='*.adoc',
        extractor=extract_urls_df, suffix='.adoc.py'):
    outputs = []
    for p in adocdir.glob(glob):
        df = extractor(filepath=p)
        outputs.append(df)
    return outputs

def update_nlpia_lines(adoc_dir=None, dest=LINES_FILEPATH):
    if not adoc_dir:
        adoc_dir = BASE_DIR.parent / 'nlpia-manuscript' / 'manuscript' / 'adoc'
        if not adoc_dir.is_dir():
            adoc_dir = ADOC_DIR
    df = extract_big_line_df_from_files(adoc_dir)
    df.to_csv(dest)
    return df


def parse_args(
        adocs=None,
        adocs_help='Path to asciidoc or text file containing doctest-format code blocks',
        output=None,
        output_help='Path to new py file created from code blocks in INPUT',
        description='Transcoder for doctest-formatted code blocks in asciidoc/txt files to py, or ipynb code blocks',
        format_help='Output file format or type (md, py, ipynb, python, or notebook)'):

    parser = argparse.ArgumentParser(description=description)

    parser.add_argument(
        'path', type=Path, default=None, help=adocs_help, nargs='?',
    )

    parser.add_argument(
        '--adocs', type=Path, default=adocs,
        help=adocs_help
    )
    parser.add_argument(
        '--output', type=Path, default=output,
        help=output_help,
    )
    parser.add_argument(
        '--format', type=str, default='py',
        help=format_help
    )
    return vars(parser.parse_args())


DEFAULT_ARGS = MappingProxyType(dict(adocs='manuscript/adoc', output='manuscript/py'))


def extract_code(adocs=None, output=None):
    args = dict(
        adocs=Path(adocs or MANUSCRIPT_DIR / 'adoc'),
        output=Path(output or MANUSCRIPT_DIR / 'py')
        )
    args = parse_args(**args)

    if args['path']:
        args['adocs'] = args['path']

    if args['adocs']:
        if Path(args['adocs']).is_dir():
            return extract_code_files(adocdir=args['adocs'])
        elif Path(args['adocs']).is_file():
            return extract_code_file(filepath=args['adocs'])
    
    results = {}
    if input(f'Extract python from all adoc files in {MANUSCRIPT_DIR}? ').lower().strip()[0] == 'y':
        results['code_file_paths'] = extract_code_files()
    if input(f'Extract urls from all addoc files in {MANUSCRIPT_DIR}? ').lower().strip()[0] == 'y':
        results['urls'] = extract_urls()
    return results



if __name__ == '__main__':
    assert SRC_DATA_DIR.is_dir()
    assert MANUSCRIPT_DIR.is_dir()
    results = extract_code()



# import re
from datetime import datetime
from io import TextIOWrapper
from pathlib import Path
import re
import sys

import pandas as pd
from plotly.offline import plot as plot_html
# import plotly.graph_objs as go
import plotly.express as px
import seaborn as sns

import fitz  # pip install PyMuPDF
from matplotlib import pyplot as plt

sns.set_style('whitegrid')


LLM_PDF = '2303.18223 - A Survey of LLMs.pdf'
FORMFEED = chr(12)
FORMFEED_BYTE = FORMFEED.encode('utf8')


def normalize_name(name, max_len=None):
    name = name.split('(')[0].lower().strip()
    name = name.strip('-').strip('_').strip()
    name = name.split('[')[0].strip()
    return re.sub(r'\W+', '', name)[:max_len]


def extract_tables(pdf_path=LLM_PDF):
    """ FIXME: Only extracts a couple rows/columns """
    from tabula import read_pdf  # doesn't work well
    return read_pdf(pdf_path, pages="all")


def extract_text(pdf_path=LLM_PDF, write_file=True, page_sep=FORMFEED, header='', footer='\n\n' + '_'*80 + '\n\n'):
    doc = fitz.open(pdf_path)
    pages = []
    for page in doc:
        text = header or ''
        text += page.get_text()  # get plain text (is in UTF-8)
        text += footer or ''

        # blocks = page.get_text_blocks()
        pages.append(text)

    return (page_sep or '\n').join(pages)


FOSS_ORG = {
    'T5': ['https://huggingface.co/t5-large', 'Google', ''],
    'mT5': ['https://https://huggingface.co/google/mt5-large', 'Google', ''],
    'PanGu-α': ['https://huggingface.co/sunzeyeah/pangu-13B', 'PCNL', ''],
    'CPM-2': ['https://huggingface.co/mymusise/CPM-GPT2', 'Tsinghua University', ''],
    'T0': ['https://huggingface.co/bigscience/T0', 'Hugging Face', ''],
    'GPT-NeoX-20B': ['https://huggingface.co/EleutherAI/gpt-neox-20b', 'EleutherAI', ''],
    'CodeGen': ['https://huggingface.co/Salesforce/codegen-16B-multi', 'Salesforce', ''],
    'Tk-Instruct': ['https://huggingface.co/allenai/tk-instruct-11b-def', 'AllenAI', ''],
    'UL2': ['https://huggingface.co/google/flan-ul2', 'Google', ''],
    'OPT': ['https://huggingface.co/facebook/opt-66b', 'Facebook', ''],
    'NLLB': ['https://huggingface.co/facebook/nllb-200-3.3B', 'Meta', ''],
    'BLOOM': ['https://huggingface.co/bigscience/bloom', 'Hugging Face', ''],
    'GLM-10b': ['https://huggingface.co/THUDM/glm-10b', 'Tsinghua University', ''],
    'GLM': ['https://huggingface.co/THUDM/glm-large-chinese', 'Tsinghua University', ''],
    'Flan-T5': ['https://huggingface.co/google/flan-t5-xxl', 'Google', ''],
    'mT0': ['https://huggingface.co/bigscience/bloomz', 'Hugging Face', ''],
    # 'Galactica-mini': ['https://huggingface.co/facebook/galactica-125m', 'Meta', ''],
    # 'Galactica-base': ['https://huggingface.co/facebook/galactica-1.3b', 'Meta', ''],
    # 'Galactica-standard': ['https://huggingface.co/facebook/galactica-6.7b', 'Meta', ''],
    # 'Galactica-large': ['https://huggingface.co/facebook/galactica-30b', 'Meta', ''],
    # 'Galactica-huge': ['https://huggingface.co/facebook/galactica-120b', 'Meta', ''],
    'Galactica': ['https://huggingface.co/facebook/galactica-120b', 'Meta', ''],
    'BLOOMZ': ['https://huggingface.co/bigscience/bloomz', 'Hugging Face', ''],
    'OPT-IML': ['https://huggingface.co/HuggingFaceH4/opt-iml-max-30b', 'Hugging Face', ''],
    'Pythia': ['https://github.com/EleutherAI/pythia', 'EleutherAI', ''],
    'LLaMA': ['https://github.com/juncongmoo/pyllama', 'Google', ''],
    'Vicuna': ['https://vicuna.lmsys.org/', 'Berkeley+CMU+Stanford+UCSD', ''],
    'Koala': ['https://vicuna.lmsys.org/', 'Berkeley', ''],
    'GShard': ['', '', ''],
    'GPT-3': ['https://openai.com', 'OpenAI', ''],
    'LaMDA': ['', '', ''],
    'HyperCLOVA': ['', '', ''],
    'Codex': ['', '', ''],
    'ERNIE 3.0': ['', '', ''],
    'Jurassic-1': ['', '', ''],
    'FLAN': ['', '', ''],
    'MT-NLG': ['', '', ''],
    'Yuan 1.0': ['', '', ''],
    'Anthropic': ['', '', ''],
    'WebGPT': ['', '', ''],
    'Gopher': ['', '', ''],
    'ERNIE 3.0 Titan': ['', '', ''],
    'GLaM': ['', '', ''],
    'InstructGPT': ['', 'OpenAI', ''],
    'AlphaCode': ['', '', ''],
    'Chinchilla': ['', '', ''],
    'PaLM': ['', 'Google', ''],
    'Cohere': ['', '', ''],
    'YaLM': ['', '', ''],
    'AlexaTM': ['', '', ''],
    'Luminous': ['', '', ''],
    'Sparrow': ['', '', ''],
    'WeLM': ['', '', ''],
    'U-PaLM': ['', 'Google', ''],
    'Flan-PaLM': ['https://huggingface.co/google/flan-t5-xxl', 'Google', ''],
    'Flan-U-PaLM': ['', 'Google', ''],
    'Alpaca': ['https://github.com/tatsu-lab/stanford_alpaca/', 'Stanford', ''],
    'GPT-4': ['https://openai.com', 'OpenAI', ''],
    'PanGU-Σ': ['', '', ''],
## Added by HL:
}
DF_FOSS_ORG = pd.DataFrame(FOSS_ORG).T
DF_FOSS_ORG.columns = 'Source Organization Paper'.split()
DF_FOSS_ORG.index = list(map(normalize_name, DF_FOSS_ORG.index.values))

ADD_LLMS = [
    {
        'Name': 'AutoGPT',
        'Paper': 'https://www.researchgate.net/profile/Mohamed-Fezari-2/publication/370107237_From_GPT_to_AutoGPT_a_Brief_Attention_in_NLP_Processing_using_DL/links/643fd87a2eca706c8b6d151b/From-GPT-to-AutoGPT-a-Brief-Attention-in-NLP-Processing-using-DL.pdf',
        'Parents': ['AgentGPT'],
        'Description': 'IL8N of AgentGPT. Seems to be compatible with the Chinese language. Uses GPT-3 to connect to break a task into achievable tasks and query APIs to accomplish those tasks.',
    },{
        'Name': 'AgentGPT',
        'Source': 'https://github.com/reworkd/AgentGPT',
        'Organization': 'Reworkd',
        'Description': 'Uses GPT-3 to connect to break a task into achievable tasks and query APIs to accomplish those tasks.',
    },{
        'Name': 'Claude',
        'Source': 'https://anthropic.org',
        'Organization': 'Anthropic',
        'Open': False,
        'Description': 'Claims to use "Constitutional AI" and "harmless training" to respond appropriately to malicious or toxic conversation partners',
    },{
        'Source': 'https://github.com/NVIDIA/Megatron-LM',
        'Organization': 'NVIDIA',
        'Paper': 'https://arxiv.org/pdf/2205.05198.pdf',
        'Name': 'Megatron-LM',
        'Release': datetime(2022, 5, 1),
        'Size': 8_300_000_000,
        'Open': True
    },
]

DF_ADD_LLMS = pd.DataFrame(ADD_LLMS)
DF_ADD_LLMS.index = list(map(normalize_name, DF_ADD_LLMS['Name']))


def scrape_wikipedia(
        url='https://en.wikipedia.org/wiki/Large_language_model',
        match='large language models',
        columns='Name Release Organization Size Tokens Openness Description'.split()):
    df = pd.read_html(url, match=match)[0]
    df.columns = columns + list(df.columns)[len(columns):]
    max_len = max(map(len, DF_FOSS_ORG.index.values))
    df.index = list(map(normalize_name, df['Name'], [max_len]*len(df)))
    df = df.sort_values(['Release', 'Size'])
    return df


def scrape_llm_survey(readme='https://github.com/rucaibox/llmsurvey'):
    """ Scatterplot of LLM size vs release date """
    df = pd.read_html(readme, match='Release Time',
        parse_dates=True)[0].dropna()
    df.columns = 'Open,Name,Release,Size,Reference'.split(',')
    df = df.sort_values('Release')

    links = pd.read_html(readme, match='Release Time',
        extract_links='body')[0].dropna()
    links = links['Link']['Link'].values
    df['Link'] = list(zip(*links))[1]

    # Typo corrections, cleaning, estimation of missing values
    df['Open'] = df['Open'].str.lower().str.startswith('p').copy()    
    if 'Openness' not in df.columns:
        df['Openness'] = ['Open Source' if isopen else 'Proprietary' for isopen in df['Open']]
    df['Name'] = df['Name'].replace({'Galatica': 'Galactica'})
    df.set_index('Name', inplace=True, drop=False)
    df['Size'] = df['Size'].replace({r'^[^0-9\s]+$': str(8*int(df['Size']['GPT-3']))}, regex=True)
    df['Size'] = df['Size'].astype(int) * 1_000_000_000
    return df


def merge_llm_dfs(dfs=None):
    """ Combine open source model information with closed source info from LLM Survey paper """
    if dfs is None:
        dfs = [
            scrape_llm_survey(),
            DF_FOSS_ORG.copy(),
            scrape_wikipedia(),
            DF_ADD_LLMS
            ]
    for i, df in enumerate(dfs):
        dfs[i].index = list(map(normalize_name, df.index.values))    
    df = pd.concat(dfs, axis=1)
    return df



def plot_llm_sizes(df='https://github.com/rucaibox/llmsurvey',
        x='Release', y='Size', symbol='Openness', size=12,
        template="seaborn",
        text='index',
        dest='llm_sizes_scatter.html', display=True, 
        font_size=18,
        width=2000, height=500, log_x=False, log_y=True,
        **kwargs):
    """ Scatterplot of LLM size vs release date """
    if isinstance(df, (str, Path, TextIOWrapper)):
        df = scrape_llm_survey(readme=df)
    df = df.drop_duplicates(subset=['Release', 'Size'], keep='last')
    if 'Openness' not in df.columns:
        df['Openness'] = [
            'Open Source' if isopen else 'Proprietary'
            for isopen in df['Open']]
    if isinstance(size, (int, float)):
        size = [size]*len(df)
    if isinstance(text, str):
        text = getattr(df, text, text)
    df['Size (trainable parameters)'] = df['Size']
    if dest and dest.lower().endswith('html'):
        fig = px.scatter(df, 
            x='Release', y='Size (trainable parameters)', 
            symbol=symbol, size=size,
            log_x=log_x, log_y=log_y,
            width=width, height=height,
            text=text,
            **kwargs)
        fig.update_layout( 
            font_family="Gravitas One,Arial Bold,Open Sans,Arial",
            font_size=font_size,
            legend=dict(title=None,
                yanchor="top", y=0.98,
                xanchor="left", x=0.02))
        fig.update_traces(textposition='middle center')
        # scatter = go.Scatter(x=x, y=y, line=None, fill=color)
        plot_html(fig, show_link=False, validate=True, output_type='file', 
            filename=dest,
            image=None, image_width=width, image_height=height, 
            include_plotlyjs=True, include_mathjax=False,
            config=None,
            # autoplay=True, animation_opts=None
            )
    else:
        # df.plot(ax=ax, kind='scatter', x='Release', legend=True, y='Size',
        #         style='Openness',
        #         palette={'Open Source': 'teal', 'Proprietary': 'red'},
        #         markers={'Open Source': 'o', 'Proprietary': 's'},
        #         sizes={'Open Source': 12, 'Proprietary': 10},
        #         rot=-65)
        fig = plt.figure(figsize=(10,7))
        sns.scatterplot(data=df,
                x='Release', legend=True, y='Size',
                style='Openness',
                hue='Openness',
                )
                # palette={'Open Source': 'teal', 'Proprietary': 'red'},
                # markers={'Open Source': 'o', 'Proprietary': 's'},
                # sizes={'Open Source': 12, 'Proprietary': 10}
        fig = plt.gcf()
        if display:
            plt.show()

    return fig


if __name__ == '__main__':
    if sys.argv[1:]:
        dest = ' '.join(sys.argv[1:])
        df = scrape_llm_survey()
        df = df.sort_values(['Release', 'Size'])
        df = df.drop_duplicates(['Release', 'Size'], keep='last')
        df = df.sort_values(['Release'])
        IGNORE_NAMES = ['mT5', 'ERNIE 3.0 Titan', 'WebGPT', 'BLOOMZ', 'LaMDA', 
            'Cohere', 'CodeGeeX', 'CodeGenX', 'Jurassic-1', 'Koala']
        for name in IGNORE_NAMES:
            if name in df.index:
                df = df.drop(axis=1, index=name)
        df['Release'] = df['Release'].str.split('/')
        df['Release'] = df['Release'].apply(lambda x: datetime(int(x[0]), int(x[1]), 1))
        df.sort_values('Release')
        df = df.sort_values('Release')
        # df.index = df['Name'].replace({'OPT': 'OPT  .', 'BLOOM': '.  BLOOM'})
        fig = plot_llm_sizes(df, opacity=.2,
            x='Release', y='Size', color='Openness', symbol='Openness',
            dest=dest, display=True,
            width=1400, height=700, log_x=False, log_y=True)

"""
df.columns
df.columns[2] = 'Release'

plt.grid('on')
plt.show()

pip install plotly
from plotly.offline.offline import _plot_html
import plotly
plotly.offline.offline.plot?
plotly.offline.offline.plot?
from plotly.offline.offline import plot as _plot_html
from plotly.graph_objs import Scatter, Layout
from plotly.graph_objs.scatter import Marker
from plotly.graph_objs.layout import XAxis, YAxis
from nlpia2.constants import SRC_DATA_PATH

np = pd.np

PLOTLY_HTML = \"\"\"
<html>
  <head>
    <meta charset="utf-8" />
    <!-- <meta http-equiv="Content-Type" content="text/html; charset=utf-8"> -->
    <script type="text/javascript">
    {plotlyjs}
    </script>
  </head>
  <body>
    {plotlyhtml}
  </body>
</html>
\"\"\"

DEFAULT_PLOTLY_CONFIG = {
    'staticPlot': False,  # no interactivity, for export or image generation
    'workspace': False,  # we're in the workspace, so need toolbar etc
    'editable': False,  # we can edit titles, move annotations, etc
    'autosizable': False,  # plot will respect layout.autosize=true and infer its container size
    'fillFrame': False,  # if we DO autosize, do we fill the container or the screen?
    'scrollZoom': False,  # mousewheel or two-finger scroll zooms the plot
    'doubleClick': 'reset+autosize',  # double click interaction (false, 'reset', 'autosize' or 'reset+autosize')
    'showTips': True,  # new users see some hints about interactivity
    'showLink': True,  # link to open this plot in plotly
    'sendData': True,  # if we show a link, does it contain data or just link to a plotly file?
    'linkText': 'Edit chart',  # text appearing in the sendData link
    'displayModeBar': 'true',  # display the modebar (true, false, or 'hover')
    'displaylogo': False,  # add the plotly logo on the end of the modebar
    'plot3dPixelRatio': 2,  # increase the pixel ratio for 3D plot images
    'setBackground': 'opaque'  # fn to add the background color to a different container or 'opaque'
                               # to ensure there's white behind it
}
import os

from matplotlib import pyplot as plt
import seaborn as sns
sns.set_style?
sns.set_style('white grid')
sns.set_style('whitegrid')
from nlpia2 import constants
constants.SRC_DATA_DIR
pwd
import plotly.graph_objs as go

plot_html([go.Scatter(x=[1, 2, 3], y=[3, 2, 6])], filename='my-graph.html')
import plot.graph_objs as go

more my-graph.html
"""
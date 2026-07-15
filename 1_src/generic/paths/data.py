from pathlib import Path
import os

RAIZ = Path(os.getcwd())#.parent.parent.parent 

DOCS     = RAIZ / '0_docs'
SRC      = RAIZ / '1_src'
NEW_DATA = RAIZ / '2_new-data'
DATA     = RAIZ / '2_data'

DIR_AGGREGATORS = DATA / '1_processed' / '_aggregator_'
DIR_BLOG        = DATA / '1_processed' / '_blog_'
DIR_TASK        = DATA / '1_processed' / '_task_' / 'Model'  # Methods files # old DIR_SCAN
DIR_TOOL        = DATA / '1_processed' / '_tools_'           # Tools files   # old DIR_DATABASE

DIR_DYN_PIPE_INS = SRC / 'dynamic_analysis' / 'pipeline'
DIR_TEMPLATE     = SRC / 'template' / 'html'
DIR_GERADOR      = SRC / 'template' / '.out'

DIR_AGGREGATORS.mkdir(parents=True, exist_ok=True)
DIR_BLOG.mkdir(parents=True, exist_ok=True)
DIR_TOOL.mkdir(parents=True, exist_ok=True)
DIR_TASK.mkdir(parents=True, exist_ok=True)
DIR_GERADOR.mkdir(parents=True, exist_ok=True)

__all__ = ["DIR_AGGREGATORS", "DIR_BLOG", "DIR_TASK", "DIR_TOOL", "DIR_TEMPLATE", "DIR_DYN_PIPE_INS", "DIR_GERADOR"]

if __name__ == 'main':
    for name_adress, some_adress in zip(["DIR_AGGREGATORS", "DIR_BLOG", "DIR_TASK", "DIR_TOOL", "DIR_TEMPLATE", "DIR_DYN_PIPE_INS", "DIR_GERADOR"],[DIR_AGGREGATORS, DIR_BLOG, DIR_TASK, DIR_TOOL, DIR_TEMPLATE, DIR_DYN_PIPE_INS, DIR_GERADOR]):
        print(f'{name_adress}: {some_adress}')
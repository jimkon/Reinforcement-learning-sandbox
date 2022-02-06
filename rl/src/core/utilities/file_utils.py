from os import makedirs, listdir
from os.path import exists, split, splitext, join
import uuid

import pandas as pd
from markdown import markdown

from rl.src.core.configs.storage_configs import UNIQUE_STRING_LENGHT
from rl.src.core.configs.general_configs import EXPERIMENT_STORE_LOGS_DIRECTORY_ABSPATH
from rl.src.core.configs.log_configs import LOG_CSV_DIR_PATH, LOG_HTML_DIR_PATH


def create_path(path):
    if "." in path:
        path = split(path)[0]

    if not exists(path):
        makedirs(path)


def unique_string():
    return uuid.uuid4().hex[:UNIQUE_STRING_LENGHT].upper()


def markdown_to_html(abspath):
    with open(abspath, "r", encoding="utf-8") as input_file:
        text = input_file.read()

    html = markdown(text)

    path, filename = split(abspath)

    filename, ext = splitext(filename)

    html_abspath = join(path, filename+'.html')

    with open(html_abspath, "w", encoding="utf-8", errors="xmlcharrefreplace") as output_file:
        output_file.write(html)

    return html_abspath


def generate_markdown_from_logs(tags=None):
    logs_dir_path = join(EXPERIMENT_STORE_LOGS_DIRECTORY_ABSPATH, LOG_CSV_DIR_PATH)
    files = listdir(logs_dir_path)
    files_abspath = [join(logs_dir_path, file) for file in files]

    dfs = [pd.read_csv(file, index_col=False) for file in files_abspath]

    df = pd.concat(dfs).sort_values(by='timestamp')
    # df = df[df['tags'].str.contain('markdown')]

    file_str = '   \n'.join(df['message'].to_list())

    markdown_abspath = join(EXPERIMENT_STORE_LOGS_DIRECTORY_ABSPATH, LOG_HTML_DIR_PATH)+"/report.md"

    with open(markdown_abspath, "w", encoding="utf-8") as output_file:
        output_file.write(file_str)

    return markdown_abspath


if __name__=="__main__":
    fpath = generate_markdown_from_logs()
    markdown_to_html(fpath)

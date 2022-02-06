from os import makedirs
from os.path import exists, split, splitext, join
import uuid

from markdown import markdown

from rl.src.core.configs.storage_configs import UNIQUE_STRING_LENGHT


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


if __name__=="__main__":
    markdown_to_html(r"C:\Users\jim\PycharmProjects\Reinforcement-learning-sandbox\README.md")

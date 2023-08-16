import fire

from tdf_tool.pipeline import Pipeline
from ruamel import yaml

from tdf_tool.tools.print import Print


import io
import sys
# 将标准输出流的编码方式设置为 UTF-8（用于兼容windows）
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def main():
    fire.Fire(Pipeline())

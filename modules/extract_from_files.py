import re
import codecs
import os


mod_name = __name__


def prepare_regexes(config):
    return {}


def process_lines(process_input):
    yield {}


def extract_from_files(config, data):
    config = config[mod_name.split(".")[-1]]
    regex = prepare_regexes(config)
    init_dir = os.getcwd()
    for code_file in data:
        with codecs.open(code_file, 'rb', "utf-8") as cf:
            line_info = {}
            for count, content in enumerate(cf, start=1):
                if re.match(regex["hit"], content):
                    line_info[count] = content.strip()
            if line_info:
                process_input = {
                    "init_dir": init_dir,
                    "code_file": code_file,
                    "line_info": line_info,
                    "regex": regex}
                for line in process_lines(process_input):
                    yield line

from modules.gather_files import gather_files
from modules.git_blames_from_files import git_blames_from_files
from modules.filter_by_age import filter_by_age
from modules.exclude import exclude
from modules.raise_if_present import raise_if_present
from modules.aggregate_by import aggregate_by
from modules.text_summary import text_summary
from modules.print_summary import print_summary
from modules.save_to_file import save_to_file
from modules.process_results import process_results

from enclose import print_log as enclose

pipeline = {
    100: gather_files,
    200: git_blames_from_files,
    400: filter_by_age,
    410: exclude,
    500: raise_if_present,
    600: aggregate_by,
    700: text_summary,
    800: print_summary,
    810: save_to_file,
    900: process_results,
}

data = {
    "gather_files": {
        "root_paths": ["./"],
        "file_sufixes": [".py", ".rb"],
    },
    "git_blames_from_files": {
        "tokens": ["todo", "fixme"],
        "case-sensitive": False,
    },
    "filter_by_age": {
        "oldest": 180,
        "earliest": -1,
    },
    "exclude": {
        "file_path": [{
            "values": ["config.py"],
            "functions": [lambda data, value: data == value]
        }],
    },
    "raise_if_present": {
        "case-sensitive": True,
        "token": ["XXX"],
    },
    "aggregate_by": {
        "keys": ["token", "file_path"],
        "case-sensitive": False,
    },
    "text_summary": {
        "indent": "  ",
        "column_separator": "  ",
        "max_width": 80,
        "timestamp": True,
        "column_order":
        ["token", "date", "email", "line_count", "file_path", "code"]
    },
    "save_to_file": {
        "path": "./",
        "filename": "report.txt",
        "overwrite": False,
    },
    "process_results": {
        "drop": True,
    },
}

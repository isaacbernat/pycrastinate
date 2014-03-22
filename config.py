from modules import *
import enclose

enclose = enclose.print_log

pipeline = {
    100: gather_files,
    200: git_blames_from_files,
    400: filter_by_age,
    410: exclude,
    500: raise_if_present,
    600: aggregate_by,
    700: text_summary,
    800: print_summary,
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
    },
    "process_results": {
        "drop": True,
    }
}

from modules import *
import enclose

enclose = enclose.print_log

pipeline = {
    100: gather_git_blames_python,
    400: filter_by_age,
    500: raise_if_present,
    600: aggregate_by,
    700: print_summary,
}

data = {
    "gather_git_blames_python": {
        "init_path": "./",
        "tokens": {
            "todo": 0,
            "fixme": 1,
        },
        "file_sufixes": [".py", ".rb"],
        "default_email": "default@email.com",
    },
    "filter_by_age": {
        "oldest": 180,
        "earliest": -1,
    },
    "raise_if_present": {
        "case-sensitive": True,
        "token": ["XXX"],
    },
    "aggregate_by": {
        "keys": ["token", "file_path"],
        "case-sensitive": False,
    },
    "print_summary": {
        "indent": "  ",
        "column_separator": "  ",
        "max_width": 80,
    }
}

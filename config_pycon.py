from modules.gather_git_blames_shell import gather_git_blames_shell
from modules.aggregate_by import aggregate_by
from modules.text_summary import text_summary
from modules.print_summary import print_summary
from modules.process_results import process_results
from enclose import print_log as enclose

pipeline = {
    100: gather_git_blames_shell,
    600: aggregate_by,
    700: text_summary,
    800: print_summary,
    900: process_results,
}

data = {
    "gather_git_blames_shell": {
        "init_path": "/Users/ec/django",
        "tokens": ["todo", "fixme"],
        "file_sufixes": [".py"],
        "include_committer": False,
    },
    "aggregate_by": {
        "keys": ["token", "author"],
    },
    "text_summary": {
        "columns": ["token", "date", "email", "line_count", "file_path",
                    "code"]
    },
}

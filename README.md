Pycrastinate
============
Tired of `TODO` from people who have not touched that code in years? What about `FIXME`?

Pycrastinate is a **language-agnostic** tool that helps you keep your codebase (whether it is legacy or new) under control, without any extra effort on your part.

Requirements
------------
* Python 2.7+ / Python 3.3+
* Specific modules may have further dependencies (but these are optional)

Installation
------------
Clone this git repository

Usage
-----
### Try it out
Pycrastinate can be used right out of the box! It just needs a recent version of `git` (tested with 1.8.0+). Type `python pycrastinate.py` inside its root directory and experience the magic.

### Tune it
Edit `config.py` to your liking. Change the `root_paths` for whichever paths hold the files you want to analyse, the `file_sufixes` to include only those that you want (e.g. only python files), the `tokens` that should be considered (e.g. `TODO`), their case-sensitivity, etc.

### Master it
It is highly encouraged to read at least this succint documentation section if you plan to really use pycrastinate.

Documentation
-------------
Each* module has its own documentation and set of tests you can refer to. Here is a general overview of how the project is structured. The basic config file for the default settings is also covered.

### Structure
* `config.py`: this is the file where you **configure** (set which, their order, their parameters, etc.) pipelines you want to execute.
* `pycrastinate.py`: this is the file you run to **execute** the pipelines.
* `modules`: steps that can be run in the pipeline process.
* `enclose`: closures that can be applied for each module execution (e.g. logging).
* `tests`: unit tests for the other files. Simply type `nosetests`.
* `utils`: semi-generic utilities that may be used across different modules (e.g. memoisation decorator).

### config.py
The config file is itself split into 3 sections:

* `imports`: to access `modules` and set `enclose`.
* `pipeline`: this is a `key: value` dictionary where the **key** is the *priority* (i.e. order) in which the processor will be executed and the **value** is the *function* (from a `module`) be executed. Lower numbers will run first. Ties are indeterministic.
* `data`: this is a `key: value` dictionary where the configuration parameters for each function (from a `module`) are set. To avoid name clashes the **key** is always the *name of the module* (which contains the function). **Values** are *dictionaries* (usually functions can accept more than one parameter. In this case, having key names instead of other (simpler) data structures (e.g. lists) makes it more human-readable).

#### Example
```python
#----- imports section -----
from modules import *
from enclose import print_log as enclose

#----- pipeline section -----
"""
We set our pipeline strategy. Note: some modules may perform multiple steps
1.- gather files                  -> return file paths
2.- inspect files                 -> return extracted line_metadata
3.- generate additional metadata  -> return line_metadata (+ additions)
4.- filter on line metadata       -> return line_metadata (subset)
5.- trigger actions               -> return line_metadata (unaltered)
6.- aggregate results             -> return line_metadata (aggregated)
7.- generate report/render        -> return report
8.- deliver/notify/act on report  -> return report (unaltered)
9.- process results (generators)  -> return input as list, drop it, etc.
"""

"""
We want to use `gather_git_blames_shell` instead of `gather_files` together with `git_blames_from_files` modules.
It is >4x faster (tested on python 2.7 and 3.3+) but has additional requisites.
Namely `git` (v. 1.8.5+), `grep`, `cut`, `awk`, `sed`, `xargs` and `cat`.
It performs both gather and inspect steps at once.
"""
pipeline = {
    100: gather_git_blames_shell,
    400: filter_by_age,
    500: raise_if_present,
    600: aggregate_by,
    700: html_summary,
    800: send_email,
    900: process_results,
}

#----- data section -----
"""
Here we configure each module we are using that needs it.
The dictionary keys are the module names.
"""
data = {
    "gather_git_blames_shell": {
        "init_path": "./",
        "tokens": ["todo", "fixme"],
        "case-sensitive": False,
        "file_sufixes": [".py", ".rb"],
        "include_committer": False,
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
    "html_summary": {
        "title": "Pycrastinate HTML report",
        "css": ["td{font-family: monospace}"],
        "timestamp": True,
    },
    "send_email": {
        "to": ["another_example@gmail.com"],
        "cc": [],
        "bcc": [],
        "from": "example@gmail.com",
        "username": "example@gmail.com",
        "password": "example_password",
        "smtp_name": "smtp.gmail.com",
        "smtp_port": 587,
        "subject": "Pycrastinate example report",
    },
    "process_results": {
        "drop": True,
    }
}
```

### Further information
TODO (check each specific file)

*If you find some module with incomplete documentation/tests you may want to report it (and be patient), but you can also consider contributing a fix.

Contributing
------------
Pycrastinate is still pretty much under continuous improvement. This means that there might be bugs, additional desired functionalities or unclear examples within the documentation. Feel free to open issues for any of them and/or reach me.

### New features
Pull requests are most welcome. Do not be intimidated but keep in mind a few considerations before creating a PR:

* Check other branches, so that the feature you want to implement is not already being worked on at the moment.

* Write enough tests to cover at least the most common use case scenarios of the feature. Also, do not break existing tests (run `nosetests`). Documentation is a big plus.

* Try to keep high standards of code quality. After all this code is going to be public and can potentially be contributed by many others after you.

* Be consistent with the current style (e.g. PEP8). Code conventions can change and adapt, but they need to be coherent project-wide.

### Contributors
Pycrastinate started as a hack-day project at [Wrapp](https://www.wrapp.com) by [Isaac Bernat](https://github.com/isaacbernat), who is the current maintainer. He is not doing this alone and wants to thank everyone else involved in the project. He is reachable via e-mail at <isaac.bernat@gmail.com>

Licence
-------
TODO choose one

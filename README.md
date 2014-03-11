Pycrastinate
============
TODOs are meant to be done... at some point. This is why they were written in first place, right? Pycrastinate is a **language-agnostic** tool which helps you accomplish that goal and keep your codebase under control -- effortlessly!

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
Pycrastinate can be used right out of the box! It just needs a recent version of `git` (tested with 1.8.0+). Type `python pycrastinate.py` inside its root directory.

### Tune it
Edit `config.py` to your liking. Change the `init_path` for whichever path holds the files you want to analyse, the `file_sufixes` to include only those that you want, the (case-insensitive) `tokens` that should be considered, etc.

### Master it
It is highly encouraged to read at least this succint documentation section if you plan to really use pycrastinate.

Documentation
-------------
Each module has its own documentation and set of tests you can refer to. Here there is a general overview of how the project is structured and the basic config file for the default settings is also covered.

### Structure
* `config.py`: this is the file where you **configure** (set which, their order, their parameters, etc.) pipelines you want to execute.
* `pycrastinate.py`: this is the file you run to **execute** the pipelines.
* `modules`: steps that can be run in the pipeline process.
* `enclose`: closures that can be applied for each module execution (e.g. logging)
* `tests`: unit tests for other files lie here. Simply type `nosetests`.

### config.py
The config file is itself split into 4 sections:

* `imports`: to access `modules` and `enclose` contents
* `enclose`: here you can set which closure you want to apply for each module being executed.
* `pipeline`: this is a `key: value` dictionary where the key is the priority (i.e. order) in which the processor will be executed and the value is the module of name to be executed. Lower number will run first.
* `data`: this is a `key: value` dictionary where the configuration parameters for each module you run are set. To avoid name clashes the key is always the name of the module. Usually the value is a dictionary when more than one parameter is required for the module to be configured.

#### Example
```python
#----- imports section -----
from modules import *
import enclose

#----- enclose section -----
"""
We want to log on the screen every time a module starts and ends.
Thus, we add the corresponding module
"""
enclose = enclose.print_log

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
"""

pipeline = {
"""
We want to use `gather_git_blames_shell` instead of the other python modules.
It is much faster but has additional requisites to run.
Namely `git` (at least 1.8.5), `grep`, `cut`, `awk`, `sed`, `xargs` and `cat`.
It also performs both gather and inspect steps at once.
"""
    100: gather_git_blames_shell,
    400: filter_by_age,
    500: raise_if_present,
    600: aggregate_by,
    700: print_summary,
}

#----- data section -----
"""
Here we configure each module we are using that needs it.
The dictionary keys are the module names.
"""
data = {
    "gather_git_blames_shell": {
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
```

### Further information
TODO (check each specific file)

Contributing
------------
Pycrastinate is still pretty much under continuous improvement. This means that there might be bugs, additional desired functionalities or unclear examples within the documentation. Feel free to open issues for any of them and/or reach me.

### New features
Pull requests are most welcome. Do not be intimidated but keep in mind a few considerations before considering a PR:

* Check other branches, so that the feature you want to implement is not already being worked on at the moment.

* Write enough tests to cover at least the most common use case scenarios of the feature. Also, do not break existing tests (run `nosetests`)

* Try to keep high standards of code quality. After all this code is going to be public and can potentially be contributed by many others after you.

* Be consistent with the current style. Code conventions can change and adapt, but they need to be coherent project-wide.

### Contributors
Pycrastinate started as a hack-day project at [Wrapp](https://www.wrapp.com) by [Isaac Bernat](https://github.com/isaacbernat), who is the current maintainer. He has not done this alone and wants to thank everyone else involved in the project. He is reachable via e-mail at <isaac.bernat@gmail.com>

Licence
-------
TODO choose one

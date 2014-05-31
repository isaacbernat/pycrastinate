Pycrastinate
============
Tired of `TODO` from people who have not touched that code in years? What about `FIXME`?

Pycrastinate is a **language-agnostic** tool that helps you keep your codebase (whether it is legacy or new) under control in a transparent way (i.e. without interfering with your coding).

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

### Dive in
Pycrastinate was featured in a 25-minutes talk in PyCon Sweden 2014. You can view the original slides [on your browser here](http://prezi.com/47crucgh9ukr/?utm_campaign=share&utm_medium=copy&rc=ex0share) or [on PDF here](https://www.dropbox.com/s/07fihcso355clw1/PycrastinatePyConSweden2014.pdf). There you can find real use-case examples.

### Tune it
Edit `config.py` to your liking. Change the `root_paths` for whichever paths hold the files you want to analyse, the `file_sufixes` to include only those that you want (e.g. only python files), the `tokens` that should be considered (e.g. `TODO`), their case-sensitivity, etc.

### Master it
It is highly encouraged to read at least this succint documentation section and the slides from PyCon 2014 if you plan to really use pycrastinate.


Documentation
-------------
Each module has its own documentation and set of tests you can refer to. Here is a general overview of how the project is structured. The basic config file for the default settings is also covered.

### Structure
* `config.py`: this is the file where you **configure** (set which, their order, their parameters, etc.) pipelines you want to execute.
* `pycrastinate.py`: this is the file you run to **execute** the pipelines.
* `modules`: steps that can be run in the pipeline process.
* `enclose`: closures that can be applied for each module execution (e.g. logging, sending realtime metrics to dashboards, etc.).
* `tests`: unit tests for the other files. Simply type `nosetests --with-isolation`.
* `utils`: semi-generic utilities that may be used across different modules (e.g. memoisation decorator).

### config.py
The config file is itself split into 3 sections:

* `imports`: to access `modules` and set `enclose`.
* `pipeline`: this is a `key: value` dictionary where the **key** is the *priority* (i.e. order) in which the processor will be executed and the **value** is the *function* (from a `module`) to be executed. Lower numbers will run first. Ties are indeterministic.
* `data`: this is a `key: value` dictionary where the configuration parameters for each function (from a `module`) are set. To avoid name clashes the **key** is always the *name of the module* (which contains the function). **Values** are *dictionaries* (usually functions can accept more than one parameter. In this case, having *key* names instead of other (simpler) data structures (e.g. lists) makes it more human-readable).

#### Example
This is the example run on PyCon 2014 Sweden for Django project:

**>240k lines of code, >1.7k python files, >60 `TODO`+`FIXME`...  in < 3.5 seconds!**

```python
#----- imports section -----
from modules.gather_git_blames_shell import gather_git_blames_shell
from modules.aggregate_by import aggregate_by
from modules.text_summary import text_summary
from modules.print_summary import print_summary
from modules.process_results import process_results
from enclose import print_log as enclose

#----- pipeline section -----
"""
We want to use `gather_git_blames_shell` instead of `gather_files` together with `git_blames_from_files` modules (which are pure python implementations). It is usually >2x faster (tested on python 2.7 and 3.3+) but has additional requisites (namely `git` (v. 1.8.5+), `grep`, `cut`, `awk`, `sed`, `xargs` and `cat`).
It performs both gather and inspect steps at once.
"""
pipeline = {
    100: gather_git_blames_shell,
    600: aggregate_by,
    700: text_summary,
    800: print_summary,
    900: process_results,
}

#----- data section -----
"""
Here we configure each module (we are using many default values, hence it is not bulky, but has many options). The dictionary keys are the module names.
"""
data = {
    "gather_git_blames_shell": {
        "init_path": "/Users/ec/django", #here goes your path to django
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
```

This is [a basic console report](http://pastebin.com/BGmUkhxR) like the one generated in that presentation.

### Further information
*TODO* (check each specific file)

If you find some module with incomplete documentation/tests you may want to report it (and be patient), but you can also consider contributing a fix.

Contributing
------------
Pycrastinate is still pretty much under continuous improvement. This means that there might be bugs, additional desired functionalities or unclear examples within the documentation. Feel free to open issues for any of them and/or reach me.

### New features
Pull requests are most welcome. Do not be intimidated but keep in mind a few considerations before creating a PR:

* Check other branches, so that the feature you want to implement is not already being worked on at the moment.

* Write enough tests to cover at least the most common use case scenarios of the feature. Also, do not break existing tests (run `nosetests --with-isolation`). Documentation is a big plus.

* Try to keep high standards of code quality. After all this code is going to be public and can potentially be contributed by many others after you.

* Be consistent with the current style (e.g. PEP8). Code conventions can change and adapt, but they need to be coherent project-wide.

### Contributors
Pycrastinate started as a hack-day project at [Wrapp](https://www.wrapp.com) by [Isaac Bernat](https://github.com/isaacbernat), who is the current maintainer. He is not doing this alone and wants to thank everyone else involved in the project. He is reachable via e-mail at <isaac.bernat@gmail.com>

Licence
-------
*TODO* choose one

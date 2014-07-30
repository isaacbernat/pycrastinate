Pycrastinate
============
Tired of `TODO` from people who have not touched that code in years? What about `FIXME`?

Pycrastinate is a **language-agnostic** tool that helps you keep your codebase (whether it is legacy or new) under control in a transparent way (i.e. without interfering with the way you program).

This tool empowers you to find TODOs (or whatever else you want) in your code; extract/create metadata (e.g. when the TODO lines were committed, the e-mail of the committer, etc.); filter them out according to any criteria (you can feed it with your own lambda functions, e.g. commits less than 15 days old); trigger actions (e.g. throw an exception to break your CI (Continuous Integration) system, send an e-mail to repo owners/committers/etc.); perform custom multi-level aggregation (e.g. email > repo); generate human readable reports (HTML, console friendly txt) and more.

The main goal is to aid in detection, handling and prioritisation of FIXMEs and other potentially hacky code in repositories before it is too late (i.e. other code starts relying on them, developers forget what they really meant/which issues addressed, etc.)

Requirements
------------
* Python 2.7+ / Python 3.3+
* Specific modules may have further dependencies (but these are optional)

Installation
------------
- Clone this git repository `git clone https://github.com/isaacbernat/pycrastinate.git`

or

- Get it from pypi `pip install pycrastinate` (may not be the latest version)

Usage
-----
### Try it out
It simply works out of the box! If you cloned this git repo just run `python pycrastinate.py config.py` inside its root directory and experience the magic (tested under `git` 1.8.0+). Otherwise run `python pycrastinate.py config_not_git.py`. If you want to run it within another python script do the following:

```python
from pycrastinate import pycrastinate

pycrastinate("full_path_to_your_config_file/config_name.py")
```

### Dive in
Pycrastinate was featured in a 25-minute talk in [PyCon Sweden 2014](http://2014.pycon.se/). You can view the original slides [on your browser here](http://prezi.com/47crucgh9ukr/?utm_campaign=share&utm_medium=copy&rc=ex0share) or [on PDF here](https://github.com/isaacbernat/pycrastinate/blob/master/docs/PycrastinatePyConSweden2014.pdf). There you can find real use-case examples. There is also a rather improvised [5-minute lightning talk](http://youtu.be/C_GBFxt_3s0?t=16m27s) I gave on the topic on [PyData Berlin 2014](pydata.org/berlin2014/) and [EuroPython 2014](https://ep2014.europython.eu/en/).

### Tune it
Create your own config file. Change the `root_paths` for whichever paths hold the files you want to analyse, the `file_sufixes` to include only those that you want (e.g. only python files), the `tokens` that should be considered (e.g. `TODO`), their case-sensitivity, etc. and then store it on the root path for pycrastinate. The config name must not have any `.` besides de final `.py` and you can use it by running `python pycrastinate.py path_to_you_config/your_config_name.py`

### Master it
It is highly encouraged to read at least this succint documentation section and the [slides](https://github.com/isaacbernat/pycrastinate#dive-in) from PyCon Sweden 2014 if you plan to really use pycrastinate.


Documentation
-------------
Here is a general overview of all you need to know to customise your pycrastinate flows.

### Configuration
Configuration files (e.g. `config.py`, `config_pycon.py`, etc.) can be split into 3 sections:

* `imports`: to access `modules` and set `enclose`.
* `pipeline`: this is a `key: value` dictionary where the **key** is the *priority* (i.e. order) in which the processor will be executed and the **value** is the *function* (from a `module`) to be executed. Lower numbers will run first. Ties are indeterministic (so you probably want to avoid them).
* `data`: this is a `key: value` dictionary where the configuration parameters for each function (from a `module`) are set. To avoid name clashes the **key** is always the *name of the module* (which contains the function). **Values** are *dictionaries* (usually functions can accept more than one parameter. In this case, having *key* names instead of other (simpler) data structures (e.g. lists) makes it more human-readable).

#### Example
This is the example run on PyCon Sweden 2014 for Django project ([config_pycon.py](https://github.com/isaacbernat/pycrastinate/blob/master/config_pycon.py)):

- **250k lines** of python code analysed from 13k files (1.8k python files),
- **>60 `TODO`+`FIXME` reported** (>20 of these found are 5+ years old)
- All in less than **3.5 seconds!**

```python
#----- imports section -----
from modules.gather_git_blames_shell import gather_git_blames_shell
from modules.aggregate_by import aggregate_by
from modules.text_summary import text_summary
from modules.print_summary import print_summary
from modules.process_results import process_results
from enclose import print_log as enclose

#----- pipeline section -----
pipeline = {
    100: gather_git_blames_shell,
    600: aggregate_by,
    700: text_summary,
    800: print_summary,
    900: process_results,
}

#----- data section -----
"""
Here we configure each module. We use implicit default values to keep it simple.
The dictionary keys are the module names.
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

### Modules
Each module has its own [documentation](https://github.com/isaacbernat/pycrastinate/tree/master/modules#module-specifics) and [set of tests](https://github.com/isaacbernat/pycrastinate/tree/master/tests) you can refer to. They are organised into *pipelines* to build up pycrastinate flows.

#### Pipelines
**Definition**: chain of processing elements, arranged so that the output of each element is the input of the next. - [en.wikipedia.org](http://en.wikipedia.org/wiki/Pipeline_(software))

The many modules available in pycrastinate can be grouped into categories depending on which step of the pipeline they are executed. A module may span more than one (consecutive) category (but that is not the norm) and not all categories must be present to create a flow which solves real-life use-cases. There are some examples [from the PyCon Sweden 2014 presentation](https://github.com/isaacbernat/pycrastinate#dive-in) you can refer to. Here is a diagram that helps understanding those categories.

![pipeline diagram](https://github.com/isaacbernat/pycrastinate/blob/master/docs/pipeline_diagram.png?raw=true "Diagram with the ordered module categories in pycrastinate pipelines")

##### Find & Extract
The first steps of the pipeline are those which:
* Enable us to find the files and lines of code we are interested in.
* Take the metadata we want from them (and only that).

##### Act & Analyse
With the desired metadata from the previous steps, we can:
* Act on it.
* Turn it into knowledge and changes.

### Project structure
* `config.py` (or custom config): this is the file where you **configure** (set which, their order, their parameters, etc.) the modules that define the pipeline.
* `pycrastinate.py`: this is the file you run to **execute** the pipeline.
* `modules`: steps that can be run in the pipeline process.
* `enclose`: closures that can be applied for each module execution in the pipeline (e.g. logging, sending realtime metrics to dashboards, etc.).
* `tests`: unit tests for the other files. Simply type `nosetests --with-isolation`.
* `utils`: semi-generic utilities that may be used across different modules (e.g. memoisation decorator).
* `docs`: auxiliary files (e.g. images) needed for documentation purposes.

### pycrastinate.py
The *main* function which runs the whole pipeline is just a simple python one-liner.
```python
def run(pipeline, config, enclose):
    return reduce(lambda results, func: enclose(func, (config, results)),
                  OrderedDict(sorted(pipeline.items())).values(), [])
```
Here there is an illustrative image on how it works [from the PyCon Sweden 2014 presentation](https://github.com/isaacbernat/pycrastinate#dive-in).

![pycrastinate.py diagram](https://github.com/isaacbernat/pycrastinate/blob/master/docs/pycrastinate_diagram.png?raw=true "Diagram with the ordered module categories in pycrastinate pipelines")

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

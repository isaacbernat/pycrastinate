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
Pycrastinate was featured in a 25-minute talk in [PyCon Sweden 2014](http://2014.pycon.se/). You can view the original slides [on your browser here](http://prezi.com/47crucgh9ukr/?utm_campaign=share&utm_medium=copy&rc=ex0share) or [on PDF here](https://github.com/isaacbernat/pycrastinate/blob/master/docs/PycrastinatePyConSweden2014.pdf). There you can find real use-case examples.

### Tune it
Edit `config.py` to your liking. Change the `root_paths` for whichever paths hold the files you want to analyse, the `file_sufixes` to include only those that you want (e.g. only python files), the `tokens` that should be considered (e.g. `TODO`), their case-sensitivity, etc.

### Master it
It is highly encouraged to read at least this succint documentation section and the slides from PyCon Sweden 2014 if you plan to really use pycrastinate.


Documentation
-------------
Here is a general overview of all you need to know to customise your pycrastinate flows.

### config.py
The config file is split into 3 sections:

* `imports`: to access `modules` and set `enclose`.
* `pipeline`: this is a `key: value` dictionary where the **key** is the *priority* (i.e. order) in which the processor will be executed and the **value** is the *function* (from a `module`) to be executed. Lower numbers will run first. Ties are indeterministic (so you probably want to avoid them).
* `data`: this is a `key: value` dictionary where the configuration parameters for each function (from a `module`) are set. To avoid name clashes the **key** is always the *name of the module* (which contains the function). **Values** are *dictionaries* (usually functions can accept more than one parameter. In this case, having *key* names instead of other (simpler) data structures (e.g. lists) makes it more human-readable).

#### Example
This is the example run on PyCon Sweden 2014 for Django project:

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

### Modules
Each module has its own [documentation](https://github.com/isaacbernat/pycrastinate/tree/master/modules) and [set of tests](https://github.com/isaacbernat/pycrastinate/tree/master/tests) you can refer to. They are organised into *pipelines* to build up pycrastinate flows.

#### Pipelines
**Definition**: chain of processing elements, arranged so that the output of each element is the input of the next. - [en.wikipedia.org](http://en.wikipedia.org/wiki/Pipeline_(software))

The many modules available in pycrastinate can be grouped into categories depending on which step of the pipeline they are executed. A module may span more than one (consecutive) category (but that is not the norm) and not all categories must be present to create a flow which solves real-life use-cases. There are some examples [from the PyCon Sweden 2014 presentation](https://github.com/isaacbernat/pycrastinate#dive-in) you can refer to. Here is a diagram that helps understanding those categories.

![pipeline diagram](https://github.com/isaacbernat/pycrastinate/blob/master/docs/pipeline_diagram.png?raw=true "Diagram with the ordered module categories in pycrastinate pipelines")

##### Find & Extract
The first steps of the pipeline are those which:
* Enable us to find the files and lines of code we are interested in.
* Take the metadata we want from them (and only that).

###### Gather files
Get a list of file paths we are interested in getting through the pipeline.

*Example*: I am only interested in python files (ended in ".py") from a couple of specific directories.

###### Inspect files
Get metadata from the lines of code you are interested in (located in the file paths collected in the previous step).

*Example*: I want to get metadata from all lines of code with `FIXME` or `TODO` on them. For each of them I also want to get the e-mail address of their authors and the time they were last modified.

###### Extract more metadata
Generate more metadata from what you already have.

*Example*: Every two Fridays we have a hackday. I want to add that information.

###### Filter
Remove sets of metadata that match some restriction.

*Example*: I am not interested in code more recent than 2 weeks.

##### Act & Analyse
With the desired metadata from the previous steps, we can:
* Act on it.
* Turn it into knowledge and changes.

###### Trigger actions
Act on specific metadata.

*Example*: I want to rise an Exception if there are `FIXME` in the metadata.

###### Aggregate
Group metadata on specific criteria.

*Example*: I want to aggregate the metadata by (1) type of token (e.g. `FIXME` vs `TODO`) and (2) file path, so the information is more manageable.

###### Create report
Generate a human-readable report on the aggregated metadata.

*Example*: I want to generate HTMLs with github links to the found codelines so it is convenient for me to access them and analyse the information.

###### Deliver
Act on results from previous steps.

*Example*: I want to send an e-mail with a report for all the aggregated lines of code to their respective authors and a copy to myself.

##### Process results
**TL;DR** this is a special module you always add in the end.

This module is needed because many of the modules in pycrastinate are lazily evaluated (in order to have lower memory footprints). That means that in the end the results from those modules would never be executed if there was no consumer for them. This lightweight module acts as the necessary consumer for those.

### Project structure
* `config.py`: this is the file where you **configure** (set which, their order, their parameters, etc.) pipelines you want to execute.
* `pycrastinate.py`: this is the file you run to **execute** the pipelines.
* `modules`: steps that can be run in the pipeline process.
* `enclose`: closures that can be applied for each module execution (e.g. logging, sending realtime metrics to dashboards, etc.).
* `tests`: unit tests for the other files. Simply type `nosetests --with-isolation`.
* `utils`: semi-generic utilities that may be used across different modules (e.g. memoisation decorator).
* `docs`: auxiliary files (e.g. images) needed for documentation purposes.

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

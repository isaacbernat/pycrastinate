Modules
=======
Here is a description of the modules, which includes:

- How they can work together as a whole to create a pycrastinate pipeline
- How each of them may be individually configured, etc.

For more information you can refer to their specific code files, [set of tests](https://github.com/isaacbernat/pycrastinate/tree/master/tests) or contact [the project maintainers](https://github.com/isaacbernat/pycrastinate#contributors).

The big picture: A pycrastinate pipeline
----------------------------------------
*This excerpt is taken from the main readme*:

**Definition**: chain of processing elements, arranged so that the output of each element is the input of the next. - [en.wikipedia.org](http://en.wikipedia.org/wiki/Pipeline_(software))

The many modules available in pycrastinate can be grouped into categories depending on which step of the pipeline they are executed. A module may span more than one (consecutive) category (but that is not the norm) and not all categories must be present to create a flow which solves real-life use-cases. There are some examples [from the PyCon Sweden 2014 presentation](https://github.com/isaacbernat/pycrastinate#dive-in) you can refer to. Here is a diagram that helps understanding those categories.

![pipeline diagram](https://github.com/isaacbernat/pycrastinate/blob/master/docs/pipeline_diagram.png?raw=true "Diagram with the ordered module categories in pycrastinate pipelines")

### Find & Extract
The first steps of the pipeline are those which:
* Enable us to find the files and lines of code we are interested in.
* Take the metadata we want from them (and only that).

### Act & Analyse
With the desired metadata from the previous steps, we can:
* Act on it.
* Turn it into knowledge and changes.

Module specifics
----------------
Here there is a description of each category and the list of modules that fit within.

### Gather files
Get a list of file paths we are interested in getting through the pipeline.

*Example*: I am only interested in python files (ended in ".py") from a couple of specific directories.

#### gather_files
##### Parameters
###### root_paths
- **type**: list of strings.
- **description**: They are the initial paths to recursively scan.
- **defaults**: current path (`["./"]`).

###### file_sufixes
- **type**: list of strings.
- **description**: Filepaths found ended with any of these will be returned.
- **defaults**: python files (`[".py"]`).

##### Config sample:
```python
"gather_files": {
    "root_paths": ["./"],
    "file_sufixes": [".py", ".rb"],
},
```

### Inspect files
Get metadata from the lines of code you are interested in (located in the file paths collected in the previous step).

*Example*: I want to get metadata from all lines of code with `FIXME` or `TODO` on them. For each of them I also want to get the e-mail address of their authors and the time they were last modified.

### Extract more metadata
Generate more metadata from what you already have.

*Example*: Every two Fridays we have a hackday. I want to add that information.

### Filter
Remove sets of metadata that match some restriction.

*Example*: I am not interested in code more recent than 2 weeks.

### Trigger actions
Act on specific metadata.

*Example*: I want to rise an Exception if there are `FIXME` in the metadata.

### Aggregate
Group metadata on specific criteria.

*Example*: I want to aggregate the metadata by (1) type of token (e.g. `FIXME` vs `TODO`) and (2) file path, so the information is more manageable.

### Create report
Generate a human-readable report on the aggregated metadata.

*Example*: I want to generate HTMLs with github links to the found codelines so it is convenient for me to access them and analyse the information.

### Deliver
Act on results from previous steps.

*Example*: I want to send an e-mail with a report for all the aggregated lines of code to their respective authors and a copy to myself.

### Process results
**TL;DR** this is a special module you always add in the end.

This module is needed because many of the modules in pycrastinate are lazily evaluated (in order to have lower memory footprints). That means that in the end the results from those modules would never be executed if there was no consumer for them. This lightweight module acts as the necessary consumer for those.

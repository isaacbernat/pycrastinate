#!/usr/bin/env python
# coding: utf-8

import setuptools

setuptools.setup(
    name="pycrastinate",
    version="0.1.0",
    py_modules=["pycrastinate"],
    author="Isaac Bernat",
    author_email="isaac.bernat@gmail.com",
    url="https://github.com/isaacbernat/pycrastinate",
    license="None",
    description="Keep your TODO, FIXME, etc. under control by triggering actions, generating reports, date/author/custom filtering, automated e-mails and more",
    keywords=["todo", "fixme", "xxx", "comments", "extract", "clean",
              "report", "creep", "git"],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Topic :: Documentation",
        "Topic :: Software Development",
        "Topic :: Software Development :: Bug Tracking",
        "Topic :: Software Development :: Documentation",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Software Development :: Version Control",
        "Topic :: Utilities",
        ],
    long_description="""\
Pycrastinate
=======================
**TODO less, DO more**: *Keep your code clean without changing the way you code.*

Tired of `TODO` from people who have not touched that code in years? What about `FIXME`?

Pycrastinate is a **language-agnostic** tool that helps you keep your codebase (whether it is legacy or new) under control in a transparent way.

Usage
============
Try it out
----------------
It simply works out of the box! If you want to run it within another python script do the following:

*from pycrastinate import pycrastinate*
*pycrastinate("full_path_to_your_config_file/config_name.py")*

If you want to run it as a command line tool just run `python pycrastinate.py path_to_your_config/config.py` inside its root directory and experience the magic. You can get sample config.py and config_not_git.py files from https://github.com/isaacbernat/pycrastinate

Dive in
----------------
Pycrastinate was featured in a 25-minute talk in PyCon Sweden 2014. There you can find the PDF and the original version http://2014.pycon.se/ . The slides include real life use-case examples.

Tune it
----------------
Create your own config file. Change the `root_paths` for whichever paths hold the files you want to analyse, the `file_sufixes` to include only those that you want (e.g. only python files), the `tokens` that should be considered (e.g. `TODO`), their case-sensitivity, etc. and then store it on the root path for pycrastinate. The config name must not have any "." besides de final ".py" and you can use it by running `python pycrastinate.py your_config_name`

Master it
----------------
It is highly encouraged to read at least the succint github documentation and check the slides from PyCon Sweden 2014 if you plan to use pycrastinate seriously.


For more documentation see the homepage.
"""
)

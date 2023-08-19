JGT Tools
=========

JGT Tools is a collection of package helpers
for common CLI functions
within a properly-formatted repository.


Quickstart
----------

Just include ``jgt_tools`` in your package VirtualEnv,
and you'll have access to these CLI calls:

- ``env-setup`` - set up the development environment
  with all packages and pre-commit checks
- ``self-check`` - run self-checks/linters/etc. on your repository
- ``run-tests`` - run your in-repo test suite
- ``build-docs`` - build repo documentation locally
- ``build-and-push-docs`` - both build the docs,
  then publish to your gh-pages branch
- ``check-version`` - raise an error if package-relevant files have changed
  without a version bump

Details for each script can be found by calling with the ``--help`` flag.

.. tip::
   In order to keep the environment as clean as possible,
   JGT Tools will only install the libraries needed to start the tool itself.
   However, several of the default commands
   rely on additional libraries.
   When ``env-setup`` is run for the first time,
   it will check to see if each set of commands is still default,
   and if so, install the libraries those commands need.


run-tests
---------
The ``run-tests`` commands will
pass through any additional parameters
provided on the command line.
For example,
by default ``run-tests`` maps to::

    poetry run python -m pytest -vvv

Running ``run-tests -s`` would run::

    poetry run python -m pytest -vvv -s

Documentation Index
-------------------

In order to get the full benefit from ``build-docs``,
it is encouraged to create an index file
that pulls together all the documentation.
This file needs to be in the root folder
and should be called ``.jgt_tools.index``.
This will be moved into the working directory for Sphinx
and be used when building the documentation.
Additional information can be found on the `Sphinx site`_.

Configuration
-------------

A number of the actions to be called
can be customized in a ``[tool.jgt_tools]``
in your ``pyproject.toml`` file.
Available values are:

- ``env_setup_commands`` - a list of commands to be run
  under the ``env-setup`` call
- ``self_check_commands`` - a list of commands to be run
  under the ``self-check`` call
- ``run_tests_commands`` - a list of commands to be run
  under the ``run-tests`` call
- ``build_docs_commands`` - a list of commands to be run
  under the ``build-docs`` call

For example::

    [tool.jgt_tools]
    env_setup_commands = [
        "poetry install",
        "poetry run pip install other_package",
        "./my_custom_setup_script.sh"
    ]
    build_docs_commands = []

would run your specified commands for ``env-setup``
and skip the default api doc builder.

.. note::
    NOTE: All commands provided in ``[tools.jgt_tools]``
    will be run from project root.
    To ensure your commands run as expected,
    provide any paths in your custom commands relative from root.

build_docs_commands
~~~~~~~~~~~~~~~~~~~

Specifically for ``build_docs_commands``,
there are some variables
that can be used to aid in documentation building,
using Python-style curly-brace formatting::

    BASE_DIR: Root library directory
    PACKAGE_NAME: Folder name containing package
    DOCS_WORKING_DIRECTORY: Temporary directory where docs are built (needed for Sphinx)
    DOCS_OUTPUT_DIRECTORY: Final directory where docs are saved

For example::

    [tool.jgt_tools]
    build_docs_commands = [
        "poetry run sphinx-apidoc --output-dir {DOCS_WORKING_DIRECTORY} --no-toc --force --module-first {PACKAGE_NAME}
    ]

builds the Sphinx API docs for the current package
and stores the output files
in the temporary working directory.

check-version
~~~~~~~~~~~~~

In addition,
the function to verify which files are relevant to ``check-version``
can be customized.
By default, if any files in the diff against master are ``.py`` files,
a version bump is expected,
but the user can provide an alternate function to verify filenames.

The function should expect a list of strings
representing file paths relative from project root
(as provided by ``git diff master --name-only``)
and return a boolean representing if a version change should be ensured
(i.e. ``True`` if version should be checked).

This can be registered as a plugin in your ``pyproject.toml`` file::

    [tools.poetry.plugins."file_checkers"]
    "version_trigger" = "my_module:my_function"

or in your ``setup.py`` file::

    setup(
        ...
        entry_points={
            "version_trigger": ["version_trigger = my_module:my_fuction"]
        }
    )

.. _`Sphinx site`: http://www.sphinx-doc.org/en/master/usage/quickstart.html#defining-document-structure

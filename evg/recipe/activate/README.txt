evg.recipe.activate
===================

This recipe can be used to create an activation script for zc.buildout
environment.

You can see an example of how to use the recipe below::

    >>> data = """
    ... [buildout]
    ... parts = activate
    ...
    ... [activate]
    ... recipe = evg.recipe.activate
    ... """
    >>> touch('buildout.cfg', data=data)
    >>> sh('bin/buildout -vvvvvv install activate')



Run buildout. Then on POSIX systems you can do::

    $ source bin/activate

This will change your ``$PATH`` to point to the virtualenv ``bin/`` directory.
You have to use ``source`` because it changes the environment in-place. After
activating an environment you can use the function ``deactivate`` to undo the
changes::

    (buildout) $ deactivate

The ``activate`` script will also modify your shell prompt to indicate which
environment is currently active.


Supported options
=================

The recipe supports the following options:

activate
  The name of the script created in the bin folder. This script is the
  equivalent of the ``activate`` virtualenv. It defaults to ``activate``.

deactivate
  The name of the function to deactivate environment. It defaults to
  ``deactivate``.

name
  The name of the environment. It will use buildout directory name by default.

platform
  The name of paltform to generate scripts. It will be detected by default.
  Possible values are: ``posix``, ``win32``, ``cygwin`` and ``jython``.

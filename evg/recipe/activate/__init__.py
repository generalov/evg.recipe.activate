# -*- coding: utf-8 -*-

##############################################################################
#
# Copyright (c) 2010 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""
This recipe creates an activation script for zc.buildout environment.
See ``README.txt`` for details.
"""

__all__ = ("Recipe", "uninstall")


import os
import re


POSIX_ACTIVATE_SCRIPT_TEMPLATE = """
# This file must be used with "source bin/${activate}" *from bash*
# you cannot run it directly

${deactivate} () {
    if [ -n "$_OLD_BUILDOUT_PATH" ] ; then
        PATH="$_OLD_BUILDOUT_PATH"
        export PATH
        unset _OLD_BUILDOUT_PATH
    fi

    # This should detect bash and zsh, which have a hash command that must
    # be called to get it to forget past commands.  Without forgetting
    # past commands the $PATH changes we made may not be respected
    if [ -n "$BASH" -o -n "$ZSH_VERSION" ] ; then
        hash -r
    fi

    if [ -n "$_OLD_BUILDOUT_PS1" ] ; then
        PS1="$_OLD_BUILDOUT_PS1"
        export PS1
        unset _OLD_BUILDOUT_PS1
    fi

    if [ ! "$1" = "nondestructive" ] ; then
    # Self destruct!
        unset -f "${deactivate}"
    fi
}

# unset irrelavent variables
${deactivate} nondestructive

BUILDOUT_ENV="${buildout:directory}"

_OLD_BUILDOUT_PATH="$PATH"
PATH="$BUILDOUT_ENV/bin:$PATH"
export PATH

_OLD_BUILDOUT_PS1="$PS1"
if [ "`basename \"$BUILDOUT_ENV\"`" = "__" ] ; then
    # special case for Aspen magic directories
    # see http://www.zetadev.com/software/aspen/
    PS1="[`basename \`dirname \"$BUILDOUT_ENV\"\``] $PS1"
else
    PS1="(`basename \"$BUILDOUT_ENV\"`)$PS1"
fi
export PS1

# This should detect bash and zsh, which have a hash command that must
# be called to get it to forget past commands.  Without forgetting
# past commands the $PATH changes we made may not be respected
if [ -n "$BASH" -o -n "$ZSH_VERSION" ] ; then
    hash -r
fi
"""


class PosixDefaults(object):
    """Settings for POSIX systems"""

    activate_script_name = "activate"
    deactivate_script_name = "deactivate"
    activate_script_template = POSIX_ACTIVATE_SCRIPT_TEMPLATE.lstrip()


class Recipe(object):
    """zc.buildout recipe"""

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options

        defaults = PosixDefaults
        options.setdefault("activate", defaults.activate_script_name)
        options.setdefault("deactivate", defaults.deactivate_script_name)

        self.bin_directory = buildout["buildout"]["bin-directory"]
        self.activate_script_path = os.path.join(self.bin_directory,
                                                 options["activate"])
        self.activate_script_template = defaults.activate_script_template

    def install(self):
        """Install the ``activate`` script"""
        script_paths = []
        script_paths.extend(self._create_activate_script())
        return script_paths

    def update(self):
        pass

    def _create_activate_script(self):
        result = self._render(self.activate_script_template)
        output = open(self.activate_script_path, "wt")
        output.write(result)
        output.close()
        return [self.activate_script_path, ]

    def _render(self, source):
        template=re.sub(r"\$\{([^:]+?)\}", r"${%s:\1}" % self.name, source)
        return self.options._sub(template, [])


def uninstall(name, options):
    pass

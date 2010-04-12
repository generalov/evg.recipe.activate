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
import sys
import re


class Recipe(object):
    """zc.buildout recipe"""

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options
        options.setdefault("activate", ACTIVATE)
        options.setdefault("deactivate", DEACTIVATE)
        options.setdefault("directory", buildout["buildout"]["directory"])
        options.setdefault("bin-directory", buildout["buildout"]["bin-directory"])
	name = os.path.basename(os.path.abspath(options["directory"]))
	if name == '__':
	    # special case for Aspen magic directories
	    # see http://www.zetadev.com/software/aspen/
	    name = os.path.basename(os.path.abspath(os.path.dirname(options["directory"])))
        options.setdefault("name", name)
        options.setdefault("platform", get_platform())

    def install(self):
        """Install the ``activate`` script"""
        activate = self.options['activate']
        deactivate = self.options['deactivate']
        platform = self.options['platform']
        bin_dir = self.options['bin-directory']
        files = {}
        if WIN32 in platform or JYTHON in platform:
            files.update({'%s.bat' % activate : ACTIVATE_BAT,
                          '%s.bat' % deactivate : DEACTIVATE_BAT})
        if CYGWIN in platform or POSIX in platform:
            files.update({activate: ACTIVATE_SH})
        assert files, "Can't to detect platform"
        script_paths = []
        for name, content in files.items():
            dest = os.path.join(bin_dir, name)
            content = self.render(content)
            writefile(dest, content)
            script_paths.append(dest)
        return script_paths

    def update(self):
        pass

    def render(self, source):
        template=re.sub(r"\$\{([^:]+?)\}", r"${%s:\1}" % self.name, source)
        return self.options._sub(template, [])


def uninstall(name, options):
    pass

CYGWIN = 'cygwin'
JYTHON = 'jython'
POSIX = 'posix'
WIN32 = 'win32'
def get_platform():
    platform = set()
    if sys.platform.startswith('java'):
        platform.add(JYTHON)
    if sys.platform == 'win32' and os._name == 'nt':
        platform.add(WIN32)
    if os.environ.get('OS') == 'Windows_NT' and os.environ.get('OSTYPE') == 'cygwin':
        platform.add(CYGWIN)
    if not platform:
        platform.add(POSIX)
    return '+'.join(sorted(platform))

def writefile(dest, content):
    f = open(dest, "wt")
    f.write(content)
    f.close()

ACTIVATE = 'activate'

DEACTIVATE = 'deactivate'

ACTIVATE_SH = r"""
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

    unset BUILDOUT_ENV
    if [ ! "$1" = "nondestructive" ] ; then
    # Self destruct!
        unset -f ${deactivate}
    fi
}

# unset irrelavent variables
${deactivate} nondestructive

BUILDOUT_ENV="${directory}"
export BUILDOUT_ENV

_OLD_BUILDOUT_PATH="$PATH"
PATH="${bin-directory}:$PATH"
export PATH

if [ -z "$BUILDOUT_ENV_DISABLE_PROMPT" ] ; then
    _OLD_BUILDOUT_PS1="$PS1"
    PS1="(${name})$PS1"
    export PS1
fi

# This should detect bash and zsh, which have a hash command that must
# be called to get it to forget past commands.  Without forgetting
# past commands the $PATH changes we made may not be respected
if [ -n "$BASH" -o -n "$ZSH_VERSION" ] ; then
    hash -r
fi
""".lstrip()

ACTIVATE_BAT = r"""
@echo off
set BUILDOUT_ENV=${buildout:directory}

if not defined PROMPT (
    set PROMPT=$P$G
)

if defined _OLD_BUILDOUT_PROMPT (
    set PROMPT=%_OLD_BUILDOUT_PROMPT%
)

set _OLD_BUILDOUT_PROMPT=%PROMPT%
set PROMPT=(${name}) %PROMPT%

if defined _OLD_BUILDOUT_PATH set PATH=%_OLD_BUILDOUT_PATH%; goto SKIPPATH

set _OLD_BUILDOUT_PATH=%PATH%

:SKIPPATH
set PATH=${buildout:bin-directory};%PATH%

:END
""".lstrip().replace('\n', '\r\n')

DEACTIVATE_BAT = r"""
@echo off

if defined _OLD_BUILDOUT_PROMPT (
    set PROMPT=%_OLD_BUILDOUT_PROMPT%
)
set _OLD_BUILDOUT_PROMPT=

if defined _OLD_BUILDOUT_PATH set PATH=%_OLD_BUILDOUT_PATH%

set _OLD_BUILDOUT_PATH=

:END

""".lstrip().replace('\n', '\r\n')

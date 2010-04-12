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
This module contains the tool of evg.recipe.activate
"""

import os
from setuptools import setup, find_packages


def read(*path):
    return open(os.path.join(os.path.dirname(__file__), *path)).read()

long_description="\n\n".join([read("evg", "recipe", "activate", "README.txt"),
			      read("CHANGES.txt")])

setup(name="evg.recipe.activate",
      version="0.2",
      description="This recipe generates activation script for zc.buildout environment.",
      author="Evgeny V. Generalov",
      author_email="e.generalov@gmail.com",
      license="ZPL 2.1",
      url="http://github.com/generalov/evg.recipe.activate",
      classifiers=[
        "Framework :: Buildout",
        "Topic :: Software Development :: Build Tools",
	"License :: OSI Approved :: Zope Public License",
        "Development Status :: 5 - Production/Stable",
      ],
      keywords="buildout",
      packages=find_packages(exclude=["ez_setup"]),
      namespace_packages=["evg", "evg.recipe"],
      include_package_data=True,
      install_requires=[
        "setuptools",
        "zc.buildout",
        "zc.recipe.egg",
      ],
      entry_points="""
        # -*- Entry points: -*-
        [zc.buildout]
        default = evg.recipe.activate:Recipe
        [zc.buildout.uninstall]
        default = evg.recipe.activate:uninstall
      """,
      long_description=long_description,
      zip_safe=False,
)

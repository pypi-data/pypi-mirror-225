# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wx-stubs',
 'wx-stubs.DateTime',
 'wx-stubs.FileType',
 'wx-stubs.Image',
 'wx-stubs.TopLevelWindow',
 'wx-stubs.Window',
 'wx-stubs.adv',
 'wx-stubs.aui',
 'wx-stubs.dataview',
 'wx-stubs.glcanvas',
 'wx-stubs.grid',
 'wx-stubs.grid.GridBlocks',
 'wx-stubs.html',
 'wx-stubs.html2',
 'wx-stubs.lib',
 'wx-stubs.lib.agw',
 'wx-stubs.lib.agw.ribbon',
 'wx-stubs.lib.agw.ribbon.buttonbar',
 'wx-stubs.lib.agw.ribbon.gallery',
 'wx-stubs.lib.agw.ribbon.toolbar',
 'wx-stubs.lib.analogclock',
 'wx-stubs.lib.analogclock.lib_setup',
 'wx-stubs.lib.analogclock.lib_setup.fontselect',
 'wx-stubs.lib.buttons',
 'wx-stubs.lib.calendar',
 'wx-stubs.lib.colourselect',
 'wx-stubs.lib.newevent',
 'wx-stubs.lib.scrolledpanel',
 'wx-stubs.lib.wxpTag',
 'wx-stubs.media',
 'wx-stubs.propgrid',
 'wx-stubs.ribbon',
 'wx-stubs.richtext',
 'wx-stubs.stc',
 'wx-stubs.xml',
 'wx-stubs.xrc']

package_data = \
{'': ['*'],
 'wx-stubs': ['ActivateEvent/*',
              'ConfigBase/*',
              'DataObject/*',
              'HelpEvent/*',
              'StandardPaths/*',
              'StaticBitmap/*',
              'StockPreferencesPage/*'],
 'wx-stubs.grid': ['Grid/*', 'GridActivationSource/*'],
 'wx-stubs.lib': ['dialogs/*']}

setup_kwargs = {
    'name': 'types-wxpython',
    'version': '0.8.0',
    'description': 'Typing stubs for wxPython',
    'long_description': "[![PyPI version](https://badge.fury.io/py/types-wxpython.svg)](https://badge.fury.io/py/types-wxpython)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/types-wxpython)\n![GitHub branch checks state](https://img.shields.io/github/checks-status/AlexionSoftware/types-wxpython/main)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/types-wxpython)\n![GitHub](https://img.shields.io/github/license/AlexionSoftware/types-wxpython)\n\n# Typing stubs for wxPython\nVersion: wxPython 4.2.0\n\nThis package contains typings stubs for [wxPython](https://pypi.org/project/wxPython/)\n\nThis package is not maintained by the maintainers of wxPython. This is made by users of wxPython.\n\nAny help is always welcome.\n\n## How it works\nThe base for the stubs is generated from [docs.wxpython.org](https://docs.wxpython.org/). It crawls the documentation looking for the Python-classes, functions and literals. This means changes in the documentation will also be applied in the stubs automatically, when they are regenerated.\n\nWe do not update anything in the `wx-stubs` folder manually. Everything is generated using the generator.\n\nExecute `run.bat`/`run.sh` to generate the stubs.\n\n### Overrides\nBecause we generated things based of online information, we sometimes has to resort to guessing, or sometimes the online documentation does not contain certain information. This fix these problems we can override the typing.\n\nYou will find the overrides in [`generator/overrides.py`](https://github.com/AlexionSoftware/types-wxpython/blob/main/generator/overrides.py).\n\nIn this file any parameter can be overriden by specifing the key and the params you want to overrides. You can change the typing of any class, function or literal. These are applied after the typing is collected from the online docs. \n\nTo update the stubs run: `run.bat`. This will result in newly updated stubs in the `wx-stubs` folder.\n\n### Missing\nThe online documentation can be incomplete, or sometimes we just don't seem to be able to comprehend the page. In these cases we can add typing to the stubs.\n\nYou will find this file in: [`generator/extras.py`](https://github.com/AlexionSoftware/types-wxpython/blob/main/generator/extras.py).\n\nHere you can add any missing typing.\n\nTo update the stubs run: `run.bat`. This will result in newly updated stubs in the `wx-stubs` folder.\n\n## Help is appreciated\nWe started this project because we use wxPython ourselves and code typing is really helpful to find bugs. \nBut there is so much in wxPython. We fixed problems in the stubs as they came up for our code. This can result in things not working for your code. \n\nWe decided to opensource the work we put in to create the best wxPython typing there is. \nWe would like you help to. You can create an issue if you find problems with the typing. Or create a pull request if you fixed something.\n\n### Guidelines\n* You don't need to commit newly generated stubs in your PR. We will generate them when we publish a new version of the stubs.\n",
    'author': 'Alexion Software',
    'author_email': 'info@alexion.nl',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/AlexionSoftware/types-wxpython',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8.1,<4.0.0',
}


setup(**setup_kwargs)

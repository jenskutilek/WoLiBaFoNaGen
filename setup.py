"""
py2app/py2exe build script for MyApplication.

Will automatically ensure that all build prerequisites are available
via ez_setup

Don't use the system-installed py2app, install your own copy instead:
pip install --user --ignore-installed py2app

Windows:
pip install --user -U py2exe_py2

Usage (Mac OS X):
    python setup.py py2app
Usage (Windows):
    python setup.py py2exe
"""
#import ez_setup
#ez_setup.use_setuptools()

import sys
from setuptools import setup

mainscript = 'WoLiBaFoNaGen.py'

PLIST = dict(
    CFBundleIdentifier="de.kutilek.WoLiBaFoNaGen",
    NSHumanReadableCopyright=u"Copyright © 2017-2022 by Jens Kutílek",
    LSMinimumSystemVersion="10.12.0",
    CFBundleShortVersionString="2.0.0",
    CFBundleVersion="2",
)

APP = [{
    "script": mainscript,
    "plist": PLIST,
    }
]

DATA_FILES = [
    "wordlists/japanese.txt",
    "wordlists/movie-characters.txt",
    "wordlists/music-classical.txt",
    "wordlists/music-country.txt",
    "wordlists/music-jazz.txt",
    "wordlists/rock-groups.txt",
    "wordlists/swahili.txt",
    "wordlists/tolkien.txt",
    "wordlists/wordsDan.txt",
    "wordlists/wordsEn.txt",
    "wordlists/wordsNld.txt",
    "wordlists/yiddish.txt",
]

OPTIONS = {
    "argv_emulation": False,
    "excludes": [
        "sphinx",
        "matplotlib",
        "numpy",
        "Image",
        "pillow",
        "wheel",
        "setuptools",
        "unittest",
        "pydoc",
        "pip",
        "http",
        "html",
        "distutils",
    ],  # modules are not available in dist
    "site_packages": True,
}


if sys.platform == 'darwin':
    extra_options = dict(
        setup_requires=['py2app'],
        app=[mainscript],
        # Cross-platform applications generally expect sys.argv to
        # be used for opening files.
        options=dict(py2app=OPTIONS),
    )

elif sys.platform == 'win32':
    extra_options = dict(
        setup_requires=['py2exe'],
        app=[mainscript],
    )
else:
    extra_options = dict(
        # Normally unix-like platforms will use "setup.py install"
        # and install the main script as such
        scripts=[mainscript],
    )

setup(
    name="WoLiBaFoNaGen",
    data_files=DATA_FILES,
    **extra_options
)

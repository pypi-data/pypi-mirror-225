from setuptools import setup

import ilan_dev

kwds = {}
try:
    kwds['long_description'] = open('README.rst').read()
except IOError:
    pass


setup(
    name = "ilan-dev",
    version = ilan_dev.__version__,
    author = "Ilan Schnell",
    author_email = "ilanschnell@gmail.com",
    url = "https://github.com/ilanschnell/ilan-dev",
    license = "BSD",
    classifiers = [
        "License :: OSI Approved :: Python Software Foundation License",
        "Environment :: Console",
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Utilities",
    ],
    description = "a few personal tools I use for development",
    py_modules = ["ilan_dev"],
    scripts = ['cleanup', 'tarinfo'],
    **kwds
)

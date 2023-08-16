from setuptools import setup, find_packages
import codecs
import os


VERSION = '0.0.2'
DESCRIPTION = 'task_1 from gnanendra'
LONG_DESCRIPTION = 'A package that allows to build a basic file moving'

# Setting up
setup(
    name="movefilestd",
    version=VERSION,
    author="Subhajit",
    author_email="singha111subhajit@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[],
    keywords=['python',],
    url='https://github.com/singha111subhajit/movefilestd.git',
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)

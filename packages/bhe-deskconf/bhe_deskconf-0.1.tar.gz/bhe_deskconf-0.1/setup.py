import setuptools
from pathlib import Path

setuptools.setup(name='bhe_deskconf',
                 version=0.1,
                 long_description=Path('README.MD').read_text(),
                 packages=setuptools.find_packages(exclude=["test", "data"])
                 )
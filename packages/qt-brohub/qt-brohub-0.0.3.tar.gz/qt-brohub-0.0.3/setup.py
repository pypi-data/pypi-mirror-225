import glob

from Cython.Build import cythonize
from setuptools import find_packages, setup

pyx_files = glob.glob("src/brohub/**/*.pyx", recursive=True)

setup(
    packages=find_packages(where="src", exclude=["tests"]),
    ext_modules=cythonize(pyx_files),
)

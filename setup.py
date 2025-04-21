from setuptools import setup
from Cython.Build import cythonize

setup(
    name='docker_tests',
    ext_modules=cythonize("main.py", language_level=3),
    zip_safe=False,
)

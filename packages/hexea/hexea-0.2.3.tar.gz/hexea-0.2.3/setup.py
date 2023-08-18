from setuptools import setup
from pybind11.setup_helpers import Pybind11Extension, build_ext
import os

os.environ["CFLAGS"] = "-std=c++11"

setup(
    ext_modules=[
        Pybind11Extension("hexea._board", ["hexea/board.cpp"])
    ],
    cmd_class={"build_ext": build_ext},
    zip_safe=False
)

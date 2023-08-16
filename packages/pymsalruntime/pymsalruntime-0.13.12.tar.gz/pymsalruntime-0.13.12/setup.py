# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

from os import path
import os
import setuptools
import sys
from setuptools import Extension, setup
import platform

try:
    from Cython.Build import cythonize
except ImportError:
    cythonize = None


# https://cython.readthedocs.io/en/latest/src/userguide/source_files_and_compilation.html#distributing-cython-modules
def no_cythonize(extensions, **_ignore):
    for extension in extensions:
        sources = []
        for sfile in extension.sources:
            filepath, ext = path.splitext(sfile)
            if ext in (".pyx", ".py"):
                if extension.language == "c++":
                    ext = ".cpp"
                else:
                    ext = ".c"
                sfile = filepath + ext
            sources.append(sfile)
        extension.sources[:] = sources
    return extensions


def get_mac_target_architecture():
    if os.environ.get("TARGET_ARCH") == "arm64":
        return "arm64"
    else:
        return "x86_64"


arch_args = []

if platform.system() == "Windows":
    library_list = ["msalruntime"] if sys.maxsize > 2**32 else ["msalruntime_x86"]
    library_list.append("user32")
elif platform.system() == "Darwin":
    library_list = [f"msalruntime_{get_mac_target_architecture()}", f"pyRunloopAPIs_{get_mac_target_architecture()}"]
    arch_args += ["-arch", get_mac_target_architecture()]
else:
    library_list = []

ext_modules = [
    Extension(
        name="pymsalruntime.pymsalruntime",
        sources=["pymsalruntime/PyMsalRuntime.pyx"],
        libraries=library_list,
        library_dirs=["build_resources"],  # At build time the most recently built version of
        # the .h, .lib, is copied here for compilation.
        include_dirs=["build_resources"],
        # Uncomment below for producing PDB to debug.
        # extra_compile_args=["-Ox", "-Zi"],
        # extra_link_args=["-debug:full"],
        # extra_compile_args=["-O0"],
        extra_compile_args=arch_args,
        extra_link_args=arch_args,
    )
]

if cythonize:  # Cythonize pyx files to .c files if we can, or assume precompiled sources are included.
    compiler_directives = {"language_level": 3, "embedsignature": True}
    ext_modules = cythonize(ext_modules, compiler_directives=compiler_directives)
else:
    ext_modules = no_cythonize(ext_modules)

version_file_path = path.normpath(path.join(path.dirname(__file__), "version.txt"))
with open(version_file_path, "r") as version_file:
    runtime_version = version_file.read().strip()

setup(
    name="pymsalruntime",
    version=runtime_version,
    description="The MSALRuntime Python Interop Package",
    author="Microsoft Corporation",
    license="MIT",
    author_email="MSALRuntime@microsoft.com",
    python_requires=">=3.6",
    packages=["pymsalruntime"],  # At build time the most recently built version of
    # the .dll copied here for distribution.
    classifiers=[
        "License :: OSI Approved :: MIT License",
    ],
    package_data={
        "": ["*.dylib", "*.dll", "*.pyi"],
    },
    ext_modules=ext_modules,
)

import setuptools
from setuptools.command.build_ext import build_ext

c_reader_module = setuptools.Extension('recorder_utils/libreader',
                                        ['recorder_utils/reader.c'], include_dirs=['recorder_utils'], extra_compile_args=['-std=c99'])

class my_build_ext(build_ext):
    # The default implementation of this function adds some
    # libraries to the linker during the building process.
    # e.g ['python3.x']
    #
    # However, in many clusters such as Theta and BlueWaters,
    # the path of libpython.so is unkown to the build script
    # thus it will cuase errors.
    #
    # Therefore, we overwrite this function to avoid adding
    # additional libraries.
    def get_libraries(self, ext):
        return ext.libraries

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="recorder-utils",
    version="0.3.0",
    author="Onewbiek",
    author_email="yankun0213@gmail.com",
    description="Recorder utility build upon the package \'recorder-viz\'",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/onewbiek/Recorder-utils",
    packages=['recorder_utils'],                  # package for import: after installaion, import recorder_utils
    package_data = {'recorder_utils': ['*.h']},   # *.h by default will not be copied, we use this to ship it.
    install_requires=[
        "mpi4py==3.1.4",
        "pandas",
    ],
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: University of Illinois/NCSA Open Source License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.7',
    entry_points={
        "console_scripts": [
            "recorder2csv=recorder_utils.recorder2csv:main"
        ]
    },
    ext_modules=[c_reader_module],
    cmdclass={'build_ext': my_build_ext},
)

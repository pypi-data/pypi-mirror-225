from setuptools import setup, find_packages

VERSION = '0.0.6'
DESCRIPTION = 'Time your function'
LONG_DESCRIPTION = 'A package that allows you to see the runtime of function.'

# Setting up
setup(
    name="functionTime",
    version=VERSION,
    author="Nayan-Chimariya",
    author_email="<cnayan789@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['colorama'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
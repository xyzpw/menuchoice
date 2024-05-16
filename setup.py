from setuptools import setup
import menuchoice

with open("README.md", "r") as f:
    readme = f.read()

setup(
    name="menuchoice",
    version=menuchoice.__version__,
    description=menuchoice.__description__,
    long_description=readme,
    long_description_content_type="text/markdown",
    author=menuchoice.__author__,
    maintainer=menuchoice.__author__,
    url="https://github.com/xyzpw/menuchoice/",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Environment :: Console",
        "Environment :: Console :: Curses",
        "Intended Audience :: Developers",
    ],
    keywords=[
        "menu selector",
        "item selector",
        "ansi",
    ],
    license=menuchoice.__license__,
)

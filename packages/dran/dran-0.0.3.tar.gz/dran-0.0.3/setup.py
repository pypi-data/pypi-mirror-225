# coding=utf-8
from setuptools import find_packages,setup
from src import __version__
# reqs is a list of requirement
# e.g. ['django==1.5.1', 'mezzanine==1.4.6']
with open('requirements.txt') as f:
    reqs = f.read().splitlines()

# include readme file
with open("README.md", "r") as f:
    long_description= f.read()

setup(
    name="dran", # can be different, needs to be unique
    version=__version__, # 0.0.x implies this is an unstable version
    description="Data reduction and analysis of HartRAO 26m telescope drift scans",
    long_description=long_description,
    long_description_content_type="text/markdown",
    py_modules=["dran"], # the modules we're importing
    packages=find_packages("src"), # these are the code files
    package_dir={'':'src'}, # the package we're installing
    # py_modules=[path.stem for path in Path("src").glob("*.py")],
    include_package_data=True,
    url="https://github.com/Pfesi/dran", # update once you have a release
    author="Pfesesani van Zyl",
    author_email="pfesi24@gmail.com",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3.8",
        "Topic :: Scientific/Engineering :: Astronomy",
        "Operating System :: OS Independent"
    ],
    project_urls={
        "Documentation": "https://dran.readthedocs.io/",
        "Changelog": "https://dran.readthedocs.io/en/latest/changelog.html",
        "Issue Tracker": "https://github.com/Pfesi/dran/issues",
    },
    keywords=[
        # eg: "keyword1", "keyword2", "keyword3",
        "dran", 'single-dish',
    ],
    python_requires=">=3.8",
    # dependencies, if you change this re-run install
    install_requires = reqs,
    # [
        # eg: "aspectlib==1.1.1", "six>=1.7",
                        # ]

    # development requirements
    # pip install -e .[dev]
    extras_require = {
        "dev": [
            "pytest>=3.7",
            # "tox>=",
        ]
    },
    entry_points={
        "console_scripts": [
            "dran-cli=_cli:main", #name = dran.module:function
            "dran-auto=_auto:main", #dran.module:function
            "dran-gui=_gui:main", #dran.module:function
            "dran=_dran:main", #dran.module:function
            "dran-docs=_docs:main",
        ]
    },
)
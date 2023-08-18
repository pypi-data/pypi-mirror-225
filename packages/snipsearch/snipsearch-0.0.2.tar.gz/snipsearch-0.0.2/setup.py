# -*- coding: utf-8 -*-
"""
Created on Sun Jul  2 12:18:08 2023

@author: jkris

"""
# SETUP PROCESS BELOW
# cleandoc -d ./../src/snipsearch -w
# python setup.py bdist_wheel sdist
# twine check dist/*
# twine upload dist/*

from os import path
from pprint import pprint
from requests import get
from setuptools import find_packages, setup
from pipreqs.pipreqs import get_all_imports, get_pkg_names, get_import_local

kwargs = {}

# Find Package Name
setupdir = path.split(path.realpath(__file__))[0]
pkgname = path.split(setupdir)[1]
kwargs["name"] = pkgname
print(f"\npkgname: {pkgname}")

# USER PARAMETERS
kwargs[
    "description"
] = "Python package to search multiple strings within Python snippets."
kwargs["python_requires"] = ">=3.9"
kwargs["entry_points"] = {"console_scripts": [f"{pkgname}={pkgname}:cli_main"]}
kwargs["install_requires"] = []
kwargs["packages"] = []  # ["pkg.assets"]
# kwargs["package_data"] = ({f"{pkgname}": ["assets/*"]},)
# kwargs["include_package_data"] = True

# Find Latest Version and Add 0.0.1
VERSION = "0.0.1"
pkgpage = get(f"https://pypi.org/project/{pkgname}/", timeout=10).text
if "page not found" not in pkgpage and "404" not in pkgpage:
    start_ind = pkgpage.find('<h1 class="package-header__name">') + 33
    latest_start = pkgpage[start_ind:]
    latest = latest_start[0 : latest_start.find("</h1>")]
    latest = latest.strip().split(" ")[1]
    print(f"\nlatest: {latest}")
    latest_split = latest.split(".")
    latest_split[2] = str(int(latest_split[2]) + 1)
    VERSION = ".".join(latest_split)
kwargs["version"] = VERSION
print(f"\nversion: {kwargs['version']}")

# RUN CLEANDOC HERE WITH CURRENT VERSION
if __name__ == "__main__":
    try:
        from cleandoc import cleandoc_all

        cleandoc_all(path.join(setupdir, "src", pkgname), release=VERSION)
    except ImportError:
        print("\n!!!! SKIPPING CLEANDOC CHECK !!!!")

# User README as PyPI home page
with open("README.md", "r", encoding="utf-8") as readme:
    readme_text = readme.read()

# Get Module Dependencies and their Versions
imports = get_all_imports(f"./src/{pkgname}", encoding="utf-8")
pkgnames = get_pkg_names(imports)
pkgdicts_all = get_import_local(pkgnames, encoding="utf-8")
pkgdicts = []
for pkgdict_orig in pkgdicts_all:
    pkgdicts_names = [pkgdict["name"] for pkgdict in pkgdicts]
    if pkgdict_orig["name"] not in pkgdicts_names:
        pkgdicts.append(pkgdict_orig)
pkglist = [pkgdict["name"] + ">=" + pkgdict["version"] for pkgdict in pkgdicts]
kwargs["install_requires"].extend(pkglist)

# Find all Packages and Sub-Packages
packages = find_packages(where="src")
kwargs["packages"].extend(packages)

print("\nkwargs:")
pprint(kwargs)
print("\n")

# Run Setup
setup(
    **kwargs,
    long_description=readme_text,
    long_description_content_type="text/markdown",
    author="Jason Krist",
    author_email="jkrist2696@gmail.com",
    url=f"https://github.com/jkrist2696/{pkgname}",
    license="GNU GPLv3",
    package_dir={f"{pkgname}": f"src/{pkgname}"},
)

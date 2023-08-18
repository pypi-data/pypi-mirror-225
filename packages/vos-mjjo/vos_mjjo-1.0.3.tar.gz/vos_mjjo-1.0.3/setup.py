import setuptools
from mjjo import (
    author,
    version,
    description
)


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="vos_mjjo", # Replace with your own username
    version=version,
    author=author,
    author_email="mj.jo@valueofspace.com",
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jomujin/vos-mjjo",
    packages=setuptools.find_packages(),
    package_data={"mjjo": ["data/*.txt", "data/*.pkl"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=[
        "symspellpy",
        "pandas"
    ],
    entry_points={
        'console_scripts': [
            'shortcut1 = package.module:func',
        ],
        'gui_scripts': [
            'shortcut2 = package.module:func',
        ]
    },
    test_suite="tests.tests.suite"
)

from pathlib import Path
from setuptools import setup, find_packages
from hides import __version__, __description__, __license__, __name__
from hides import __author__, __email__

this_directory = Path(__file__).parent
long_description = (this_directory/"README.md").read_text()

classifiers = [
    "Development Status :: 1 - Planning",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Operating System :: Unix",
    "Operating System :: MacOS :: MacOS X",
    "Operating System :: Microsoft :: Windows",
]

setup(
    name=__name__,
    version=__version__,
    author=__author__,
    author_email=__email__,
    license=__license__,
    url=f"https://github.com/a-tharva/{__name__}",
    description=__description__,
    long_description=long_description + '\n\n' + open('CHANGELOG.txt').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[],
    keywords=['python'],
    entry_points={
        'console_scripts': [
            'hides = hides.hides:main',
        ],
    },
    classifiers=classifiers,
)
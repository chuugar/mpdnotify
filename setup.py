from setuptools import setup, find_packages
from mpdnotify import __productname__, __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
        name=__productname__,
        version=__version__,
        description='mpdnotify - get notification when changing song',
        long_description=long_description,
        long_description_content_type="text/markdown",
        url='https://github.com/chuugar/mpdnotify',
        author='chuugar',
        author_email='charles-thomas@sfr.fr',
        license='GPL3',
        packages=find_packages(),
        entry_points={
            'console_scripts': ['mpdnotify=mpdnotify.cli:main'],
            },
        include_package_data=True,
        install_requires=[
            'python-mpd2',
            'Pillow',
            ],
        classifiers=[
            'Environment :: Console',
            'Environment :: Console :: Curses',
            'License :: OSI Approved :: GNU General Public License (GPL)',
            'Programming Language :: Python :: 3',
            'Topic :: Multimedia :: Sound/Audio :: Mixers',
            'Topic :: Utilities',
            ],
        )

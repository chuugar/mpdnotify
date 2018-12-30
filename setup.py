from setuptools import setup
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
        license='GPL3',
        package=['mpdnotify'],
        install_requires=[
            "mutagen",
            "Pillow",
            "python-mpd2",
            ],
        entry_points={
            'console_scripts': ['mpdnotify=mpdnotify.cli:main'],
            },
        include_package_data=True,
        classifiers=[
            'Environment :: Console',
            'Environment :: Console :: Curses',
            'License :: OSI Approved :: GNU GPL License',
            'Programming Language :: Python :: 3',
            'Topic :: Multimedia :: Sound/Audio :: Mixers',
            'Topic :: Utilities',
            ],
)

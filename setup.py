"""
to publish our package
"""
import os
from setuptools import setup


def read(filename):
    """
    reading README file
    """
    with open(os.path.join(os.path.dirname(__file__), filename)) as _in:
        return _in.read()


# This call to setup() does all the work
setup(
    name="ardicsrtcollector",
    # The version of this library.
    # Read this as
    #   - MAJOR VERSION 1
    #   - MINOR VERSION 0
    #   - MAINTENANCE VERSION 0
    version="1.0.14",
    description="Generates a dataset for the Turkish speech recognition.",
    # description and Project name| library name
    long_description=read('README.md'),
    long_description_content_type="text/markdown",

    author="ARDIC R&D",
    author_email="yavuz.erzurumlu@ardictech.com",
    url="https://github.com/IoT-Ignite/ArdicSrtCollector.git",
    # These are the dependencies the library needs in order to run.
    install_requires=[
        'youtube-channel-transcript-api',
        'youtube_transcript_api',
        'youtube-dl',
        'launchpadlib',
    ],

    py_modules=["ardicsrtcollector", "ardicsrtcollector/crop_mp3_srt/crop_mp3_srt",
                "ardicsrtcollector/youtube_srt_mp3",
                "ardicsrtcollector/helper/helper"],
    packages=['ardicsrtcollector'],
    packages_dir={'': 'ardicsrtcollector'},

    include_package_data=True,

    entry_points={
        "console_scripts": [
            "ardicsrtcollector=ardicsrtcollector:main",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: Apache Software License",
        "Intended Audience :: Developers"
    ],

    # Here are the keywords of my library.
    keywords='dataset, speech recognition, srt, youtube srt',
    license="MIT",
)

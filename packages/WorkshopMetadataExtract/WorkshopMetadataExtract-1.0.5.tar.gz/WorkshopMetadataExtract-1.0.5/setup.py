from setuptools import setup

"""
:authors: laVashik
:license: MIT license 
:copyright: (c) 2023 laVashik
"""

version = '1.0.5'

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='WorkshopMetadataExtract',
    version=version,
    author='laVashik',
    author_email='lavash.assistant@gmail.com',
    description='WME - Is a Python module that allows you to easily fetch and download workshop files from the Steam Workshop. This module makes use of the Steam API to retrieve information about workshop files, including their creators, file sizes, file URLs, and more. You can also download the workshop files and save them to your local machine using this module.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/IaVashik/WorkshopMetadataExtract',
    include_package_data=True,

    packages=['WorkshopMetadataExtract'],
    install_requires=['requests'],

    
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)

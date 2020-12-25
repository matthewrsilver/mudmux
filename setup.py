import glob
import os
from setuptools import setup, find_packages

ALL_SCRIPT_FILES = [
    os.path.sep.join(script_file_path.split(os.path.sep)[1:])
    for script_file_path in glob.glob('mudmux/scripts/**', recursive=True)
]

setup(
    name='mudmux',
    version='0.1.0',
    description='An environment for playing the text-based RPG Medievia.',
    url='https://github.com/matthewrsilver/mudmux',
    author='Matthew Silver',
    author_email='redacted@email.com',
    license='MIT License',
    packages=find_packages(),
    package_data={
        'mudmux': [
            'config/*',
            'data/notes.txt',
            'logs/communications.log',
            'src/*',
            'Dockerfile',
            'docker-compose.yaml'
        ] + ALL_SCRIPT_FILES
    },
    include_package_data=True,
    entry_points={
        'console_scripts': ['mudmux=mudmux.launch:main'],
    },
    install_requires=[
        'tmuxp==1.3.2'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
)

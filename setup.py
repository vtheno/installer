from setuptools import setup
import sys
import os
from pathlib import Path
from subprocess import call
dir = Path(__file__).parent.absolute()
os.chdir(str(dir))
call([sys.executable, 'actual_setup.py', 'install'])
call([sys.executable, 'install_binary.py'])

version = 0.1
readme = ''

setup(
    name='pspy-placeholder',
    version=version if isinstance(version, str) else str(version),
    keywords="",  # keywords of your project that separated by comma ","
    description="",  # a concise introduction of your project
    long_description=readme,
    long_description_content_type="text/markdown",
    license='mit',
    python_requires='>=3.5.0',
    url='https://github.com/purescript-python/installer',
    author='thautawarm',
    author_email='twshere@outlook.com',
    packages=['pspy_placeholder'],
    install_requires=[],
    package_data={
        'pspy_placeholder': [
            each.name for each in Path('pspy_placeholder').iterdir()
            if each.name.startswith('pspy')
        ]
    },
    platforms="any",
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    zip_safe=False,
)

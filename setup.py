import re

from setuptools import setup

# inspired by https://github.com/Rapptz/discord.py/blob/master/setup.py

requirements = []
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

version = ''
with open('valorant/__init__.py') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)  # type: ignore

readme = ''
with open('README.md') as f:
    readme = f.read()

extras_require = {
    'speed': ['orjson>=3.8.11,<4.0'],
}

packages = [
    'valorant',
    'valorant.models',
    'valorant.types',
]

setup(
    name='valorant.py',
    author='STACiA',
    url='https://github.com/staciax/valorant',
    project_urls={
        "Issue tracker": "https://github.com/staciax/valorant/issues",
    },
    version=version,
    packages=packages,
    license='MIT',
    description='An Asynchronous Unofficial Valorant API Wrapper for Python',
    long_description=readme,
    long_description_content_type='text/markdown',
    include_package_data=True,
    install_requires=requirements,
    extras_require=extras_require,
    python_requires='>=3.8.0',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)

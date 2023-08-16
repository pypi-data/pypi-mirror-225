from setuptools import setup

setup(
    name="passwordtools-yt",
    version="0.2.0",
    readme="README.md",
    description="A package for creating passwords and testing password strength",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    python_requires='>=3.10',
    author="Yair-T",
    url="https://github.com/Yair-T",
    packages=['passwordtools'],
    license='MIT LICENSE',
    project_urls={
        'Documentation': 'https://yair-t.github.io/passwordtools-docs/',
        'Bug Tracker': 'https://github.com/Yair-T/passwordtools/issues',
        'Source Code': 'https://github.com/Yair-T/passwordtools'
    },
)
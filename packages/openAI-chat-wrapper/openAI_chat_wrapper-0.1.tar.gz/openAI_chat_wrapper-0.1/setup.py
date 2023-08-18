from setuptools import setup, find_packages

setup(
    name='openAI_chat_wrapper',
    version='0.1',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[],
)

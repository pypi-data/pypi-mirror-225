import os

from setuptools import find_packages, setup

with open('requirements.txt', 'r') as f:
    packages = f.read().splitlines()
    print(packages)


def read_file(filename):
    with open(os.path.join(os.path.dirname(__file__), filename)) as file:
        return file.read()


setup(
    name='ATENIGMA',
    version='0.1.4',
    author='Prasaanth',
    author_email='prasaanth2k@gmail.com',
    description='''
ATENIGMA is a versatile CLI utility that offers basic file encryption and decryption functionalities. This tool leverages the `cryptography` Python library to provide a user-friendly way to secure your files through AES encryption. With ATENIGMA, you can encrypt files with your custom password, adding an extra layer of protection to your sensitive data.
''',
    install_requires=packages,
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
    entry_points={
        'console_scripts': [
            'atenigma=atenigma.banner:show_banner'
        ]

    }
)

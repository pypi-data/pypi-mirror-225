from setuptools import find_packages, setup

with open('requirements.txt', 'r') as f:
    packages = f.read().splitlines()
    print(packages)

setup(
    name='ATENIGMA',
    version='0.0.1',
    author='Prasaanth',
    author_email='prasaanth2k@gmail.com',
    description='''
ATENIGMA is a versatile CLI utility that offers basic file encryption and decryption functionalities. This tool leverages the `cryptography` Python library to provide a user-friendly way to secure your files through AES encryption. With ATENIGMA, you can encrypt files with your custom password, adding an extra layer of protection to your sensitive data.
''',
    install_requires=packages,
    entry_points={
        'console_scripts': [
            'atenigma=atenigma.banner:show_banner'
        ]

    }
)
